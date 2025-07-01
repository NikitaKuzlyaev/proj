from typing import Type, TypeVar, Callable, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.session import get_async_session
from core.repository.crud.base import BaseCRUDRepository

T = TypeVar("T", bound=BaseCRUDRepository)


def get_repository(repo_type: Type[T]) -> Callable[[AsyncSession], T]:
    def _get_repo(
            async_session: AsyncSession = Depends(get_async_session),
    ) -> T:
        return repo_type(async_session=async_session)

    return _get_repo


# def get_repository_manual(repo_type: Type[T]) -> Callable[[AsyncSession], T]:
#
#     async_session: AsyncSession = get_async_session()
#     repo = repo_type(async_session=async_session)
#     return repo

async def get_repository_manual(repo_type: Type[T]) -> T:
    async_session_generator = get_async_session()
    async for session in async_session_generator:
        repo = repo_type(async_session=session)
        return repo

    raise RuntimeError("Failed to acquire async session")