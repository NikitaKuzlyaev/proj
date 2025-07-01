from typing import Optional

from pydantic import Field

from core.schemas.base import BaseSchemaModel


class AdminPermissionSignature(BaseSchemaModel):
    permission_id: Optional[int]
    sign: bool = Field(default=False)


