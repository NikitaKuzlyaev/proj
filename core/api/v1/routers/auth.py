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

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])

from templates import templates


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request, response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("is_login")

    return templates.TemplateResponse("login.html",
                                      {"request": request})


@router.post("/login")
async def post_login(
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
        account_repo: AccountCRUDRepository = Depends(get_repository(AccountCRUDRepository)),
):
    try:
        account = await account_repo.read_user_by_password_authentication(
            AccountInLogin(username=username, password=password)
        )
    except Exception:
        raise await http_exc_400_credentials_bad_signin_request()

    token = jwt_generator.generate_access_token(account)
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    response.set_cookie(key="is_login", value='True', httponly=False)
    return response


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("signup.html",
                                      {"request": request})


@router.post("/register")
async def post_register(
        response: Response,
        username: str = Form(...),
        password: str = Form(...),
        account_repo: AccountCRUDRepository = Depends(get_repository(AccountCRUDRepository)),
):
    try:
        await account_repo.is_username_taken(username=username)
        account = await account_repo.create_account(AccountInCreate(username=username, password=password))
    except Exception:
        raise await http_exc_400_credentials_bad_signup_request()

    token = jwt_generator.generate_access_token(account)
    response = RedirectResponse("/", status_code=302)
    response.set_cookie(key="access_token", value=token, httponly=True)
    response.set_cookie(key="is_login", value='True', httponly=False)
    return response


@router.post("/logout")
async def post_logout(
        response: Response,
        account_repo: AccountCRUDRepository = Depends(get_repository(AccountCRUDRepository)),
):
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("access_token")
    response.delete_cookie("is_login")

    return response
