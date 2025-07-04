from typing import Sequence

from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationJoinResponse, OrganizationJoinPolicyType, OrganizationMemberId
from core.schemas.organization_member import OrganizationMemberDetailInfo, \
    OrganizationMemberDeleteResponse
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.organization_member import IOrganizationMemberService
from core.services.interfaces.user import IUserService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.permission import PermissionDenied
from core.utilities.loggers.log_decorator import log_calls


class OrganizationMemberService(IOrganizationMemberService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            user_service: IUserService,
            org_service: IOrganizationService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.user_service = user_service
        self.org_service = org_service

    @log_calls
    async def delete_organization_member(
            self,
            user_id: int,
            org_id: int,
    ) -> None:
        member: OrganizationMember = (
            await self.member_repo.get_organization_member_by_user_and_org(
                org_id=org_id,
                user_id=user_id,
            )
        )
        if not member:
            return

        await self.org_repo.delete_user_from_organization(member=member)


    @log_calls
    async def get_organization_members_for_admin(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[OrganizationMemberDetailInfo]:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        res: Sequence[OrganizationMemberDetailInfo] = (
            await self.member_repo.get_organization_members_detail_info_by_org_id(
                org_id=org_id,
            )
        )
        return res

    @log_calls
    async def get_organization_members_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMember] | None:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        org_members: Sequence[OrganizationMember] | None = (
            await self.member_repo.get_organization_members_by_org_id(org_id=org_id)
        )
        return org_members

    @log_calls
    async def join_organization(
            self,
            user_id: int,
            org_id: int,
            code: int | None = None,
    ) -> OrganizationMemberId:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        try:
            org_member: OrganizationMember | None = (
                await self.get_organization_member_by_user_and_org(user_id=user_id, org_id=org_id)
            )
            if org_member:
                raise EntityAlreadyExists('Пользователь уже в организации')
        except EntityDoesNotExist:
            pass  # Если OrganizationMember не нашелся, то все ок

        if org.join_policy == OrganizationJoinPolicyType.CLOSED.value:
            raise PermissionDenied('Организация закрыта')
        elif org.join_policy == OrganizationJoinPolicyType.CODE.value:
            # заглушка
            if code is None:
                raise PermissionDenied('Код вступления неверный')

        org_member: OrganizationMember = (
            await self.member_repo.create_organization_member(
                user_id=user_id,
                org_id=org_id,
            )
        )
        res = OrganizationMemberId(
            member_id=org_member.id,
        )
        return res

    @log_calls
    async def get_organization_member_by_user_and_org(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        org_member: OrganizationMember | None = (
            await self.member_repo.get_organization_member_by_user_and_org(
                org_id=org_id,
                user_id=user_id,
            )
        )
        if not org_member:
            raise EntityDoesNotExist

        return org_member

    @log_calls
    async def get_organization_member_by_id(
            self,
            org_member_id: int,
    ) -> OrganizationMember:
        org_member: OrganizationMember | None = (
            await self.member_repo.get_organization_member_by_id(
                org_member_id=org_member_id,
            )
        )
        if not org_member:
            raise EntityDoesNotExist

        return org_member
