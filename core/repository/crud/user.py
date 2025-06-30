import typing

from sqlalchemy import select

from core.dependencies.repository import get_repository
from core.models.user import User
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.user import UserCreate
from core.services.security import hash_password, verify_password, create_access_token
from core.utilities.exceptions.auth import TokenException
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist


class UserCRUDRepository(BaseCRUDRepository):

    async def create_user(
            self,
            data: UserCreate
    ) -> User:
        user_exists = (
            await self.async_session.scalar(
                select(
                    User
                ).where(
                    User.username == data.username,
                )
            )
        )
        if user_exists:
            raise EntityAlreadyExists("Account with id `{id}` already exist!")

        user = User(
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        self.async_session.add(user)
        await self.async_session.commit()
        await self.async_session.refresh(user)

        return user

    async def authenticate_user(
            self,
            username: str,
            password: str,
    ):
        user = (
            await self.async_session.scalar(
                select(
                    User
                ).where(
                    User.username == username,
                )
            )
        )

        if not user or not verify_password(password, user.hashed_password):
            raise TokenException("Invalid credentials")

        return create_access_token({"sub": user.username})

    async def get_user_by_username(
            self,
            username: str,
    ):
        user = (
            await self.async_session.scalar(
                select(
                    User
                ).where(
                    User.username == username,
                )
            )
        )

        if not user:
            raise EntityDoesNotExist("")

        return user

    async def get_user_by_id(
            self,
            user_id: int,
    ) -> User | None:
        """
        Возвращает объект User с указанным id
        :param user_id: id объекта User
        :return: объект User c указанным user_id или None
        """
        stmt = (
            select(
                User
            ).where(
                User.id == user_id,
            )
        )
        res = await self.async_session.execute(stmt)
        return res.one_or_none()

    # Debug!!!!
    async def get_all_users(
            self,
    ) -> typing.Sequence[User]:
        result = (
            await self.async_session.execute(
                select(
                    User
                )
            )
        )
        users = result.scalars().all()

        return users


account_repo = get_repository(repo_type=UserCRUDRepository)
