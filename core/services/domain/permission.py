import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from core.dependencies.repository import get_repository
from core.models import Organization
from core.models.organizationMember import OrganizationMember
# from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from core.models.user import User
from core.schemas.organization import OrganizationInCreate, OrganizationCreateInRequest
# from core.schemas.folder import RootFolderInCreate
# from core.models.folder import Folder
from core.dependencies.authorization import get_user


class PermissionService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo

    async def can_user_edit_organization(
            self,
            org_id: int,
            user_id: int,
    ) -> bool:
        flag: bool = \
            await self.permission_repo.can_user_edit_organization(
                user_id=user_id,
                org_id=org_id
            )
        return flag

    async def can_user_edit_project(
            self,
            project_id: int,
            user_id: int,
    ) -> bool:
        flag: bool = \
            await self.permission_repo.can_user_edit_project(
                user_id=user_id,
                project_id=project_id
            )
        return flag


    async def can_user_create_projects_inside_organization(
            self,
            org_id: int,
            user_id: int,
    ) -> bool:
        flag: bool = \
            await self.permission_repo.can_user_create_projects_inside_organization(
                user_id=user_id,
                org_id=org_id
            )
        return flag



def get_permission_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
) -> PermissionService:
    return PermissionService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo
    )
