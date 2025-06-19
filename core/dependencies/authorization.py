from typing import Optional, Any, Coroutine
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import HTTPException, Request, Depends
from jose import JWTError
from fastapi import Security, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from core.dependencies.repository import get_repository
from core.models.account import Account
from core.repository.crud.account import AccountCRUDRepository
from core.schemas.account import AccountInResponse
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer

from core.schemas.jwt import JWTAccount
from core.schemas.session import UserSession
from core.services.securities.auth import jwt_generator

from core.database.connection import get_session
from core.utilities.exceptions.auth import InvalidToken, ExpiredToken, TokenException


async def get_token_from_cookie(
        request: Request
) -> str:
    """
    """
    token = request.cookies.get("access_token")

    if not token:
        raise InvalidToken

    return token


async def get_jwt_username(
        token: str,
) -> str:
    """
    """
    try:
        res = jwt_generator.retrieve_details_from_token(token)["username"]
    except TokenException as e:
        raise e

    return res


async def get_user_jwt_session(
        request: Request,
        jwt_username: str = Depends(get_jwt_username),
) -> JWTAccount:
    """
    """
    return JWTAccount(username=jwt_username)


async def check_user_jwt_session(
        request: Request,
) -> Optional[JWTAccount]:
    """
    """
    try:
        jwt_username: str = await get_jwt_username()
    except:
        return None

    return JWTAccount(username=jwt_username)


async def get_account(
        request: Request,
        account_repo: AccountCRUDRepository = Depends(get_repository(AccountCRUDRepository)),
) -> Account | None:
    """
    """
    try:
        token = await get_token_from_cookie(request=request)
        jwt_username: str = await get_jwt_username(token=token)

        account: Account = await account_repo.read_account_by_username(username=jwt_username)
        return account
    except ValueError:
        return None
