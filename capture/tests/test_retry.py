from unittest.mock import AsyncMock

import pytest

from capture.retry import capture_retry


@pytest.mark.asyncio
async def test_retry_succeeds_first_try():
    mock_fn = AsyncMock(return_value="result.webp")

    @capture_retry(max_attempts=3, delay_s=0.01)
    async def workflow(ctx):
        return await mock_fn(ctx)

    result = await workflow("ctx")
    assert result == "result.webp"
    assert mock_fn.call_count == 1


@pytest.mark.asyncio
async def test_retry_succeeds_on_second_attempt():
    mock_fn = AsyncMock(side_effect=[None, "result.webp"])

    @capture_retry(max_attempts=3, delay_s=0.01)
    async def workflow(ctx):
        return await mock_fn(ctx)

    result = await workflow("ctx")
    assert result == "result.webp"
    assert mock_fn.call_count == 2


@pytest.mark.asyncio
async def test_retry_exhausts_all_attempts():
    mock_fn = AsyncMock(return_value=None)

    @capture_retry(max_attempts=3, delay_s=0.01)
    async def workflow(ctx):
        return await mock_fn(ctx)

    result = await workflow("ctx")
    assert result is None
    assert mock_fn.call_count == 3


@pytest.mark.asyncio
async def test_retry_handles_exceptions():
    mock_fn = AsyncMock(side_effect=RuntimeError("playwright crashed"))

    @capture_retry(max_attempts=2, delay_s=0.01)
    async def workflow(ctx):
        return await mock_fn(ctx)

    result = await workflow("ctx")
    assert result is None
    assert mock_fn.call_count == 2


@pytest.mark.asyncio
async def test_retry_no_delay_on_last_attempt():
    mock_fn = AsyncMock(side_effect=[None, None, "result.webp"])

    @capture_retry(max_attempts=3, delay_s=0.01)
    async def workflow(ctx):
        return await mock_fn(ctx)

    result = await workflow("ctx")
    assert result == "result.webp"
    assert mock_fn.call_count == 3
