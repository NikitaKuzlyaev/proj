import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from core.dependencies.repository import get_repository
from core.models import Organization, Permission
from core.models.organizationMember import OrganizationMember
from core.models.permissions import ResourceType, PermissionType
# from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.permission import PermissionsResponse, PermissionsShortResponse
from core.services.mappers.permission import get_permission_mapper, PermissionMapper
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
            permission_repo: PermissionCRUDRepository,
            permission_mapper: PermissionMapper,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.permission_mapper = permission_mapper

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

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> bool:
        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=resource_type,
                permission_type=permission_type,
                resource_id=resource_id
            )
        )
        res = permission is not None
        return res

    async def can_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> bool:
        res: bool = (
            await self.check_permission(
                user_id=user_id,
                resource_type=ResourceType.VACANCY.value,
                permission_type=PermissionType.EDIT_VACANCY.value,
                resource_id=vacancy_id,
            )
        )
        return res

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

    async def allow_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int
    ) -> PermissionsShortResponse:
        permission: Permission = (
            await self.permission_repo.allow_user_edit_vacancy(
                user_id=user_id,
                vacancy_id=vacancy_id,
            )
        )
        res: PermissionsShortResponse = (
            self.permission_mapper.get_short_permission_response(
                permission=permission,
            )
        )
        return res


def get_permission_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        permission_mapper: PermissionMapper = Depends(get_permission_mapper)
) -> PermissionService:
    return PermissionService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        permission_mapper=permission_mapper,
    )
