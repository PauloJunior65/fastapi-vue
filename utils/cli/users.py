from utils.database import get_session
from utils.auth import Auth, User
from utils import Session
from sqlalchemy import text
import click

help_users = """
Manipulação de usuários do sistema:\n
    - create-admin: Cria um usuário admin\n
    - create-user: Cria um usuário comum\n
"""


def add_users(db: Session, user: dict):
    user = User(**user)
    db.add(user)
    db.commit()


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
        try:
            with get_session(exec=True) as db:
                add_users(db, {
                    'username': username,
                    'password': hash,
                    'name': name if name else username,
                    'email': email if email else username+'@email.com',
                    'is_active': 1,
                    'is_superuser': 1,
                })
            click.echo(f"""
            Usuario Admin criado:
                username: {username}
                password: {password} (hash: {hash})
                name: {name if name else username}
                email: {email if email else username+'@email.com'}
            """)
        except:
            click.echo(f"""
            Usuario {username} já existe!
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
        try:
            with get_session(exec=True) as db:
                add_users(db, {
                    'username': username,
                    'password': Auth.get_password_hash(password),
                    'name': name if name else username,
                    'email': email if email else username+'@email.com',
                    'is_active': 1,
                    'is_superuser': 0,
                })
            click.echo(f"""
            Usuario criado:
                username: {username}
                password: {password} (hash: {hash})
                name: {name if name else username}
                email: {email if email else username+'@email.com'}
            """)
        except:
            click.echo(f"""
            Usuario {username} já existe!
            """)

    @cmd.command(
        "create-user-random",
        help="Cria um usuários comuns aleatórios",
    )
    @click.argument("qdt", type=int)
    def random(qdt: int):
        with get_session(exec=True) as db:
            qdt_db = db.query(User).count()
            while qdt > 0:
                qdt_db += 1
                username = f"teste{qdt_db}"
                hash = Auth.get_password_hash('teste')
                try:
                    add_users(db, {
                        'username': username,
                        'password': hash,
                        'name': username,
                        'email': username+'@email.com'
                    })
                    click.echo(f"""
                    Usuario {qdt_db} criado:
                        username: {username}
                        password: teste (hash: {hash})
                        name: {username}
                        email: {username+'@email.com'}
                    """)
                except:
                    click.echo(f"""
                    Usuario {username} já existe!
                    """)
                qdt -= 1
            db.commit()
