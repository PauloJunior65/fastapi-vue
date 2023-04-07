from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()


def _create_session_database(url: str):
    engine = create_engine(url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal, engine


_session_databases = {name: _create_session_database(
    url) for name, url in settings.databases.items() if url}


def get_session(name: str = "default"):
    return _session_databases.get(name, (None, None))[0]


def get_engine(name: str = "default"):
    return _session_databases.get(name, (None, None))[1]


def get_db():
    """Banco de dados padrão"""
    db = get_session("default")
    if db is None:
        raise ValueError("Database default not found")
    db = db()
    try:
        yield db
    finally:
        db.close()


class DBCustom:
    """Banco de dados customizado"""

    def __init__(self, db: str = "default", url: str = None):
        """Banco de dados customizado

        Args:
            db (str, optional): Nome da conexão. Defaults to "default".
            url (str, optional): Url de conexão. se não for informado, será usado o nome da conexão.
        """
        if url is not None:
            self.db = _create_session_database(url)[0]
        else:
            self.db = get_session(db)
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
