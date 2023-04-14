
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.middleware import add_middlewares
from modules import add_routers

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
add_middlewares(app)
add_routers(app)


@app.get('/', include_in_schema=False)
def index():
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    from utils.cli import cli_app
    cli_app(app)
