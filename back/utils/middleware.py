from fastapi import FastAPI,Request
from .babel import InternationalizationMiddleware,babel
from datetime import timedelta
from .config import get_settings
import time

settings = get_settings()

class Middleware:
    """
    Middleware to set the language of the request
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        assert scope["type"] == "http"
        headers = dict(scope["headers"])
        lang = str(headers.get(b'accept-language',b''), 'UTF-8').split(',')[0].lower().replace('-','_')
        lang = settings.DEFAULT_LANGUAGE if lang not in settings.languages else lang
        print('LANG:',lang)
        headers[b'accept-language'] = bytes(lang,'UTF-8')
        scope["headers"] = [(k, v) for k, v in headers.items()]
        await self.app(scope, receive, send)

def add_middlewares(app:FastAPI):
    app.add_middleware(Middleware)
    app.add_middleware(InternationalizationMiddleware, babel=babel)
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        """Middleware to add process time to response header

        Args:
            request (Request): _description_
            call_next (_type_): _description_

        Returns:
            _type_: _description_
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Process-Time-Format"] = str(timedelta(seconds=process_time))
        # logger.debug("/api/log_now starts")
        # logger.info("I'm logging")
        # logger.warning("some warnings")
        return response