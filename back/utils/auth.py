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

settings = get_settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = db.query(User).options(joinedload(User.groups)).filter(User.username == username).first()
    return user if user and verify_password(password, user.password) else None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(
        data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=_("Could not validate credentials"),
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if not all(payload.get(i) != None for i in ["username", "email", "name", "is_active", "is_superuser", "permissions"]):
            raise credentials_exception
        if payload.get("is_active") == False:
            raise HTTPException(status_code=400, detail="Inactive user")
    except JWTError:
        raise credentials_exception
    return payload


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
