from typing import Protocol, Sequence

from core.models.organizationMember import OrganizationMember
from core.schemas.organization import OrganizationJoinResponse
from core.schemas.organization_member import OrganizationMemberDetailInfo, \
    OrganizationMemberDeleteResponse


class IOrganizationMemberService(Protocol):

    async def delete_organization_member(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMemberDeleteResponse:
        ...

    async def get_organization_members_for_admin(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[OrganizationMemberDetailInfo]:
        ...

    async def join_organization(
            self,
            user_id: int,
            org_id: int,
            code: int | None = None,
    ) -> OrganizationJoinResponse:
        """
        ???

        Args:
            user_id: id пользователя совершающего запрос
            org_id: id организации
            code: код вступления в организацию

        Returns:
            OrganizationJoinResponse
        """
        ...

    async def create_org_member(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        """
        ???

        Args:
            user_id: id пользователя для которого создать объект членства
            org_id: id организации

        Returns:
            OrganizationMember
        """
        ...

    async def get_organization_member_by_user_and_org(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        """
        ???

        Args:
            user_id: id пользователя
            org_id: id организации
            raise_if_fail:

        Returns:
            OrganizationMember
        """
        ...

    async def get_organization_member_by_id(
            self,
            org_member_id: int,
    ) -> OrganizationMember:
        """
        ???

        Args:
            org_member_id:

        Returns:
            OrganizationMember
        """
        ...
