#!/usr/bin/env python3
"""
DocMaker AI — Capture Pipeline

Automates SOGo workflows with Playwright:
  - Takes screenshots at each step
  - Creates animated GIFs from step sequences
  - Outputs organized into site/docs/assets/

Usage:
  python capture.py workflows/calendar-create-event.yaml
  python capture.py --all                         # Run all workflows
  python capture.py --list                        # List available workflows

Environment variables:
  SOGO_URL       SOGo instance URL (e.g. https://demo.sogo.nu/SOGo/)
  SOGO_USERNAME  Login username
  SOGO_PASSWORD  Login password
  SOGO_RECIPIENT Recipient email for tests
  EVENT_DATE     Date for test events (YYYY-MM-DD)
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml
from PIL import Image


def load_env(env_path: Path | None = None) -> None:
    """Load .env file into environment variables."""
    if env_path is None:
        env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                key, val = key.strip(), val.strip().strip("\"'")
                if not os.environ.get(key):
                    os.environ[key] = val


# ── Paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
WORKFLOW_DIR = ROOT / "workflows"
SCREENSHOT_DIR = ROOT / "screenshots"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"


# ── Helpers ────────────────────────────────────────────────────────────

def env_substitute(value: str) -> str:
    """Substitute ${VAR} placeholders with environment variables."""
    pattern = re.compile(r"\$\{(\w+)\}")
    def replacer(match):
        key = match.group(1)
        val = os.environ.get(key)
        if val is None:
            print(f"  ⚠  Warning: environment variable ${key} is not set")
            return match.group(0)
        return val
    return pattern.sub(replacer, value)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def clean_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


# ── GIF Generation ────────────────────────────────────────────────────

def create_gif(image_paths: list[Path], output_path: Path,
               duration: int = 800, loop: int = 0) -> None:
    """Create an animated GIF from a list of PNG images."""
    if not image_paths:
        print("  ⚠  No screenshots to create GIF")
        return

    frames = []
    for img_path in image_paths:
        if img_path.exists():
            img = Image.open(img_path).convert("P", palette=Image.Palette.ADAPTIVE)
            frames.append(img)

    if len(frames) < 2:
        print("  ⚠  Need at least 2 frames for a GIF")
        return

    output_path.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration,
        loop=loop,
        optimize=True,
    )
    print(f"  ✓  GIF created: {output_path} ({len(frames)} frames)")


# ── Playwright Runner ─────────────────────────────────────────────────

def generate_playwright_script(workflow: dict) -> str:
    """Generate a Playwright Python script from a workflow definition."""
    name = workflow.get("name", "Unnamed Workflow")
    steps = workflow.get("steps", [])

    # Ensure unique run ID for this execution
    run_id = str(int(time.time()))

    lines = [
        "import asyncio",
        "from playwright.async_api import async_playwright",
        "import os",
        "",
        f'WORKFLOW_NAME = {json.dumps(name)}',
        f'RUN_ID = {json.dumps(run_id)}',
        f'SCREENSHOT_DIR = {json.dumps(str(SCREENSHOT_DIR))}',
        f'GIF_DIR = {json.dumps(str(GIF_DIR))}',
        f'ASSETS_DIR = {json.dumps(str(ASSETS_DIR))}',
        "",
        "",
        "async def run():",
        "    screenshots = []",
        "    gif_frames = []",
        "    gif_active = False",
        "    gif_name = None",
        "",
        '    async with async_playwright() as p:',
        '        browser = await p.chromium.launch(headless=True)',
        (  # noqa: E501
            '        context = await browser.new_context('
            'viewport={"width": 1280, "height": 800}, ignore_https_errors=True)'
        ),
        "        page = await context.new_page()",
        "",
    ]

    # Add each step
    for i, step in enumerate(steps):
        step_id = step.get("id", f"step-{i}")
        action = step.get("action", "")
        selector = step.get("selector", "")
        value = step.get("value", "")
        url = step.get("url", "")
        wait_after = step.get("wait_after", 0)
        take_screenshot = step.get("screenshot", False)
        gif_start = step.get("gif_start", False)
        gif_end = step.get("gif_end", False)
        gif_name_val = step.get("gif_name", None)
        wait_before = step.get("wait_before", 0)

        # Comment
        lines.append(f"        # ── Step {i+1}: {step_id} ({action}) ──")

        # Optional wait before
        if wait_before:
            lines.append(f"        await page.wait_for_timeout({wait_before * 1000})")

        # Action
        if action == "navigate":
            resolved_url = env_substitute(url)
            lines.append(f"        await page.goto({json.dumps(resolved_url)})")
            lines.append("        await page.wait_for_load_state('networkidle')")

        elif action == "click":
            lines.append(f"        await page.click({json.dumps(selector)})")

        elif action == "type":
            resolved_value = env_substitute(value)
            lines.append(f"        await page.click({json.dumps(selector)})")
            lines.append(f"        await page.fill({json.dumps(selector)}, '')")
            lines.append(
                f"        await page.type({json.dumps(selector)}, "
                f"{json.dumps(resolved_value)}, delay=50)"
            )

        elif action == "select":
            resolved_value = env_substitute(value)
            lines.append(
                f"        await page.select_option({json.dumps(selector)}, "
                f"{json.dumps(resolved_value)})"
            )

        elif action == "dblclick":
            lines.append(f"        await page.dblclick({json.dumps(selector)})")

        elif action == "toggle":
            lines.append(f"        await page.click({json.dumps(selector)})")
            lines.append("        await page.wait_for_timeout(300)")

        elif action == "wait":
            lines.append(f"        await page.wait_for_timeout({int(value or 1) * 1000})")

        # Screenshot
        if take_screenshot:
            filename = env_substitute(take_screenshot)
            filepath = f"{{SCREENSHOT_DIR}}/{filename}"
            lines.append(
                f"        await page.screenshot(path={json.dumps(filepath)}, full_page=False)"
            )
            lines.append(f"        screenshots.append({json.dumps(filepath)})")

        # GIF tracking
        if gif_start:
            lines.append("        gif_frames = []")
            lines.append("        gif_active = True")
            lines.append(f"gif_name = {json.dumps(gif_name_val) if gif_name_val else 'None'}")
            gif_file = f"{{SCREENSHOT_DIR}}/_gif_frame_{step_id}.png"
            lines.append(
                f"        await page.screenshot(path={json.dumps(gif_file)}, full_page=False)"
            )
            lines.append(f"        gif_frames.append({json.dumps(gif_file)})")

        if gif_end:
            gif_file = f"{{SCREENSHOT_DIR}}/_gif_frame_{step_id}.png"
            lines.append(
                f"        await page.screenshot(path={json.dumps(gif_file)}, full_page=False)"
            )
            lines.append(f"        gif_frames.append({json.dumps(gif_file)})")
            lines.append("        gif_active = False")
            if gif_name_val:
                lines.append(f"gif_name = {json.dumps(env_substitute(gif_name_val))}")
            lines.append("""
        # Generate GIF
        import subprocess
        from pathlib import Path
        gif_output = Path(f"{GIF_DIR}/{gif_name or 'animation.gif'}")
        gif_output.parent.mkdir(parents=True, exist_ok=True)
        if len(gif_frames) >= 2:
            from PIL import Image
            frames = []
            for f in gif_frames:
                img = Image.open(f).convert('P', palette=Image.Palette.ADAPTIVE)
                frames.append(img)
            frames[0].save(
                gif_output,
                save_all=True,
                append_images=frames[1:],
                duration=800,
                loop=0,
                optimize=True,
            )
            print(f'GIF created: {gif_output}')
            # Copy to assets
            import shutil
            assets_dir = Path(f'{ASSETS_DIR}')
            assets_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(gif_output), str(assets_dir / gif_output.name))
            print(f'GIF copied to assets: {assets_dir / gif_output.name}')
