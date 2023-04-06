from fastapi import FastAPI, Request
from utils.babel import babel
from utils.middleware import add_middlewares

app = FastAPI()
add_middlewares(app)

@app.get("/")
async def read_item(request: Request):
    return {
        'locale': request.headers.get('accept-language'),
    }

if __name__ == "__main__":
    babel.run_cli()