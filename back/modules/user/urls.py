from typing import Annotated

from fastapi_babel import _
from fastapi_pagination import Page, paginate

from models.auth import Group, Permission, User, UserGroup
from utils import *

from .schemas import *

settings = get_settings()

router = APIRouter(
    tags=["users"],
    prefix='/users',
    responses=responses,
)


@router.get("/init", response_model=InitResponse)
async def init(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission(["user.view", "user.edit", "user.add"])
    return {
        'groups': db.query(Group).options(joinedload(Group.permissions)).all(),
        'permissions': db.query(Permission).options(joinedload(Permission.in_group)).all()
    }


@router.get("", response_model=Page[UserBase])
async def index(auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.view")
    return paginate(db.query(User).options(joinedload(User.groups)), length_function=lambda x: db.query(User).count())


@router.get("/{id}", response_model=UserBase)
async def show(id: int, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.view")
    return db.query(User).options(joinedload(User.groups)).get(id)


@router.post("", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def create(data: UserCreate, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.add")
    return save_user(db, data.dict())


@router.put("/{id}", response_model=UserBase)
async def edit(id: int, data: UserUpdate, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.edit")
    return save_user(db, data.dict(), id)


def save_user(db: Session, obj: dict, id=None) -> User:
    groups = obj.pop("groups")
    password = obj.pop("password")
    if password:
        obj['password'] = Auth.get_password_hash(password)
    if id != None:
        res = db.query(User).filter(User.id == id).update(obj)
        if res < 1:
            exception_field("id", _("Usuário não encontrado"))
        db.commit()
    else:
        obj = User(**obj)
        db.add(obj)
        db.commit()
        id = obj.id
    if groups:
        db.query(UserGroup).filter(UserGroup.user_id == id).delete()
        db.add_all([UserGroup(user_id=id, group_id=group)
                    for group in groups])
        db.commit()
    return db.query(User).options(joinedload(User.groups)).get(id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, auth: Annotated[Auth, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]):
    auth.check_permission("user.delete")
    obj = db.query(User).filter(User.id == id).delete()
    db.commit()
    if not obj:
        exception_field("id", _("Usuário não encontrado"))
