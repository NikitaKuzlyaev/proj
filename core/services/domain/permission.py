from typing import cast, Callable, Awaitable

from core.models import Permission, User, Vacancy, Organization, OrganizationMember, Application, Project
from core.models.permissions import ResourceType, PermissionType
from core.repository.crud.application import ApplicationCRUDRepository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.admin import AdminPermissionSignature
from core.schemas.organization import OrganizationVisibilityType
from core.schemas.permission import PermissionsShortResponse
from core.schemas.project import ProjectVisibilityType
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.permission import IPermissionService
from core.services.mappers.permission import PermissionMapper
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls
from core.utilities.methods.trusted_method import trusted_method


class PermissionService(IPermissionService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            permission_mapper: PermissionMapper,
            user_repo: UserCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
            project_repo: ProjectCRUDRepository,
            org_service: IOrganizationService,
            application_repo: ApplicationCRUDRepository,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.permission_mapper = permission_mapper
        self.user_repo = user_repo
        self.vacancy_repo = vacancy_repo
        self.project_repo = project_repo
        self.org_service = org_service
        self.application_repo = application_repo

    @trusted_method
    @log_calls
    async def is_user_admin(
            self,
            user_id: int,
    ) -> bool:
        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.DOMAIN.value,
                resource_id=user_id,
                permission_type=PermissionType.ADMIN.value,
            )
        )
        if not permission:
            return False
        return True

    # @log_calls
    # async def check_all(
    #         self,
    #         permissions: list[Callable[[], Awaitable[bool]]],
    # ) -> bool:
    #     for permission in permissions:
    #         result = await permission()
    #         if not result:
    #             return False
    #     return True

    @log_calls
    async def raise_if_not_all(
            self,
            permissions: list[Callable[[], Awaitable[bool]]],
    ) -> None:
        for permission in permissions:
            result = await permission()
            if not result:
                raise PermissionDenied('Permission denied')


    @log_calls
    async def can_user_see_project(
            self,
            user_id: int,
            project_id: int,
    ) -> bool:
        if await self.is_user_admin(user_id=user_id):
            return True
        if await self.can_user_edit_project(project_id=project_id):
            return True

        project: Project | None = (
            await self.project_repo.get_project_by_id(
                project_id=project_id,
            )
        )
        if not project or project.visibility != ProjectVisibilityType.OPEN.value:
            return False

        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=cast(int, project.organization_id),
            )
        )
        if not org:
            return False

        if org.visibility == OrganizationVisibilityType.OPEN.value:
            return True
        else:
            org_member: OrganizationMember | None = (
                await self.member_repo.get_organization_member_by_user_and_org(
                    user_id=user_id,
                    org_id=org.id,
                )
            )
            if org_member:
                return True

        return False

    @log_calls
    async def can_user_create_organizations(
            self,
            user_id: int,
    ) -> bool:
        if await self.is_user_admin(user_id=user_id):
            return True

        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.DOMAIN.value,
                resource_id=user_id,
                permission_type=PermissionType.CREATE_ORGANIZATION.value,
            )
        )
        if permission:
            return True
        return False

    @log_calls
    async def can_user_edit_yourself_application(
            self,
            user_id: int,
            application_id: int,
    ) -> bool:
        application: Application | None = (
            await self.application_repo.get_application_by_id(
                application_id=application_id,
            )
        )
        if not application:
            return False

        if await self.is_user_admin(user_id=user_id):
            return True

        res = bool(application.user_id == user_id)
        return res

    @log_calls
    async def can_user_see_organization_detail(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        res: Organization | None = (
            await self.org_service.get_organization_by_id(
                org_id=org_id,
            )
        )
        if self.org_service.is_org_open_to_view(org=res):
            return True

        if await self.is_user_admin(user_id=user_id):
            return True

        res: OrganizationMember | None = (
            await self.member_repo.get_organization_member_by_user_and_org(
                user_id=user_id,
                org_id=org_id,
            )
        )
        if res: return True

        res: bool = (
            await self.check_permission(
                user_id=user_id,
                resource_id=org_id,
                resource_type=ResourceType.ORGANIZATION.value,
                permission_type=PermissionType.EDIT_ORGANIZATION.value,
            )
        )
        if res: return True

        return False

    @log_calls
    async def can_user_edit_organization(
            self,
            org_id: int,
            user_id: int,
    ) -> bool:
        if await self.is_user_admin(user_id=user_id):
            return True

        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.ORGANIZATION.value,
                resource_id=org_id,
                permission_type=PermissionType.EDIT_ORGANIZATION.value,
            )
        )
        if not permission:
            return False
        return True

    @log_calls
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
                resource_id=resource_id,
            )
        )
        res = permission is not None
        return res

    @log_calls
    async def can_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> bool:
        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.VACANCY.value,
                resource_id=vacancy_id,
                permission_type=PermissionType.EDIT_VACANCY.value,
            )
        )
        if not permission:
            return False
        return True

    @log_calls
    async def can_user_edit_project(
            self,
            user_id: int,
            project_id: int,
    ) -> bool:
        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.PROJECT.value,
                resource_id=project_id,
                permission_type=PermissionType.EDIT_PROJECT.value,
            )
        )
        if not permission:
            return False
        return True

    @log_calls
    async def can_user_create_projects_inside_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        permission: Permission | None = (
            await self.permission_repo.search_exist_permission(
                user_id=user_id,
                resource_type=ResourceType.ORGANIZATION.value,
                resource_id=org_id,
                permission_type=PermissionType.CREATE_PROJECTS_INSIDE_ORGANIZATION.value,
            )
        )
        if not permission:
            return False
        return True

    @log_calls
    async def allow_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int
    ) -> PermissionsShortResponse:

        # user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        # if not user:
        #     raise EntityDoesNotExist('User not found')
        #
        # vacancy: Vacancy | None = await self.vacancy_repo.get_vacancy_by_id(vacancy_id=vacancy_id)
        # if not vacancy:
        #     raise EntityDoesNotExist('Vacancy not found')

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
