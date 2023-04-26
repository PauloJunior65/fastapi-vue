from datetime import datetime, timedelta
from typing import Annotated, Any, List

from fastapi import Depends, FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi_babel import _
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from pydantic.utils import GetterDict
from sqlalchemy import text
from sqlalchemy.orm import Session, joinedload

from models.auth import User

from .cache import Cache, get_cache
from .config import get_settings
from .database import get_db
from .helper import exception


def exceptions(name: str):
    """Exceptions for auth

    Args:
        name (str): Code of exception, can be: is_active, isvalid, expired, permission, invalid

    Returns:
        HTTPException: Exception
    """
    exception(
        mensagem={
            'is_active': _("Usuário inativo"),
            'isvalid': _("Usuário ou senha inválidos"),
            'expired': _("Token expirado"),
            'permission': _("Você não tem permissão para esta ação")
        }.get(name, _("Não foi possível validar as credenciais")),
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers={"WWW-Authenticate": "Bearer"})


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
    def token_data(self) -> dict:
        if settings.AUTH_MODE in ['db', 'cache']:
            return jsonable_encoder(self, include=['id'])
        return jsonable_encoder(self, exclude_none=True)

    def check_permission(self, permission: str):
        if self.is_superuser or \
            (isinstance(permission, str) and permission in self.permissions) or \
                (isinstance(permission, list) and any(p in self.permissions for p in permission)):
            return
        exceptions('permission')

    @classmethod
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
        data = self.token_data
        if expires_delta < 0:
            expire = datetime.utcnow() + timedelta(days=365*20)
        else:
            expire = datetime.utcnow() + timedelta(minutes=expires_delta)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if with_exp:
            return encoded_jwt, expire
        return encoded_jwt

    @classmethod
    def authenticate(self, db: Session, username: str, password: str, cache: Cache = None):
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
        if isinstance(user, User) and pwd_context.verify(password, user.password):
            if user.is_active == False:
                exceptions('is_active')
            self._set_permissions(db, user)
            user = Auth.from_orm(user)
            if settings.AUTH_MODE == 'cache' and cache is not None:
                cache.set(f"USER:{user.id}", user,
                          settings.AUTH_CACHE_TIMEOUT_MINUTES * 60)
            return user
        exceptions('isvalid')

    @classmethod
    def find_id(self, db: Session, id: int):
        user = db.query(User).options(joinedload(User.groups)).filter(
            User.id == id).first()
        if user:
            self._set_permissions(db, user)
            return Auth.from_orm(user)
        return None

    @classmethod
    def _set_permissions(self, db: Session, user: User):
        permissions = []
        for item in db.execute(text(
                f"SELECT CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id = {user.id};")).fetchall():
            permissions.append(item[0])
        setattr(user, 'permissions', permissions)
        return user

    @classmethod
    def load_payload(self, payload: dict, db: Session = None, cache: Cache = None):
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
            data = {i: payload.get(i) for i in set(
                payload.keys()) & set(Auth.__fields__.keys())}
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


def add_auth(app: FastAPI):
    if settings.AUTH_MODE == 'cache':
        @app.post("/token", response_model=LoginResponse, tags=['auth'])
        async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)], cache: Annotated[Cache, Depends(get_cache)]):
            auth = Auth.authenticate(
                db, form_data.username, form_data.password, cache)
            token = auth.create_token()
            return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

        @app.get("/refresh", response_model=LoginResponse, tags=['auth'])
        async def refresh(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)], cache: Annotated[Cache, Depends(get_cache)]):
            auth = auth.reload(db, cache)
            token = auth.create_token()
            return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

    else:
        @app.post("/token", response_model=LoginResponse, tags=['auth'])
        async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
            auth = Auth.authenticate(
                db, form_data.username, form_data.password)
            token = auth.create_token()
            return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

        @app.get("/refresh", response_model=LoginResponse, tags=['auth'])
        async def refresh(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
            auth = auth.reload(db)
            token = auth.create_token()
            return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)
