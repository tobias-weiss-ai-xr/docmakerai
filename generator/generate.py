"""Tutorial generation engine.

Orchestrates LLM-based analysis of captured steps and renders
markdown tutorials using Jinja2 templates.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Optional

import typer
import yaml
from jinja2 import Environment, FileSystemLoader
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
)

from generator.llm import LLMClient
from generator.schema import (
    CaptureResult,
    GeneratorConfig,
    StepResult,
    Tutorial,
    TutorialStep,
)

cli = typer.Typer(
    name="generator",
    help="DocMaker AI — LLM tutorial generator",
    add_completion=False,
)

console = Console()
HERE = Path(__file__).parent


def _load_capture(capture_path: str) -> CaptureResult:
    """Load a capture result JSON file."""
    with open(capture_path) as f:
        data = json.load(f)
    return CaptureResult(**data)


def _load_config() -> GeneratorConfig:
    """Load provider configuration from YAML."""
    config_path = HERE / "config" / "providers.yaml"
    if config_path.exists():
        with open(config_path) as f:
            data = yaml.safe_load(f)
        return GeneratorConfig(**data)
    return GeneratorConfig()


def _build_mermaid_diagram(tutorial: Tutorial) -> str:
    """Build a Mermaid.js flowchart from tutorial steps."""
    lines = ["graph TD"]
    prev_id = None
    for i, step in enumerate(tutorial.steps):
        node_id = f"S{i + 1}"
        step_id = step.id.replace("-", "_").replace(" ", "_")
        safe_title = step.title.replace('"', "'")
        lines.append(f'    {node_id}["{safe_title}"]')
        if prev_id:
            lines.append(f"    {prev_id} --> {node_id}")
        prev_id = node_id
    lines.append(f"    {prev_id} --> Done((Done))")
    return "\n".join(lines)


def _generate_intro(steps: list[TutorialStep]) -> str:
    """Generate an introduction based on the tutorial steps."""
    total_steps = len(steps)
    first_action = steps[0].title.lower() if steps else "get started"
    return (
        f"This tutorial will guide you through **{total_steps} steps** "
        f"to complete this task. You will learn how to {first_action} "
        f"and progress through the entire workflow."
    )


def _generate_conclusion(steps: list[TutorialStep]) -> str:
    """Generate a conclusion for the tutorial."""
    if not steps:
        return "You have completed this tutorial."
    last_step = steps[-1]
    return (
        f"You have successfully completed this workflow. "
        f"After **{last_step.title.lower()}**, "
        f"you should see the expected result. "
        f"You can now proceed to related tutorials or explore other features."
    )


def _extract_prerequisites(capture: CaptureResult, steps: list[TutorialStep]) -> list[str]:
    """Extract prerequisites from the workflow."""
    prereqs = ["A working SOGo account with valid credentials"]
    for step in capture.steps:
        if step.action in ("navigate", "click") and "login" in step.id.lower():
            prereqs.append("Access to the SOGo web interface")
            break
    return prereqs


def _generate_tags(capture: CaptureResult) -> list[str]:
    """Generate relevant tags from the workflow."""
    tags = ["tutorial", "sogo", "how-to"]
    name_lower = capture.workflow_name.lower()
    if "login" in name_lower or "log in" in name_lower:
        tags.extend(["authentication", "getting-started"])
    elif "email" in name_lower or "mail" in name_lower:
        tags.extend(["email", "communication"])
    elif "calendar" in name_lower:
        tags.extend(["calendar", "scheduling"])
    elif "contact" in name_lower:
        tags.extend(["contacts", "address-book"])
    return tags


def _rerender_with_jinja(tutorial: Tutorial) -> str:
    """Render the tutorial markdown using the Jinja2 template."""
    template_dir = HERE / "templates"
    env = Environment(loader=FileSystemLoader(str(template_dir)))
    template = env.get_template("tutorial.md.j2")

    for step in tutorial.steps:
        if step.screenshot_path:
            step.screenshot_path = os.path.relpath(
                step.screenshot_path,
                start=os.path.dirname(str(HERE)),
            )

    return template.render(tutorial=tutorial)


def generate_tutorial(
    capture_result: CaptureResult,
    llm_client: Optional[LLMClient] = None,
) -> Tutorial:
    """Generate a complete Tutorial from a CaptureResult."""
    steps: list[TutorialStep] = []
    total = len(capture_result.steps)

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing steps...", total=total)

        for step_result in capture_result.steps:
            screenshot_desc = ""
            if step_result.screenshot_path and llm_client:
                try:
                    screenshot_desc = llm_client.analyze_step_screenshot(
                        screenshot_path=step_result.screenshot_path,
                        step_description=step_result.description,
                        step_action=step_result.action,
                    )
                except Exception as e:
                    console.print(f"  [yellow]LLM analysis failed for {step_result.id}: {e}[/]")

            tutorial_step = TutorialStep(
                id=step_result.id,
                title=_generate_step_title(step_result),
                description=_generate_step_description(step_result, screenshot_desc),
                tip=step_result.description if "login" in step_result.id and "tip" in step_result.id else None,
                screenshot_path=step_result.screenshot_path,
                expected_outcome=_generate_expected_outcome(step_result),
            )
            steps.append(tutorial_step)
            progress.update(task, advance=1)

    tutorial = Tutorial.new(
        title=capture_result.workflow_name,
        description=f"Step-by-step guide: {capture_result.workflow_name.lower()}",
    )
    tutorial.steps = steps
    tutorial.introduction = _generate_intro(steps)
    tutorial.prerequisites = _extract_prerequisites(capture_result, steps)
    tutorial.tags = _generate_tags(capture_result)
    tutorial.conclusion = _generate_conclusion(steps)
    tutorial.workflow_diagram = _build_mermaid_diagram(tutorial)

    return tutorial


def _generate_step_title(step: "StepResult") -> str:
    """Generate a human-readable step title from the action and description."""
    action_map = {
        "navigate": "Navigate to",
        "click": "Click on",
        "type": "Enter",
        "wait": "Wait for",
        "wait_for_selector": "Wait for",
        "fill_form": "Fill in",
        "select_option": "Select",
    }
    prefix = action_map.get(step.action, step.action.capitalize())
    desc = step.description.split(".")[0].strip()
    if len(desc) > 60:
        desc = desc[:57] + "..."
    return f"{prefix} {desc}"


def _generate_step_description(
    step: "StepResult",
    screenshot_analysis: str,
) -> str:
    """Combine step metadata with LLM screenshot analysis into a description."""
    parts = [step.description]
    if screenshot_analysis:
        parts.append(f"\n\n*{screenshot_analysis}*")
    return "".join(parts)


def _generate_expected_outcome(step: "StepResult") -> Optional[str]:
    """Generate expected outcome text based on the action."""
    outcomes = {
        "navigate": "The page will load and display the requested content.",
        "click": "The interface will respond to your click.",
        "type": "The input field will contain your text.",
        "wait_for_selector": "The expected element will appear on the page.",
        "fill_form": "The form fields will be populated.",
    }
    return outcomes.get(step.action)


@cli.command()
def generate(
    capture: Path = typer.Option(
        ...,
        "--capture",
        "-c",
        help="Path to capture-result.json file",
        exists=True,
        file_okay=True,
        readable=True,
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output path for the generated tutorial (.md file or directory)",
    ),
    capture_dir: Optional[Path] = typer.Option(
        None,
        "--capture-dir",
        help="Directory containing multiple capture-result.json files (batch mode)",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
) -> None:
    """Generate a tutorial markdown file from a capture result."""
    config = _load_config()

    llm_client: Optional[LLMClient] = None
    has_api_key = any(
        os.environ.get(p.api_key_env) for p in config.providers.values() if p.api_key_env
    )
    if has_api_key:
        llm_client = LLMClient(config)
        console.print(f"[dim]LLM provider: {config.default_provider} ({llm_client.model})[/]")
    else:
        console.print("[yellow]No LLM API keys found. Using fallback descriptions.[/]")

    capture_paths: list[Path] = []
    if capture_dir:
        capture_paths = list(capture_dir.rglob("capture-result.json"))
        if not capture_paths:
            console.print("[red]No capture-result.json files found in directory.[/]")
            raise typer.Exit(1)
    else:
        capture_paths = [capture]

    for cap_path in capture_paths:
        console.print(f"\n[bold]Processing:[/] {cap_path}")

        capture_result = _load_capture(str(cap_path))
        tutorial = generate_tutorial(capture_result, llm_client)

        if output.is_dir() or not capture_dir:
            out_path = output / f"{Path(cap_path).parent.name}.md" if output.suffix != ".md" else output
        else:
            out_path = output

        out_path.parent.mkdir(parents=True, exist_ok=True)

        markdown = _rerender_with_jinja(tutorial)
        with open(out_path, "w") as f:
            f.write(markdown)

        console.print(f"[green]Tutorial saved:[/] {out_path}")
