"""Integration tests for auth endpoints - login/logout flows."""

from app.core.security import hash_password
from app.models.user import UserModel


def test_login_flow_success(client, db_session):
    """Test complete login flow with valid credentials."""
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
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "testuser@example.com"
    assert data["user"]["role"] == "auditor"
    assert "expires_at" in data


def test_login_invalid_credentials(client, db_session):
    """Test login with invalid credentials returns 401."""
    # Create test user
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    # Attempt login with wrong password
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@example.com", "password": "Wrong-pass-1"},
    )

    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_login_inactive_user(client, db_session):
    """Test login with inactive user returns 401."""
    # Create inactive user
    user = UserModel(
        email="inactive@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()

    # Attempt login
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "inactive@example.com", "password": "Test-pass-1"},
    )

    assert response.status_code == 401
    assert "Account is inactive" in response.json()["detail"]


def test_logout_flow_success(client, db_session):
    """Test complete logout flow."""
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
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # Logout
    logout_response = client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert logout_response.status_code == 200
    assert logout_response.json()["message"] == "Logged out successfully"


def test_logout_without_token(client):
    """Test logout without token returns 401."""
    response = client.post("/api/v1/auth/logout")
    assert response.status_code == 401


def test_protected_endpoint_without_auth(client):
    """Test accessing protected endpoint without auth returns 401."""
    response = client.get("/api/v1/cases")
    assert response.status_code == 401


def test_protected_endpoint_with_auth(client, db_session):
    """Test accessing protected endpoint with valid token succeeds."""
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


def test_protected_endpoint_with_revoked_token(client, db_session):
    """Test accessing protected endpoint with revoked token returns 401."""
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
    client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Try to access protected endpoint with revoked token
    response = client.get(
        "/api/v1/cases",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
