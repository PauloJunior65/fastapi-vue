from utils import *
from .schemas import *
from fastapi_babel import _

settings = get_settings()

router = APIRouter(
    tags=["auth"],
    prefix='/auth',
    responses=responses,
)

if settings.AUTH_MODE == 'cache':
    @router.post("/token", response_model=LoginResponse)
    async def login(request: Request, user: Login, db: Session = Depends(get_db), cache: Cache = Depends(get_cache)):
        auth = Auth.authenticate(db, user.username, user.password, cache)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)
else:
    @router.post("/token", response_model=LoginResponse)
    async def login(request: Request, user: Login, db: Session = Depends(get_db)):
        auth = Auth.authenticate(db, user.username, user.password)
        token = auth.create_token()
        return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)


@router.get("/refresh", response_model=LoginResponse)
async def refresh(request: Request, auth: Auth = Depends(get_current_user), db: Session = Depends(get_db)):
    auth = auth.reload(db)
    token = auth.create_token()
    return LoginResponse(access_token=token[0], token_type='bearer', expire=token[1], user=auth)
