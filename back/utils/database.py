from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()
def _create_session_database(url:str):
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

_session_databases = {name: _create_session_database(url) for name,url in settings.databases.items()}

def get_db():
    """Default database"""
    db = _session_databases.get("default")
    if db is None:
        raise ValueError("Database default not found")
    db = db()
    try:
        yield db
    finally:
        db.close()

class DBCustom:
    """Custom database"""
    def __init__(self):
        pass

    def __call__(self, db:str="default"):
        db = _session_databases.get(db)
        if db is None:
            raise ValueError(f"Database {db} not found")
        db = db()
        try:
            yield db
        finally:
            db.close()
