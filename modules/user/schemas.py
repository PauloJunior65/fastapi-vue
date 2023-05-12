from datetime import datetime
from typing import Union

from fastapi_babel import _
from pydantic import BaseModel, EmailStr, Field, validator

from utils import *
from utils.auth import AuthGroup


class FormIndex(BaseModel):
    search: str = Field(
        default='', description="Filtrar por username, nome ou email")
    group: int = Field(ge=1, default=None, description="Filtrar por grupo")
    order: str = Field(default="nome", description="Ordenar por")
    asc: bool = Field(default=True, description="Ordenar por ordem crescente")

    @validator('order')
    def validate_order(cls, v):
        if v not in ["id", "username", "name", "email"]:
            exception_field("order", _("Campo de ordenação inválido"))
        return v


class UserBaseModel(BaseModel):
    username: str = Field(min_length=3, max_length=255)
    name: str = Field(min_length=3, max_length=300)
    email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True


password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"


class UserCreate(UserBaseModel):
    password: str = Field(min_length=8, regex=password_regex)
    groups: list[int] = []


class UserUpdate(UserBaseModel):
    id: int
    password: Union[str, None] = Field(min_length=8, regex=password_regex)
    groups: list[int] = []


class UserBase(UserBaseModel):
    id: int
    date_joined: datetime = None
    created_at: datetime
    updated_at: datetime
    groups: list[AuthGroup] = []


class GroupBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
