"""Shared test fixtures for the backend test suite."""
import os
import tempfile
from pathlib import Path

# 1. Configuration BEFORE anything imports the app: the committed dev.env, then test overrides.
_BACKEND = Path(__file__).resolve().parents[1]
for _seed in ("dev.env", ".env.example"):
    if (_BACKEND / _seed).is_file():
        for _line in (_BACKEND / _seed).read_text().splitlines():
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _key, _value = _line.removeprefix("export ").split("=", 1)
                os.environ.setdefault(_key.strip(), _value.strip().strip("\"'"))
        break

_DB_FILE = Path(tempfile.mkdtemp()) / "test.db"
os.environ["DATABASE_URL"] = f"sqlite:///{_DB_FILE.as_posix()}"
os.environ["RATE_LIMIT_ENABLED"] = "false"
os.environ["TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import app.models  # noqa: F401 - registers every model on Base before create_all
from app.database import Base, get_db
from app.main import app as fastapi_app

engine = create_engine(os.environ["DATABASE_URL"], connect_args={"check_same_thread": False})
TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


@pytest.fixture(autouse=True)
def _fresh_schema():
    """Create fresh schema for each test."""
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session() -> Session:
    """Provide a database session for tests."""
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session):
    """Provide a test client with database session override."""
    fastapi_app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(fastapi_app) as test_client:
        yield test_client
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def auth_client(client, db_session):
    """Provide an authenticated test client logged in as intake handler."""
    from app.core.security import hash_password
    from app.models.user import UserModel

    # Create test user
    user = UserModel(
        email="tester@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="intake_exception_handler",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login through real auth endpoint
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "tester@example.com", "password": "Test-pass-1"},
    )
    assert response.status_code == 200, response.text
    token = response.json().get("access_token")

    if token:
        client.headers["Authorization"] = f"Bearer {token}"

    return client
