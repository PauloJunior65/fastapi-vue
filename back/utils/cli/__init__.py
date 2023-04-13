from fastapi import FastAPI

help = """
Bem vindo ao sistema de comandos do projeto.
"""


def cli_app(app: FastAPI):
    import click
    from .translation import cmd_translation, help_translation
    from .users import cmd_users, help_users
    from .group_perms import cmd_group_perms, help_group_perms

    @click.group("cmd",
                 help="\n--------------------------------------\n".join([
                     help, help_translation, help_users, help_group_perms
                 ]))
    def cmd():
        click.clear()

    @cmd.command("start", help="Iniciar servidor uvicorn")
    def start():
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)

    @cmd.command("start-server", help="Iniciar servidor uvicorn com acesso externo")
    def start_server():
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)

    cmd_translation(cmd)
    cmd_users(cmd)
    cmd_group_perms(cmd)

    cmd()
