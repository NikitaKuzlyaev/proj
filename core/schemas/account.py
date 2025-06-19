import datetime

import pydantic

from core.schemas.base import BaseSchemaModel


class AccountInCreate(BaseSchemaModel):
    username: str
    password: str


class AccountInUpdate(BaseSchemaModel):
    username: str | None
    password: str | None


class AccountInLogin(BaseSchemaModel):
    username: str
    password: str


class AccountWithToken(BaseSchemaModel):
    token: str
    username: str
    created_at: datetime.datetime


class AccountInResponse(BaseSchemaModel):
    id: int
    authorized_account: AccountWithToken
