from core.models import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import UserCreate
from core.services.security import decode_token
from core.utilities.exceptions.auth import TokenException
from core.utilities.exceptions.database import EntityDoesNotExist


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


async def verify_refresh_token(
        token: str,
        user_repo: UserCRUDRepository,
) -> User | None:
    try:
        payload = decode_token(token=token)
        username: str = payload.get("sub")
        token_type: str = payload.get("token_type")

        if username is None or token_type is None or token != 'refresh':
            raise TokenException("Invalid authentication credentials")

        user: User = (
            await user_repo.get_user_by_username(
                username=username,
            )
        )

        return user

    except TokenException as e:
        raise e
    except EntityDoesNotExist as e:
        raise e
    except Exception as e:
        raise e


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
    if not user:
        raise EntityDoesNotExist

    return user
