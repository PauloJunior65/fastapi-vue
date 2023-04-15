from sqlalchemy.orm import Session, joinedload
from models.auth import User, Group, UserGroup


class UserRepository:
    model = User

    @classmethod
    def find_all(cls, db: Session) -> list[User]:
        objs = db.query(User).options(joinedload(User.groups)).all()
        return cls._load_users(db, objs)

    @classmethod
    def _load_users(db: Session, objs: list[User]):
        obj_ids = {}
        for o in objs:
            setattr(o, 'permissions', [])
            obj_ids[o.id] = o
        for item in db.execute("SELECT u.user_id,CONCAT(p.permission_group,'.',p.permission_code) AS perm FROM `auth_user_has_group` AS u JOIN auth_group AS g ON g.id = u.group_id LEFT JOIN auth_group_has_permission AS p ON g.id = p.group_id WHERE u.user_id in :ids;", {'ids': tuple(obj_ids.keys())}).fetchall():
            obj_ids[item['user_id']].permissions.append(item['perm'])
        return objs
