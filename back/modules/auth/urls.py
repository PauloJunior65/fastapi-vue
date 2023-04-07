from utils import *
from fastapi_babel import _

router = APIRouter(
    tags=["auth"],
    prefix='/auth',
    responses=responses,
)


@router.get("")
async def index():
    return _("Not found")
