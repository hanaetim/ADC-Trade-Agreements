"""Unit tests for AuthService - password hashing, token issuance, session revocation."""
import pytest
from sqlalchemy import select

from app.core.security import hash_password, hash_token
from app.models.auth_session import AuthSessionModel
from app.models.user import UserModel
from app.services.auth_service import AuthService


def test_login_success(db_session):
    """Test successful login with valid credentials."""
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
    auth_service = AuthService(db_session)
    response = auth_service.login(email="testuser@example.com", password="Test-pass-1")

    # Verify response
    assert response.access_token is not None
    assert response.token_type == "bearer"
    assert response.user.email == "testuser@example.com"
    assert response.user.role == "auditor"
    assert response.expires_at is not None

    # Verify session created
    token_hash = hash_token(response.access_token)
    stmt = select(AuthSessionModel).where(AuthSessionModel.token_hash == token_hash)
    session = db_session.execute(stmt).scalar_one_or_none()
    assert session is not None
    assert session.user_id == str(user.id)
    assert session.revoked_at is None


def test_login_invalid_email(db_session):
    """Test login with non-existent email."""
    auth_service = AuthService(db_session)

    with pytest.raises(ValueError, match="Invalid email or password"):
        auth_service.login(email="nonexistent@example.com", password="Test-pass-1")


def test_login_invalid_password(db_session):
    """Test login with incorrect password."""
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
    auth_service = AuthService(db_session)

    with pytest.raises(ValueError, match="Invalid email or password"):
        auth_service.login(email="testuser@example.com", password="Wrong-pass-1")


def test_login_inactive_user(db_session):
    """Test login with inactive user account."""
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
    auth_service = AuthService(db_session)

    with pytest.raises(ValueError, match="Account is inactive"):
        auth_service.login(email="inactive@example.com", password="Test-pass-1")


def test_logout_success(db_session):
    """Test successful logout revokes session."""
    # Create test user and login
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    auth_service = AuthService(db_session)
    response = auth_service.login(email="testuser@example.com", password="Test-pass-1")
    token = response.access_token

    # Logout
    revoked = auth_service.logout(token)
    assert revoked is True

    # Verify session revoked
    token_hash = hash_token(token)
    stmt = select(AuthSessionModel).where(AuthSessionModel.token_hash == token_hash)
    session = db_session.execute(stmt).scalar_one_or_none()
    assert session is not None
    assert session.revoked_at is not None


def test_logout_already_revoked(db_session):
    """Test logout on already revoked session returns False."""
    # Create test user and login
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    auth_service = AuthService(db_session)
    response = auth_service.login(email="testuser@example.com", password="Test-pass-1")
    token = response.access_token

    # First logout
    auth_service.logout(token)

    # Second logout attempt
    revoked = auth_service.logout(token)
    assert revoked is False


def test_validate_token_success(db_session):
    """Test token validation with valid token."""
    # Create test user and login
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    auth_service = AuthService(db_session)
    response = auth_service.login(email="testuser@example.com", password="Test-pass-1")

    # Validate token
    auth_user = auth_service.validate_token(response.access_token)
    assert auth_user.email == "testuser@example.com"
    assert auth_user.role == "auditor"
    assert auth_user.is_active is True


def test_validate_token_revoked_session(db_session):
    """Test token validation fails for revoked session."""
    # Create test user and login
    user = UserModel(
        email="testuser@example.com",
        hashed_password=hash_password("Test-pass-1"),
        role="auditor",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()

    auth_service = AuthService(db_session)
    response = auth_service.login(email="testuser@example.com", password="Test-pass-1")
    token = response.access_token

    # Revoke session
    auth_service.logout(token)

    # Validate token should fail
    with pytest.raises(ValueError, match="Session has been revoked"):
        auth_service.validate_token(token)


def test_validate_token_invalid(db_session):
    """Test token validation with invalid token."""
    auth_service = AuthService(db_session)

    with pytest.raises(ValueError, match="Token validation failed"):
        auth_service.validate_token("invalid.token.here")
