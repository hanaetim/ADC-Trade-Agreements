"""Authentication service with login, logout, token validation, and session management."""
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_token,
    verify_password,
)
from app.models.user import UserModel
from app.repositories.auth_repository import SessionRepository
from app.schemas.auth import AuthUser, TokenResponse


class AuthService:
    """Authentication service for login, logout, and token validation."""

    def __init__(self, db: Session):
        self.db = db
        self.session_repo = SessionRepository(db)

    def login(self, email: str, password: str) -> TokenResponse:
        """
        Authenticate user and create session.

        Args:
            email: User email
            password: Plain text password

        Returns:
            TokenResponse with access_token and user info

        Raises:
            ValueError: If credentials are invalid or user is inactive
        """
        # Find user by email
        stmt = select(UserModel).where(UserModel.email == email)
        user = self.db.execute(stmt).scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise ValueError("Invalid email or password")

        if not user.is_active:
            raise ValueError("Account is inactive")

        # Create JWT token with exp claim
        access_token, expires_at = create_access_token(user_id=str(user.id), role=user.role)

        # Store SHA-256 hash of token in auth_sessions
        token_hash = hash_token(access_token)
        issued_at = datetime.now(timezone.utc)

        self.session_repo.create_session(
            user_id=str(user.id),
            token_hash=token_hash,
            issued_at=issued_at,
            expires_at=expires_at,
        )

        # Return token and user info
        auth_user = AuthUser(
            user_id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=auth_user,
            expires_at=expires_at,
        )

    def logout(self, token: str) -> bool:
        """
        Revoke session by setting revoked_at timestamp.

        Args:
            token: JWT token to revoke

        Returns:
            True if session was revoked, False if session not found or already revoked
        """
        token_hash = hash_token(token)
        revoked_session = self.session_repo.revoke_session(token_hash)
        return revoked_session is not None

    def validate_token(self, token: str) -> AuthUser:
        """
        Validate JWT token and check session status.

        Args:
            token: JWT token to validate

        Returns:
            AuthUser with user info

        Raises:
            ValueError: If token is invalid, expired, or session is revoked
        """
        # Verify JWT signature and expiry
        try:
            payload = decode_access_token(token)
        except ValueError as e:
            raise ValueError(f"Token validation failed: {e}")

        # Check session not revoked
        token_hash = hash_token(token)
        session = self.session_repo.get_session_by_token_hash(token_hash)

        if not session:
            raise ValueError("Session not found")

        if session.revoked_at is not None:
            raise ValueError("Session has been revoked")

        # Check session expiry (defensive check, JWT exp should already be validated)
        # Ensure timezone-aware comparison (SQLite may return naive datetimes)
        expires_at = session.expires_at.replace(tzinfo=timezone.utc) if session.expires_at.tzinfo is None else session.expires_at
        if expires_at < datetime.now(timezone.utc):
            raise ValueError("Session has expired")

        # Update last_activity_at for inactivity timeout enforcement
        self.session_repo.update_last_activity(token_hash)

        # Get user from database (convert string UUID from JWT to UUID)
        import uuid as uuid_module
        user_id = uuid_module.UUID(payload["sub"]) if isinstance(payload["sub"], str) else payload["sub"]
        stmt = select(UserModel).where(UserModel.id == user_id)
        user = self.db.execute(stmt).scalar_one_or_none()

        if not user:
            raise ValueError("User not found")

        if not user.is_active:
            raise ValueError("User is inactive")

        return AuthUser(
            user_id=user.id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
        )
