import pytest
import os
from pathlib import Path


def pytest_configure(config):
    env_test_path = Path(__file__).parent.parent / ".env.test"
    if env_test_path.exists():
        from dotenv import load_dotenv

        load_dotenv(env_test_path, override=True)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    from app.core.config import config

    if "sqlite" in config.database_url:
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        import app.adapters.postgres.database as db_module

        # Create engine with SQLite specific args
        test_engine = create_engine(
            config.database_url, connect_args={"check_same_thread": False}
        )
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=test_engine
        )

        # Patch the module
        db_module.engine = test_engine
        db_module.SessionLocal = TestingSessionLocal


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
