from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry

from utils.hashing import get_password_hash, verify_password

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'auth_user'
    __table_args__ = {'comment': 'Tabela de usuários do sistema'}

    id: Mapped[int] = mapped_column(primary_key=True, init=False, comment='ID do usuário')
    username: Mapped[str] = mapped_column(unique=True, index=True, nullable=False, comment='Nome de usuário')
    password: Mapped[str] = mapped_column(init=False, nullable=False, comment='Senha do usuário criptografada')
    name: Mapped[str] = mapped_column(nullable=False, comment='Nome do usuário completo')
    email: Mapped[str] = mapped_column(unique=True, nullable=True, comment='E-mail do usuário')
    is_active: Mapped[bool] = mapped_column(init=False, default=True, nullable=False, comment='Usuário ativo')
    is_superuser: Mapped[bool] = mapped_column(init=False, default=False, nullable=False, comment='Usuário superusuário')
    date_joined: Mapped[datetime] = mapped_column(init=False, nullable=True, comment='Data do último login')
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), comment='Data de criação do registro')

    def check_password(self, password: str) -> bool:
        return verify_password(password, self.password)

    def set_password(self, password: str) -> None:
        self.password = get_password_hash(password)


@table_registry.mapped_as_dataclass
class Group:
    __tablename__ = 'auth_group'
    __table_args__ = {'comment': 'Tabela de grupos de usuários do sistema'}

    id: Mapped[int] = mapped_column(primary_key=True, init=False, comment='ID do grupo')
    name: Mapped[str] = mapped_column(nullable=False, comment='Nome do grupo')
    description: Mapped[str] = mapped_column(nullable=False, comment='Descrição do grupo')


@table_registry.mapped_as_dataclass
class UserGroup:
    __tablename__ = 'auth_user_has_group'
    __table_args__ = {'comment': 'Tabela de usuários em grupos do sistema'}

    user_id: Mapped[int] = mapped_column(ForeignKey('auth_user.id'), primary_key=True, comment='ID do usuário')
    group_id: Mapped[int] = mapped_column(ForeignKey('auth_group.id'), primary_key=True, comment='ID do grupo')
    created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), comment='Data que o usuário foi adicionado ao grupo')
    added_by: Mapped[int] = mapped_column(ForeignKey('auth_user.id'), nullable=True, comment='ID do usuário que adicionou o usuário ao grupo')


@table_registry.mapped_as_dataclass
class PermissionGroup:
    __tablename__ = 'auth_permission_group'
    __table_args__ = {'comment': 'Tabela de grupos de permissões do sistema'}

    id: Mapped[int] = mapped_column(primary_key=True, init=False, comment='ID do grupo de permissão')
    group: Mapped[str] = mapped_column(unique=True, nullable=False, comment='Grupo de permissão')
    name: Mapped[str] = mapped_column(nullable=False, comment='Nome do grupo de permissão')
    description: Mapped[str] = mapped_column(nullable=True, comment='Descrição do grupo de permissão')


@table_registry.mapped_as_dataclass
class Permission:
    __tablename__ = 'auth_permission'
    __table_args__ = {'comment': 'Tabela de permissões do sistema'}

    id: Mapped[int] = mapped_column(primary_key=True, init=False, comment='ID da permissão')
    group_id: Mapped[int] = mapped_column(ForeignKey('auth_permission_group.id'), primary_key=True, comment='ID do grupo da permissão')
    code: Mapped[str] = mapped_column(unique=True, nullable=False, comment='Código da permissão')
    name: Mapped[str] = mapped_column(nullable=False, comment='Nome da permissão')
    description: Mapped[str] = mapped_column(nullable=True, comment='Descrição da permissão')


# @table_registry.mapped_as_dataclass
# class GroupPermission:
#     __tablename__ = 'auth_group_has_permission'
#     __table_args__ = {'comment': 'Tabela de permissões em grupos do sistema'}

#     group_id: Mapped[int] = mapped_column(foreign_key='auth_group.id', primary_key=True, init=False, comment='ID do grupo')
#     permission_id: Mapped[int] = mapped_column(foreign_key='auth_permission.id', primary_key=True, init=False, comment='ID da permissão')
#     created_at: Mapped[datetime] = mapped_column(init=False, server_default=func.now(), comment='Data que a permissão foi adicionada ao grupo')
#     added_by: Mapped[int] = mapped_column(foreign_key='auth_user.id', nullable=True, comment='ID do usuário que adicionou a permissão ao grupo')
