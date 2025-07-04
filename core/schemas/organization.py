import datetime
from enum import Enum
from typing import Sequence, Optional

from pydantic import field_validator, Field

from core.schemas.base import BaseSchemaModel


class OrganizationJoinResponse(BaseSchemaModel):
    member_id: Optional[int]


class OrganizationMemberId(BaseSchemaModel):
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


class OrganizationMembersForAdminRequest(BaseSchemaModel):
    org_id: int


class OrganizationId(BaseSchemaModel):
    org_id: int


class OrganizationAndUserId(BaseSchemaModel):
    user_id: int
    org_id: int


class OrganizationInPatch(BaseSchemaModel):
    org_id: int
    org_name: str
    org_short_description: Optional[str] = None
    org_long_description: Optional[str] = None
    org_visibility: OrganizationVisibilityType
    org_activity_status: OrganizationActivityStatusType
    org_join_policy: OrganizationJoinPolicyType


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
    org_id: int
    org_name: str
    org_short_description: Optional[str] = None
    org_creator_id: int
    is_user_member: bool
    org_join_policy: OrganizationJoinPolicyType


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
    org_id: int
    org_name: str
    org_short_description: Optional[str] = None
    org_long_description: Optional[str] = None
    org_created_at: str
    org_creator_id: int
    org_number_of_members: int
    allow_user_edit: bool = Field(default=False)
    allow_user_delete: Optional[bool] = Field(default=False)

    @field_validator("org_created_at", mode="before")
    @classmethod
    def format_created_at(cls, v: datetime.datetime | str) -> str:
        if isinstance(v, datetime.datetime):
            return v.isoformat()
        return v
