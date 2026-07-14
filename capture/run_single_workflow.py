"""Run a single capture workflow in isolation (separate process)."""
import sys
import json
import os
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from capture.run_task_first_captures import (
    VIDEO_DIR,
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
            "--disable-features=TranslateUI",
            "--disable-background-networking",
        ],
    )
    ctx = await setup_authenticated_context(browser, VIDEO_DIR)
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
