from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from core.caches import Cache, get_cache
from core.databases import get_database
from core.exceptions import get_exception_route
from core.settings import get_settings
from schemas.auth import LoginResponse

settings = get_settings()

routers = APIRouter(
    tags=["main"],
    responses=get_exception_route(),
)

if settings.AUTH_MODE == 'cache':
    @routers.post("/token", response_model=LoginResponse, tags=['auth'])
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_database)], cache: Annotated[Cache, Depends(get_cache)]):
        auth = Auth.authenticate(
            db, form_data.username, form_data.password, cache)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

    @routers.get("/refresh", response_model=LoginResponse, tags=['auth'])
    async def refresh(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)], cache: Annotated[Cache, Depends(get_cache)]):
        auth = auth.reload(db, cache)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

else:
    @routers.post("/token", response_model=LoginResponse, tags=['auth'])
    async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
        auth = Auth.authenticate(
            db, form_data.username, form_data.password)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)

    @routers.get("/refresh", response_model=LoginResponse, tags=['auth'])
    async def refresh(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
        auth = auth.reload(db)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)
