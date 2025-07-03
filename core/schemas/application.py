from enum import Enum

from core.schemas.base import BaseSchemaModel


class ApplicationRequest(BaseSchemaModel):
    vacancy_id: int
    description: str

class ApplicationActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELED = "CANCELED"
    INACTIVE = "INACTIVE"


class ApplicationShortInfo(BaseSchemaModel):
    application_id: int
    vacancy_id: int