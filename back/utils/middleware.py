from fastapi import FastAPI,Request,Response
from fastapi_babel.middleware import InternationalizationMiddleware
from .babel import babel
from typing import Optional
from datetime import timedelta
from .config import get_settings
import time

settings = get_settings()

class I18nMiddleware(InternationalizationMiddleware):
    """
    Middleware para internacionalização
    """
    async def dispatch(self, request: Request, call_next):
        lang_code: Optional[str] = request.headers.get("Accept-Language", settings.DEFAULT_LANGUAGE)
        lang_code = lang_code.split(',')[0].replace('-','_')
        self.babel.locale = settings.DEFAULT_LANGUAGE if lang_code not in settings.languages else lang_code
        response:Response = await call_next(request)
        return response

def add_middlewares(app:FastAPI):
    app.add_middleware(I18nMiddleware,babel=babel)
    
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