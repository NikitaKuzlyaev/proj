import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from core.dependencies.repository import get_repository
from core.schemas.folder import RootFolderInCreate
from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.folder import FolderCRUDRepository
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from core.models.user import User
from core.models.organization import Organization
#from core.models.folder import Folder
from core.schemas.organization import OrganizationInCreate


async def create_root_folder(
        root_folder_in_create_schema: RootFolderInCreate,
        folder_repo: FolderCRUDRepository = Depends(get_repository(FolderCRUDRepository)),
):
    try:
        new_root_folder = await folder_repo.create_root_folder(root_folder_in_create_schema)
        return new_root_folder
    except Exception as e:
        raise e
