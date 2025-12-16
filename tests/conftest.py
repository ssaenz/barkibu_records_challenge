"""Pytest configuration and fixtures"""

import pytest
import os
from pathlib import Path


# Load test environment variables before any imports
def pytest_configure(config):
    """Load .env.test file before running tests"""
    env_test_path = Path(__file__).parent.parent / ".env.test"
    if env_test_path.exists():
        from dotenv import load_dotenv

        load_dotenv(env_test_path, override=True)


@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test"""
    from app.adapters.postgres.database import engine, Base, SessionLocal

    # Drop all tables
    Base.metadata.drop_all(bind=engine)
    # Recreate all tables
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def db_session():
    """Provide a database session for tests"""
    from app.adapters.postgres.database import SessionLocal

    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
