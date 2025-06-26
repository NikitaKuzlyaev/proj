import datetime
from typing import Sequence, Optional

import pydantic

from core.schemas.base import BaseSchemaModel

class PermissionsResponse(BaseSchemaModel):
    can_create_global_organizations: Optional[bool] = None
