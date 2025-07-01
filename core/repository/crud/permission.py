from sqlalchemy import select

from core.dependencies.repository import get_repository
from core.models.permissions import Permission, PermissionType, ResourceType
from core.repository.crud.base import BaseCRUDRepository


class PermissionCRUDRepository(BaseCRUDRepository):

    async def search_exist_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission | None:
        """
        Найти существующий Permission с указанными параметрами
        :param user_id: id объекта User
        :param resource_type: тип ресурса (str, Enum)
        :param permission_type: тип разрешения (str, Enum)
        :param resource_id: id ресурса
        :return: существующий Permission или None
        """
        permission = await self.async_session.execute(
            select(
                Permission
            ).where(
                Permission.user_id == user_id,
                Permission.resource_type == resource_type,
                Permission.resource_id == resource_id,
                Permission.permission_type == permission_type
            )
        )
        permission = permission.scalar_one_or_none()
        return permission

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission | None:
        """
        Создать Permission с указанными параметрами
        :param user_id: id объекта User
        :param resource_type: тип ресурса (str, Enum)
        :param permission_type: тип разрешения (str, Enum)
        :param resource_id: id ресурса
        :return: созданный или существующий Permission
        """
        permission: Permission | None = (
            await self.search_exist_permission(
                user_id=user_id,
                resource_type=resource_type,
                permission_type=permission_type,
                resource_id=resource_id,
            )
        )
        if permission:
            return permission

        permission: Permission = Permission(
            user_id=user_id,
            resource_type=ResourceType(resource_type),
            resource_id=resource_id,
            permission_type=PermissionType(permission_type),
        )
        self.async_session.add(instance=permission)
        await self.async_session.commit()
        await self.async_session.refresh(instance=permission)
        return permission

    async def allow_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> Permission:
        """
        Разрешить User редактирование Vacancy
        :param user_id: id объекта User
        :param vacancy_id: id объекта Vacancy
        :return: Созданный или существующий Permission
        """
        permission: Permission = (
            await self.create_permission(
                user_id=user_id,
                resource_type=ResourceType.VACANCY.value,
                permission_type=PermissionType.EDIT_VACANCY.value,
                resource_id=vacancy_id,
            )
        )
        return permission

    async def allow_user_edit_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> Permission:
        """
        Разрешить User редактирование Organization
        :param user_id: id объекта User
        :param org_id: id объекта Organization
        :return: Созданный или существующий Permission
        """
        permission: Permission = (
            await self.create_permission(
                user_id=user_id,
                resource_type=ResourceType.ORGANIZATION.value,
                permission_type=PermissionType.EDIT_ORGANIZATION.value,
                resource_id=org_id,
            )
        )
        return permission


    async def user_admin_permission(
            self,
            user_id: int,
    ) -> Permission | None:
        """
        Узнать имеет ли User admin-permission
        :param user_id: id объекта User
        :return: True / False
        """
        result = await self.async_session.execute(
            select(
                Permission
            ).where(
                Permission.user_id == user_id,
                Permission.resource_id == user_id,
                Permission.resource_type == ResourceType.DOMAIN.value,
                Permission.permission_type == PermissionType.ADMIN.value,
            )
        )
        return result.scalar_one_or_none()


    async def can_user_edit_organization(
            self,
            user_id: int,
            org_id: int
    ) -> bool:
        """
        Узнать существование Permission на редактирование Organization для User
        :param user_id: id объекта User
        :param org_id: id объекта Organization
        :return: True / False
        """
        result = await self.async_session.execute(
            select(
                Permission
            ).where(
                Permission.user_id == user_id,
                Permission.resource_id == org_id,
                Permission.resource_type == ResourceType.ORGANIZATION.value,
                Permission.permission_type == PermissionType.EDIT_ORGANIZATION.value,
            )
        )
        return bool(result.scalar_one_or_none())

    async def can_user_create_projects_inside_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        """
        Узнать существование Permission на создание Project для User внутри Organization
        :param user_id: id объекта User
        :param org_id: id объекта Organization
        :return: True / False
        """
        result = await self.async_session.execute(
            select(
                Permission
            ).where(
                Permission.user_id == user_id,
                Permission.resource_id == org_id,
                Permission.resource_type == ResourceType.ORGANIZATION.value,
                Permission.permission_type == PermissionType.CREATE_PROJECTS_INSIDE_ORGANIZATION.value
            )
        )
        return bool(result.scalar_one_or_none())

    async def can_user_edit_project(
            self,
            user_id: int,
            project_id: int,
    ) -> bool:
        """
        Узнать существование Permission на редактирование Project для User
        :param user_id: id объекта User
        :param project_id: id объекта Project
        :return: True / False
        """
        result = await self.async_session.execute(
            select(
                Permission
            ).where(
                Permission.user_id == user_id,
                Permission.resource_id == project_id,
                Permission.resource_type == ResourceType.PROJECT.value,
                Permission.permission_type == PermissionType.EDIT_PROJECT.value
            )
        )
        return bool(result.scalar_one_or_none())


permission_repo = get_repository(
    repo_type=PermissionCRUDRepository
)
