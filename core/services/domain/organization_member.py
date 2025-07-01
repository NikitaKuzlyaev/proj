from fastapi import Depends

from core.dependencies.repository import get_repository
from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.models.user import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationJoinResponse, OrganizationJoinPolicyType
# from core.services.domain.organization import get_organization_service
# from core.services.providers.organization import get_organization_service
from core.services.domain.user import UserService, get_user_service
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.organization_member import IOrganizationMemberService
from core.utilities.exceptions.database import EntityDoesNotExist, EntityAlreadyExists
from core.utilities.exceptions.permission import PermissionDenied


class OrganizationMemberService(IOrganizationMemberService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            user_service: UserService,
            org_service: IOrganizationService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.user_service = user_service
        self.org_service = org_service

    async def join_organization(
            self,
            user_id: int,
            org_id: int,
            code: int | None = None,
    ) -> OrganizationJoinResponse:

        try:
            organization: Organization = await self.org_service.get_organization_by_id(org_id=org_id)
            user: User = await self.user_service.get_user_by_id(user_id=user_id)

            org_member: OrganizationMember | None = (
                await self.get_organization_member_by_user_and_org(user_id=user_id, org_id=org_id, raise_if_fail=False)
            )
            if org_member:
                raise EntityAlreadyExists('Пользователь уже в организации')

            if organization.join_policy == OrganizationJoinPolicyType.CLOSED.value:
                raise PermissionDenied('Организация закрыта')
            elif organization.join_policy == OrganizationJoinPolicyType.CODE.value:
                # заглушка
                if code is None:
                    raise PermissionDenied('Код вступления неверный')

            org_member: OrganizationMember = await self.create_org_member(
                user_id=user_id,
                org_id=org_id,
            )
            res = OrganizationJoinResponse(member_id=org_member.id)
            return res
        except Exception as e:
            raise e

    async def create_org_member(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        organization: Organization = await self.org_service.get_organization_by_id(org_id=org_id)
        user: User = await self.user_service.get_user_by_id(user_id=user_id)

        org_member: OrganizationMember = (
            await self.member_repo.create_organization_member(
                user_id=user_id,
                org_id=org_id,
            )
        )
        return org_member

    async def get_organization_member_by_user_and_org(
            self,
            user_id: int,
            org_id: int,
            raise_if_fail: bool = True
    ) -> OrganizationMember:
        print('get_organization_member_by_user_and_org >>>', '\n' * 10)

        organization: Organization = await self.org_service.get_organization_by_id(org_id=org_id)
        user: User = await self.user_service.get_user_by_id(user_id=user_id)

        org_member: OrganizationMember | None = (
            await self.member_repo.get_organization_member_by_user_and_org(
                org_id=org_id,
                user_id=user_id,
            )
        )
        if raise_if_fail and org_member:
            raise EntityDoesNotExist
        print('get_organization_member_by_user_and_org <<<', '\n' * 10)
        return org_member

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

#
# def get_organization_member_service(
#         org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
#         member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
#         permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
#         user_service: UserService = Depends(get_user_service),
#         org_service: IOrganizationService = Depends(get_organization_service)
# ) -> OrganizationMemberService:
#     return OrganizationMemberService(
#         org_repo=org_repo,
#         member_repo=member_repo,
#         permission_repo=permission_repo,
#         user_service=user_service,
#         org_service=org_service,
#     )
