from fastapi import FastAPI, Request,Depends
from utils.middleware import add_middlewares

app = FastAPI()
add_middlewares(app)

from utils import *

@app.get("/")
async def read_item(request: Request,cache:Cache = Depends(get_cache),cache2:Cache = Depends(CacheCustom(db=2))):
    a = cache.get_or_set('b:b2',{'a':1})
    a = cache2.get_or_set('a:b2',{'a':1})
    return {
        'locale': request.headers.get('accept-language'),
        'db': a,
    }

if __name__ == "__main__":
    from utils.comands import Comands
    Comands()