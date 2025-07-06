from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from core.dependencies.repository import get_repository
from core.models.user import User
from core.repository.crud.user import UserCRUDRepository
from core.services.domain import auth as auth_service
from core.utilities.exceptions.database import EntityDoesNotExist

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

from core.services.security import decode_token


async def get_user(
        token: str = Depends(oauth2_scheme),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> User:
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    print(token)
    try:
        payload = decode_token(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        user: User = (
            await auth_service.get_user_by_username(
                username=username,
                user_repo=user_repo,
            )
        )

        return user

    except EntityDoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
