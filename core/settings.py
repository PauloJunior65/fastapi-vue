from functools import lru_cache
from typing import Set

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    SECRET_KEY: str = ""
    ALGORITHM: str = ""

    AUTH_MODE: str = "static"  # db, cache, static
    AUTH_CACHE_TIMEOUT_MINUTES: int = 5
    AUTH_TOKEN_EXPIRE_MINUTES: int = 30

    CACHE_URL: str = "redis://localhost:6379"
    CACHE_TIMEOUT: int = 300

    DATABASE_DEBUG: bool = False
    DATABASE_URL: str = "mysql+pymysql://root:root@mariadb/fastapi"
    DATABASE_URLS: dict = {}

    DEFAULT_LANGUAGE: str = "pt"
    SUPPORTED_LANGUAGE: Set[str] = set(['pt', 'en'])

    MODE_TEST: bool = False

    class Config:
        env_file = ".env"

    @property
    def languages(self):
        return list(set([self.DEFAULT_LANGUAGE]) | self.SUPPORTED_LANGUAGE)

    @property
    def databases(self):
        if self.MODE_TEST:
            return {
                'default':  "sqlite:///:memory:",
                **{k: "sqlite:///:memory:" for k in self.DATABASE_URLS.keys()}
            }
        return {
            'default':  self.DATABASE_URL,
            **self.DATABASE_URLS
        }


@lru_cache()
def get_settings():
    return Settings()
