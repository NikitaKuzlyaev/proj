from typing import Protocol
from typing import Sequence

from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.models.user import User
from core.schemas.organization import OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType, OrganizationJoinResponse


class IOrganizationService(Protocol):

    async def join_organization(
            self,
            user_id: int,
            org_id: int,
            code: int | None = None,
    ) -> OrganizationJoinResponse:
        ...

    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        ...

    async def get_all_organizations_with_short_info(
            self,
            user_id: int,
    ) -> Sequence[OrganizationShortInfoResponse]:
        ...

    async def get_organization_by_id(
            self,
            org_id: int,
    ) -> Organization:
        ...

    async def create_organization(
            self,
            name: str,
            short_description: str,
            long_description: str,
            user_id: int,
    ) -> Organization:
        ...

    async def delete_organization(
            self,
            org: Organization,
            user: User,
    ) -> bool:
        ...

    async def get_organization_members_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        ...

    async def patch_organization_by_id(
            self,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str,
            visibility: OrganizationVisibilityType,
            activity_status: OrganizationActivityStatusType,
            join_policy: OrganizationJoinPolicyType,
    ) -> Organization:
        ...
