import typing

import sqlalchemy
from pyasn1.type.univ import Sequence
from sqlalchemy import select
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.dependencies.repository import get_repository
# from core.schemas.user import UserInCreate, UserInLogin, UserInUpdate, UserCreate
from core.models.user import User
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.user import UserCreate
from core.services.securities.hashing import pwd_generator
from core.services.security import hash_password, verify_password, create_access_token
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from core.utilities.exceptions.auth import PasswordDoesNotMatch, TokenException
from core.services.securities.credential import account_credential_verifier


class UserCRUDRepository(BaseCRUDRepository):

    async def create_user(
            self,
            data: UserCreate
    ) -> User:
        user_exists = await self.async_session.scalar(select(User).where(User.username == data.username))
        if user_exists:
            raise EntityAlreadyExists("Account with id `{id}` already exist!")

        user = User(username=data.username, hashed_password=hash_password(data.password))
        self.async_session.add(user)
        await self.async_session.commit()
        await self.async_session.refresh(user)

        return user

    async def authenticate_user(
            self,
            username: str,
            password: str,
    ):
        user = await self.async_session.scalar(select(User).where(User.username == username))

        if not user or not verify_password(password, user.hashed_password):
            raise TokenException("Invalid credentials")

        return create_access_token({"sub": user.username})

    async def get_user_by_username(
            self,
            username: str,
    ):
        user = await self.async_session.scalar(select(User).where(User.username == username))

        if not user:
            raise EntityDoesNotExist("")

        return user

    # Debug!!!!
    async def get_all_users(
            self,
    ) -> typing.Sequence[User]:
        result = await self.async_session.execute(select(User))
        users = result.scalars().all()

        return users


account_repo = get_repository(repo_type=UserCRUDRepository)
