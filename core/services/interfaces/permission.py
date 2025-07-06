from typing import Protocol

from starlette.responses import JSONResponse

from core.schemas.admin import AdminPermissionSignature
from core.schemas.permission import PermissionsShortResponse


class IPermissionService(Protocol):

    async def can_user_see_project(
            self,
            user_id: int,
            project_id: int,
    ) -> bool:
        ...

    async def can_user_create_organizations(
            self,
            user_id: int,
    ) -> bool:
        ...

    async def can_user_edit_yourself_application(
            self,
            user_id: int,
            application_id: int,
    ) -> bool:
        ...

    async def can_user_see_organization_detail(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        ...

    async def is_user_admin(
            self,
            user_id: int,
    ) -> bool:
        ...

    async def can_user_edit_organization(
            self,
            org_id: int,
            user_id: int,
    ) -> bool:
        ...

    async def check_permission(
            self,
            user_id: int,
            resource_type: str,
            permission_type: str,
            resource_id: int,
    ) -> bool:
        ...

    async def can_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int,
    ) -> bool:
        ...

    async def can_user_edit_project(
            self,
            user_id: int,
            project_id: int,
    ) -> bool:
        ...

    async def can_user_create_projects_inside_organization(
            self,
            user_id: int,
            org_id: int,
    ) -> bool:
        ...

    async def allow_user_edit_vacancy(
            self,
            user_id: int,
            vacancy_id: int
    ) -> PermissionsShortResponse:
        ...
