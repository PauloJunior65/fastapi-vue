from fastapi import FastAPI, Request
# from fastapi.staticfiles import StaticFiles
from utils.babel import _,babel
from utils.middleware import add_middlewares
# from routers import add_routers
# add_middlewares(app)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# add_routers(app)

app = FastAPI()
add_middlewares(app)
# babel.init_app(app)

@app.get("/")
async def read_item(request: Request):
    return {
        'locale': request.headers.get('accept-language'),
        'test': _('Hello World'),
    }
    # return _("Hello World")

