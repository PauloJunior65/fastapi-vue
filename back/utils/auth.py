from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import get_settings
from models.auth import User
from sqlalchemy.orm import joinedload
from fastapi_babel import _
from typing import List, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.utils import GetterDict

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
        return ['id', 'username', 'password', 'name', 'is_superuser', 'permissions']

    def check_permission(self, permission: str):
        if self.is_superuser or \
            (isinstance(permission, str) and permission in self.permissions) or \
                (isinstance(permission, list) and any(p in self.permissions for p in permission)):
            return
        raise HTTPException(
            status_code=403,
            detail=_("You dont have permission to this action."))

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

    def create_token(self, expires_delta: timedelta = None):
        data = {key: value for key,
                value in self.dict() if key in self.token_fields}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        data.update({"exp": expire})
        encoded_jwt = jwt.encode(
            data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def authenticate(db: Session, username: str, password: str):
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
                raise HTTPException(status_code=400, detail="Inactive user")
            permissions = []
            for item in db.execute("SELECT CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id = :id;", {'id': user.id}).fetchall():
                permissions.append(item['perm'])
            setattr(user, 'permissions', permissions)
            return Auth.from_orm(user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Incorrect username or password"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    @staticmethod
    def load_payload(payload: dict):
        data = dict()
        for i in Auth.token_fields:
            if i not in payload.keys():
                return None
            data[i] = payload.get(i)
        return Auth(**data)


class CurrentUser:
    """Classe para verificar se o usuario esta """

    def __init__(self, permissions: list[str] = []):
        """

        Args:
            permissions (list[str], optional): _description_. Defaults to [].
        """
        self.permissions = permissions

    async def __call__(self, token: str = Depends(oauth2_scheme)):
        return _check_token(token, self.permissions)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return _check_token(token)


def _check_token(token: str, permissions: list = []):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=_("Não foi possível validar as credenciais"),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Le o token e verifica se é valido
        payload: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user = Auth.load_payload(payload)
        if user is None:
            raise credentials_exception
        if permissions:
            user.check_permission(permissions)
        return user
    except JWTError:
        raise credentials_exception
