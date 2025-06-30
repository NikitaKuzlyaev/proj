from typing import Sequence

from fastapi import Depends

from core.dependencies.repository import get_repository
from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.models.user import User
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization import OrganizationInCreate, OrganizationCreateInRequest, OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType
from core.schemas.organization_member import OrganizationMemberInCreate
from core.utilities.exceptions.database import EntityDoesNotExist


class OrganizationService:
    def __init__(
            self,
            org_repo: OrganizationCRUDRepository,
            member_repo: OrganizationMemberCRUDRepository,
            permission_repo: PermissionCRUDRepository
    ):
        self.org_repo = org_repo
        self.member_repo = member_repo
        self.permission_repo = permission_repo

    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        """
        Получить все существующие объекты Organization
        :return: последовательность объектов Organization
        """
        try:
            orgs: Sequence[Organization] = (
                await self.org_repo.get_all_organizations()
            )
            return orgs
        except Exception as e:
            raise e

    async def get_all_organizations_with_short_info(
            self,
            user_id: int,
    ) -> Sequence[OrganizationShortInfoResponse]:
        """
        Получить короткую информацию о всех Organization доступных пользователю с указанным id
        :param user_id: id объекта User
        :return: последовательность объектов OrganizationShortInfoResponse
        """
        try:
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

        except Exception as e:
            raise e

    async def get_organization_by_id(
            self,
            org_id: int,
    ) -> Organization:
        """
        Получить объект Organization по его id
        :param org_id: id объекта Organization для поиска
        :return: найденный объект Organization или исключение EntityDoesNotExist
        """
        org: Organization | None = (
            await self.org_repo.get_organization_by_id(
                org_id=org_id,
            )
        )
        if not org:
            raise EntityDoesNotExist

        return org

    async def create_organization(
            self,
            name: str,
            short_description: str,
            long_description: str,
            user_id: int,
    ) -> Organization:

        try:
            new_org = (
                await self.org_repo.create_organization(
                    name=name,
                    short_description=short_description,
                    long_description=long_description,
                    creator_id=user_id,
                )
            )
            new_member = \
                await self.member_repo.create_organization_member(
                    org_create=OrganizationMemberInCreate(
                        user_id=user_id,
                        organization_id=new_org.id
                    )
                )
            new_permission_for_edit_organization = \
                await self.permission_repo.allow_user_edit_organization(
                    user_id=user_id,
                    org_id=new_org.id
                )
            return new_org
        except Exception as e:
            raise e

    async def delete_organization(
            self,
            org: Organization,
            user: User,
    ) -> bool:
        try:
            if org.creator_id != user.id:
                return False

            res: None = \
                await self.org_repo.delete_organization(
                    org_id=org.id
                )

            return True
        except Exception as e:
            raise e

    async def get_organization_members_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        try:
            org_members: Sequence[OrganizationMember] = \
                await  self.member_repo.get_organization_members_by_org_id(
                    org_id=org_id,
                )
            return org_members
        except Exception as e:
            raise e

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
        try:
            org: Organization = \
                await self.org_repo.patch_organization_by_id(
                    org_id=org_id,
                    name=name,
                    short_description=short_description,
                    long_description=long_description,
                    visibility=visibility.value,
                    activity_status=activity_status.value,
                    join_policy=join_policy.value,
                )
            return org
        except Exception as e:
            raise e


def get_organization_service(
        org_repo: OrganizationCRUDRepository = Depends(get_repository(OrganizationCRUDRepository)),
        member_repo: OrganizationMemberCRUDRepository = Depends(get_repository(OrganizationMemberCRUDRepository)),
        permission_repo: PermissionCRUDRepository = Depends(get_repository(PermissionCRUDRepository)),
) -> OrganizationService:
    return OrganizationService(
        org_repo=org_repo,
        member_repo=member_repo,
        permission_repo=permission_repo
    )
