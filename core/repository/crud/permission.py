import typing
from typing import Sequence

import sqlalchemy
from sqlalchemy import select
from sqlalchemy.sql import functions as sqlalchemy_functions

from core.dependencies.repository import get_repository
from core.models import Project
from core.models.organizationMember import OrganizationMember

# from core.schemas.user import UserInCreate, UserInLogin, UserInUpdate
from core.models.user import User

from core.schemas.organization_member import OrganizationMemberInCreate
from core.models.organization import Organization
from core.models.permissions import Permission, PermissionType, ResourceType

from core.repository.crud.base import BaseCRUDRepository
from core.services.securities.hashing import pwd_generator
from core.utilities.exceptions.database import EntityAlreadyExists, EntityDoesNotExist
from core.utilities.exceptions.auth import PasswordDoesNotMatch
from core.services.securities.credential import account_credential_verifier


class PermissionCRUDRepository(BaseCRUDRepository):

    async def can_user_edit_organization(
            self,
            user_id: int,
            org_id: int
    ) -> bool:
        stmt = select(Permission).where(
            Permission.user_id == user_id,
            Permission.resource_id == org_id,
            Permission.resource_type == ResourceType.ORGANIZATION.value,
            Permission.permission_type == PermissionType.EDIT_ORGANIZATION.value,
        )
        result = await self.async_session.execute(stmt)
        return bool(result.scalar_one_or_none())

    async def search_exist_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission | None:
        stmt = select(Permission).where(
            Permission.user_id == user_id,
            Permission.resource_type == resource_type,
            Permission.resource_id == resource_id,
            Permission.permission_type == permission_type
        )
        permission = await self.async_session.execute(stmt)
        permission = permission.scalar_one_or_none()
        return permission

    async def create_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> Permission | None:
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
            org_id: int
    ) -> Permission:
        permission: Permission  = (
            await self.create_permission(
                user_id=user_id,
                resource_type=ResourceType.ORGANIZATION.value,
                permission_type=PermissionType.EDIT_ORGANIZATION.value,
                resource_id=org_id,
            )
        )
        return permission

    async def can_user_create_projects_inside_organization(
            self,
            user_id: int,
            org_id: int
    ) -> bool:
        stmt = select(Permission).where(
            Permission.user_id == user_id,
            Permission.resource_id == org_id,
            Permission.resource_type == ResourceType.ORGANIZATION.value,
            Permission.permission_type == PermissionType.CREATE_PROJECTS_INSIDE_ORGANIZATION.value,
        )
        result = await self.async_session.execute(stmt)
        return bool(result.scalar_one_or_none())

    async def can_user_edit_project(
            self,
            user_id: int,
            project_id: int
    ) -> bool:
        stmt = select(Project).where(
            Project.id == project_id,
        )
        res = await self.async_session.execute(stmt)
        project: Project = res.scalar_one_or_none()
        return project.creator_id == user_id


permission_repo = get_repository(repo_type=PermissionCRUDRepository)
