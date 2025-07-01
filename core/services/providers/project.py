from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.repository.crud.project import ProjectCRUDRepository
from core.repository.crud.user import UserCRUDRepository
from core.services.domain.project import ProjectService
from core.services.interfaces.project import IProjectService
from core.services.interfaces.user import IUserService
from core.services.mappers.project import ProjectMapper, get_project_mapper
from core.services.providers.user import get_user_service


def get_project_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        project_repo: ProjectCRUDRepository = Depends(get_repository(ProjectCRUDRepository)),
        user_repo: UserCRUDRepository = Depends(get_repository(UserCRUDRepository)),
        project_mapper: ProjectMapper = Depends(get_project_mapper),
        user_service: IUserService = Depends(get_user_service),
) -> IProjectService:
    return ProjectService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        project_repo=project_repo,
        user_repo=user_repo,
        project_mapper=project_mapper,
        user_service=user_service,
    )
