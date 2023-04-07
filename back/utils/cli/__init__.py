from fastapi import FastAPI

help = """
Bem vindo ao sistema de comandos do projeto.
"""


def cli_app(app: FastAPI):
    import click
    from .translation import cmd_translation, help_translation
    from .users import cmd_users, help_users

    @click.group("cmd",
                 help="\n--------------------------------------\n".join([
                     help, help_translation, help_users
                 ]))
    def cmd():
        pass

    @cmd.command("start", help="Iniciar servidor uvicorn")
    def start():
        import uvicorn
        uvicorn.run(app, host="127.0.0.1", port=8000)

    @cmd.command("start-server", help="Iniciar servidor uvicorn com acesso externo")
    def start_server():
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)

    cmd_translation(cmd)
    cmd_users(cmd)

    cmd()
