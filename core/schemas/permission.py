from typing import Optional

from core.schemas.base import BaseSchemaModel


class PermissionsResponse(BaseSchemaModel):
    can_create_global_organizations: Optional[bool] = None


class PermissionsShortResponse(BaseSchemaModel):
    permission_id: int
