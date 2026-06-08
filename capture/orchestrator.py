"""Playwright-based capture orchestrator.

Loads a workflow YAML definition and drives Playwright (async) through
the defined step sequence, capturing screenshots and metadata.
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Optional

import yaml
from playwright.async_api import Browser, BrowserContext, Page, async_playwright

from capture.schema import (
    CaptureResult,
    StepAction,
    StepResult,
    Workflow,
    WorkflowStep,
)

HIGHLIGHT_STYLE = """
    border: 3px solid #ff4444 !important;
    box-shadow: 0 0 8px rgba(255, 68, 68, 0.6) !important;
"""

MAX_RETRIES = 3
RETRY_BACKOFF_MS = 1000


def load_workflow(path: str | Path) -> Workflow:
    """Load a workflow definition from a YAML file."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Workflow file not found: {path}")

    with open(path) as f:
        data = yaml.safe_load(f)

    return Workflow(**data)


def _resolve_env(value: str) -> str:
    """Resolve ${ENV_VAR} placeholders in a string."""

    def _replace(match: re.Match) -> str:
        var_name = match.group(1)
        fallback = match.group(0) or ""
        return os.environ.get(var_name, fallback)

    return re.sub(r"\$\{(\w+)\}", _replace, value)


def _resolve_step_value(step: WorkflowStep) -> str:
    """Resolve the value of a step, substituting environment variables."""
    if step.value is not None:
        return _resolve_env(step.value)
    return ""


class CaptureOrchestrator:
    """Orchestrates web capture by driving Playwright through workflow steps."""

    def __init__(
        self,
        workflow: Workflow,
        output_dir: str | Path,
        headless: bool = True,
        slow_mo: int = 0,
    ) -> None:
        self.workflow = workflow
        self.output_dir = Path(output_dir)
        self.headless = headless
        self.slow_mo = slow_mo
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    async def run(self) -> CaptureResult:
        """Execute the full workflow and return the capture result."""
        result = CaptureResult.new(self.workflow, str(self.output_dir))
        start_time = time.monotonic()

        self.output_dir.mkdir(parents=True, exist_ok=True)
        screenshots_dir = self.output_dir / "screenshots"
        screenshots_dir.mkdir(exist_ok=True)

        async with async_playwright() as pw:
            self._browser = await pw.chromium.launch(
                headless=self.headless,
                slow_mo=self.slow_mo,
            )
            self._context = await self._browser.new_context(
                viewport={"width": 1280, "height": 900},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
            )
            self._page = await self._context.new_page()

            for step in self.workflow.steps:
                step_result = await self._execute_step(step, screenshots_dir)
                result.steps.append(step_result)

            await self._context.close()
            await self._browser.close()

        result.duration_ms = int((time.monotonic() - start_time) * 1000)
        return result

    async def _execute_step(
        self,
        step: WorkflowStep,
        screenshots_dir: Path,
    ) -> StepResult:
        """Execute a single workflow step with retry logic."""
        assert self._page is not None

        last_error: Optional[str] = None
        screenshot_path: Optional[str] = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                await self._perform_action(step)
                screenshot_path = await self._capture_with_highlight(
                    step, screenshots_dir
                )

                if step.wait_after:
                    await self._page.wait_for_timeout(step.wait_after)

                return StepResult(
                    id=step.id,
                    action=step.action.value,
                    url=self._page.url,
                    description=step.description,
                    screenshot_path=screenshot_path,
                    selector=step.selector,
                    success=True,
                    error=None,
                )

            except Exception as exc:
                last_error = str(exc)
                if attempt < MAX_RETRIES:
                    await self._page.wait_for_timeout(RETRY_BACKOFF_MS)

        return StepResult(
            id=step.id,
            action=step.action.value,
            url=None,
            description=step.description,
            screenshot_path=None,
            selector=step.selector,
            success=False,
            error=last_error,
        )

    async def _perform_action(self, step: WorkflowStep) -> None:
        """Dispatch a workflow step to the appropriate Playwright action."""
        assert self._page is not None

        if step.action == StepAction.NAVIGATE:
            url = step.url or "/"
            full_url = url if url.startswith("http") else f"{self.workflow.base_url.rstrip('/')}{url}"
            await self._page.goto(full_url, wait_until="networkidle")

        elif step.action == StepAction.CLICK:
            assert step.selector, f"Click step '{step.id}' requires a selector"
            await self._page.click(step.selector)

        elif step.action == StepAction.TYPE:
            assert step.selector, f"Type step '{step.id}' requires a selector"
            value = _resolve_step_value(step)
            await self._page.fill(step.selector, "")

            await self._page.type(step.selector, value, delay=30)

        elif step.action == StepAction.WAIT:
            ms = int(step.value or "1000")
            await self._page.wait_for_timeout(ms)

        elif step.action == StepAction.WAIT_FOR_SELECTOR:
            assert step.selector, f"wait_for_selector step '{step.id}' requires a selector"
            await self._page.wait_for_selector(step.selector, timeout=15000)

        elif step.action == StepAction.SCREENSHOT:
            pass

        elif step.action == StepAction.FILL_FORM:
            assert step.selector, f"fill_form step '{step.id}' requires a selector"
            await self._page.fill(step.selector, _resolve_step_value(step))

        elif step.action == StepAction.SELECT_OPTION:
            assert step.selector, f"select_option step '{step.id}' requires a selector"
            await self._page.select_option(step.selector, _resolve_step_value(step))

    async def _capture_with_highlight(
        self,
        step: WorkflowStep,
        screenshots_dir: Path,
    ) -> Optional[str]:
        """Take a screenshot with optional highlight around the targeted element."""
        assert self._page is not None

        if not step.screenshot:
            return None

        if step.selector:
            try:
                await self._page.evaluate(
                    """
                    (selector) => {
                        const el = document.querySelector(selector);
                        if (!el) return false;
                        el.dataset.docmakerHighlight = 'true';
                        el.style.border = '3px solid #ff4444';
                        el.style.boxShadow = '0 0 8px rgba(255, 68, 68, 0.6)';
                        el.scrollIntoView({ behavior: 'instant', block: 'center' });
                        return true;
                    }
                """,
                    step.selector,
                )
                await self._page.wait_for_timeout(300)
            except Exception:
                pass

        screenshot_path = screenshots_dir / f"step-{step.id}.png"
        await self._page.screenshot(path=str(screenshot_path), full_page=False)

        if step.selector:
            try:
                await self._page.evaluate(
                    """
                    (selector) => {
                        const el = document.querySelector(selector);
                        if (el) {
                            delete el.dataset.docmakerHighlight;
                            el.style.border = '';
                            el.style.boxShadow = '';
                        }
                    }
                """,
                    step.selector,
                )
            except Exception:
                pass

        return str(screenshot_path)

    async def cleanup(self) -> None:
        """Close browser resources."""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
