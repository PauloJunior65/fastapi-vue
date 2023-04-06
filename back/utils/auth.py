from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .config import get_settings
from models.auth import User
from sqlalchemy.orm import joinedload
from utils.babel import _
from fastapi.encoders import jsonable_encoder

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthUser:
    permissions = []
    
    def __init__(self,user:User):
        pass
    
    # @property
    # def permissions(self):
    #     if self._permissions is None:
    #         self.permissions = []
    #         for item in self._db.execute("SELECT CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id = :id;", {'id': obj.id}).fetchall():
    #             self.permissions.append(item['perm'])
    #     return self._permissions
    
    # def to_dict(self,db):
    #     db
    #     data = self.__dict__
    #     data['permissions']
    #     return data

class auth:
    
    @staticmethod
    def verify_password(plain_password:str, hashed_password:str):
        """Verifica se a senha é valida

        Args:
            plain_password (str): Senha em texto plano
            hashed_password (str): Senha criptografada

        Returns:
            bool: True se a senha for valida
        """
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        """_summary_

        Args:
            password (_type_): _description_

        Returns:
            _type_: _description_
        """
        return pwd_context.hash(password)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
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
        user = db.query(User).options(joinedload(User.groups)).filter(User.username == username).first()
        if user and auth.verify_password(password, user.password):
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Incorrect username or password"),
            headers={"WWW-Authenticate": "Bearer"},
        )

    # @staticmethod
    # def create_access_token(user: User, expires_delta: timedelta=None):
    #     user = jsonable_encoder(User.from_orm(UserRepository._load_user(db,user)))
    #     if expires_delta:
    #         expire = datetime.utcnow() + expires_delta
    #     else:
    #         expire = datetime.utcnow() + timedelta(minutes=15)
    #     data.update({"exp": expire})
    #     encoded_jwt = jwt.encode(
    #         data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    #     return encoded_jwt

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Não foi possível validar as credenciais"),
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # Le o token e verifica se é valido
            payload: dict = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            if not all(payload.get(i) != None for i in ["username", "email", "name", "is_active", "is_superuser", "permissions"]):
                raise credentials_exception
            if payload.get("is_active") == False:
                raise HTTPException(status_code=400, detail="Inactive user")
        except JWTError:
            raise credentials_exception
        return payload

    @staticmethod
    def check_permission(current_user: dict, permission: str):
        if current_user.get("is_superuser"):
            return
        if isinstance(permission, str) and permission in current_user.get("permissions",[]):
            return
        if isinstance(permission, list) and any(p in current_user.get("permissions",[]) for p in permission):
            return
        raise HTTPException(
            status_code=403,
            detail=_("You dont have permission to this action."))
