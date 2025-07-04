from fastapi import Depends

from core.dependencies.repository import get_repository
from core.models import OrganizationMember
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.services.domain.organization import OrganizationService
from core.services.domain.user import UserService
from core.services.interfaces.organization import IOrganizationService
from core.services.mappers.organization import get_org_mapper
from core.services.providers.user import get_user_service


def get_organization_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        user_service: UserService = Depends(get_user_service),
        org_mapper: OrganizationMember = Depends(get_org_mapper)
) -> IOrganizationService:
    return OrganizationService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        user_service=user_service,
        org_mapper=org_mapper,
    )
