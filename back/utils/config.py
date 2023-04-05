from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    SECRET_KEY:str=""
    ALGORITHM:str=""
    ACCESS_TOKEN_EXPIRE_MINUTES:int=0
    
    REDIS_HOST:str = "127.0.0.1"
    REDIS_PORT:int = 6379
    REDIS_PASSWORD:str = ""
    REDIS_DB:int = 1
    REDIS_TIMEOUT:int = 300
    
    DATABASE_URL:str = ""

    class Config:
        env_file = ".env"

    def redis(self):
        return {
            'host': self.REDIS_HOST,
            'port': self.REDIS_PORT,
            'password': self.REDIS_PASSWORD,
            'db': self.REDIS_DB
        }
    
    def database(self, db:str="default"):
        return {
            'default': self.DATABASE_URL,
        }

@lru_cache()
def get_settings():
    return Settings()
