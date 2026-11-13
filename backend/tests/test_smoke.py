"""Smoke tests for basic application functionality."""
import uuid
from datetime import datetime, timezone

from app.core.security import hash_password
from app.models.user import UserModel


def test_health_endpoint(client):
    """Test health check endpoint returns 200."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["ok", "degraded"]
    assert "database" in data


def test_root_endpoint(client):
    """Test root endpoint returns welcome message."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data


def test_database_connection(db_session):
    """Test database session can create and query a user."""
    user = UserModel(
        id=uuid.uuid4(),
        email="smoke_test@example.com",
        hashed_password=hash_password("SmokeTest123!"),
        role="auditor",
        is_active=True,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    db_session.add(user)
    db_session.commit()

    # Query the user back
    queried_user = db_session.query(UserModel).filter(UserModel.email == "smoke_test@example.com").first()
    assert queried_user is not None
    assert queried_user.email == "smoke_test@example.com"
    assert queried_user.role == "auditor"


def test_password_hashing(db_session):
    """Test password hashing and verification."""
    from app.core.security import verify_password

    plain_password = "TestPassword123!"
    hashed = hash_password(plain_password)

    # Verify correct password
    assert verify_password(plain_password, hashed) is True

    # Verify incorrect password
    assert verify_password("WrongPassword", hashed) is False


def test_jwt_token_creation():
    """Test JWT token creation and decoding."""
    from app.core.security import create_access_token, decode_access_token

    user_id = str(uuid.uuid4())
    role = "external_applicant"

    token, expires_at = create_access_token(user_id, role)

    # Decode and verify
    payload = decode_access_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert "exp" in payload
    assert "iat" in payload


def test_seed_data_creates_users(db_session):
    """Test that seed function creates expected users."""
    from app.seed import seed_users

    # Run seed
    seed_users(db_session)

    # Verify all roles are seeded
    expected_roles = [
        "external_applicant",
        "intake_exception_handler",
        "specialist_reviewer",
        "section_head",
        "policy_legal_approver",
        "technical_committee",
        "auditor",
    ]

    for role in expected_roles:
        user = db_session.query(UserModel).filter(UserModel.role == role).first()
        assert user is not None, f"User with role {role} was not seeded"
        assert user.is_active is True
