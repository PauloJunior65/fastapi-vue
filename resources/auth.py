from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic_core import ValidationError
from sqlmodel import Session, select

from core.caches import Cache, get_cache
from core.databases import get_database
from core.exceptions import create_exception, create_field_exception
from core.hashing import create_access_token, read_access_token
from core.settings import get_settings
from models.auth import User

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthUser(User):

    def __init__(self, **data):
        permissions = data.pop('permissions', [])
        super().__init__(**data)
        self.permisions = permissions

    def reload(self, session: Session):
        user = session.scalar(select(AuthUser).where(AuthUser.id == self.id))
        if not user:
            raise create_exception('Usuário não encontrado', status_code=404)
        self.__dict__.update(user.__dict__)

    def create_token(self):
        expire = settings.AUTH_TOKEN_EXPIRE_MINUTES
        if self.disabled_expire_token:
            expire = 0
        if settings.AUTH_MODE in {'db', 'cache'}:
            return create_access_token(data={'user_id': self.id}, expires_delta=expire)
        return create_access_token(data={'user': self.model_dump()}, expires_delta=expire)

    def check_permission(self, permissions: list, exception: bool = False):
        if self.is_superuser:
            return True
        for permission in permissions:
            if permission in self.permisions:
                return True
        if exception:
            raise create_exception('Permissão negada', status_code=403)
        return False


def authenticate_user(session: Session, username: str = None, email: str = None, password: str = None, exception: bool = True) -> AuthUser:
    if (not username or not email) or not password:
        if exception:
            raise create_exception('Usuário ou senha não informados', status_code=400)
        return False
    user = session.scalar(select(AuthUser).where((User.username == username) | (User.email == email)))
    if not user:
        if exception:
            raise create_field_exception('username', 'Usuário não encontrado')
        return False
    if not user.check_password(password):
        if exception:
            raise create_field_exception('password', 'Senha incorreta')
        return False
    return user


def authenticate_token(session: Session, cache: Cache, token: str, exception: bool = True) -> AuthUser:
    data = read_access_token(token, exception=exception)
    if not data:
        raise create_exception('Token inválido', status_code=401)
    modo = settings.AUTH_MODE
    if modo == 'db' and isinstance(data.get('user_id'), int):
        user = session.scalar(select(AuthUser).where(AuthUser.id == data['user_id']))
        if user:
            return user
    elif modo == 'cache' and isinstance(data.get('user_id'), int):
        data = cache.get(f'users:{data.get('user_id')}')
        if not data:
            user = session.scalar(select(AuthUser).where(AuthUser.id == data['user_id']))
            if user:
                cache.set(f'users:{user.id}', user.model_dump(), timeout=settings.AUTH_CACHE_TIMEOUT_MINUTES)
                return user
        else:
            try:
                return AuthUser.model_validate(data, strict=True)
            except ValidationError:
                raise create_exception('Token inválido', status_code=401)
    elif modo == 'state' and isinstance(data.get('user'), dict):
        try:
            return AuthUser.model_validate(data['user'], strict=True)
        except ValidationError:
            raise create_exception('Token inválido', status_code=401)
    else:
        raise create_exception('Token inválido', status_code=401)
    raise create_exception('Usuário não encontrado', status_code=404)


def check_token(token: str, permissions: list = [], db: Session = None, cache: Cache = None) -> AuthUser:
    user: AuthUser = authenticate_token(db, cache, token)
    if permissions:
        user.check_permission(permissions, exception=True)
    return user


if settings.AUTH_MODE == 'cache':
    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database), cache: Cache = Depends(get_cache)) -> AuthUser:
        return check_token(token, db=db, cache=cache)

    class CurrentUser:
        """Classe para verificar se o usuario esta """

        def __init__(self, permissions: list[str] = []):
            """
            Inicializa a classe

            Args:
                permissions (list[str], optional): _description_. Defaults to [].
            """
            self.permissions = permissions

        async def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_database), cache: Cache = Depends(get_cache)) -> AuthUser:
            return check_token(token, permissions=self.permissions, db=db, cache=cache)
else:
    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)) -> AuthUser:
        return check_token(token, db=db)

    class CurrentUser:
        """Classe para verificar se o usuario esta """

        def __init__(self, permissions: list[str] = []):
            """
            Inicializa a classe

            Args:
                permissions (list[str], optional): _description_. Defaults to [].
            """
            self.permissions = permissions

        async def __call__(self, token: str = Depends(oauth2_scheme), db: Session = Depends(get_database)) -> AuthUser:
            return check_token(token, permissions=self.permissions, db=db)
