from typing import Annotated

import fastapi
from fastapi import Depends, HTTPException
from fastapi import Security
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, Request, Response

from core.dependencies.authorization import oauth2_scheme
from core.dependencies.repository import get_repository
from core.models import User
from core.repository.crud.user import UserCRUDRepository
from core.schemas.user import UserCreate, UserOut, Token
from core.services.domain import auth as auth_service
from core.services.domain.auth import verify_refresh_token
from core.services.security import REFRESH_TOKEN_EXPIRE_MINUTES, create_refresh_token, create_access_token
from core.utilities.exceptions.auth import UnauthorizedException, TokenException

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserOut)
async def register(
        data: UserCreate,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
):
    user: User = (
        await auth_service.register_user(
            data=data,
            user_repo=user_repo,
        )
    )
    return user


@router.post("/login",
             response_model=Token,
             status_code=200)
async def login_for_access_token(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> dict[str, str]:
    """"""
    try:
        access_token: str = (
            await auth_service.authenticate_user(
                username=form_data.username,
                password=form_data.password,
                user_repo=user_repo,
            )
        )
        refresh_token: str = (
            create_refresh_token(
                data={"sub": form_data.username},
            )
        )
        max_age = REFRESH_TOKEN_EXPIRE_MINUTES

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            #
            # secure=True,
            # ТОЛЬКО В ДЕБАГЕ!!!
            secure=True,
            #
            # samesite="lax",
            # Только в ДЕБАГЕ!!!
            samesite="none",
            #
            max_age=max_age * 60,
            path='/',
        )

        return {"access_token": access_token, "token_type": "bearer"}

    except TokenException as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/refresh")
async def refresh_access_token(
        request: Request,
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> dict[str, str]:
    """"""
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing.")

    user: User | None = (
        await verify_refresh_token(
            token=refresh_token,
            user_repo=user_repo,
        )
    )
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")

    new_access_token = create_access_token(data={"sub": user.username})
    return {"access_token": new_access_token, "token_type": "bearer"}


"""
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


"""