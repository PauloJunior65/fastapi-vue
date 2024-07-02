from datetime import datetime, timedelta

from fastapi import status
from jwt import decode, encode
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from pwdlib import PasswordHash
from zoneinfo import ZoneInfo

from core.exceptions import create_exception
from core.settings import get_settings

settings = get_settings()

pwd_context = PasswordHash.recommended()


def get_password_hash(password: str):
    """
    Faz o hash da senha fornecida usando o pwd_context.

    Args:
        password (str): A senha a ser hash.

    Returns:
        str: A senha hash.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    Verifica se uma senha em texto simples corresponde a uma senha hash.

    Args:
        plain_password (str): A senha em texto simples a ser verificada.
        hashed_password (str): A senha hash a ser comparada.

    Returns:
        bool: True se a senha em texto simples corresponder à senha hash, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: int = settings.AUTH_TOKEN_EXPIRE_MINUTES):
    """
    Cria um token de acesso com base nos dados fornecidos.

    Args:
        data (dict): Os dados a serem codificados no token de acesso.
        expires_delta (int, opcional): O tempo de expiração do token de acesso em minutos.
            Padrão: AUTH_TOKEN_EXPIRE_MINUTES.

    Returns:
        str: O token de acesso codificado.
    """
    to_encode = data.copy()
    if expires_delta > 0:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=expires_delta)
    else:
        expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(days=365 * 5)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def read_access_token(token: str, exception=True) -> dict:
    """
    Decodifica o token de acesso e retorna o payload como um dicionário.

    Args:
        token (str): O token de acesso a ser decodificado.

    Returns:
        dict: O payload decodificado como um dicionário.

    Raises:
        Exception: Se o token estiver expirado ou inválido.
    """
    try:
        return decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except ExpiredSignatureError:
        if exception:
            raise create_exception(
                message='Expired token',
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"})
    except InvalidTokenError:
        if exception:
            raise create_exception(
                message='Invalid token',
                status_code=status.HTTP_401_UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"})
    return False
