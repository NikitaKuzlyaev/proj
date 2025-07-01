from typing import Protocol
from typing import Sequence

from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.schemas.organization import OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType


class IOrganizationService(Protocol):

    async def get_all_organizations(
            self,
    ) -> Sequence[Organization]:
        """
        Возвращает список всех объектов организаций

        Returns:
            Sequence[Organization]: Список организаций
        """
        ...

    async def get_all_organizations_with_short_info(
            self,
            user_id: int,
    ) -> Sequence[OrganizationShortInfoResponse]:
        """
        Возвращает список объектов с краткой информацией о каждой организации, видимой для пользователя

        Args:
            user_id: id пользователя совершающего запрос

        Returns:
            Sequence[OrganizationShortInfoResponse]: Список с объектами с краткой информацией о каждой организации,
            видимой для пользователя
        """
        ...

    async def get_organization_by_id(
            self,
            user_id: int,
            org_id: int,
    ) -> Organization:
        """
        Получает объект организации по ее id

        Args:
            user_id: id пользователя совершающего запрос
            org_id: id организации для получения ее объекта

        Returns:
            Organization: Объект Organization
        """
        ...

    async def create_organization(
            self,
            user_id: int,
            name: str,
            short_description: str,
            long_description: str,
    ) -> Organization:
        """
        Создание нового объекта организации от лица пользователя

        Args:
            user_id: id пользователя совершающего запрос
            name: название организации
            short_description: короткое описание организации
            long_description: длинное описание организации

        Returns:
            Organization: Объект Organization
        """
        ...

    async def get_organization_members_by_org_id(
            self,
            user_id: int,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        """
        Получение участников организации

        Args:
            user_id: id пользователя совершающего запрос
            org_id: id организации

        Returns:
            Sequence[OrganizationMember]: Список участников организации
        """
        ...

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
    ) -> Organization:
        """
        Обновление существующей организации от лица пользователя

        Args:
            user_id: id пользователя совершающего запрос
            org_id: id организации
            name: название
            short_description: короткое описание
            long_description: длинное описание
            visibility: тип видимости
            activity_status: тип активности
            join_policy: тип политики вступления в организацию

        Returns:
            Organization: Обновленный объект организации
        """
        ...
