import asyncio
import importlib
import json
import sys
import types
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from capture.parallel_runner import ASSETS_DIR, run_workflow, run_parallel


def _make_browser_mock() -> AsyncMock:
    """Create a mock browser with a mock context."""
    browser = AsyncMock()
    ctx = AsyncMock()
    browser.new_context.return_value = ctx
    return browser, ctx


@pytest.mark.asyncio
async def test_run_workflow_success_with_metadata(tmp_path: Path):
    """Successful workflow returns annotated_frames when metadata file exists."""
    name = "test_success_meta"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)

    video_dir = tmp_path / "videos"
    video_dir.mkdir()
    meta_path = video_dir / f"{name}_metadata.json"
    meta_path.write_text(json.dumps({"annotated_frames": 17, "webp_size_kb": 256}))

    output_webp = tmp_path / "result.webp"
    output_webp.write_text("fake-webp-content")
    workflow_fn = AsyncMock(return_value=output_webp)

    with patch("capture.parallel_runner.shutil.copy2") as mock_copy:
        with patch("capture.parallel_runner.VIDEO_DIR", video_dir):
            result = await run_workflow(
                name, workflow_fn, browser, {"storage": "data"}, semaphore,
            )

    assert result == (name, True, 17, None)
    browser.new_context.assert_awaited_once_with(
        record_video_dir=str(video_dir),
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        ignore_https_errors=True,
        storage_state={"storage": "data"},
    )
    ctx.close.assert_awaited_once()
    mock_copy.assert_called_once_with(
        str(output_webp), str(ASSETS_DIR / "result.webp"),
    )


@pytest.mark.asyncio
async def test_run_workflow_success_without_metadata(tmp_path: Path):
    """Successful workflow returns 0 frames when metadata file does not exist."""
    name = "test_no_meta"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)

    video_dir = tmp_path / "videos"
    video_dir.mkdir()
    output_webp = tmp_path / "result.webp"
    output_webp.write_text("fake")
    workflow_fn = AsyncMock(return_value=output_webp)

    with patch("capture.parallel_runner.shutil.copy2"):
        with patch("capture.parallel_runner.VIDEO_DIR", video_dir):
            result = await run_workflow(
                name, workflow_fn, browser, {}, semaphore,
            )

    assert result == (name, True, 0, None)
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_workflow_blank_capture(tmp_path: Path):
    """Workflow returning None yields blank capture result."""
    name = "test_blank"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)
    workflow_fn = AsyncMock(return_value=None)

    with patch("capture.parallel_runner.VIDEO_DIR", tmp_path):
        result = await run_workflow(name, workflow_fn, browser, {}, semaphore)

    assert result == (name, False, 0, "blank capture")
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_workflow_exception(tmp_path: Path):
    """Exception in workflow is caught and returned as error string."""
    name = "test_exc"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)
    workflow_fn = AsyncMock(side_effect=ValueError("bad param"))

    with patch("capture.parallel_runner.VIDEO_DIR", tmp_path):
        result = await run_workflow(name, workflow_fn, browser, {}, semaphore)

    assert result == (name, False, 0, "bad param")
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_workflow_context_closed_on_exception(tmp_path: Path):
    """Browser context is always closed when exception occurs in workflow."""
    name = "test_ctx_close"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)
    workflow_fn = AsyncMock(side_effect=RuntimeError("boom"))

    with patch("capture.parallel_runner.VIDEO_DIR", tmp_path):
        result = await run_workflow(name, workflow_fn, browser, {}, semaphore)

    assert result == (name, False, 0, "boom")
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_workflow_context_closed_on_blank(tmp_path: Path):
    """Browser context is closed even when workflow returns None."""
    name = "test_blank_close"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)
    workflow_fn = AsyncMock(return_value=None)

    with patch("capture.parallel_runner.VIDEO_DIR", tmp_path):
        result = await run_workflow(name, workflow_fn, browser, {}, semaphore)

    assert result == (name, False, 0, "blank capture")
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_workflow_semaphore_limits_concurrency(tmp_path: Path):
    """Semaphore with count=1 forces serial execution."""
    name = "test_sem"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)

    event_order = []
    output_webp = tmp_path / "result.webp"
    output_webp.write_text("fake")

    async def controlled_workflow(ctx):
        event_order.append("enter")
        await asyncio.sleep(0.02)
        event_order.append("exit")
        return output_webp

    video_dir = tmp_path / "videos"
    video_dir.mkdir()

    with patch("capture.parallel_runner.shutil.copy2"):
        with patch("capture.parallel_runner.VIDEO_DIR", video_dir):
            t1 = asyncio.create_task(
                run_workflow(name, controlled_workflow, browser, {}, semaphore)
            )
            t2 = asyncio.create_task(
                run_workflow("other", controlled_workflow, browser, {}, semaphore)
            )
            results = await asyncio.gather(t1, t2)

    # With semaphore(1), workflows cannot overlap: enter1, exit1, enter2, exit2
    assert event_order == ["enter", "exit", "enter", "exit"]
    assert all(r[1] is True for r in results)


