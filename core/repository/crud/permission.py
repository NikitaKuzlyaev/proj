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

    async def allow_user_edit_organization(
            self,
            user_id: int,
            org_id: int
    ) -> Permission:
        print("allow_user_edit_organization",'\n'*10)

        # Попытка найти уже существующее разрешение
        stmt = select(Permission).where(
            Permission.user_id == user_id,
            Permission.resource_type == ResourceType.ORGANIZATION.value,
            Permission.resource_id == org_id,
            Permission.permission_type == PermissionType.EDIT_ORGANIZATION.value
        )
        permission = await self.async_session.execute(stmt)
        permission = permission.scalar_one_or_none()
        if permission:
            print("here", permission,'\n'*10)
            return permission

        # Если разрешения нет — создаём
        new_permission = Permission(
            user_id=user_id,
            resource_type=ResourceType.ORGANIZATION.value,
            resource_id=org_id,
            permission_type=PermissionType.EDIT_ORGANIZATION.value,
        )
        self.async_session.add(instance=new_permission)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_permission)
        return new_permission

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
