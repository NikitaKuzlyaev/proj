# core/services/providers/organization.py
from fastapi import Depends

from core.dependencies.repository import get_repository
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.services.domain.organization import OrganizationService
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.organization_member import IOrganizationMemberService
from core.services.providers.organization_member import get_organization_member_service


def get_organization_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
        # user_service: UserService = Depends(get_user_service),
        org_member_service: IOrganizationMemberService = Depends(get_organization_member_service),
) -> IOrganizationService:
    return OrganizationService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo,
        # user_service=user_service,
        org_member_service=org_member_service,
    )
