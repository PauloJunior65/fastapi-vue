from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from utils.babel import _,babel
from utils.middleware import add_middlewares
# from routers import add_routers


app = FastAPI()
babel.init_app(app)
add_middlewares(app)
app.mount("/static", StaticFiles(directory="static"), name="static")
# add_routers(app)