from core.models import Permission, User, Vacancy, Organization, Project
from core.models.permissions import ResourceType, PermissionType
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.schemas.admin import AdminPermissionSignature
from core.schemas.permission import PermissionsShortResponse
from core.services.interfaces.permission import IPermissionService
from core.services.mappers.permission import PermissionMapper
from core.utilities.exceptions.database import EntityDoesNotExist


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
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.permission_mapper = permission_mapper
        self.user_repo = user_repo
        self.vacancy_repo = vacancy_repo
        self.project_repo = project_repo

    async def user_admin_permission(
            self,
            user_id: int,
    ) -> AdminPermissionSignature:
        permission: Permission | None = (
            await self.permission_repo.user_admin_permission(
                user_id=user_id,
            )
        )
        if not permission:
            result = AdminPermissionSignature(
                permission_id=None,
                sign=False,
            )
        else:
            result = AdminPermissionSignature(
                permission_id=permission.id,
                sign=True,
            )

        return result

    async def can_user_edit_organization(
            self,
            org_id: int,
            user_id: int,
    ) -> bool:
        # user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        # if not user:
        #     raise EntityDoesNotExist('User not found')
        #
        # org: Organization | None = await self.user_repo.get_user_by_id(user_id=user_id)
        # if not user:
        #     raise EntityDoesNotExist('User not found')

        flag: bool = (
            await self.permission_repo.can_user_edit_organization(
                user_id=user_id,
                org_id=org_id,
            )
        )
        return flag

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> bool:
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')

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

    async def can_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> bool:
        """
        Проверка прав User для редактирования объекта Vacancy
        :param user_id: id объекта User
        :param vacancy_id: id объекта Vacancy
        :return:
        """
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')

        vacancy: Vacancy | None = await self.vacancy_repo.get_vacancy_by_id(vacancy_id=vacancy_id)
        if not vacancy:
            raise EntityDoesNotExist('Vacancy not found')

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
            user_id: int,
            project_id: int,
    ) -> bool:
        """
        Проверка прав User для редактирования объекта Project
        :param user_id: id объекта User
        :param project_id: id объекта Project
        :return: True / False
        """
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')

        project: Project | None = await self.project_repo.get_project_by_id(project_id=project_id)
        if not project:
            raise EntityDoesNotExist('Project not found')

        flag: bool = (
            await self.permission_repo.can_user_edit_project(
                user_id=user_id,
                project_id=project_id,
            )
        )
        return flag

    async def can_user_create_projects_inside_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        """
        Проверка прав User для создания Project внутри Organization
        :param user_id: id объекта User
        :param org_id: id объекта Organization
        :return: True / False
        """
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')

        org: Organization | None = await self.org_repo.get_organization_by_id(org_id=org_id)
        if not org:
            raise EntityDoesNotExist('Organization not found')

        flag: bool = (
            await self.permission_repo.can_user_create_projects_inside_organization(
                user_id=user_id,
                org_id=org_id,
            )
        )
        return flag

    async def allow_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int
    ) -> PermissionsShortResponse:
        """
        Разрешить User с указанным user_id редактировать Vacancy с указанным vacancy_id
        :param user_id: id объекта User
        :param vacancy_id: id объекта Vacancy
        :return: PermissionsShortResponse содержащий id объекта Permission
        """
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')

        vacancy: Vacancy | None = await self.vacancy_repo.get_vacancy_by_id(vacancy_id=vacancy_id)
        if not vacancy:
            raise EntityDoesNotExist('Vacancy not found')

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


# def get_permission_service(
#         org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
#         member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
#         permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
#         permission_mapper: PermissionMapper = Depends(get_permission_mapper),
#         user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
#         vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
#         project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
# ) -> PermissionService:
#     return PermissionService(
#         org_repo=org_repo,
#         member_repo=member_repo,
#         permission_repo=permission_repo,
#         permission_mapper=permission_mapper,
#         user_repo=user_repo,
#         vacancy_repo=vacancy_repo,
#         project_repo=project_repo,
#     )
