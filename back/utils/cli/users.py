from utils.database import get_engine
from utils.auth import Auth
from sqlalchemy import text
import click

help_users = """
Manipulação de usuários do sistema:\n
    - create-admin: Cria um usuário admin\n
    - create-user: Cria um usuário comum\n
"""


def cmd_users(cmd: click.Group):
    @cmd.command(
        "create-admin",
        help="Cria um usuário admin",
    )
    @click.argument("username", type=str)
    @click.argument("password", type=str)
    @click.option("--email", required=False, type=str)
    @click.option("--name", required=False, type=str)
    def admin(username: str, password: str, **kwargs):
        name = kwargs.get('name', username)
        email = kwargs.get('email', username+'@email.com')
        hash = Auth.get_password_hash(password)
        with get_engine().connect() as db:
            db.execute(
                text("INSERT INTO `auth_user` (`username`, `password`, `name`, `email`, `is_active`, `is_superuser`) VALUES (:username, :password, :name, :email, 1, 1)"), {
                    'username': username,
                    'password': hash,
                    'name': {name if name else username},
                    'email': email if email else username+'@email.com'
                })
            db.commit()
        click.echo(f"""
        Usuario Admin criado:
            username: {username}
            password: {password} (hash: {hash})
            name: {name if name else username}
            email: {email if email else username+'@email.com'}
        """)

    @cmd.command(
        "create-user",
        help="Cria um usuário comum",
    )
    @click.argument("username", type=str)
    @click.argument("password", type=str)
    @click.option("--email", type=str, default=None)
    @click.option("--name", type=str, default=None)
    def user(username: str, password: str, **kwargs):
        name = kwargs.get('name', username)
        email = kwargs.get('email', username+'@email.com')
        hash = Auth.get_password_hash(password)
        with get_engine().connect() as db:
            db.execute(
                text("INSERT INTO `auth_user` (`username`, `password`, `name`, `email`, `is_active`, `is_superuser`) VALUES (:username, :password, :name, :email, 1, 0)"), {
                    'username': username,
                    'password': Auth.get_password_hash(password),
                    'name': {name if name else username},
                    'email': email if email else username+'@email.com'
                })
            db.commit()
        click.echo(f"""
        Usuario criado:
            username: {username}
            password: {password} (hash: {hash})
            name: {name if name else username}
            email: {email if email else username+'@email.com'}
        """)
