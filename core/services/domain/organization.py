from typing import Sequence

# from core.dependencies.repository import get_repository, get_repository_manual
from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType, \
    OrganizationInfoForEditResponse, OrganizationDetailInfoResponse, OrganizationId
from core.services.interfaces.organization import IOrganizationService
from core.services.interfaces.user import IUserService
from core.services.mappers.organization import OrganizationMapper
from core.utilities.exceptions.database import EntityDoesNotExist
from core.utilities.loggers.log_decorator import log_calls


class OrganizationService(IOrganizationService):
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository,
            user_service: IUserService,
            org_mapper: OrganizationMapper,
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo
        self.user_service = user_service
        self.org_mapper = org_mapper

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
    async def get_organization_detail_info_by_id(
            self,
            org_id: int,
    ) -> OrganizationDetailInfoResponse:
        org: Organization = (
            await self.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist('Организация не существует')

        org_members: Sequence[OrganizationMember] = (
            await self.get_organization_members_by_org_id(
                org_id=org_id,
            )
        )
        res = OrganizationDetailInfoResponse(
            org_id=org.id,
            org_name=org.name,
            org_short_description=org.short_description,
            org_long_description=org.long_description,
            org_creator_id=org.creator_id,
            org_created_at=org.created_at.isoformat(),
            org_number_of_members=len(org_members),
        )
        return res

    @log_calls
    async def get_organization_info_for_edit(
            self,
            org_id: int,
    ) -> OrganizationInfoForEditResponse:

        org: Organization = (
            await self.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist('Организация не существует')

        res = self.org_mapper.compile_organization_info_for_edit(org=org)
        return res

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
                    org_id=org.id,
                    org_name=org.name,
                    org_short_description=org.short_description,
                    org_creator_id=org.creator_id,
                    is_user_member=(org.id in user_orgs_id_set),
                    org_join_policy=OrganizationJoinPolicyType(org.join_policy),
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
        return org

    @log_calls
    async def create_organization(
            self,
            user_id: int,
            name: str,
            short_description: str,
            long_description: str,
    ) -> OrganizationId:
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
        res = OrganizationId(org_id=new_org.id)
        return res

    @log_calls
    async def get_organization_members_by_org_id(
            self,
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
            org_name: str,
            org_short_description: str,
            org_long_description: str,
            org_visibility: OrganizationVisibilityType,
            org_activity_status: OrganizationActivityStatusType,
            org_join_policy: OrganizationJoinPolicyType,
    ) -> OrganizationId:
        org: Organization | None = (
            await self.org_repo.patch_organization_by_id(
                org_id=org_id,
                name=org_name,
                short_description=org_short_description,
                long_description=org_long_description,
                visibility=org_visibility.value,
                activity_status=org_activity_status.value,
                join_policy=org_join_policy.value,
            )
        )
        if not org:
            raise EntityDoesNotExist("Организация с указанным id не существует")
        res = OrganizationId(org_id=org_id)
        return res
