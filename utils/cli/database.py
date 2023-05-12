from slugify import slugify
from subprocess import run
import click


help_database = """
Modulo do Database:\n
    - migrations: é responsável pela criação de novas migrações com base nas alterações efectuadas nos seus modelos.
    - migrate: é responsável por aplicar e retirar a aplicação das migrações.
"""


def cmd_database(cmd: click.Group):
    @cmd.command(
        "migrations",
        help="é responsável pela criação de novas migrações com base nas alterações efectuadas nos seus modelos."
    )
    @click.argument("name", nargs=-1, type=str)
    def migrations(name: tuple):
        click.echo("Migrations:")
        name: str = slugify(" ".join(name), separator="_")
        if not name:
            name = "migration"
        try:
            run(["alembic", "revision", "--autogenerate", "-m", name])
            click.echo("Migrations created successfully.")
        except Exception as err:
            click.echo(err)

    @cmd.command(
        "migrate",
        help="é responsável por aplicar e retirar a aplicação das migrações."
    )
    def migrate():
        click.echo("Migrate:")
        try:
            run(["alembic", "upgrade", "head"])
            click.echo("Migrate successfully.")
        except Exception as err:
            click.echo(err)
