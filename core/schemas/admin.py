from enum import Enum
from typing import Optional

from pydantic import Field

from core.schemas.base import BaseSchemaModel
from core.schemas.vacancy import VacancyActivityStatusType, VacancyVisibilityType


class AdminPermissionSignature(BaseSchemaModel):
    permission_id: Optional[int]
    sign: bool = Field(default=False)


