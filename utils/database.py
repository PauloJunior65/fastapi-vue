from functools import lru_cache

from sqlmodel import Session, create_engine

from utils.config import get_settings

settings = get_settings()

if settings.DATABASE_DEBUG:
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@lru_cache()
def get_engines():
    return {name: create_engine(url) for name, url in settings.databases.items() if isinstance(url, str)}


def get_session(name: str = "default"):
    engine = get_engines().get(name)
    if engine is None:
        raise ValueError(f"Database {name} not found")
    with Session(engine) as session:
        try:
            session.begin()
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()