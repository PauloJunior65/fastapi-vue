from fastapi_babel import Babel
from fastapi_babel import BabelConfigs
from fastapi.templating import Jinja2Templates
from pathlib import Path
from .config import get_settings
import os

settings = get_settings()

path = Path(__file__).parent
configs = BabelConfigs(
    ROOT_DIR=path,
    BABEL_DEFAULT_LOCALE=settings.DEFAULT_LANGUAGE,
    BABEL_TRANSLATION_DIRECTORY="lang",
)
configs.BABEL_CONFIG_FILE = os.path.join(path, 'babel.cfg')
configs.BABEL_MESSAGE_POT_FILE = os.path.join(path, 'messages.pot')
babel = Babel(configs=configs)

templates = Jinja2Templates(directory="templates")
babel.install_jinja(templates)

if __name__ == "__main__":
    babel.run_cli()
