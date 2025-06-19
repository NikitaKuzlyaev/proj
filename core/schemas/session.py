from pydantic import BaseModel


class UserSession(BaseModel):
    key: str
    secret: str
    contest_id: int


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"