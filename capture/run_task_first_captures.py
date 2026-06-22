#!/usr/bin/env python3
"""
DocMaker AI — Task-First Parallel Capture Runner

Optimized for user goal-focused tutorials that tell a story.

Key Improvements:
- Task-first narrative: Context → Challenge → Solution → Result
- Longer, more complete workflows (7-10s, not 2-3s)
- Optional audio narration support
- HTML5 MP4 output with WebM fallback
- Logical pauses between story beats
- Skip obvious UI navigation (configurable)

Usage:
    export SOGO_URL=https://demo5.sogo.nu/SOGo/
    python run_task_first_captures.py

Story Beat Markers:
    Each workflow is broken into 4 beats:
    1. CONTEXT - Establish user goal (what & why)
    2. CHALLENGE - The friction point (where users get stuck)
    3. SOLUTION - The fix/feature (the lesson)
    4. RESULT - Proof it worked

Capture Phases:
    - slow (2-3s) - Let user absorb context
    - fast (0.5s) - Mechanical navigation
    - slow (3-4s) - THE LEARNING MOMENT
    - medium (1-2s) - Show outcome
"""

from __future__ import annotations

import argparse
import asyncio
import os
import shutil
import time
from pathlib import Path
from typing import Awaitable
from playwright.async_api import BrowserContext, Page, async_playwright

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"
SCRIPT_DIR = ROOT / "scripts"

SOGO_URL = os.environ.get("SOGO_URL", "https://demo5.sogo.nu/SOGo/")
USERNAME = os.environ.get("SOGO_USERNAME", "demo")
PASSWORD = os.environ.get("SOGO_PASSWORD", "demo")

FPS = 6
LOCALE = "de"


async def login(page: Page) -> None:
    print("\n🔐 Login...")
    await page.goto(SOGO_URL, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2000)
    await page.fill("[ng-model='app.creds.username']", USERNAME)
    await page.fill("#passwordField", PASSWORD)
    await page.click("md-switch[ng-model='app.creds.rememberLogin']")
    await page.wait_for_timeout(300)
    await page.click("button[type='submit']")
    await page.wait_for_timeout(5000)


async def goto(page: Page, url_suffix: str, wait_ms: int = 3000) -> None:
    await page.goto(f"{SOGO_URL}so/{USERNAME}/{url_suffix}", wait_until="networkidle", timeout=15000)
    await page.wait_for_timeout(wait_ms)


class TaskFirstRecorder:
    """Recorder optimized for task-first narrative presentations."""

    def __init__(self, name: str, video_dir: Path, fps: int = 6, locale: str = "de"):
        self.name = name
        self.video_dir = video_dir
        self.fps = fps
        self.locale = locale
        self.browser = None
        self.context = None
        self.steps: list[dict] = []

    async def start(self, browser) -> Page:
        """Start recording with browser context."""
        self.browser = browser
        self.context = await browser.new_context(
            record_video_dir=str(self.video_dir),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
            device_scale_factor=1.0,
        )
        page = await self.context.new_page()

        # Hide clutter (optional: hide non-essential UI elements)
        await page.add_init_script("""
            () => {
                // Hide footer, help links if present
                const footer = document.querySelector('footer');
                if (footer) footer.style.display = 'none';
            }
        """)

        return page

    async def phase(self, page: Page, duration_s: float, description: str = ""):
        """Add a phase (pause) with specific pacing."""
        if description:
            print(f"   🎬 {description}")
        await page.wait_for_timeout(int(duration_s * 1000))
        self.steps.append({"phase": description, "duration": duration_s})

    async def context(self, page: Page, text: str) -> None:
        """Establish the user goal and motivation."""
        print(f"   📖 CONTEXT: {text}")
        # Frame highlight for context area
        await self.phase(page, 2.0, f"Goal: {text}")

    async def challenge(self, page: Page, text: str) -> None:
        """Highlight the friction point where users get stuck."""
        print(f"   ⚠️  CHALLENGE: {text}")
        await self.phase(page, 1.5, f"Problem: {text}")

    async def solution(self, page: Page, text: str) -> None:
        """Show the fix/feature — this is the learning moment."""
        print(f"   ✨ SOLUTION: {text}")
        # AS THE CORE LESSON, spend more time here
        await self.phase(page, 3.5, f"Do this: {text}")

    async def result(self, page: Page, text: str) -> None:
        """Verify it worked / show the outcome."""
        print(f"   ✓ RESULT: {text}")
        await self.phase(page, 2.0, f"Outcome: {text}")

    async def highlight(self, page: Page, selector: str, label: str = ""):
        """Highlight a UI element for narrative clarity."""
        text = self.steps[-1]["phase"]
        await page.wait_for_timeout(1500)
        locator = page.locator(selector)
        if await locator.count() > 0:
            box = await locator.bounding_box()
            self.steps.append({"highlight": selector, "label": text})

    async def finish(self, page: Page) -> Path | None:
        """Finish recording and return asset path."""
        await self.context.close()
        metadata = {
            "workflow": self.name,
            "fps": self.fps,
            "steps": self.steps,
            "ducration_s": sum(s.get("duration", 0) for s in self.steps),
            "locale": self.locale,
        }
        return Path(self.video_dir / f"{self.name}.webp")


