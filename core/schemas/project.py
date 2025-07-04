from enum import Enum
from typing import Optional

from pydantic import Field

from core.schemas.base import BaseSchemaModel
from core.schemas.vacancy import VacancyActivityStatusType, VacancyVisibilityType


class ProjectVisibilityType(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class ProjectActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class ProjectManagerInfo(BaseSchemaModel):
    user_id: int
    avatar: Optional[str]
    name: Optional[str]


class ProjectOfVacancyInfo(BaseSchemaModel):
    id: int
    name: str


class ProjectVacanciesFullInfoResponse(BaseSchemaModel):
    vacancy_id: int
    manager: ProjectManagerInfo
    project: ProjectOfVacancyInfo
    name: str
    short_description: str
    number_of_active_applications: int
    number_of_active_offers: int
    created_at: str
    activity_status: VacancyActivityStatusType
    visibility: VacancyVisibilityType
    can_user_make_applications: bool = Field(default=True)
    can_user_edit: bool = Field(default=False)
    has_user_active_applications: bool = Field(default=False)
    has_user_active_offer: bool = Field(default=False)


class ProjectCreateRequest(BaseSchemaModel):
    org_id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: ProjectVisibilityType
    activity_status: ProjectActivityStatusType


class ProjectPatchRequest(BaseSchemaModel):
    project_id: int
    org_id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: ProjectVisibilityType
    activity_status: ProjectActivityStatusType


class ProjectFullInfoResponse(BaseSchemaModel):
    org_id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: ProjectVisibilityType
    activity_status: ProjectActivityStatusType
    manager: ProjectManagerInfo
    open_vacancies: Optional[int] = Field(default=0)
    team_current_size: Optional[int] = Field(default=0)
    team_full_size: Optional[int] = Field(default=0)


class CreatedProjectResponse(BaseSchemaModel):
    project_id: int


class PatchedProjectResponse(BaseSchemaModel):
    project_id: int


class ProjectsInOrganizationRequest(BaseSchemaModel):
    org_id: int


class ProjectsInOrganizationShortInfoResponse(BaseSchemaModel):
    project_id: int
    project_name: str
    project_short_description: Optional[str] = None
    project_manager: ProjectManagerInfo
    project_open_vacancies: Optional[int] = Field(default=0)
    project_team_current_size: Optional[int] = Field(default=0)
    project_team_full_size: Optional[int] = Field(default=0)
