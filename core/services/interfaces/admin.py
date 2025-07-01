from typing import Protocol

from core.schemas.admin import AdminPermissionSignature


class IAdminService(Protocol):


    async def base_admin_check(
            self,
            user_id: int,
    ) -> AdminPermissionSignature:
        ...


