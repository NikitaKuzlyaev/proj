from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import UserCreate
from core.services.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status


async def register_user(
        data: UserCreate,
        user_repo: UserCRUDRepository,
) -> User:
    user: User = await user_repo.create_user(data=data)

    return user


async def authenticate_user(
        username: str,
        password: str,
        user_repo: UserCRUDRepository,
) -> str:

    token: str = await user_repo.authenticate_user(username=username, password=password)

    return token

async def get_user_by_username(
        username: str,
        user_repo: UserCRUDRepository,
) -> User:

    user: User = await user_repo.get_user_by_username(username=username)

    return user

# DEBUG!!!!
async def get_all_users(
        user_repo: UserCRUDRepository,
) -> Sequence[User]:

    users: Sequence[User] = await user_repo.get_all_users()

    return users
