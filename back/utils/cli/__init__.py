from fastapi import FastAPI

help = """
Bem vindo ao sistema de comandos do projeto.
"""


def cli_app(app: FastAPI):
    import click
    from .translation import cmd_translation, help_translation
    from .users import cmd_users, help_users
    from .group_perms import cmd_group_perms, help_group_perms
    from .database import cmd_database, help_database

    @click.group("cmd",
                 help="\n--------------------------------------\n".join([
                     help, help_translation, help_users, help_group_perms, help_database
                 ]))
    def cmd():
        click.clear()

    @cmd.command("start", help="Iniciar servidor uvicorn")
    def start():
        import uvicorn
        uvicorn.run("main:app", host="127.0.0.1",
                    port=8001, workers=1, reload=True)
        # uvicorn.run(app, host="127.0.0.1", port=8001)

    @cmd.command("start-server", help="Iniciar servidor uvicorn com acesso externo")
    def start_server():
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8001)

    cmd_translation(cmd)
    cmd_users(cmd)
    cmd_group_perms(cmd)
    cmd_database(cmd)

    cmd()
