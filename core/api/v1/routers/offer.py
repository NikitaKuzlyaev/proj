import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from core.dependencies.repository import get_repository
#from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.user import UserCRUDRepository
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/offer", tags=["offer"])

from templates import templates

"""
    ----------------------------------------------------------
    for managers only
"""


@router.get("/", response_class=HTMLResponse)
async def get_all_active_offers_in_organization(request: Request, response: Response):
    # Вывести список всех офферов в указанной организации
    ...


@router.delete("/", response_class=HTMLResponse)
async def delete_offer(request: Request, response: Response):
    # Удалить оффер (отозвать)
    ...


"""
    ----------------------------------------------------------
"""
