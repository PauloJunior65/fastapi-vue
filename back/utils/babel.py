from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi_babel.middleware import InternationalizationMiddleware
from fastapi_babel import _
from fastapi.templating import Jinja2Templates
from pathlib import Path
templates = Jinja2Templates(directory="templates")
configs = BabelConfigs(
    ROOT_DIR=Path(__file__).parent.parent,
    BABEL_DEFAULT_LOCALE="pt_br",
    BABEL_TRANSLATION_DIRECTORY="lang",
)
babel = Babel(configs=configs)

babel.install_jinja(templates)

if __name__ == "__main__":
    babel.run_cli()