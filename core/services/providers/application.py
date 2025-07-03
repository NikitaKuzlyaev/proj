from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.application import ApplicationCRUDRepository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.services.domain.application import ApplicationService
from core.services.interfaces.application import IApplicationService
from core.services.interfaces.permission import IPermissionService
from core.services.providers.permission import get_permission_service


def get_application_service(
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
        permission_service: IPermissionService = Depends(get_permission_service),
        application_repo: ApplicationCRUDRepository = Depends(get_repository(ApplicationCRUDRepository)),
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
) -> IApplicationService:
    return ApplicationService(
        project_repo=project_repo,
        vacancy_repo=vacancy_repo,
        permission_service=permission_service,
        application_repo=application_repo,
        org_repo=org_repo,
    )
