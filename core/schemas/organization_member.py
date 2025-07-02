from typing import Optional

from pydantic import Field

from core.schemas.base import BaseSchemaModel


class OrganizationMemberInCreate(BaseSchemaModel):
    user_id: int
    org_id: int


class OrganizationMemberForAdminResponse(BaseSchemaModel):
    user_id: int
    #username: str

class OrganizationMemberDetailInfo(BaseSchemaModel):
    user_id: int
    org_id: int
    user_name: str
    joined_at: str

class OrganizationMemberDeleteResponse(BaseSchemaModel):
    success: bool = Field(default=False)
    message: Optional[str] = None