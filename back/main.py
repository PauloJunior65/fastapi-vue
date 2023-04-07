from fastapi import FastAPI
from utils.middleware import add_middlewares
from modules import add_routers

app = FastAPI()
add_middlewares(app)
add_routers(app)

if __name__ == "__main__":
    from utils.comands import Comands
    Comands()
