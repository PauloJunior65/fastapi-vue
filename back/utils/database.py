from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Default database"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class DBCustom:
    """Custom database"""
    def __init__(self):
        pass

    def __call__(self, db:str="default"):
        database = settings.database()
        if db not in database:
            raise ValueError(f"Database {db} not found")
        engine = create_engine(database.get(db))
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