""")

        # Optional wait after
        if wait_after:
            lines.append(f"        await page.wait_for_timeout({wait_after * 1000})")

    # Close browser
    lines.append("")
    lines.append("        await browser.close()")
    lines.append("")
    lines.append("    # Copy screenshots to assets")
    lines.append("    import shutil")
    lines.append("    assets_dir = Path(ASSETS_DIR)")
    lines.append("    assets_dir.mkdir(parents=True, exist_ok=True)")
    lines.append("    for shot in screenshots:")
    lines.append("        src = Path(shot)")
    lines.append("        if src.exists():")
    lines.append("            shutil.copy2(str(src), str(assets_dir / src.name))")
    lines.append("    print(f'Copied {len(screenshots)} screenshots to {assets_dir}')")
    lines.append("")
    lines.append("")
    lines.append("asyncio.run(run())")

    return "\n".join(lines)


def run_workflow(workflow_path: Path) -> bool:
    """Load a workflow YAML and execute it via Playwright."""
    print(f"\n{'='*60}")
    print(f"  Workflow: {workflow_path.name}")
    print(f"{'='*60}")

    with open(workflow_path) as f:
        workflow = yaml.safe_load(f)

    if not workflow:
        print("  ✗  Empty workflow file")
        return False

    print(f"  Name: {workflow.get('name', 'Unnamed')}")
    print(f"  Steps: {len(workflow.get('steps', []))}")

    # Generate Playwright script
    script = generate_playwright_script(workflow)

    # Write temporary script
    script_path = SCREENSHOT_DIR / f"_run_{workflow_path.stem}.py"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    with open(script_path, "w") as f:
        f.write(script)

    # Execute
    print("  Running Playwright...")
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        print("  ✗  Error running workflow:")
        print(f"     {result.stderr.strip()}")
        return False

    print(result.stdout)
    if result.stderr:
        print(f"  Stderr: {result.stderr.strip()}")
    print("  ✓  Workflow completed")
    return True


# ── CLI ────────────────────────────────────────────────────────────────

def list_workflows() -> None:
    """List available workflow YAML files."""
    workflows = sorted(WORKFLOW_DIR.glob("*.yaml"))
    if not workflows:
        print("No workflows found in capture/workflows/")
        return
    print("\nAvailable workflows:")
    for wf in workflows:
        with open(wf) as f:
            meta = yaml.safe_load(f) or {}
        print(f"  {wf.name}")
        print(f"    Name:  {meta.get('name', 'N/A')}")
        print(f"    Steps: {len(meta.get('steps', []))}")
        print()


def run_all() -> None:
    """Run all workflows in sequence."""
    workflows = sorted(WORKFLOW_DIR.glob("*.yaml"))
    if not workflows:
        print("No workflows found")
        return

    clean_dir(SCREENSHOT_DIR)
    clean_dir(GIF_DIR)
    ensure_dir(ASSETS_DIR)

    success = 0
    for wf in workflows:
        if run_workflow(wf):
            success += 1

    print(f"\n{'='*60}")
    print(f"  Completed: {success}/{len(workflows)} workflows")
    print(f"  Screenshots: {SCREENSHOT_DIR}")
    print(f"  GIFs: {GIF_DIR}")
    print(f"  Assets (for site): {ASSETS_DIR}")
    print(f"{'='*60}")


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser(
        description="DocMaker AI — Capture Pipeline",
    )
    parser.add_argument("workflow", nargs="?", help="Path to workflow YAML file")
    parser.add_argument("--all", action="store_true", help="Run all workflows")
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument("--install", action="store_true", help="Install Playwright browsers")

    args = parser.parse_args()

    if args.install:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        return

    if args.list:
        list_workflows()
        return

    if args.all:
        run_all()
        return

    if args.workflow:
        wf_path = Path(args.workflow)
        if not wf_path.exists():
            wf_path = WORKFLOW_DIR / args.workflow
            if not wf_path.exists():
                print(f"Workflow not found: {args.workflow}")
                sys.exit(1)

        ensure_dir(SCREENSHOT_DIR)
        ensure_dir(GIF_DIR)
        ensure_dir(ASSETS_DIR)
        run_workflow(wf_path)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
