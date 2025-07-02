from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.user import IUserService
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class OrganizationService(IOrganizationService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            user_service: IUserService,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.user_service = user_service

    def is_org_open_to_view(
            self,
            org: Organization,
    ) -> bool:
        if not org:
            return False
        if org.join_policy != OrganizationJoinPolicyType.OPEN.value:
            return False
        if org.visibility != OrganizationVisibilityType.OPEN.value:
            return False
        return True

    @log_calls
    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        orgs: Sequence[Organization] = (
            await self.org_repo.get_all_organizations()
        )
        return orgs

    @log_calls
    async def get_all_organizations_with_short_info(
            self,
            user_id: int,
    ) -> Sequence[OrganizationShortInfoResponse]:
        all_orgs: Sequence[Organization] = (
            await self.org_repo.get_all_organizations()
        )
        user_orgs: Sequence[OrganizationMember] = (
            await self.member_repo.get_all_user_organization_memberships(
                user_id=user_id,
            )
        )
        user_orgs_id_set = set([member.organization_id for member in user_orgs])
        result = (
            [
                OrganizationShortInfoResponse(
                    id=org.id,
                    name=org.name,
                    short_description=org.short_description,
                    creator_id=org.creator_id,
                    is_user_member=(org.id in user_orgs_id_set),
                    join_policy=OrganizationJoinPolicyType(org.join_policy),
                ) for org in all_orgs
            ]
        )
        return result

    @log_calls
    async def get_organization_by_id(
            self,
            org_id: int,
    ) -> Organization | None:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")
        return org

    @log_calls
    async def create_organization(
            self,
            user_id: int,
            name: str,
            short_description: str,
            long_description: str,
    ) -> Organization:
        new_org = (
            await self.org_repo.create_organization(
                name=name,
                short_description=short_description,
                long_description=long_description,
                creator_id=user_id,
            )
        )
        await self.member_repo.create_organization_member(
            user_id=user_id,
            org_id=new_org.id,
        )
        await self.permission_repo.allow_user_edit_organization(
            user_id=user_id,
            org_id=new_org.id
        )
        return new_org

    @log_calls
    async def get_organization_members_by_org_id(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        org_members: Sequence[OrganizationMember] = (
            await self.member_repo.get_organization_members_by_org_id(
                org_id=org_id,
            )
        )
        return org_members

    @log_calls
    async def patch_organization_by_id(
            self,
            user_id: int,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str,
            visibility: OrganizationVisibilityType,
            activity_status: OrganizationActivityStatusType,
            join_policy: OrganizationJoinPolicyType,
    ) -> Organization | None:
        org: Organization | None = (
            await self.org_repo.patch_organization_by_id(
                org_id=org_id,
                name=name,
                short_description=short_description,
                long_description=long_description,
                visibility=visibility.value,
                activity_status=activity_status.value,
                join_policy=join_policy.value,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")

        return org
