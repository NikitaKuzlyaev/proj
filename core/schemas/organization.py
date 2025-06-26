import datetime
from enum import Enum
from typing import Sequence, Optional

import pydantic
from pydantic import field_validator, Field

from core.schemas.base import BaseSchemaModel


class OrganizationInCreate(BaseSchemaModel):
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    creator_id: int


class OrganizationInUpdate(BaseSchemaModel):
    ...


class OrganizationInDelete(BaseSchemaModel):
    id: int

class OrganizationInPatch(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None


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


class OrganizationJoinPolicy(str, Enum):
    OPEN = "OPEN"
    INVITE_ONLY = "INVITE"
    CLOSED = "CLOSED"


class OrganizationShortInfoResponse(BaseSchemaModel):
    id: int
    name: str
    short_description: Optional[str] = None
    creator_id: int
    is_user_member: bool
    join_policy: OrganizationJoinPolicy


class SequenceOrganizationResponse(BaseSchemaModel):
    body: Sequence[OrganizationResponse]


class SequenceAllOrganizationsShortInfoResponse(BaseSchemaModel):
    body: Sequence[OrganizationShortInfoResponse]


class OrganizationDetailInfoResponse(BaseSchemaModel):
    # by design
    id: int
    name: str
    short_description: Optional[str] = None
    long_description: Optional[str] = None
    created_at: str
    creator_id: int
    # Вычисляемые
    number_of_members: int
    allow_user_edit: bool = Field(default=True)
    allow_user_delete: Optional[bool] = Field(default=False)

    # number_of_all_projects: int
    # number_of_active_projects: int
    # number_of_active_vacancies: int
    # number_of_active_threads: int

    @field_validator("created_at", mode="before")
    @classmethod
    def format_created_at(cls, v: datetime.datetime | str) -> str:
        if isinstance(v, datetime.datetime):
            return v.isoformat()
        return v
