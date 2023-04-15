from utils import *
from .schemas import *
from fastapi_babel import _

settings = get_settings()

router = APIRouter(
    tags=["users"],
    prefix='/users',
    responses=responses,
)


@router.get("", response_model=list[UserBase])
async def index(auth: Auth = Depends(get_current_user), db: Session = Depends(get_db)):
    auth.check_permission("user.view")
    return ''
