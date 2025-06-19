import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from core.dependencies.repository import get_repository
from core.schemas.account import AccountInCreate, AccountInLogin, AccountInResponse, AccountWithToken
from core.repository.crud.account import AccountCRUDRepository
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)

router = fastapi.APIRouter(prefix="/folder", tags=["folder"])

from templates import templates

"""
    ----------------------------------------------------------
"""


@router.get("/", response_class=HTMLResponse)
async def get_folders_in_organization(request: Request, response: Response):
    ...


@router.post("/", response_class=HTMLResponse)
async def create_folder(request: Request, response: Response):
    ...


@router.patch("/", response_class=HTMLResponse)
async def patch_folder(request: Request, response: Response):
    ...


@router.delete("/", response_class=HTMLResponse)
async def delete_folder(request: Request, response: Response):
    ...


"""
    ----------------------------------------------------------
"""


@router.get("/child", response_class=HTMLResponse)
async def get_child_folders(request: Request, response: Response):
    ...


@router.get("/parent", response_class=HTMLResponse)
async def get_parent_folder(request: Request, response: Response):
    ...
