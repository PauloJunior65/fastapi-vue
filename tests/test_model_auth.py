from sqlalchemy import select
from sqlalchemy.orm import Session

from models.auth import Group, Permission, PermissionGroup, User, UserGroup


def test_model_auth_user(session: Session):
    # Create a new user
    new_user = User(username='user_test', name='User Test', email='teste@gmail.com')
    new_user.set_password('123456')
    session.add(new_user)
    session.commit()

    user: User = session.scalar(select(User).where(User.username == new_user.username))

    assert user.username == new_user.username
    assert user.name == new_user.name
    assert user.email == new_user.email
    assert user.check_password('123456')
    assert user.is_active

    # Update the user
    new_user.username = 'user_test_updated'
    session.commit()

    user: User = session.scalar(select(User).where(User.username == new_user.username))

    assert user.username == new_user.username

    # Delete the user
    session.delete(user)
    session.commit()

    user: User = session.scalar(select(User).where(User.username == new_user.username))

    assert user is None


def test_model_auth_group(session: Session):
    # Create a new group
    new_group = Group(name='group_test', description='Group Test')
    session.add(new_group)
    session.commit()

    group: Group = session.scalar(select(Group).where(Group.name == new_group.name))

    assert group.name == new_group.name

    # Update the group
    new_group.name = 'group_test_updated'
    session.commit()

    group: Group = session.scalar(select(Group).where(Group.name == new_group.name))

    assert group.name == new_group.name

    # Delete the group
    session.delete(group)
    session.commit()

    group: Group = session.scalar(select(Group).where(Group.name == new_group.name))

    assert group is None


def test_model_auth_user_group(session: Session):
    # Create a new user
    new_user = User(username='user_test', name='User Test', email='teste@gmail.com')
    new_user.set_password('123456')
    session.add(new_user)
    session.commit()

    # Create a new group
    new_group = Group(name='group_test', description='Group Test')
    session.add(new_group)
    session.commit()

    # Create a new user group association
    user_group = UserGroup(user_id=new_user.id, group_id=new_group.id, added_by=new_user.id)
    session.add(user_group)
    session.commit()

    # Retrieve the user group association
    user_group: UserGroup = session.scalar(
        select(UserGroup).where(UserGroup.user_id == new_user.id and UserGroup.group_id == new_group.id)
    )
    assert user_group.user_id == new_user.id
    assert user_group.group_id == new_group.id

    # Delete the user group association
    session.delete(user_group)
    session.commit()

    # Verify that the user group association is deleted
    user_group: UserGroup = session.scalar(
        select(UserGroup).where(UserGroup.user_id == new_user.id and UserGroup.group_id == new_group.id)
    )
    assert user_group is None

    # Delete the user and group
    session.delete(new_user)
    session.delete(new_group)
    session.commit()


def test_model_auth_permission_group(session: Session):
    # Create a new permission group
    new_permission_group = PermissionGroup(group='permission_group_test', name='Permission Group Test', description='Permission Group Test')
    session.add(new_permission_group)
    session.commit()

    permission_group: PermissionGroup = session.scalar(select(PermissionGroup).where(PermissionGroup.group == new_permission_group.group))

    assert permission_group.group == new_permission_group.group

    # Update the permission group
    new_permission_group.group = 'permission_group_test_updated'
    session.commit()

    permission_group: PermissionGroup = session.scalar(select(PermissionGroup).where(PermissionGroup.group == new_permission_group.group))

    assert permission_group.group == new_permission_group.group

    # Delete the permission group
    session.delete(permission_group)
    session.commit()

    permission_group: PermissionGroup = session.scalar(select(PermissionGroup).where(PermissionGroup.group == new_permission_group.group))

    assert permission_group is None


def test_model_auth_permission(session: Session):
    # Create a new permission group
    new_permission_group = PermissionGroup(group='permission_group_test', name='Permission Group Test', description='Permission Group Test')
    session.add(new_permission_group)
    session.commit()

    # Create a new permission
    new_permission = Permission(group_id=new_permission_group.id, code='permission_test', name='Permission Test', description='Permission Test')
    session.add(new_permission)
    session.commit()

    permission: Permission = session.scalar(select(Permission).where(Permission.code == new_permission.code))

    assert permission.code == new_permission.code

    # Update the permission
    new_permission.code = 'permission_test_updated'
    session.commit()

    permission: Permission = session.scalar(select(Permission).where(Permission.code == new_permission.code))

    assert permission.code == new_permission.code

    # # Delete the permission
    # session.delete(permission)
    # session.commit()

    # permission: Permission = session.scalar(select(Permission).where(Permission.code == new_permission.code))

    # assert permission is None

    # # Delete the permission group
    # session.delete(new_permission_group)
    # session.commit()
