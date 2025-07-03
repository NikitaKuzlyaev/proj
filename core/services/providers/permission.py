from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.application import ApplicationCRUDRepository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.repository.crud.vacancy import VacancyCRUDRepository
from core.services.domain.permission import PermissionService
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.permission import IPermissionService
from core.services.mappers.permission import PermissionMapper, get_permission_mapper
from core.services.providers.organization import get_organization_service


def get_permission_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        permission_mapper: PermissionMapper = Depends(get_permission_mapper),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        vacancy_repo: VacancyCRUDRepository = Depends(get_repository(VacancyCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        org_service: IOrganizationService = Depends(get_organization_service),
        application_repo: ApplicationCRUDRepository = Depends(get_repository(ApplicationCRUDRepository)),
) -> IPermissionService:
    return PermissionService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        permission_mapper=permission_mapper,
        user_repo=user_repo,
        vacancy_repo=vacancy_repo,
        project_repo=project_repo,
        org_service=org_service,
        application_repo=application_repo,
    )
