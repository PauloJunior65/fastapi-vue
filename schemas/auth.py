from datetime import datetime

from pydantic import BaseModel


class UserView(BaseModel):
    id: int
    username: str
    email: str
    name: str
    is_superuser: bool = False
    groups = []
    permissions: list[str] = []


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expire: datetime = None
    user: UserView


class Token(BaseModel):
    access_token: str
    token_type: str
    expire: datetime = None


class TokenData(BaseModel):
    username: str
    password: str