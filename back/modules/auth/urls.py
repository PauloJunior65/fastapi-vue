from utils import *

router = APIRouter(
    tags=["auth"],
    prefix='/user',
    # responses={404: {"description": "Not found"}},
)


@router.get("")
async def index():
    return list(Auth.__fields__.keys())
