from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.services.domain.vacancy import VacancyService
from core.services.interfaces.permission import IPermissionService
from core.services.interfaces.vacancy import IVacancyService
from core.services.mappers.vacancy import VacancyMapper, get_vacancy_mapper
from core.services.providers.permission import get_permission_service


def get_vacancy_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
        vacancy_mapper: VacancyMapper = Depends(get_vacancy_mapper),
        permission_service: IPermissionService = Depends(get_permission_service),
) -> IVacancyService:
    return VacancyService(
        org_repo=org_repo,
        member_repo=member_repo,
        project_repo=project_repo,
        vacancy_repo=vacancy_repo,
        vacancy_mapper=vacancy_mapper,
        permission_service=permission_service,
    )
