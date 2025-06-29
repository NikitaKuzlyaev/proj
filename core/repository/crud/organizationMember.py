from typing import Sequence

from sqlalchemy import select

from core.dependencies.repository import get_repository
from core.models.organizationMember import OrganizationMember
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.organization_member import OrganizationMemberInCreate


class OrganizationMemberCRUDRepository(BaseCRUDRepository):

    async def get_organization_members_by_user_id(
            self,
            user_id: int
    ) -> Sequence[OrganizationMember]:
        stmt = select(OrganizationMember).where(OrganizationMember.user_id == user_id)
        result = await self.async_session.execute(stmt)
        return result.scalars().all()

    async def get_organization_members_by_org_id(
            self,
            org_id: int
    ) -> Sequence[OrganizationMember]:
        stmt = select(OrganizationMember).where(OrganizationMember.organization_id == org_id)
        result = await self.async_session.execute(stmt)
        return result.scalars().all()

    async def create_organization_member(
            self,
            org_create: OrganizationMemberInCreate
    ) -> OrganizationMember:
        new_org_member: OrganizationMember = (
            OrganizationMember(
                user_id=org_create.user_id,
                organization_id=org_create.organization_id,
            )
        )
        self.async_session.add(instance=new_org_member)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_org_member)
        return new_org_member

    async def get_all_user_organization_memberships(
            self,
            user_id: int
    ) -> Sequence[OrganizationMember]:
        query = select(OrganizationMember).where(OrganizationMember.user_id == user_id)
        result = await self.async_session.execute(query)
        return result.scalars().all()

org_member_repo = get_repository(repo_type=OrganizationMemberCRUDRepository)
