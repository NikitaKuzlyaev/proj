from core.models import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import UserCreate


async def register_user(
        data: UserCreate,
        user_repo: UserCRUDRepository,
) -> User:
    user: User = (
        await user_repo.create_user(
            data=data,
        )
    )
    return user


async def authenticate_user(
        username: str,
        password: str,
        user_repo: UserCRUDRepository,
) -> str:
    token: str = (
        await user_repo.authenticate_user(
            username=username,
            password=password,
        )
    )
    return token


async def get_user_by_username(
        username: str,
        user_repo: UserCRUDRepository,
) -> User:
    user: User = (
        await user_repo.get_user_by_username(
            username=username,
        )
    )
    return user
