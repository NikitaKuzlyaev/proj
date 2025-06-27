import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from core.dependencies.repository import get_repository
from core.models import Organization, Project
from core.models.organizationMember import OrganizationMember
# from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.schemas.project import ProjectCreateRequest, ProjectPatchRequest
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


class ProjectService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo

    async def get_all_projects_in_organization_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[Project]:
        res: Sequence[Project] = \
            await self.project_repo.get_all_projects_in_organization_by_org_id(
                org_id=org_id
            )
        return res

    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project:
        res: Project = \
            await self.project_repo.get_projects_by_id(
                project_id=project_id
            )
        return res

    async def create_project(
            self,
            user_id: int,
            project_create_schema: ProjectCreateRequest
    ) -> Project:
        new_proj: Project = \
            await self.project_repo.create_project(
                org_id=project_create_schema.org_id,
                user_id=user_id,
                name=project_create_schema.name,
                short_description=project_create_schema.short_description,
                long_description=project_create_schema.long_description,
                activity_status=project_create_schema.activity_status.value,
                visibility=project_create_schema.visibility.value,
            )
        return new_proj

    async def patch_project(
            self,
            project_patch_schema: ProjectPatchRequest
    ) -> Project:
        try:
            org: Project = \
                await self.project_repo.patch_project_by_id(
                    project_id=project_patch_schema.project_id,
                    org_id=project_patch_schema.org_id,
                    name=project_patch_schema.name,
                    short_description=project_patch_schema.short_description,
                    long_description=project_patch_schema.long_description,
                    visibility=project_patch_schema.visibility.value,
                    activity_status=project_patch_schema.activity_status.value,
                )
            return org
        except Exception as e:
            raise e

    async def get_project_creator(
            self,
            project_id: int,
    ) -> User | None:
        user: User = \
            await self.project_repo.get_project_creator(
                project_id=project_id
            )
        return user

def get_project_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
) -> ProjectService:
    return ProjectService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        project_repo=project_repo,
    )
