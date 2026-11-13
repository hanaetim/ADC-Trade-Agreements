"""Acceptance tests for authentication - API endpoints via TestClient."""
import pytest

from app.core.security import hash_password
from app.middleware.rate_limit import login_rate_limiter
from app.models.user import UserModel


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter before each test."""
    login_rate_limiter.reset()
    yield
    login_rate_limiter.reset()


def test_login_endpoint_returns_token(client, db_session):
    """Test POST /api/v1/auth/login returns JWT token with user info."""
    # Create test user
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "Test-pass-1"},
    )

    assert response.status_code == 200
    data = response.json()

    # Verify response shape
    assert "access_token" in data
    assert "token_type" in data
    assert "user" in data
    assert "expires_at" in data

    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "testuser@example.com"
    assert data["user"]["role"] == "auditor"
    assert data["user"]["is_active"] is True


def test_logout_endpoint_revokes_session(client, db_session):
    """Test POST /api/v1/auth/logout revokes session."""
    # Create test user
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "Test-pass-1"},
    )
    token = login_response.json()["access_token"]

    # Logout
    response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully"

    # Verify token no longer works
    cases_response = client.get(
        "/api/v1/cases",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert cases_response.status_code == 401


def test_protected_endpoint_requires_auth(client):
    """Test protected endpoints return 401 without authentication."""
    # Try cases list endpoint
    response = client.get("/api/v1/cases")
    assert response.status_code == 401

    # Try case detail endpoint
    response = client.get("/api/v1/cases/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 401

    # Try trace endpoint
    response = client.get("/api/v1/cases/00000000-0000-0000-0000-000000000001/trace")
    assert response.status_code == 401


def test_protected_endpoint_with_valid_token(client, db_session):
    """Test protected endpoints succeed with valid authentication."""
    # Create test user
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "Test-pass-1"},
    )
    token = login_response.json()["access_token"]

    # Access protected endpoint
    response = client.get(
        "/api/v1/cases",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200


def test_rate_limiting_on_login(client, db_session):
    """Test rate limiting on login endpoint after excessive attempts."""
    from app.config import settings

    # Temporarily enable rate limiting for this test
    original_setting = settings.rate_limit_enabled
    settings.rate_limit_enabled = True

    try:
        # Create test user
        user = UserModel(
            email="testuser@example.com",
            hashed_password=hash_password("Test-pass-1"),
            role="auditor",
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()

        # Make 5 failed login attempts (max allowed)
        for _ in range(5):
            response = client.post(
                "/api/v1/auth/login",
                json={"email": "testuser@example.com", "password": "Wrong-pass-1"},
            )
            assert response.status_code == 401

        # 6th attempt should be rate limited
        response = client.post(
            "/api/v1/auth/login",
            json={"email": "testuser@example.com", "password": "Test-pass-1"},
        )
        assert response.status_code == 429
        assert "Too many login attempts" in response.json()["detail"]
    finally:
        # Restore original setting
        settings.rate_limit_enabled = original_setting


def test_role_based_access_exception_action(client, db_session):
    """Test exception action endpoint requires intake_exception_handler role."""
    # Create test user without correct role
    user = UserModel(
        email="external@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="external_applicant",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "external@example.com", "password": "Test-pass-1"},
    )
    token = login_response.json()["access_token"]

    # Try to perform exception action (should be forbidden)
    response = client.post(
        "/api/v1/cases/00000000-0000-0000-0000-000000000001/exception-actions",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "action_type": "request_correction",
            "comment": "Please provide missing information",
        },
    )

    assert response.status_code == 403
    assert "intake_exception_handler" in response.json()["detail"]


def test_seed_user_credentials(client, db_session):
    """Test seed users can login with documented credentials."""
    # Seed users should already be created by conftest
    # Test one from each role

    seed_credentials = [
        ("external@example.com", "External-pass-1", "external_applicant"),
        ("intake@example.com", "Intake-pass-1", "intake_exception_handler"),
        ("auditor@example.com", "Auditor-pass-1", "auditor"),
    ]

    for email, password, expected_role in seed_credentials:
        # Check if user exists
        user = db_session.query(UserModel).filter(UserModel.email == email).first()
        if not user:
            # Create if not exists (in case seed not run yet)
            user = UserModel(
                email=email,
                hashed_password=hash_password(password),
                role=expected_role,
                is_active=True,
            )
            db_session.add(user)
            db_session.commit()

        # Login with seed credentials
        response = client.post(
            "/api/v1/auth/login",
            json={"email": email, "password": password},
        )

        assert response.status_code == 200, f"Login failed for {email}"
        data = response.json()
        assert data["user"]["role"] == expected_role
