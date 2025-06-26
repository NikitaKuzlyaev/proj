from typing import List, Sequence

import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from core.dependencies.repository import get_repository
from core.models import User

from core.repository.crud.user import UserCRUDRepository
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/debug", tags=["debug"])

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from core.schemas.user import UserCreate, UserOut, Token
from core.services.domain import auth as auth_service


@router.post("/get-all-users")
async def register(
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
):
    users = await auth_service.get_all_users(user_repo=user_repo)

    return [
        {
            "id": user.id,
            "username": user.username,
        }
        for user in users
    ]
