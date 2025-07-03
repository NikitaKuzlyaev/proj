from typing import Sequence, Tuple

from sqlalchemy import select, Row, delete

from core.dependencies.repository import get_repository
from core.models import User, Organization
from core.models.organizationMember import OrganizationMember
from core.repository.crud.base import BaseCRUDRepository
from core.schemas.organization_member import OrganizationMemberDetailInfo
from core.utilities.loggers.log_decorator import log_calls


class OrganizationMemberCRUDRepository(BaseCRUDRepository):
    @log_calls
    async def delete_member_by_id(
            self,
            member_id: int,
    ) -> None:
        await self.async_session.execute(
            delete(
                OrganizationMember
            ).where(
                OrganizationMember.id == member_id,
            )
        )
        await self.async_session.commit()


    @log_calls
    async def get_organization_member_by_user_and_org(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember | None:
        result = await self.async_session.execute(
            select(
                OrganizationMember
            ).where(
                OrganizationMember.organization_id == org_id,
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalars().one_or_none()

    @log_calls
    async def get_organization_member_by_id(
            self,
            org_member_id: int,
    ) -> OrganizationMember | None:
        """
        Получить объект OrganizationMember с OrganizationMember.id == org_member_id
        :param org_member_id: id объекта User
        :return: объект OrganizationMember или None
        """
        result = await self.async_session.execute(
            select(
                OrganizationMember
            ).where(
                OrganizationMember.id == org_member_id,
            )
        )
        return result.scalars().one_or_none()

    @log_calls
    async def get_organization_members_by_user_id(
            self,
            user_id: int,
    ) -> Sequence[OrganizationMember]:
        """
        Получает объекты OrganizationMember с OrganizationMember.user_id == user_id
        :param user_id: id объекта User
        :return: последовательность объектов OrganizationMember
        """
        result = await self.async_session.execute(
            select(
                OrganizationMember
            ).where(
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalars().all()

    @log_calls
    async def get_organization_members_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        """
        Получает объекты OrganizationMember с OrganizationMember.organization_id == org_id
        :param org_id: id объекта Organization
        :return: последовательность объектов OrganizationMember
        """
        result = await self.async_session.execute(
            select(
                OrganizationMember
            ).where(
                OrganizationMember.organization_id == org_id,
            )
        )
        return result.scalars().all()

    @log_calls
    async def get_organization_members_detail_info_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMemberDetailInfo]:

        rows = await self.async_session.execute(
            select(
                OrganizationMember,
                User,
                Organization,
            ).where(
                OrganizationMember.organization_id == org_id,
            ).join(
                User, User.id == OrganizationMember.user_id
            ).join(
                Organization, Organization.id == OrganizationMember.organization_id
            )
        )
        tuples: Sequence[
            Row[
                Tuple[
                    OrganizationMember,
                    User,
                    Organization,
                ]
            ]
        ] = rows.all()

        result: Sequence[OrganizationMemberDetailInfo] = (
            [
                OrganizationMemberDetailInfo(
                    user_id=user.id,
                    org_id=org.id,
                    user_name=user.username,
                    joined_at=org_member.created_at.isoformat(),
                ) for org_member, user, org in tuples
            ]
        )
        return result

    @log_calls
    async def create_organization_member(
            self,
            user_id: int,
            org_id: int,
    ) -> OrganizationMember:
        """
        Создает новый объект OrganizationMember с ключами на объекты User и Organization
        :param user_id: id объекта User
        :param org_id: id объекта Organization
        :return: возвращает созданный объект OrganizationMember
        """
        new_org_member: OrganizationMember = (
            OrganizationMember(
                user_id=user_id,
                organization_id=org_id,
            )
        )
        self.async_session.add(instance=new_org_member)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_org_member)
        return new_org_member

    @log_calls
    async def get_all_user_organization_memberships(
            self,
            user_id: int,
    ) -> Sequence[OrganizationMember]:
        """
        Получить все объекты OrganizationMember связанные по ключу с User c id равным user_id
        :param user_id: id объекта User
        :return: последовательность объектов OrganizationMember
        """
        result = await self.async_session.execute(
            select(
                OrganizationMember
            ).where(
                OrganizationMember.user_id == user_id,
            )
        )
        return result.scalars().all()


org_member_repo = get_repository(
    repo_type=OrganizationMemberCRUDRepository
)
