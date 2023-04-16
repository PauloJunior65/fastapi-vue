from collections import defaultdict
from typing import List

from fastapi_babel import _
from pydantic import BaseModel
from pydantic.utils import GetterDict

from models.auth import Permission


class UserGetter(GetterDict):
    def get(self, key: str, default=None):
        if key in {'id', 'name', 'email'}:
            return getattr(self._obj.user, key)
        else:
            return super(UserGetter, self).get(key, default)


class UserBase(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
        getter_dict = UserGetter


class PermissionGetter(GetterDict):
    def get(self, key: str, default=None):
        if key in {'permissions'}:
            groups = defaultdict(
                lambda: {'name': '', 'description': '', 'permissions': []})
            for permission in self._obj.permissions:
                permission: Permission = permission.permission
                groups[permission.group]['name'] = _(permission.in_group.name)
                groups[permission.group]['description'] = _(
                    permission.in_group.description)
                groups[permission.group]['permissions'].append({
                    'code': permission.group+'.' + permission.code,
                    'name': _(permission.name),
                })
            groups = list(map(lambda x: {
                          **x, 'permissions': sorted(x['permissions'], key=lambda x: x['name'])}, groups.values()))
            return sorted(groups, key=lambda x: x['name'])
        else:
            return super(PermissionGetter, self).get(key, default)


class PermissionBase(BaseModel):
    code: str
    name: str


class GroupPermissionBase(BaseModel):
    name: str
    description: str
    permissions: List[PermissionBase] = []


class GroupBase(BaseModel):
    id: int
    name: str

    users: List[UserBase] = []
    permissions: List[GroupPermissionBase] = []

    class Config:
        orm_mode = True
        getter_dict = PermissionGetter


class GroupCreate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GroupEdit(GroupCreate):
    id: int
