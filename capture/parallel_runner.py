import asyncio
import json
import shutil
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
GIF_DIR = ROOT / "gifs"
ASSETS_DIR = ROOT.parent / "site" / "docs" / "assets"


async def run_workflow(
    name: str,
    workflow_fn,
    browser,
    storage: dict,
    semaphore: asyncio.Semaphore,
) -> tuple[str, bool, int, str | None, float]:
    async with semaphore:
        print(f"\n── {name} ──")
        start = time.time()
        ctx = await browser.new_context(
            record_video_dir=str(VIDEO_DIR),
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            ignore_https_errors=True,
            storage_state=storage,
        )
        try:
            webp_path = await workflow_fn(ctx)
            if webp_path:
                shutil.copy2(str(webp_path), str(ASSETS_DIR / webp_path.name))
                meta_path = VIDEO_DIR / f"{name}_metadata.json"
                if meta_path.exists():
                    meta = json.loads(meta_path.read_text())
                    elapsed = time.time() - start
                    frames = meta["annotated_frames"]
                    size_kb = meta["webp_size_kb"]
                    print(f"  ✓  {webp_path.name} — {frames} frames, {size_kb}KB ({elapsed:.1f}s)")
                    return (name, True, frames, None, elapsed)
                elapsed = time.time() - start
                print(f"  ✓  {webp_path.name} ({elapsed:.1f}s)")
                return (name, True, 0, None, elapsed)
            elapsed = time.time() - start
            return (name, False, 0, "blank capture", elapsed)
        except Exception as e:
            elapsed = time.time() - start
            print(f"  ✗  Error ({elapsed:.1f}s): {e}")
            return (name, False, 0, str(e), elapsed)
        finally:
            await ctx.close()


async def run_parallel(
    workflows: list[tuple[str, Any]],
    browser,
    storage: dict,
    workers: int = 4,
) -> list[tuple[str, bool, int, str | None, float]]:
    semaphore = asyncio.Semaphore(workers)
    tasks = [run_workflow(name, fn, browser, storage, semaphore) for name, fn in workflows]
    return await asyncio.gather(*tasks)
