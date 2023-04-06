from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()
def _create_session_database(url:str):
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

_session_databases = {name: _create_session_database(url) for name,url in settings.databases.items() if url}

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
    def __init__(self,db:str="default"):
        self.db = _session_databases.get(db)
        if self.db is None:
            raise ValueError(f"Database {db} not found")

    def __call__(self):
        db = self.db()
        try:
            yield db
        finally:
            db.close()

def covert_to_dict(obj):
    """Convert object SQLAlchemy to dict"""
    if hasattr(obj, '_asdict'):
        return obj._asdict()
    return obj.__dict__

def covert_to_dict_list(obj):
    """Convert list object SQLAlchemy to list dict"""
    return list(map(covert_to_dict, obj))