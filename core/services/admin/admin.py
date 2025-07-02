from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.schemas.admin import AdminPermissionSignature
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.user import IUserService
from core.services.mappers.project import ProjectMapper
from core.utilities.loggers.log_decorator import log_calls


class AdminService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            project_repo: ProjectCRUDRepository,
            user_repo: UserCRUDRepository,
            project_mapper: ProjectMapper,
            user_service: IUserService,
            permission_service: IPermissionService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.project_repo = project_repo
        self.user_repo = user_repo
        self.project_mapper = project_mapper
        self.user_service = user_service
        self.permission_service = permission_service

    @log_calls
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
