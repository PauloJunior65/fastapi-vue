from typing import Annotated

from fastapi_babel import _
from fastapi_pagination import Page, paginate

from models.auth import Group
from utils import *

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
        db.query(Group).options(joinedload(Group.users),
                                joinedload(Group.permissions)),
        length_function=lambda x: db.query(Group).count())


@router.get("/{id}", response_model=GroupBase)
async def show(id: int, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("group.view")
    return db.query(Group).options(joinedload(Group.users), joinedload(Group.permissions)).get(id)


@router.post("", response_model=GroupBase, status_code=status.HTTP_201_CREATED)
async def create(data: GroupCreate, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.add")
    return save_group(db, data.dict())


@router.put("/{id}", response_model=GroupBase)
async def edit(id: int, data: GroupEdit, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.edit")
    return save_group(db, data.dict(), id)


def save_group(db: Session, obj: dict, id=None) -> Group:
    if id != None:
        res = db.query(Group).filter(Group.id == id).update(obj)
        if res < 1:
            exception_field("id", _("Grupo não encontrado"))
        db.commit()
    else:
        obj = Group(**obj)
        db.add(obj)
        db.commit()
    return db.query(Group).options(joinedload(Group.users), joinedload(Group.permissions)).get(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.delete")
    obj = db.query(Group).filter(Group.id == id).delete()
    db.commit()
    if not obj:
        exception_field("id", _("Grupo não encontrado"))
