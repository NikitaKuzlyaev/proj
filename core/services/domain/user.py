from core.models import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.user import IUserService
from core.services.mappers.vacancy import VacancyMapper
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls

class UserService(IUserService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            project_repo: ProjectCRUDRepository,
            vacancy_repo: VacancyCRUDRepository,
            vacancy_mapper: VacancyMapper,
            permission_service: IPermissionService,
            user_repo: UserCRUDRepository,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.project_repo = project_repo
        self.vacancy_repo = vacancy_repo
        self.vacancy_mapper = vacancy_mapper
        self.permission_service = permission_service
        self.user_repo = user_repo

    @log_calls
    async def get_user_by_id(
            self,
            user_id: int,
    ) -> User:
        user: User | None = await self.user_repo.get_user_by_id(user_id=user_id)
        if not user:
            raise EntityDoesNotExist('User not found')
        return user

