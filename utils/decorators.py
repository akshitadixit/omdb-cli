import functools
import time
from typing import Callable, Any

# for timing coroutines/async functions
def async_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapped(*args, **kwargs) -> Any:
            # print(f"starting {func} with args {args} {kwargs}")
            start = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                end = time.time()
                print(f"\n\nfinished {func} in {(end-start):.4f} second(s)")

        return wrapped

    return wrapper


# for timing sync fucntions
def sync_timed():
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapped(*args, **kwargs) -> Any:
            # print(f"starting {func} with args {args} {kwargs}")
            start = time.time()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.time()
                print(f"\n\nfinished {func} in {(end-start):.4f} second(s)")

        return wrapped

    return wrapper
