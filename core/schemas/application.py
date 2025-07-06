from enum import Enum

from core.schemas.base import BaseSchemaModel


class ApplicationRequest(BaseSchemaModel):
    vacancy_id: int
    description: str

class UserApplicationsInOrganizationRequest(BaseSchemaModel):
    org_id: int

class ApplicationId(BaseSchemaModel):
    application_id: int

class ApplicationCancelByUserRequest(BaseSchemaModel):
    application_id: int

class ApplicationActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    REJECTED = "REJECTED"
    ACCEPTED = "ACCEPTED"
    CANCELED = "CANCELED"
    INACTIVE = "INACTIVE"


class ApplicationShortInfo(BaseSchemaModel):
    application_id: int
    vacancy_id: int


class ApplicationLimits(BaseSchemaModel):
    application_number_current: int
    application_number_max: int


class ApplicationMainInfo(BaseSchemaModel):
    application_id: int
    description: str
    vacancy_id: int
    vacancy_name: str
    project_id: int
    project_name: str
    activity_status: ApplicationActivityStatusType
    created_at: str