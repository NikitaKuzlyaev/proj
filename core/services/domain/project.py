from typing import Sequence

from fastapi import HTTPException

from core.models import Organization, Project
from core.models.user import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.project import ProjectFullInfoResponse, CreatedProjectResponse, PatchedProjectResponse, \
    ProjectsInOrganizationShortInfoResponse
from core.services.interfaces.project import IProjectService
from core.services.interfaces.user import IUserService
from core.services.mappers.project import ProjectMapper
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class ProjectService(IProjectService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
            user_repo: UserCRUDRepository,
            project_mapper: ProjectMapper,
            user_service: IUserService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.project_mapper = project_mapper
        self.user_service = user_service

    @log_calls
    async def get_projects_short_info_in_organization(
            self,
            user_id: int,
            org_id:int,
    ) -> Sequence[ProjectsInOrganizationShortInfoResponse]:

        res: Sequence[ProjectsInOrganizationShortInfoResponse] = (
            await self.project_repo.get_projects_short_info_in_organization(
                user_id=user_id,
                org_id=org_id,
            )
        )
        return res

    @log_calls
    async def get_all_projects_in_organization_by_org_id(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[Project]:
        res: Sequence[Project] = (
            await self.project_repo.get_all_projects_in_organization_by_org_id(
                org_id=org_id,
            )
        )
        return res

    @log_calls
    async def get_project_by_id(
            self,
            project_id: int,
    ) -> Project:
        """
        Получить объект Project по его id
        :param project_id: id объекта Project
        :return: объект Project с указанным id
        """
        project: Project | None = await self.project_repo.get_project_by_id(project_id=project_id)
        if not project:
            raise EntityDoesNotExist('Project not found')
        return project

    @log_calls
    async def get_project_full_info_response(
            self,
            user_id: int,
            project_id: int,
    ) -> ProjectFullInfoResponse:
        project: Project = await self.get_project_by_id(project_id=project_id)
        user: User = await self.user_service.get_user_by_id(user_id=user_id)

        res: ProjectFullInfoResponse = (
            self.project_mapper.get_project_full_info_response(
                project=project,
                manager=user,
            )
        )
        return res

    @log_calls
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

    @log_calls
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

    @log_calls
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

