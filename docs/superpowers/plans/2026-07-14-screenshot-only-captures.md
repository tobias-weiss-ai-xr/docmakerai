# Screenshot-Only Capture Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the slow, fragile video (WebP) capture pipeline with a fast, reliable screenshot-only pipeline that produces annotated PNG screenshots for each workflow's key moments.

**Architecture:** Each workflow function navigates SOGo 6, takes a single full-page screenshot at the "result" moment (when the feature is fully demonstrated), annotates it with a step header overlay using the existing Pillow engine, and saves it as a PNG. The entire pipeline runs in a single Playwright process — no video recording, no ffmpeg, no frame extraction, no WebP assembly. Each workflow completes in ~15 seconds instead of ~120 seconds.

**Tech Stack:** Playwright (Python, async), Pillow (annotation overlays), asyncio (sequential execution with subprocess isolation for Playwright EPIPE safety)

---

## File Structure

### Files to CREATE

| File | Responsibility |
|------|---------------|
| `capture/run_screenshot_captures.py` | New main entry point. Contains all 22 `record_*` workflow functions, the `ScreenshotRecorder` class, helpers (`login`, `goto`, `navigate_to_module`, `navigate_to_settings`), and `main()`. Each workflow is a simple async function that navigates, interacts, takes one screenshot. |
| `capture/run_single_screenshot.py` | Subprocess worker (like existing `run_single_workflow.py`). Runs one workflow in isolation, uses `os._exit(0)` to bypass Playwright EPIPE cleanup bug. |

### Files to MODIFY

| File | Change |
|------|--------|
| `capture/run_task_first_captures.py` | DELETE entirely — replaced by `run_screenshot_captures.py` |
| `capture/run_single_workflow.py` | DELETE entirely — replaced by `run_single_screenshot.py` |
| `capture/video_pipeline.py` | DELETE entirely — no video processing needed |
| `capture/annotate.py` | KEEP as-is — the Pillow overlay engine is reused for step header annotations on screenshots |
| `site/docs/sogo-*.md` (12 files) | Update `.webp` references to `.png` in markdown image syntax |
| `site/docs/sogo-gaps.md` | Update asset references table from `.webp` to `.png` |

### Files to KEEP unchanged

| File | Why |
|------|-----|
| `capture/annotate.py` | Pillow overlay engine — reused for screenshot annotations |
| `capture/capture.py` | Legacy capture script for change-detection CI — separate concern |
| `capture/detect_changes.py` | Perceptual hash drift detection — separate concern |
| `capture/baselines/` | Baseline images for drift detection |
| `capture/screenshots/` | Directory for new PNG outputs |
| `capture/requirements.txt` | No new dependencies needed |
| `site/src/components/VideoFallback.tsx` | Not used in any current markdown (all use standard `![]()` syntax) |

---

## Key Design Decisions

### 1. One screenshot per workflow (not per step)

Each workflow takes a **single** screenshot at the "result" moment — when the feature is fully visible on screen. This is the frame that matters for documentation. The context/challenge/solution narrative steps still run (navigation, clicks, fills), but only the final state is captured.

