from functools import wraps
from typing import Type

from fastapi import HTTPException

"""
Для примера mapping

EXCEPTION_MAPPING: dict[Type[Exception], tuple[int, str]] = {
    PermissionDenied: (403, "Permission denied"),
    EntityDoesNotExist: (404, "Entity does not exist"),
    EntityAlreadyExists: (409, "Entity already exists"),
}
"""


def async_http_exception_mapper(
        mapping: dict[Type[Exception], tuple[int, str | None]] = None,
):
    if mapping is None:
        mapping = {}

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                for exc_type, (status, message) in mapping.items():
                    if isinstance(e, exc_type):
                        raise HTTPException(
                            status_code=status,
                            detail=message if message is not None else str(e),
                        )
                raise HTTPException(status_code=520, detail=str(e))

        return wrapper

    return decorator
