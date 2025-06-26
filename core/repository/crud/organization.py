import typing
from typing import Sequence

import sqlalchemy
from sqlalchemy import select, update, delete
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.dependencies.repository import get_repository
#from core.models import Folder

# from core.schemas.user import UserInCreate, UserInLogin, UserInUpdate
from core.models.user import User

from core.schemas.organization import OrganizationInCreate
from core.models.organization import Organization

from core.repository.crud.base import BaseCRUDRepository
from core.services.securities.hashing import pwd_generator
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from core.utilities.exceptions.auth import PasswordDoesNotMatch
from core.services.securities.credential import account_credential_verifier


class OrganizationCRUDRepository(BaseCRUDRepository):

    async def patch_organization_by_id(
            self,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str
    ) -> Organization | None:
        stmt = (
            update(Organization)
            .where(Organization.id == org_id)
            .values(
                name=name,
                short_description=short_description,
                long_description=long_description
            )
            .execution_options(synchronize_session="fetch")
        )

        await self.async_session.execute(stmt)
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return result.scalar_one_or_none()

    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        result = await self.async_session.execute(select(Organization))
        orgs = result.scalars().all()
        return orgs

    async def get_organization_by_id(
            self,
            org_id: int
    ) -> Organization | None:
        stmt = select(Organization).where(Organization.id == org_id)
        result = await self.async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_organization(
            self,
            org_create: OrganizationInCreate
    ) -> Organization:
        """
        Создает новую организацию
        :param org_create:
        :return:
        """

        new_organization = Organization(name=org_create.name,
                                        short_description=org_create.short_description,
                                        long_description=org_create.long_description,
                                        creator_id=org_create.creator_id,
                                        root_folder_id=org_create.root_folder_id)

        self.async_session.add(instance=new_organization)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_organization)

        return new_organization

    async def delete_organization(
            self,
            org_id: int,
    ) -> None:
        stmt = delete(Organization).where(Organization.id == org_id)
        await self.async_session.execute(stmt)
        await self.async_session.commit()
        return

    # async def get_root_folder_id_by_org_id(
    #         self,
    #         org_id: int,
    # ) -> None:
    #     stmt = delete(Organization).where(Organization.id == org_id)
    #     await self.async_session.execute(stmt)
    #     await self.async_session.commit()

    # async def get_first_not_root_inner_folder_or_none(
    #         self,
    #         org_id: int,
    # ) -> Folder | None:
    #     """
    #     Возвращает первый folder дочерний к root_folder организации
    #     """
    #     # найдем вначале саму организацию по ее id
    #     stmt = select(Organization).where(Organization.id == org_id)
    #     coro = await self.async_session.execute(stmt)
    #     org: Organization = coro.scalar_one_or_none()
    #
    #     # поиск folder
    #     stmt = select(Folder).where(Folder.parent_folder_id == org.root_folder_id)
    #     coro = await self.async_session.execute(stmt)
    #     folder: Folder = coro.scalar_one_or_none()
    #
    #     return folder


org_repo = get_repository(repo_type=OrganizationCRUDRepository)
