from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, UniqueConstraint, func

from utils.hashing import get_password_hash, verify_password


class User(SQLModel, table=True):
    __tablename__ = 'auth_user'
    __table_args__ = {'comment': 'Tabela de usuários do sistema'}

    id: Optional[int] = Field(primary_key=True, description='ID do usuário')
    username: str = Field(unique=True, index=True, nullable=False, description='Nome de usuário')
    password: Optional[str] = Field(nullable=False, description='Senha do usuário criptografada')
    name: str = Field(nullable=False, description='Nome do usuário completo')
    email: str = Field(unique=True, nullable=True, description='E-mail do usuário')
    is_active: Optional[bool] = Field(default=True, nullable=False, description='Usuário ativo')
    is_superuser: Optional[bool] = Field(default=False, nullable=False, description='Usuário superusuário')
    date_joined: Optional[datetime] = Field(nullable=True, description='Data do último login')
    created_at: Optional[datetime] = Field(description='Data de criação do registro', sa_column_kwargs=dict(server_default=func.now()))

    def __setattr__(self, key, value):
        if key == 'password':
            value = get_password_hash(value)
        super().__setattr__(key, value)

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    def set_password(self, password: str) -> None:
        self.password = get_password_hash(password)


class Group(SQLModel, table=True):
    __tablename__ = 'auth_group'
    __table_args__ = {'comment': 'Tabela de grupos de usuários do sistema'}

    id: Optional[int] = Field(primary_key=True, description='ID do grupo')
    name: str = Field(nullable=False, description='Nome do grupo')
    description: str = Field(nullable=False, description='Descrição do grupo')


class UserGroup(SQLModel, table=True):
    __tablename__ = 'auth_user_has_group'
    __table_args__ = {'comment': 'Tabela de usuários em grupos do sistema'}

    user_id: int = Field(foreign_key='auth_user.id', primary_key=True, description='ID do usuário')
    group_id: int = Field(foreign_key='auth_group.id', primary_key=True, description='ID do grupo')
    created_at: Optional[datetime] = Field(description='Data que o usuário foi adicionado ao grupo', sa_column_kwargs=dict(server_default=func.now()))
    added_by: int = Field(foreign_key='auth_user.id', description='ID do usuário que adicionou o usuário ao grupo')


class PermissionGroup(SQLModel, table=True):
    __tablename__ = 'auth_permission_group'
    __table_args__ = {'comment': 'Tabela de grupos de permissões do sistema'}

    id: Optional[int] = Field(primary_key=True, description='ID do grupo de permissão')
    group: str = Field(unique=True, nullable=False, description='Grupo de permissão')
    name: str = Field(nullable=False, description='Nome do grupo de permissão')
    description: str = Field(nullable=True, description='Descrição do grupo de permissão')


class Permission(SQLModel, table=True):
    __tablename__ = 'auth_permission'
    __table_args__ = (UniqueConstraint('group_id', 'code', name='uq_group_code'), {'comment': 'Tabela de permissões do sistema'})

    id: Optional[int] = Field(primary_key=True, description='ID da permissão')
    group_id: int = Field(foreign_key='auth_permission_group.id', description='ID do grupo da permissão')
    code: str = Field(nullable=False, description='Código da permissão')
    name: str = Field(nullable=False, description='Nome da permissão')
    description: Optional[str] = Field(nullable=True, description='Descrição da permissão')


class GroupPermission(SQLModel, table=True):
    __tablename__ = 'auth_group_has_permission'
    __table_args__ = (UniqueConstraint('group_id', 'permission_id', name='uq_group_permission'), {'comment': 'Tabela de permissões em grupos do sistema'})

    group_id: int = Field(foreign_key='auth_group.id', primary_key=True, description='ID do grupo')
    permission_id: int = Field(foreign_key='auth_permission.id', primary_key=True, description='ID da permissão')
    created_at: Optional[datetime] = Field(description='Data que a permissão foi adicionada ao grupo', sa_column_kwargs=dict(server_default=func.now()))
    added_by: int = Field(foreign_key='auth_user.id', description='ID do usuário que adicionou a permissão ao grupo')
