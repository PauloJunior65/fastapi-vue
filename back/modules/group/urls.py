from typing import Annotated

from fastapi_babel import _
from fastapi_pagination import Page, paginate

from utils import *

from models.auth import Group
from .schemas import *

settings = get_settings()

router = APIRouter(
    tags=["groups"],
    prefix='/groups',
    responses=responses,
)


@router.get("", response_model=Page[GroupBase])
async def index(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("group.view")
    return paginate(
        db.query(Group).options(joinedload(Group.users), joinedload(Group.permissions)), length_function=lambda x: db.query(Group).count())
