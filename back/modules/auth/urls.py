from utils import *

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router.get("")
async def index(db: Session = Depends(get_db)):
    return db.query(User).options(joinedload(User.groups)).first()

