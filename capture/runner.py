"""CLI runner for the capture layer."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

import typer

from capture.orchestrator import CaptureOrchestrator, load_workflow

cli = typer.Typer(
    name="capture",
    help="DocMaker AI — Web capture orchestrator",
    add_completion=False,
)


def _version_callback(value: bool) -> None:
    if value:
        from capture import __version__
        print(f"DocMaker Capture v{__version__}")
        raise typer.Exit()


@cli.command()
def capture(
    workflow: Path = typer.Option(
        ...,
        "--workflow",
        "-w",
        help="Path to workflow YAML file",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    url: str = typer.Option(
        ...,
        "--url",
        help="Base URL of the target web application (overrides workflow base_url)",
    ),
    output: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output directory for capture results and screenshots",
        file_okay=False,
        dir_okay=True,
    ),
    headless: bool = typer.Option(
        True,
        "--headless/--visible",
        help="Run browser in headless mode",
    ),
    slow_mo: int = typer.Option(
        0,
        "--slow-mo",
        help="Slow down Playwright operations by N milliseconds",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        help="Show version and exit",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    """Capture a web workflow by running the Playwright orchestrator."""
    wf = load_workflow(workflow)
    if url:
        wf.base_url = url

    print(f"Workflow: {wf.name}")
    print(f"Base URL: {wf.base_url}")
    print(f"Steps: {len(wf.steps)}")
    print(f"Output: {output.resolve()}")
    print()

    orchestrator = CaptureOrchestrator(
        workflow=wf,
        output_dir=output,
        headless=headless,
        slow_mo=slow_mo,
    )

    result = asyncio.run(orchestrator.run())

    output.mkdir(parents=True, exist_ok=True)
    result_path = output / "capture-result.json"
    with open(result_path, "w") as f:
        json.dump(result.model_dump(), f, indent=2)

    print(f"\nCapture complete in {result.duration_ms}ms")
    print(f"Results saved to: {result_path}")
    print(f"Successful steps: {sum(1 for s in result.steps if s.success)}/{len(result.steps)}")

    if any(not s.success for s in result.steps):
        print("\nFailed steps:")
        for s in result.steps:
            if not s.success:
                print(f"  - {s.id}: {s.error}")
        sys.exit(1)
