from core.schemas.base import BaseSchemaModel


class OrganizationMemberInCreate(BaseSchemaModel):
    user_id: int
    organization_id: int


