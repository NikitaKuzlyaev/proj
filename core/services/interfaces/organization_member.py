from typing import Protocol

from core.models.organizationMember import OrganizationMember
from core.schemas.organization import OrganizationJoinResponse


class IOrganizationMemberService(Protocol):

    async def create_org_member(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        ...

    async def get_organization_member_by_user_and_org(
            self,
            user_id: int,
            org_id: int,
            raise_if_fail: bool = True,
    ) -> OrganizationMember:
        ...

    async def get_organization_member_by_id(
            self,
            org_member_id: int,
    ) -> OrganizationMember:
        ...

    async def join_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationJoinResponse:
        ...
