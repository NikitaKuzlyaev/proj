import fastapi
from fastapi import APIRouter, Depends, Request, Form, HTTPException, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi import Query, HTTPException
from typing import Sequence

from sqlalchemy import delete

from core.dependencies.repository import get_repository
from core.models import Organization
from core.models.organizationMember import OrganizationMember
#from core.repository.crud.folder import FolderCRUDRepository
# from core.schemas.user import UserInCreate, UserInLogin, UserInResponse, UserWithToken
from core.repository.crud.organization import OrganizationCRUDRepository
from core.repository.crud.organizationMember import OrganizationMemberCRUDRepository
from core.repository.crud.permission import PermissionCRUDRepository
from core.schemas.organization_member import OrganizationMemberInCreate
from core.services.securities.auth import jwt_generator
from core.utilities.exceptions.database import EntityAlreadyExists
from core.utilities.exceptions.http.exc_400 import (
    http_exc_400_credentials_bad_signin_request,
    http_exc_400_credentials_bad_signup_request,
)
from core.models.user import User
from core.schemas.organization import OrganizationInCreate, OrganizationCreateInRequest, OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType
#from core.models.folder import Folder
from core.dependencies.authorization import get_user


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
            self
    ) -> Sequence[Organization]:
        try:
            orgs: Sequence[Organization] = await self.org_repo.get_all_organizations()
            return orgs
        except Exception as e:
            raise e

    async def get_all_organizations_with_short_info(
            self,
            user: User,
    ) -> Sequence[OrganizationShortInfoResponse]:
        try:
            all_orgs: Sequence[Organization] = \
                await self.org_repo.get_all_organizations()
            user_orgs: Sequence[OrganizationMember] = \
                await self.member_repo.get_all_user_organization_memberships(
                    user_id=user.id
                )

            user_orgs_id_set = set([member.organization_id for member in user_orgs])

            result = \
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

            return result

        except Exception as e:
            raise e

    async def get_organization_by_id(
            self,
            org_id: int,
    ) -> Organization:
        try:
            org: Organization = await self.org_repo.get_organization_by_id(org_id)
            return org
        except Exception as e:
            raise e

    async def create_organization(
            self,
            org_create_in_request_schema: OrganizationCreateInRequest,
            user: User,
    ) -> Organization:
        try:
            new_org = \
                await self.org_repo.create_organization(
                    org_create=OrganizationInCreate(
                        name=org_create_in_request_schema.name,
                        short_description=org_create_in_request_schema.short_description,
                        long_description=org_create_in_request_schema.long_description,
                        creator_id=user.id,
                    )
                )
            new_member = \
                await self.member_repo.create_organization_member(
                    org_create=OrganizationMemberInCreate(
                        user_id=user.id,
                        organization_id=new_org.id
                    )
                )
            new_permission_for_edit_organization = \
                await self.permission_repo.allow_user_edit_organization(
                    user_id=user.id,
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
