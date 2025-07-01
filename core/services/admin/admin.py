from typing import Sequence

from fastapi import Depends
from fastapi import HTTPException

from core.dependencies.repository import get_repository
from core.models import Organization, Project, Permission
from core.models.user import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.admin import AdminPermissionSignature
from core.schemas.project import ProjectFullInfoResponse, CreatedProjectResponse, PatchedProjectResponse
from core.services.domain.permission import PermissionService
from core.services.domain.user import UserService
from core.services.mappers.project import ProjectMapper, get_project_mapper
from core.services.providers.permission import get_permission_service
from core.services.providers.user import get_user_service
from core.utilities.exceptions.database import EntityDoesNotExist


class AdminService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
            user_repo: UserCRUDRepository,
            project_mapper: ProjectMapper,
            user_service: UserService,
            permission_service: PermissionService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.project_mapper = project_mapper
        self.user_service = user_service
        self.permission_service = permission_service


    async def base_admin_check(
            self,
            user_id: int,
    ) -> AdminPermissionSignature:
        permission: AdminPermissionSignature = (
            await self.permission_service.user_admin_permission(
                user_id=user_id
            )
        )
        return permission


def get_admin_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        project_mapper: ProjectMapper = Depends(get_project_mapper),
        user_service: UserService = Depends(get_user_service),
        permission_service: PermissionService = Depends(get_permission_service),
) -> AdminService:
    return AdminService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        project_repo=project_repo,
        user_repo=user_repo,
        project_mapper=project_mapper,
        user_service=user_service,
        permission_service=permission_service,
    )
