from typing import Optional, Any, Coroutine
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import HTTPException, Request, Depends
from jose import JWTError
from fastapi import Security, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from core.dependencies.repository import get_repository
from core.models.user import User
from core.repository.crud.user import UserCRUDRepository
# from core.schemas.user import UserInResponse
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer

from core.schemas.jwt import JWTAccount
from core.schemas.session import UserSession
from core.services.securities.auth import jwt_generator

from core.database.connection import get_session
from core.utilities.exceptions.auth import InvalidToken, ExpiredToken, TokenException

# async def get_token_from_cookie(
#         request: Request
# ) -> str:
#     """
#     """
#     token = request.cookies.get("access_token")
#
#     if not token:
#         raise InvalidToken
#
#     return token
#
#
# async def get_jwt_username(
#         token: str,
# ) -> str:
#     """
#     """
#     try:
#         res = jwt_generator.retrieve_details_from_token(token)["username"]
#     except TokenException as e:
#         raise e
#
#     return res
#
#
# async def get_user_jwt_session(
#         request: Request,
#         jwt_username: str = Depends(get_jwt_username),
# ) -> JWTAccount:
#     """
#     """
#     return JWTAccount(username=jwt_username)
#
#
# async def check_user_jwt_session(
#         request: Request,
# ) -> Optional[JWTAccount]:
#     """
#     """
#     try:
#         jwt_username: str = await get_jwt_username()
#     except:
#         return None
#
#     return JWTAccount(username=jwt_username)
#
#
# async def get_user(
#         request: Request,
#         account_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
# ) -> User | None:
#     """
#     """
#     try:
#         token = await get_token_from_cookie(request=request)
#         jwt_username: str = await get_jwt_username(token=token)
#
#         account: User = await account_repo.read_account_by_username(username=jwt_username)
#         return account
#     except ValueError:
#         return None


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from core.services.domain import auth as auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

from core.services.security import decode_token


async def get_user(
        token: str = Depends(oauth2_scheme),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> User:

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    print(token)
    #payload = decode_token(token=token)
    try:
        payload = decode_token(token=token)
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

        user = await auth_service.get_user_by_username(username=username, user_repo=user_repo)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except JWTError as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
