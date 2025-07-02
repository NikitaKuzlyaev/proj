
import functools
import inspect


def trusted_method(func):
    is_coroutine = inspect.iscoroutinefunction(func)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return async_wrapper if is_coroutine else sync_wrapper
