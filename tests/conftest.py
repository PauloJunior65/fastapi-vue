import pytest
from fastapi.testclient import TestClient
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import Session

from core.databases import get_engines
from core.settings import get_settings
from main import app
from models import SQLModel

settings = get_settings()


def create_all_tables(engines: dict):
    for database, engine in engines.items():
        if database == 'default':
            SQLModel.metadata.create_all(engine)
        else:
            engine_default = create_engine(settings.DATABASE_URLS.get(database, "sqlite:///:memory:"))
            metadata = MetaData()
            metadata.reflect(engine_default)
            metadata.create_all(engine)
    return engines

@pytest.fixture()
def client():
    create_all_tables(get_engines())
    return TestClient(app)


@pytest.fixture()
def session():
    engines = create_all_tables({name: create_engine(url) for name, url in settings.databases.items() if isinstance(url, str)})

    def get_database(name: str = "default"):
        engine = engines.get(name)
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

    return get_database
