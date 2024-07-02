from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routes import routers

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})
app.include_router(routers)

@app.get('/')
def read_root():
    return RedirectResponse(url='/docs')

@app.get('/status')
def read_status():
    return {'status': 'ok'}
