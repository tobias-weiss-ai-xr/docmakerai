import functools
import time
from typing import Any, Callable


def capture_retry(max_attempts: int = 3, delay_s: float = 2.0):
    """Retry a capture workflow on failure with exponential backoff.

    Logs each attempt and marks blank captures in the result.
    """
    def decorator(fn: Callable) -> Callable:
        @functools.wraps(fn)
        async def wrapper(*args, **kwargs) -> Any:
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = await fn(*args, **kwargs)
                    if result is not None:
                        return result
                    print(f"  ⚠ Attempt {attempt}/{max_attempts}: blank capture, retrying...")
                except Exception as e:
                    last_error = e
                    print(f"  ⚠ Attempt {attempt}/{max_attempts}: {e}")

                if attempt < max_attempts:
                    wait = delay_s * (2 ** (attempt - 1))
                    print(f"  ⏳ Waiting {wait:.0f}s before retry...")
                    await _async_sleep(wait)

            print(f"  ✗ Failed after {max_attempts} attempts: {last_error or 'blank capture'}")
            return None

        return wrapper
    return decorator


async def _async_sleep(seconds: float):
    import asyncio
    await asyncio.sleep(seconds)
