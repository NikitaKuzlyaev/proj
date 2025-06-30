from core.schemas.base import BaseSchemaModel


class OrganizationMemberInCreate(BaseSchemaModel):
    user_id: int
    org_id: int


