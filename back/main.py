
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from utils.middleware import add_middlewares
from modules import add_routers
from utils.auth import add_auth
from fastapi.responses import JSONResponse
from fastapi_pagination import add_pagination

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
add_middlewares(app)
add_pagination(app)
add_auth(app)
add_routers(app)


@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code if hasattr(exc, 'status_code') else 500,
        content=exc.detail if hasattr(exc, 'detail') else {'detail': str(exc)},
        headers=exc.headers if hasattr(exc, 'headers') else None,
    )


@app.get('/', include_in_schema=False)
def index():
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    from utils.cli import cli_app
    cli_app(app)
