import functools
import inspect

from core.utilities.loggers.logger import logger


def log_calls(func):
    is_coroutine = inspect.iscoroutinefunction(func)

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else None
        func_name = func.__name__
        if class_name:
            logger.info(f"🟢 >>> Calling {class_name}.{func_name}")
        else:
            logger.info(f"🟢 >>> Calling {func_name}")
        result = await func(*args, **kwargs)
        logger.info(f"🔵 <<< Leaving {class_name}.{func_name}" if class_name else f"🔵 <<< Leaving {func_name}")
        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        class_name = args[0].__class__.__name__ if args else None
        func_name = func.__name__
        if class_name:
            logger.info(f"🟢 >>> Calling {class_name}.{func_name}")
        else:
            logger.info(f"🟢 >>> Calling {func_name}")
        result = func(*args, **kwargs)
        logger.info(f"🔵 <<< Leaving {class_name}.{func_name}" if class_name else f"🔵 <<< Leaving {func_name}")
        return result

    return async_wrapper if is_coroutine else sync_wrapper
