"""Run a single screenshot workflow in isolation (separate process).

With video recording enabled (default), also trims the recorded webm to
the workflow's action window (navigate → screenshot) and encodes a small
H.264 clip next to the screenshot. Context close is safe on Playwright
1.62.0; the old 1.58.2 EPIPE crash is why this subprocess isolation
exists and why it stays."""

import asyncio
import contextlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from capture.run_screenshot_captures import (
    SCREENSHOT_DIR,
    setup_authenticated_context,
)


def make_clip(video_path: Path, mp4_path: Path, t0, start, end) -> Path | None:
    """Trim webm to [start-t0-0.3s, end-t0+0.8s] and encode h264 mp4."""
    if not video_path.exists() or t0 is None or start is None or end is None:
        return None
    ss = max(0.0, start - t0 - 0.3)
    to = end - t0 + 0.8
    if to - ss < 1.0:
        return None
    subprocess.run(
        [
            "ffmpeg", "-y", "-ss", f"{ss:.2f}", "-to", f"{to:.2f}", "-i", str(video_path),
            "-c:v", "libx264", "-crf", "30", "-pix_fmt", "yuv420p",
            "-movflags", "+faststart", "-an", str(mp4_path),
        ],
        check=True, capture_output=True,
    )
    return mp4_path if mp4_path.exists() and mp4_path.stat().st_size > 1000 else None


async def run_one(module_path: str, fn_name: str):
    import importlib.util

    spec = importlib.util.spec_from_file_location("capture_mod", module_path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    fn = getattr(mod, fn_name)

    from playwright.async_api import async_playwright

    record = os.environ.get("SOGO_RECORD_VIDEO", "1") == "1"
    video_dir = SCREENSHOT_DIR / f"{fn_name}_vid" if record else None

    p = await async_playwright().start()
    browser = await p.chromium.launch(
        headless=True,
        args=[
            "--disable-dev-shm-usage",
            "--no-first-run",
        ],
    )
    # Use mod's own setup so VIDEO_* markers share one module instance
    # (importing from the package would create a second, marker-less copy).
    ctx = await mod.setup_authenticated_context(browser, video_dir)
    try:
        result = await fn(ctx)
        if result:
            print(json.dumps({"ok": True, "path": str(result)}))
        else:
            print(json.dumps({"ok": False, "error": "no result"}))
    except Exception as e:
        # A failed workflow must not leave a screenshot behind: main() treats
        # an existing PNG as success, so a half-captured shot of the wrong
        # state would silently "succeed".
        stem = fn_name[len("record_"):].replace("_", "-")
        for suffix in (".png", "_raw.png", "_metadata.json"):
            with contextlib.suppress(OSError):
                (SCREENSHOT_DIR / f"{stem}{suffix}").unlink()
        print(json.dumps({"ok": False, "error": str(e)}))

    # Finalize the video, then trim to the action window.
    await ctx.close()
    await browser.close()
    if record and mod.VIDEO_PAGE_PATH:
        stem = fn_name[len("record_"):].replace("_", "-")
        clip = make_clip(
            Path(mod.VIDEO_PAGE_PATH),
            SCREENSHOT_DIR / f"{stem}.mp4",
            mod.VIDEO_PAGE_T0, mod.VIDEO_START, mod.VIDEO_END,
        )
        if clip:
            print(json.dumps({"ok": True, "clip": str(clip)}))
    sys.stdout.flush()
    os._exit(0)


if __name__ == "__main__":
    asyncio.run(run_one(sys.argv[1], sys.argv[2]))
