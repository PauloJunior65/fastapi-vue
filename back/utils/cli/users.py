from utils.database import get_engine
from utils.auth import Auth
from sqlalchemy import text
import click

help_users = """
"""


def cmd_users(cmd: click.Group):
    @cmd.command(
        "create-admin",
        help="""Extraia todas as mensagens que foram anotadas usando gettext/_ no diretório especificado.
        Na primeira vez, será criado um arquivo messages.pot na raiz do diretório.""",
    )
    @click.argument("username", type=str)
    @click.argument("password", type=str)
    @click.option("--email", type=str, default=None)
    @click.option("--name", type=str, default=None)
    def admin(username: str, password: str, **kwargs):
        with get_engine().connect() as db:
            db.execute(
                text("INSERT INTO `auth_user` (`username`, `password`, `name`, `email`, `is_active`, `is_superuser`) VALUES (:username, :password, :name, :email, 1, 1)"), {
                    'username': username,
                    'password': Auth.get_password_hash(password),
                    'name': kwargs.get('name', username),
                    'email': kwargs.get('email', username+'@email.com')
                })
        click.echo(f"""
        Usuario criado:
            username: {username}
            password: {password}
            email: {kwargs.get('email',username+'@email.com')}
            name: {kwargs.get('name',username)}
        """)

    @cmd.command(
        "create-user",
        help="""Extraia todas as mensagens que foram anotadas usando gettext/_ no diretório especificado.
        Na primeira vez, será criado um arquivo messages.pot na raiz do diretório.""",
    )
    @click.argument("username", type=str)
    @click.argument("password", type=str)
    @click.option("--email", type=str, default=None)
    @click.option("--name", type=str, default=None)
    def user(username: str, password: str, **kwargs):
        with get_engine().connect() as db:
            db.execute(
                text("INSERT INTO `auth_user` (`username`, `password`, `name`, `email`, `is_active`, `is_superuser`) VALUES (:username, :password, :name, :email, 1, 0)"), {
                    'username': username,
                    'password': Auth.get_password_hash(password),
                    'name': kwargs.get('name', username),
                    'email': kwargs.get('email', username+'@email.com')
                })
        click.echo(f"""
        Usuario criado:
            username: {username}
            password: {password}
            email: {kwargs.get('email',username+'@email.com')}
            name: {kwargs.get('name',username)}
        """)
