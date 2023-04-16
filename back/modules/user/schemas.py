from collections import defaultdict
from datetime import datetime
from typing import Union

from fastapi_babel import _
from pydantic import BaseModel, EmailStr, Field, validator
from pydantic.utils import GetterDict

from utils.auth import AuthGroup


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