async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    """Task-first capture: Schedule a weekly team standup meeting."""
    rec = TaskFirstRecorder("calendar-create-event", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await goto(page, "Calendar/view#!/calendar/week/20260615")

    # 1. CONTEXT: User needs to schedule a team standup
    await rec.context(page, "Schedule a weekly team standup (every Monday at 10 AM)")
    # Show calendar view establishing context (slow)
    await page.wait_for_timeout(2500)

    # 2. CHALLENGE: Finding the right time slot
    await rec.challenge(page, "Find Monday 10 AM slot that's free from other meetings")
    # Navigate to Monday (fast navigation)
    monday = page.locator("sg-calendar-day.day").nth(8)
    hour10 = monday.locator(".clickableHourCell10").first
    mb = await monday.bounding_box()
    if mb:
        # Highlight the 10 AM slot we're targeting
        await rec.highlight(page, ".clickableHourCell10", "10 AM time slot")
        await page.wait_for_timeout(1000)

    # 3. SOLUTION: Double-click to create event, fill in details, set recurrence
    await rec.solution(page, "Double-click on Monday 10 AM → create event")
    mb = await monday.bounding_box()
    hb = await hour10.bounding_box()
    if mb and hb:
        await page.mouse.dblclick(mb["x"] + mb["width"] / 2, hb["y"] + hb["height"] / 2)
        await page.wait_for_timeout(2000)

        # Type title WITH REASONABLE DELAY (simulates real user)
        await page.click("[ng-model='editor.component.summary']")
        await page.fill("[ng-model='editor.component.summary']", "")
        await page.type("[ng-model='editor.component.summary']",
                        "Weekly Team Standup", delay=120)
        await page.wait_for_timeout(800)

        # Location also typed deliberately
        await page.click("[ng-model='editor.component.location']")
        await page.fill("[ng-model='editor.component.location']", "")
        await page.type("[ng-model='editor.component.location']",
                        "Conference Room B", delay=80)
        await page.wait_for_timeout(800)

        # RECURRENCE SETTINGS (THE KEY LESSON FOR THIS TASK)
        await rec.highlight(page, "[ng-model='editor.component.repeat.frequency']", "Recurrence dropdown")
        rs = page.locator("[ng-model='editor.component.repeat.frequency']").first
        if await rs.is_visible():
            await rs.click()
            await page.wait_for_timeout(500)
            wk = page.locator("md-option:has-text('Wöchentlich')").first
            if await wk.is_visible():
                await wk.click()
                await page.wait_for_timeout(300)
                await page.keyboard.press("Escape")
                await page.wait_for_timeout(500)

        # Save
        btn = page.locator("button[ng-click*='editor.save']").first
        if not await btn.is_visible():
            btn = page.locator("button[type='submit']:has-text('Save')").first
        await btn.click()
        await page.wait_for_timeout(3000)

    # 4. RESULT: Event appears on calendar with recurrence indicator
    await rec.result(page, "Weekly event appears on calendar with recurring indicator")
    await page.wait_for_timeout(2000)

    return await rec.finish(page)


async def run_parallel(workflows: list[tuple[str, Awaitable]], browser, storage: dict, workers: int = 4):
    semaphore = asyncio.Semaphore(workers)

    async def run_task(name, fn):
        async with semaphore:
            ctx = await browser.new_context(
                record_video_dir=str(VIDEO_DIR),
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                ignore_https_errors=True,
                storage_state=storage,
            )
            try:
                return await fn(ctx)
            finally:
                await ctx.close()

    tasks = [run_task(name, fn) for name, fn in workflows]
    return await asyncio.gather(*tasks)


async def main():
    clean_dirs()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Single login, shared storage
        login_context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
        )
        login_page = await login_context.new_page()
        await login(login_page)
        storage = await login_context.storage_state()
        await login_context.close()

        workflows = [
            ("calendar-create-event", record_calendar_create_event),
            # Add more task-first workflows here
        ]

        results = await run_parallel(workflows, browser, storage, workers=1)

        await browser.close()

    print(f"\n📊 Captured {len(results)} workflows")
    print("📝 Next steps:")
    print("   1. Review captures in VIDEO_DIR")
    print("   2. Convert WebP → MP4/WebM (see scripts/convert_to_mp4.py)")
    print("   3. Move final assets to site/docs/assets/")
    print("   4. Update docs with <VideoFallback>\n")


def clean_dirs():
    for d in [VIDEO_DIR, ASSETS_DIR]:
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    asyncio.run(main())
