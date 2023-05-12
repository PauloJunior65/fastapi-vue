from fastapi_babel import BabelCli
from typing import Optional
from utils.babel import babel
import click
babel_cli = BabelCli(babel)

help_translation = """
Modulo de tradução de mensagens.

Primeiro passo para extrair mensagens:\n

    1- extract -d/--dir {watch_dir}\n
    2- init -l/--lang {lang}\n
    3- add Adicione sua tradução personalizada ao arquivo .po da sua linguagem, por exemplo, no diretório FA {./lang/fa}. \n
    4- compile.\n

    Example: \n
        1- extract -d .\n
        2- init -l fa\n
        3- go to ./lang/Fa/.po and add your translations.\n
        4- compile\n

Se você já extraiu as mensagens e possui um arquivo .po e .mo existente, siga estes passos:\n
    1- extract -d/--dir {watch_dir} \n
    2- update -d/--dir {lang_dir} defaults is ./lang \n
    3- add your custome to your lang `.po` file for example FA dir {./lang/fa}. \n
    4- compile.

    Example: \n
        1- extract -d .\n
        2- update -d lang\n
        3- go to ./lang/Fa/.po and add your translations.\n
        4- compile\n
"""


def cmd_translation(cmd: click.Group):
    @cmd.command(
        "extract",
        help="""Extraia todas as mensagens que foram anotadas usando gettext/_ no diretório especificado.
        Na primeira vez, será criado um arquivo messages.pot na raiz do diretório.""",
    )
    @click.option("-d", "--dir", "dir", help="Observar diretório.")
    def extract(dir):
        try:
            babel_cli.extract(dir)
        except Exception as err:
            click.echo(err)

    @cmd.command(
        "init",
        help="""Se o diretório já existir, observe que todas as mensagens compiladas e inicializadas serão removidas. Nesse caso, é melhor usar o comando update.""",
    )
    @click.option(
        "-l",
        "--lang",
        "lang",
        help="Nome e caminho do diretório de localização, o padrão é 'en'.",
        default="en",
    )
    def init(lang: Optional[str] = None):
        try:
            babel_cli.init(lang)
        except Exception as err:
            click.echo(err)

    @cmd.command(
        "compile",
        help="""Compile todas as mensagens do diretório de tradução no arquivo .PO para o arquivo .MO, que é um arquivo de texto binário.""",
    )
    def compile():
        try:
            babel_cli.compile()
        except Exception as err:
            click. echo(err)

    @cmd.command(
        "update",
        help="""Atualize as mensagens extraídas após o comando `init` ou diretório inicializado. O padrão é `./lang`.""",
    )
    @click.option("-d", "--dir", "dir", help="Nome e caminho do diretório de localização.", default="./lang")
    def update(dir: Optional[str] = None):
        try:
            babel_cli.update(dir)
        except Exception as err:
            click.echo(err)
