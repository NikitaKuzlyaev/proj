import typing

from fastapi import Depends
from sqlalchemy.ext.asyncio import (
    async_sessionmaker as sqlalchemy_async_sessionmaker
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies.session import get_async_session
from core.repository.crud.base import BaseCRUDRepository

from typing import Type, TypeVar, Callable
from fastapi import Depends

# def get_repository(
#         repo_type: typing.Type[BaseCRUDRepository],
# ) -> typing.Callable[[AsyncSession], BaseCRUDRepository]:
#     """
#     """
#
#     def _get_repo(
#             async_session: AsyncSession = Depends(get_async_session),
#     ) -> BaseCRUDRepository:
#         return repo_type(async_session=async_session)
#
#     return _get_repo


T = TypeVar("T", bound=BaseCRUDRepository)


def get_repository(repo_type: Type[T]) -> Callable[[AsyncSession], T]:
    def _get_repo(
            async_session: AsyncSession = Depends(get_async_session),
    ) -> T:
        return repo_type(async_session=async_session)

    return _get_repo
