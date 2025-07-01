from typing import Sequence

from sqlalchemy import select, update, delete

from core.dependencies.repository import get_repository
from core.models.organization import Organization
from core.repository.crud.base import BaseCRUDRepository
from core.utilities.loggers.log_decorator import log_calls


class OrganizationCRUDRepository(BaseCRUDRepository):
    @log_calls
    async def patch_organization_by_id(
            self,
            org_id: int,
            name: str,
            short_description: str,
            long_description: str,
            visibility: str,
            activity_status: str,
            join_policy: str,
    ) -> Organization | None:
        """
        Обновляет поля объекта Organization на указанные в параметрах
        :param org_id: id объекта Organization для изменения
        :param name: название
        :param short_description: короткое описание
        :param long_description: длинное описание
        :param visibility: тип видимости (str, Enum)
        :param activity_status: статус активности (str, Enum)
        :param join_policy: политика вступления (str, Enum)
        :return: обновленные объект Organization или None
        """
        await self.async_session.execute(
            update(
                Organization
            )
            .where(
                Organization.id == org_id,
            )
            .values(
                name=name,
                short_description=short_description,
                long_description=long_description,
                visibility=visibility,
                activity_status=activity_status,
                join_policy=join_policy,
            )
            .execution_options(
                synchronize_session="fetch"
            )
        )
        await self.async_session.commit()

        result = await self.async_session.execute(
            select(
                Organization
            ).where(
                Organization.id == org_id,
            )
        )
        return result.scalar_one_or_none()

    @log_calls
    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        """
        Получить все существующие объекты Organization (Дебаг. Не рекомендуется использовать)
        :return: последовательность объектов Organization
        """
        result = await self.async_session.execute(
            select(
                Organization
            )
        )
        orgs = result.scalars().all()
        return orgs

    @log_calls
    async def get_organization_by_id(
            self,
            org_id: int
    ) -> Organization | None:
        """
        Поиск объекта Organization по его id
        :param org_id: id объекта Organization
        :return: объект Organization с указанным id или None
        """
        result = await self.async_session.execute(
            select(
                Organization
            ).where(
                Organization.id == org_id
            )
        )
        return result.scalar_one_or_none()

    @log_calls
    async def create_organization(
            self,
            name: str,
            short_description: str,
            long_description: str,
            creator_id: int,
    ) -> Organization:
        """
        Создает новый объект Organization
        :param name: название Organization
        :param short_description: короткое описание Organization
        :param long_description: длинное описание Organization
        :param creator_id: id объекта User, который считается создателем объекта
        :return:
        """
        new_organization: Organization = (
            Organization(
                name=name,
                short_description=short_description,
                long_description=long_description,
                creator_id=creator_id,
            )
        )
        self.async_session.add(instance=new_organization)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_organization)
        return new_organization

    @log_calls
    async def delete_organization(
            self,
            org_id: int,
    ) -> None:
        """
        Удаляет объект Organization с указанным id, если он существует
        :param org_id: id объекта Organization для удаления
        :return: Ничего не возвращает - None
        """
        await self.async_session.execute(
            delete(
                Organization
            ).where(
                Organization.id == org_id
            )
        )
        await self.async_session.commit()
        return


org_repo = get_repository(
    repo_type=OrganizationCRUDRepository
)
