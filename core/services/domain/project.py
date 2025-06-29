from typing import Sequence

from fastapi import Depends
from fastapi import HTTPException

from core.dependencies.repository import get_repository
from core.models import Organization, Project
from core.models.user import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.project import ProjectFullInfoResponse, CreatedProjectResponse, PatchedProjectResponse
from core.services.mappers.project import ProjectMapper, get_project_mapper
from core.utilities.exceptions.database import EntityDoesNotExist


class ProjectService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
            user_service: UserCRUDRepository,
            project_mapper: ProjectMapper,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo
        self.user_service = user_service
        self.project_mapper = project_mapper

    async def get_all_projects_in_organization_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[Project]:
        res: Sequence[Project] = (
            await self.project_repo.get_all_projects_in_organization_by_org_id(
                org_id=org_id,
            )
        )
        return res

    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project:
        res: Project = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        return res

    async def get_project_full_info_response(
            self,
            project_id: int,
            user_id: int,
    ) -> ProjectFullInfoResponse:

        try:
            project: Project = (
                await self.project_repo.get_project_by_id(
                    project_id=project_id,
                )
            )
            if not project:
                raise EntityDoesNotExist("")

            user: User = (
                await self.user_service.get_user_by_id(
                    user_id=user_id,
                )
            )
            if not user:
                raise EntityDoesNotExist("")

            res: ProjectFullInfoResponse = (
                self.project_mapper.get_project_full_info_response(
                    project=project,
                    manager=user,
                )
            )
            return res

        except Exception as e:
            raise e

    async def create_project(
            self,
            user_id: int,
            name: str,
            org_id: int,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> CreatedProjectResponse:

        org: Organization = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise HTTPException(status_code=404)

        project: Project = (
            await self.project_repo.create_project(
                user_id=user_id,
                name=name,
                org_id=org_id,
                short_description=short_description,
                long_description=long_description,
                activity_status=activity_status,
                visibility=visibility,
            )
        )
        res: CreatedProjectResponse = (
            self.project_mapper.get_created_project_response(
                project=project,
            )
        )
        return res

    async def patch_project(
            self,
            user_id: int,
            project_id: int,
            name: str,
            org_id: int,
            short_description: str,
            long_description: str,
            activity_status: str,
            visibility: str,
    ) -> PatchedProjectResponse:

        project: Project = (
            await self.project_repo.patch_project_by_id(
                project_id=project_id,
                org_id=org_id,
                name=name,
                short_description=short_description,
                long_description=long_description,
                visibility=visibility,
                activity_status=activity_status,
            )
        )
        res: PatchedProjectResponse = (
            self.project_mapper.get_patched_project_response(
                project=project,
            )
        )

        return res

    async def get_project_creator(
            self,
            project_id: int,
    ) -> User | None:
        user: User = (
            await self.project_repo.get_project_creator(
                project_id=project_id,
            )
        )
        return user


def get_project_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        user_service: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        project_mapper: ProjectMapper = Depends(get_project_mapper),
) -> ProjectService:
    return ProjectService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        project_repo=project_repo,
        user_service=user_service,
        project_mapper=project_mapper,
    )
