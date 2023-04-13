from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from passlib.context import CryptContext
from .config import get_settings
from models.auth import User
from sqlalchemy.orm import joinedload
from typing import List, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.utils import GetterDict
from fastapi_babel import _
from sqlalchemy import text
from .cache import Cache, get_cache
from .database import get_db


def exceptions(name: str):
    """Exceptions for auth

    Args:
        name (str): Code of exception, can be: is_active, isvalid, expired, permission, invalid

    Returns:
        HTTPException: Exception
    """
    raise {
        'is_active': HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Usuário inativo"),
            headers={"WWW-Authenticate": "Bearer"},
        ),
        'isvalid': HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Usuário ou senha inválidos"),
            headers={"WWW-Authenticate": "Bearer"},
        ),
        'expired': HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Token expirado"),
            headers={"WWW-Authenticate": "Bearer"},
        ),
        'permission': HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=_("Você não tem permissão para esta ação"),
        )
    }.get(name, HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=_("Não foi possível validar as credenciais"),
        headers={"WWW-Authenticate": "Bearer"},
    ))


settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthGroupGetter(GetterDict):
    def get(self, key: str, default: Any = None) -> Any:
        if key in {'id', 'name'}:
            return getattr(self._obj.group, key)
        else:
            return super(AuthGroupGetter, self).get(key, default)


class AuthGroup(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        getter_dict = AuthGroupGetter


class Auth(BaseModel):
    id: int
    username: str
    password: str
    email: EmailStr | None = None
    name: str
    is_active: bool = True
    is_superuser: bool = False
    date_joined: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    groups: List[AuthGroup] = []
    permissions: list[str] = []

    class Config:
        orm_mode = True

    @property
    def token_fields(self):
        if settings.AUTH_MODE in ['db', 'cache']:
            return ['id']
        return list(self.__fields__.keys())

    def check_permission(self, permission: str):
        if self.is_superuser or \
            (isinstance(permission, str) and permission in self.permissions) or \
                (isinstance(permission, list) and any(p in self.permissions for p in permission)):
            return
        exceptions('permission')

    def verify_password(self, password: str, hashed_password: str = None):
        """Verifica se a senha é valida

        Args:
            plain_password (str): Senha em texto plano
            hashed_password (str): Senha criptografada

        Returns:
            bool: True se a senha for valida
        """
        return pwd_context.verify(password, self.password if hashed_password is None else hashed_password)

    @staticmethod
    def get_password_hash(password):
        """_summary_

        Args:
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        return pwd_context.hash(password)

    def create_token(self, expires_delta: int = settings.AUTH_TOKEN_EXPIRE_MINUTES, with_exp: bool = True):
        data = {key: getattr(self, key) for key in self.token_fields}
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if with_exp:
            return encoded_jwt, expire
        return encoded_jwt

    @staticmethod
    def authenticate(db: Session, username: str, password: str, cache: Cache = None):
        """_summary_

        Args:
            db (Session): _description_
            username (str): _description_
            password (str): _description_

        Raises:
            HTTPException: _description_

        Returns:
            User: _description_
        """
        user = db.query(User).options(joinedload(User.groups)).filter(
            User.username == username).first()
        if user and pwd_context.verify(password, user.password):
            if user.is_active == False:
                exceptions('is_active')
            permissions = [item['perm'] for item in db.execute(text("SELECT CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id = :id;"), {
                'id': user.id}).fetchall()]
            setattr(user, 'permissions', permissions)
            user = Auth.from_orm(user)
            if settings.AUTH_MODE == 'cache' and cache is not None:
                cache.set(f"USER:{user.id}", user,
                          settings.AUTH_CACHE_TIMEOUT_MINUTES * 60)
            return user
        exceptions('isvalid')

    @staticmethod
    def find_id(db: Session, id: int):
        user = db.query(User).options(joinedload(User.groups)).filter(
            User.id == id).first()
        if user:
            permissions = [item['perm'] for item in db.execute(text("SELECT CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id = :id;"), {
                'id': user.id}).fetchall()]
            setattr(user, 'permissions', permissions)
            return Auth.from_orm(user)
        return None

    @staticmethod
    def load_payload(payload: dict, db: Session = None, cache: Cache = None):
        if settings.AUTH_MODE == 'db' and db is not None:
            auth = Auth.find_id(db, payload.get('id', 0))
            if auth is not None and auth.is_active == False:
                return None
            return auth
        elif settings.AUTH_MODE == 'cache' and cache is not None:
            auth: Auth = cache.get(f"USER:{payload.get('id', 0)}")
            if auth is None and db is not None:
                auth = Auth.find_id(db, payload.get('id', 0))
                if auth is not None:
                    cache.set(f"USER:{auth.id}", auth,
                              settings.AUTH_CACHE_TIMEOUT_MINUTES * 60)
            if auth is not None and auth.is_active == False:
                return None
            return auth
        elif settings.AUTH_MODE == 'static':
            data = dict()
            for i in Auth.token_fields:
                if i not in payload.keys():
                    return None
                data[i] = payload.get(i)
            return Auth(**data)
        return None

    def reload(self, db: Session, cache: Cache = None):
        if settings.AUTH_MODE == 'static':
            auth = Auth.find_id(db, self.id)
            if auth is not None:
                if auth.is_active == False:
                    exceptions('is_active')
                self.__dict__.update(auth.__dict__)
        return self


if settings.AUTH_MODE == 'cache':
    class CurrentUser:
        """Classe para verificar se o usuario esta """

        def __init__(self, permissions: list[str] = []):
            """

            Args:
                permissions (list[str], optional): _description_. Defaults to [].
            """
            self.permissions = permissions

        async def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), cache: Cache = Depends(get_cache)) -> Auth:
            return _check_token(token, self.permissions, db, cache)

    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db), cache: Cache = Depends(get_cache)) -> Auth:
        return _check_token(token, db=db, cache=cache)
else:
    class CurrentUser:
        """Classe para verificar se o usuario esta """

        def __init__(self, permissions: list[str] = []):
            """

            Args:
                permissions (list[str], optional): _description_. Defaults to [].
            """
            self.permissions = permissions

        async def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Auth:
            return _check_token(token, self.permissions, db)

    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Auth:
        return _check_token(token, db=db)


def _check_token(token: str, permissions: list = [], db: Session = None, cache: Cache = None) -> Auth:
    try:
        # Le o token e verifica se é valido
        payload: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = Auth.load_payload(payload, db, cache)
        if user is None:
            exceptions('invalid')
        if permissions:
            user.check_permission(permissions)
        return user
    except ExpiredSignatureError:
        exceptions('expired')
    except JWTError:
        exceptions('invalid')
