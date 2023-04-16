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


class PermissionGetterDict(GetterDict):
    def get(self, key: str, default=None):
        if key in {'group', 'code'}:
            return getattr(self._obj, 'permission_'+key)
        else:
            return super(PermissionGetterDict, self).get(key, default)


class PermissionBase(BaseModel):
    group: str
    code: str

    class Config:
        orm_mode = True
        getter_dict = PermissionGetterDict


class GroupBase(BaseModel):
    id: int
    name: str
    permissions: list[PermissionBase] = []

    class Config:
        orm_mode = True


class PermissionInGroupBase(BaseModel):
    code: str
    name: str


class GroupPermissionBase(BaseModel):
    group: str
    name: str
    permissions: list[PermissionInGroupBase] = []


class InitResponse(BaseModel):
    groups: list[GroupBase] = []
    permissions: list[GroupPermissionBase] = []

    @validator("permissions", pre=True, allow_reuse=False)
    def set_permissions(cls, v, values, **kwargs):
        groups = defaultdict(
            lambda: {'group': '', 'name': '', 'permissions': []})
        for permission in v:
            groups[permission.group]['group'] = permission.in_group.group
            groups[permission.group]['name'] = _(permission.in_group.name)
            groups[permission.group]['permissions'].append({
                'code': permission.code,
                'name': _(permission.name),
            })
        groups = list(map(lambda x: {
            **x, 'permissions': sorted(x['permissions'], key=lambda x: x['name'])}, groups.values()))
        return sorted(groups, key=lambda x: x['name'])
