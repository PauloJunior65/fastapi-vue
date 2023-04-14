from pydantic import BaseModel, create_model
from datetime import datetime
from utils.auth import Auth


class UserView(BaseModel):
    id: int
    username: str
    email: str
    name: str
    is_superuser: bool = False
    groups = []
    permissions: list[str] = []


class Login(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expire: datetime = None
    user: UserView