Rationale: Documentation pages show one image per step. A video clip or animated WebP is overkill — users want to see the end state, not watch clicks. The existing markdown uses standard `![](./assets/foo.webp)` which renders as a static image anyway (Docusaurus doesn't animate `.webp`).

### 2. Annotated screenshot with step header

Reuse `capture/annotate.py`'s `annotate_frame()` to draw a header bar on the screenshot with the result text (e.g. "RESULT: The new event appears on the calendar"). This gives context without animation.

### 3. PNG output, not WebP

PNG is universally supported, lossless, and renders correctly in all markdown renderers. No ffmpeg dependency. The annotation overlay uses Pillow which already writes PNG.

### 4. Subprocess isolation (keep existing pattern)

Keep the `os._exit(0)` subprocess pattern from `run_single_workflow.py` to avoid the Playwright 1.58.2 EPIPE cleanup bug. Each workflow runs in its own Python process.

### 5. Sequential execution only

No parallel mode. Screenshots are fast (~15s each), so 22 workflows = ~5.5 minutes total. Not worth the complexity or risk of parallel Playwright crashes.

---

## Task 1: Create ScreenshotRecorder class

**Files:**
- Create: `capture/run_screenshot_captures.py` (partial — class + helpers only)

- [ ] **Step 1: Create the file with imports, constants, and helpers**

Copy these from `run_task_first_captures.py` (lines 33-78) unchanged:
- Imports (`asyncio`, `json`, `sys`, `os`, `shutil`, `time`, `Path`, `BrowserContext`, `Page`, `async_playwright`)
- `ROOT`, `VIDEO_DIR` → rename to `SCREENSHOT_DIR` = `ROOT / "screenshots"`
- `ASSETS_DIR` = `ROOT.parent / "site" / "docs" / "assets"`
- `SOGO_URL`, `USERNAME`, `PASSWORD` constants
- Remove `FPS` and `LOCALE` constants (no longer needed for video; locale was "de" which was wrong anyway)
- Remove video_pipeline imports entirely
- Add import: `from capture.annotate import annotate_frame`
- Keep `clean_dirs()` function
- Keep `login()`, `goto()`, `navigate_to_module()`, `navigate_to_settings()` functions unchanged

```python
#!/usr/bin/env python3
"""DocMaker AI — Screenshot-Only Capture Pipeline

Fast, reliable screenshot captures for SOGo 6 documentation.
Each workflow navigates to a feature, interacts, and takes a single
annotated screenshot at the result moment.

Usage:
    export SOGO_URL=https://demov6.sogo.nu
    python capture/run_screenshot_captures.py
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import shutil
import sys
import time
from pathlib import Path

from playwright.async_api import BrowserContext, Page, async_playwright

try:
    from capture.annotate import annotate_frame
except ImportError:
    from annotate import annotate_frame


ROOT = Path(__file__).resolve().parent
SCREENSHOT_DIR = ROOT / "screenshots"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"

SOGO_URL = os.environ.get("SOGO_URL", "https://demov6.sogo.nu")
USERNAME = os.environ.get("SOGO_USERNAME", "sogo-tests1@example.org")
PASSWORD = os.environ.get("SOGO_PASSWORD", "sogo")
```

- [ ] **Step 2: Write the ScreenshotRecorder class**

Replace `TaskFirstRecorder` with a simple `ScreenshotRecorder`:

```python
class ScreenshotRecorder:
    """Takes a single annotated screenshot at the result moment."""

    def __init__(self, name: str, screenshot_dir: Path):
        self.name = name
        self.screenshot_dir = screenshot_dir

    async def start(self, context: BrowserContext) -> Page:
        page = await context.new_page()
        return page

    async def context(self, page, text: str) -> None:
        print(f"   [CONTEXT] {text}")

    async def challenge(self, page, text: str) -> None:
        print(f"   [CHALLENGE] {text}")

    async def solution(self, page, text: str) -> None:
        print(f"   [SOLUTION] {text}")

    async def result(self, page, text: str) -> None:
        print(f"   [RESULT] {text}")

    async def capture(self, page, label: str) -> Path | None:
        """Take a full-page screenshot and annotate it with the given label."""
        raw_path = self.screenshot_dir / f"{self.name}_raw.png"
        annotated_path = self.screenshot_dir / f"{self.name}.png"

        try:
            await page.screenshot(path=str(raw_path), full_page=False)
        except Exception as e:
            print(f"  Screenshot failed: {e}")
            return None

        if not raw_path.exists() or raw_path.stat().st_size < 1000:
            return None

        annotate_frame(
            str(raw_path),
            label,
            4,  # step number (always "result" = step 4)
            [],  # no highlights needed
            locale="en",
            output_path=str(annotated_path),
        )
        raw_path.unlink(missing_ok=True)

        if not annotated_path.exists():
            return None

        meta_path = self.screenshot_dir / f"{self.name}_metadata.json"
        with open(meta_path, "w") as f:
            json.dump(
                {
                    "workflow": self.name,
                    "label": label,
                    "png_file": annotated_path.name,
                    "png_size_kb": annotated_path.stat().st_size // 1024,
                },
                f,
                indent=2,
            )

        return annotated_path
```

- [ ] **Step 3: Verify the file has no import errors**

Run: `python3 -c "import capture.run_screenshot_captures"` from project root
Expected: No output (clean import)

---

## Task 2: Port all 22 workflow functions

**Files:**
- Modify: `capture/run_screenshot_captures.py` (add workflow functions)

- [ ] **Step 1: Port all 22 `record_*` functions**

For each workflow in `run_task_first_captures.py` (lines 345-932), port to the new file with these changes:

**Pattern transformation (apply to ALL 22 functions):**

BEFORE (video approach):
```python
async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    rec = TaskFirstRecorder("calendar-create-event", VIDEO_DIR, FPS, LOCALE)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)
    await rec.context(page, "Schedule a team meeting...")
    await page.wait_for_timeout(800)
    await rec.challenge(page, "Click the 'Create Event' button...")
    create_btn = page.locator('button:has-text("Create Event")').first
    if await create_btn.is_visible(timeout=3000):
        await rec.highlight(page, 'button:has-text("Create Event")', "Create Event button")
        await create_btn.click()
        await page.wait_for_timeout(1500)
    await rec.solution(page, "Enter event title, set date and time...")
    await page.wait_for_timeout(1500)
    await rec.result(page, "The new event appears on the calendar...")
    await page.wait_for_timeout(800)
    return await rec.finish(page)
```

AFTER (screenshot approach):
```python
async def record_calendar_create_event(context: BrowserContext) -> Path | None:
    rec = ScreenshotRecorder("calendar-create-event", SCREENSHOT_DIR)
    page = await rec.start(context)
    await navigate_to_module(page, "calendar")
    await page.wait_for_timeout(1000)
    await rec.context(page, "Schedule a team meeting to discuss project updates")
    await page.wait_for_timeout(800)
    await rec.challenge(page, "Click the 'Create Event' button to open the event editor")
    create_btn = page.locator('button:has-text("Create Event")').first
    if await create_btn.is_visible(timeout=3000):
        await create_btn.click()
        await page.wait_for_timeout(1500)
    await rec.solution(page, "Enter event title, set date and time, then save the event")
    await page.wait_for_timeout(1500)
    await rec.result(page, "The new event appears on the calendar at the scheduled time")
    await page.wait_for_timeout(800)
    return await rec.capture(page, "The new event appears on the calendar at the scheduled time")
```

Key changes per function:
1. `TaskFirstRecorder(...)` → `ScreenshotRecorder("name", SCREENSHOT_DIR)`
2. Remove `FPS, LOCALE` args
3. Remove all `rec.highlight()` calls (visual annotations aren't needed for a single screenshot)
4. `return await rec.finish(page)` → `return await rec.capture(page, "result text")`
5. Keep ALL navigation, clicking, and filling logic identical
6. Keep the `context()`, `challenge()`, `solution()`, `result()` print calls (they produce CLI output for logging)

The 22 workflows to port (all from `run_task_first_captures.py`):
1. `record_calendar_create_event` (line 348)
2. `record_calendar_recurring` (line 377)
3. `record_mail_compose` (line 405)
4. `record_contacts_add` (line 433)
5. `record_vacation` (line 461)
6. `record_mail_signatures` (line 489)
7. `record_mail_filters` (line 517)
8. `record_calendar_subscribe` (line 545)
9. `record_calendar_share` (line 573)
10. `record_freebusy` (line 601)
11. `record_logout` (line 629)
12. `record_preferences` (line 657)
13. `record_calendar_views` (line 685)
14. `record_contacts_edit_delete` (line 713)
15. `record_calendar_edit_delete` (line 741)
16. `record_global_search` (line 769)
17. `record_mail_read` (line 797)
18. `record_mail_folder_management` (line 825)
19. `record_mail_reply_forward_delete` (line 853)
20. `record_password_change` (line 881)
21. `record_calendar_ical` (line 909)
22. `record_contacts_import_export` (line 905)

- [ ] **Step 2: Add `setup_authenticated_context` and `main()`**

Copy `setup_authenticated_context()` from `run_task_first_captures.py` (lines 938-966), but change:
- Remove `record_video_dir=str(video_dir)` from context creation (no video recording)
- Keep everything else identical (login, sessionStorage auth injection)

Write `main()` using the subprocess isolation pattern from the existing file:
```python
async def main():
    clean_dirs()

    async with async_playwright() as p:
        verify_browser = await p.chromium.launch(
            headless=True,
            args=["--disable-dev-shm-usage", "--no-first-run"],
        )
        try:
            verify_ctx = await verify_browser.new_context(
                viewport={"width": 1280, "height": 800},
                locale="en-US",
                ignore_https_errors=True,
            )
            verify_page = await verify_ctx.new_page()
            await login(verify_page, context=verify_ctx)
            await verify_ctx.close()
        finally:
            await verify_browser.close()
        print("  Login verified.\n")

    workflows = [
        ("calendar-create-event", "record_calendar_create_event"),
        # ... all 22 workflows (name, fn_name tuples) ...
        ("contacts-import-export", "record_contacts_import_export"),
    ]

    start_time = time.time()
    results = []
    worker_script = Path(__file__).parent / "run_single_screenshot.py"

    for name, fn_name in workflows:
        print(f"\n── {name} ──")
        wf_start = time.time()
        proc = await asyncio.create_subprocess_exec(
            sys.executable,
            "-u",
            str(worker_script),
            str(Path(__file__)),
            fn_name,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
        elapsed = time.time() - wf_start
        output = stdout.decode("utf-8", errors="replace")
        print(output, end="")

        png_path = SCREENSHOT_DIR / f"{name}.png"
        if png_path.exists():
            shutil.copy2(str(png_path), str(ASSETS_DIR / png_path.name))
            meta_path = SCREENSHOT_DIR / f"{name}_metadata.json"
            if meta_path.exists():
                meta = json.loads(meta_path.read_text())
                size_kb = meta.get("png_size_kb", png_path.stat().st_size // 1024)
                print(f"  ✓  {png_path.name} — {size_kb}KB ({elapsed:.1f}s)")
            else:
                print(f"  ✓  {png_path.name} ({elapsed:.1f}s)")
            results.append((name, True, elapsed))
        else:
            print(f"  ✗  Failed ({elapsed:.1f}s)")
            results.append((name, False, elapsed))

    print("\n── Results ──")
    for name, ok, duration in results:
        mark = "✓" if ok else "✗"
        print(f"  {mark}  {name} ({duration:.1f}s)")
    total_ok = sum(1 for _, ok, _ in results if ok)
    print(f"\n  {total_ok}/{len(results)} succeeded")
    print(f"\n  Total time: {time.time() - start_time:.1f}s")
```

Add CLI entry point:
```python
if __name__ == "__main__":
    asyncio.run(main())
```

---

## Task 3: Create subprocess worker

**Files:**
- Create: `capture/run_single_screenshot.py`

- [ ] **Step 1: Write the subprocess worker**

```python
"""Run a single screenshot workflow in isolation (separate process)."""
import sys
import json
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from capture.run_screenshot_captures import (
    SCREENSHOT_DIR,
    setup_authenticated_context,
)


async def run_one(module_path: str, fn_name: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location("capture_mod", module_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, fn_name)

    from playwright.async_api import async_playwright

    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=True,
        args=[
            "--disable-dev-shm-usage",
            "--no-first-run",
        ],
    )
    ctx = await setup_authenticated_context(browser, SCREENSHOT_DIR)
    try:
        result = await fn(ctx)
        if result:
            print(json.dumps({"ok": True, "path": str(result)}))
        else:
            print(json.dumps({"ok": False, "error": "no result"}))
    except Exception as e:
        print(json.dumps({"ok": False, "error": str(e)}))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    asyncio.run(run_one(sys.argv[1], sys.argv[2]))
```

---

## Task 4: Test the new pipeline end-to-end

**Files:**
- Run: `capture/run_screenshot_captures.py`

- [ ] **Step 1: Test a single workflow via subprocess**

Run: `SOGO_URL=https://demov6.sogo.nu python3 -u capture/run_single_screenshot.py capture/run_screenshot_captures.py record_mail_read`
Expected: JSON output with `"ok": true`, file appears in `capture/screenshots/mail-read.png`

- [ ] **Step 2: Verify the screenshot is valid**

Run: `python3 -c "from PIL import Image; img = Image.open('capture/screenshots/mail-read.png'); print(f'Size: {img.size}, Mode: {img.mode}')"`
Expected: `Size: (1280, 800), Mode: RGBA`

- [ ] **Step 3: Run the full pipeline**

Run: `SOGO_URL=https://demov6.sogo.nu python3 -u capture/run_screenshot_captures.py`
Expected: 22/22 workflows succeed, all PNG files in `capture/screenshots/` and `site/docs/assets/`

- [ ] **Step 4: Verify all assets exist**

Run: `ls site/docs/assets/*.png | wc -l`
Expected: `22`

---

## Task 5: Update markdown references (.webp → .png)

**Files:**
- Modify: 12 markdown files in `site/docs/` (update image references)
- Modify: `site/docs/sogo-gaps.md` (update asset table)

- [ ] **Step 1: Replace .webp with .png in all markdown image references**

In these 12 files, change `.webp)` to `.png)` on the `![...](...)` lines:
1. `site/docs/sogo-calendar-views.md` line 30
2. `site/docs/sogo-calendar-recurring.md` line 61
3. `site/docs/sogo-calendar-ical.md` line 30
4. `site/docs/sogo-calendar-subscribe.md` line 51
5. `site/docs/sogo-calendar-edit-delete.md` line 27
6. `site/docs/sogo-contacts-edit-delete.md` line 29
7. `site/docs/sogo-contacts-add.md` line 39
8. `site/docs/sogo-calendar-share.md` line 66
9. `site/docs/sogo-calendar-freebusy.md` line 47
10. `site/docs/sogo-mail-compose.md` line 39
11. `site/docs/sogo-contacts-import-export.md` line 30
12. `site/docs/sogo-global-search.md` line 26

Use ast-grep or sed to replace all `.webp)` → `.png)` in these files.

- [ ] **Step 2: Update sogo-gaps.md asset table**

In `site/docs/sogo-gaps.md`, replace all `.webp` references with `.png` in the asset status table (lines 49-107). This is a bulk find-and-replace of `.webp` → `.png` in that file.

---

## Task 6: Clean up obsolete files

**Files:**
- Delete: `capture/run_task_first_captures.py`
- Delete: `capture/run_single_workflow.py`
- Delete: `capture/video_pipeline.py`

- [ ] **Step 1: Delete obsolete capture pipeline files**

```bash
rm capture/run_task_first_captures.py
rm capture/run_single_workflow.py
rm capture/video_pipeline.py
```

- [ ] **Step 2: Delete old WebP assets from site/docs/assets/**

```bash
rm site/docs/assets/*.webp
```

These are replaced by the new PNG files from Task 4.

- [ ] **Step 3: Verify no dangling references**

Run: `grep -r "\.webp" site/docs/*.md`
Expected: No matches (all references updated in Task 5)

---

## Task 7: Final verification and commit

- [ ] **Step 1: Run the pipeline one more time to confirm everything works**

Run: `SOGO_URL=https://demov6.sogo.nu python3 -u capture/run_screenshot_captures.py`
Expected: 22/22 succeed

- [ ] **Step 2: Verify site builds without errors**

Run: `cd site && npm run build` (or whatever the Docusaurus build command is)
Expected: Build succeeds with no broken image references

- [ ] **Step 3: Commit all changes**

Commit 1: `Replace video capture pipeline with screenshot-only pipeline`
- `capture/run_screenshot_captures.py` (new)
- `capture/run_single_screenshot.py` (new)
- `capture/run_task_first_captures.py` (deleted)
- `capture/run_single_workflow.py` (deleted)
- `capture/video_pipeline.py` (deleted)

Commit 2: `Switch all doc assets from WebP to PNG screenshots`
- `site/docs/sogo-*.md` (12 files, .webp → .png)
- `site/docs/sogo-gaps.md` (.webp → .png)
- `site/docs/assets/*.png` (22 new files)
- `site/docs/assets/*.webp` (22 deleted files)

---

## Performance Expectations

| Metric | Video Pipeline (old) | Screenshot Pipeline (new) |
|--------|----------------------|--------------------------|
| Time per workflow | ~120s (video + ffmpeg + WebP assembly) | ~15s (navigate + screenshot + annotate) |
| Total for 22 workflows | ~44 minutes | ~5.5 minutes |
| Dependencies | ffmpeg, Pillow, Playwright | Pillow, Playwright |
| Output format | Animated WebP (~200-400KB) | Static PNG (~100-200KB) |
| Failure mode | EPIPE crash, blank frames, ffmpeg errors | Screenshot fails only if page blank |
| Reliability | Requires subprocess isolation hack | Same subprocess isolation (simpler) |