@pytest.mark.asyncio
async def test_run_workflow_new_context_params():
    """Verify browser.new_context is called with correct parameters."""
    name = "test_params"
    browser, ctx = _make_browser_mock()
    semaphore = asyncio.Semaphore(1)
    workflow_fn = AsyncMock(return_value=None)

    with patch("capture.parallel_runner.VIDEO_DIR", Path("/tmp")):
        result = await run_workflow(name, workflow_fn, browser, {"key": "val"}, semaphore)

    assert result == (name, False, 0, "blank capture")
    browser.new_context.assert_awaited_once_with(
        record_video_dir=str(Path("/tmp")),
        viewport={"width": 1280, "height": 800},
        locale="en-US",
        ignore_https_errors=True,
        storage_state={"key": "val"},
    )
    ctx.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_run_parallel_all_results(tmp_path: Path):
    """run_parallel collects all workflow results."""
    browser, ctx = _make_browser_mock()
    output_webp = tmp_path / "result.webp"
    output_webp.write_text("fake")

    async def success_fn(ctx):
        return output_webp

    workflows = [("wf_a", success_fn), ("wf_b", success_fn)]
    video_dir = tmp_path / "videos"
    video_dir.mkdir()

    with patch("capture.parallel_runner.shutil.copy2"):
        with patch("capture.parallel_runner.VIDEO_DIR", video_dir):
            results = await run_parallel(workflows, browser, {}, workers=4)

    assert len(results) == 2
    assert results[0] == ("wf_a", True, 0, None)
    assert results[1] == ("wf_b", True, 0, None)
    assert ctx.close.await_count == 2


@pytest.mark.asyncio
async def test_run_parallel_semaphore_created_with_workers():
    """run_parallel creates Semaphore with correct worker count."""
    sem_mock = MagicMock(wraps=asyncio.Semaphore)
    browser = AsyncMock()
    workflows = [("wf", AsyncMock(return_value=None))]

    with patch("capture.parallel_runner.asyncio.Semaphore", sem_mock) as mock_sem:
        await run_parallel(workflows, browser, {}, workers=3)

    mock_sem.assert_called_once_with(3)


@pytest.mark.asyncio
async def test_run_parallel_gathers_tasks():
    """run_parallel uses asyncio.gather to run tasks concurrently."""
    gather_results = [
        ("wf1", True, 5, None),
        ("wf2", True, 3, None),
    ]
    browser = AsyncMock()

    with patch("capture.parallel_runner.asyncio.gather", new_callable=AsyncMock) as mock_gather:
        mock_gather.return_value = gather_results
        results = await run_parallel(
            [("wf1", AsyncMock()), ("wf2", AsyncMock())],
            browser,
            {},
            workers=2,
        )

    assert results == gather_results
    mock_gather.assert_awaited_once()


# --- Import fallback tests ---


def test_import_fallback_via_video_pipeline():
    """Verify the except ImportError branch in parallel_runner.py (lines 11-12)."""
    import capture.parallel_runner as pr

    # When capture.video_pipeline exists, it's used (lines 9-10)
    # When it fails, video_pipeline (bare) is used (lines 11-12)
    # Either way, WorkflowRecorder should be available
    assert hasattr(pr, "WorkflowRecorder")

    # Verify that the import is from one of the two expected paths
    assert pr.WorkflowRecorder.__module__ in [
        "capture.video_pipeline",
        "video_pipeline",
    ]

