from enum import Enum

from core.schemas.base import BaseSchemaModel


class VacancyVisibilityType(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class VacancyActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class VacancyCreateRequest(BaseSchemaModel):
    project_id: int
    name: str
    short_description: str
    activity_status: VacancyActivityStatusType
    visibility: VacancyVisibilityType


class VacancyCreateResponse(BaseSchemaModel):
    vacancy_id: int


class VacancyPatchResponse(BaseSchemaModel):
    vacancy_id: int


class VacancyPatchRequest(BaseSchemaModel):
    vacancy_id: int
    project_id: int
    name: str
    short_description: str
    activity_status: VacancyActivityStatusType
    visibility: VacancyVisibilityType


class VacancyShortInfoResponse(BaseSchemaModel):
    vacancy_id: int
    project_id: int
    name: str
    short_description: str
    activity_status: VacancyActivityStatusType
    visibility: VacancyVisibilityType
