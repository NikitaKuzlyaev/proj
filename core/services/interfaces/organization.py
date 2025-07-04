from typing import Protocol
from typing import Sequence

from core.models import Organization
from core.models.organizationMember import OrganizationMember
from core.schemas.organization import OrganizationShortInfoResponse, \
    OrganizationJoinPolicyType, OrganizationVisibilityType, OrganizationActivityStatusType, \
    OrganizationInfoForEditResponse, OrganizationDetailInfoResponse, OrganizationId


class IOrganizationService(Protocol):

    def is_org_open_to_view(
            self,
            org: Organization,
    ) -> bool:
        ...

    async def get_organization_detail_info_by_id(
            self,
            org_id: int,
    ) -> OrganizationDetailInfoResponse:
        ...

    async def get_organization_info_for_edit(
            self,
            org_id: int,
    ) -> OrganizationInfoForEditResponse:
        ...

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
            org_id: int,
    ) -> Organization | None:
        """
        Получает объект организации по ее id

        Args:
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
    ) -> OrganizationId:
        """
        Создание нового объекта организации от лица пользователя

        Args:
            user_id: id пользователя совершающего запрос
            name: название организации
            short_description: короткое описание организации
            long_description: длинное описание организации

        Returns:
            OrganizationId: id созданного объекта Organization
        """
        ...

    async def get_organization_members_by_org_id(
            self,
            org_id: int,
    ) -> Sequence[OrganizationMember]:
        """
        Получение участников организации

        Args:
            org_id: id организации

        Returns:
            Sequence[OrganizationMember]: Список участников организации
        """
        ...

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
        """
        Обновление существующей организации от лица пользователя

        Args:
            user_id: id пользователя совершающего запрос
            org_id: id организации
            org_name: название
            org_short_description: короткое описание
            org_long_description: длинное описание
            org_visibility: тип видимости
            org_activity_status: тип активности
            org_join_policy: тип политики вступления в организацию

        Returns:
            Organization: Обновленный объект организации
        """
        ...
