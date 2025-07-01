import datetime
from enum import Enum
from typing import Sequence, Optional

from pydantic import field_validator, Field

from core.schemas.base import BaseSchemaModel
from core.schemas.project import ProjectManagerInfo


class OrganizationJoinResponse(BaseSchemaModel):
    member_id: Optional[int]

class OrganizationInCreate(BaseSchemaModel):
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    creator_id: int


class OrganizationJoinRequest(BaseSchemaModel):
    org_id: int
    code: Optional[str] = None

class OrganizationInUpdate(BaseSchemaModel):
    ...


class OrganizationJoinPolicyType(str, Enum):
    OPEN = "OPEN"
    INVITE = "INVITE"
    CLOSED = "CLOSED"
    CODE = "CODE"


class OrganizationVisibilityType(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


class OrganizationActivityStatusType(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class OrganizationInDelete(BaseSchemaModel):
    id: int


class OrganizationInPatch(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: OrganizationVisibilityType
    activity_status: OrganizationActivityStatusType
    join_policy: OrganizationJoinPolicyType


class OrganizationProjectsShortInfoResponse(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    manager: ProjectManagerInfo
    open_vacancies: Optional[int] = Field(default=0)
    team_current_size: Optional[int] = Field(default=0)
    team_full_size: Optional[int] = Field(default=0)


class OrganizationCreateInRequest(BaseSchemaModel):
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None


class OrganizationResponse(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    creator_id: int


class OrganizationShortInfoResponse(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    creator_id: int
    is_user_member: bool
    join_policy: OrganizationJoinPolicyType


class SequenceOrganizationResponse(BaseSchemaModel):
    body: Sequence[OrganizationResponse]


class SequenceAllOrganizationsShortInfoResponse(BaseSchemaModel):
    body: Sequence[OrganizationShortInfoResponse]


class OrganizationInfoForEditResponse(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: OrganizationVisibilityType
    activity_status: OrganizationActivityStatusType
    join_policy: OrganizationJoinPolicyType


class OrganizationForEditRequest(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    visibility: OrganizationVisibilityType
    activity_status: OrganizationActivityStatusType
    join_policy: OrganizationJoinPolicyType


class OrganizationDetailInfoResponse(BaseSchemaModel):
    # by design
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    created_at: str
    creator_id: int
    number_of_members: int
    allow_user_edit: bool = Field(default=True)
    allow_user_delete: Optional[bool] = Field(default=False)

    @field_validator("created_at", mode="before")
    @classmethod
    def format_created_at(cls, v: datetime.datetime | str) -> str:
        if isinstance(v, datetime.datetime):
            return v.isoformat()
        return v
