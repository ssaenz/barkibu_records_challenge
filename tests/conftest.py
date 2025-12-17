import pytest
import os
from pathlib import Path


def pytest_configure(config):
    env_test_path = Path(__file__).parent.parent / ".env.test"
    if env_test_path.exists():
        from dotenv import load_dotenv

        load_dotenv(env_test_path, override=True)


@pytest.fixture(autouse=True)
def reset_database():
    from app.adapters.postgres.database import engine, Base, SessionLocal

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session():
    from app.adapters.postgres.database import SessionLocal

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
