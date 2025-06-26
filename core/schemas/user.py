import datetime

import pydantic

from core.schemas.base import BaseSchemaModel


class UserCreate(BaseSchemaModel):
    username: str
    password: str


class UserOut(BaseSchemaModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class Token(BaseSchemaModel):
    access_token: str
    token_type: str
