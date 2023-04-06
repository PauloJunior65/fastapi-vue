from fastapi import FastAPI, Request,Depends
from utils.middleware import add_middlewares

app = FastAPI()
add_middlewares(app)

from sqlalchemy.orm import Session
from sqlalchemy import text
from utils import get_db,DBCustom,covert_to_dict,covert_to_dict_list

@app.get("/")
async def read_item(request: Request,db: Session = Depends(get_db)):
    a = db.execute(text('SELECT * FROM auth_user')).fetchall()
    return {
        'locale': request.headers.get('accept-language'),
        'db': covert_to_dict_list(a),
    }

if __name__ == "__main__":
    from utils.comands import Comands
    Comands()