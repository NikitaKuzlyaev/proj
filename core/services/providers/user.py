from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.services.domain.user import UserService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.user import IUserService
from core.services.mappers.vacancy import VacancyMapper, get_vacancy_mapper
from core.services.providers.permission import get_permission_service


def get_user_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
        vacancy_mapper: VacancyMapper = Depends(get_vacancy_mapper),
        permission_service: IPermissionService = Depends(get_permission_service),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
) -> IUserService:
    return UserService(
        org_repo=org_repo,
        member_repo=member_repo,
        project_repo=project_repo,
        vacancy_repo=vacancy_repo,
        vacancy_mapper=vacancy_mapper,
        permission_service=permission_service,
        user_repo=user_repo,
    )