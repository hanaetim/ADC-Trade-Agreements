"""Auth session repository - append-only session management."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.auth_session import AuthSessionModel


class SessionRepository:
    """Repository for auth_sessions table with append-only enforcement."""

    def __init__(self, db: Session):
        self.db = db

    def create_session(
        self,
        user_id: str,
        token_hash: str,
        issued_at: datetime,
        expires_at: datetime,
    ) -> AuthSessionModel:
        """Create a new session record."""
        session = AuthSessionModel(
            id=uuid.uuid4(),
            user_id=user_id,
            token_hash=token_hash,
            issued_at=issued_at,
            expires_at=expires_at,
            last_activity_at=issued_at,
            revoked_at=None,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        return session

    def get_session_by_token_hash(self, token_hash: str) -> AuthSessionModel | None:
        """Get session by token hash."""
        stmt = select(AuthSessionModel).where(AuthSessionModel.token_hash == token_hash)
        return self.db.execute(stmt).scalar_one_or_none()

    def revoke_session(self, token_hash: str) -> AuthSessionModel | None:
        """Revoke a session by setting revoked_at timestamp (soft delete)."""
        session = self.get_session_by_token_hash(token_hash)
        if session and session.revoked_at is None:
            session.revoked_at = datetime.now(timezone.utc)
            session.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(session)
            return session
        return None

    def update_last_activity(self, token_hash: str) -> AuthSessionModel | None:
        """Update last_activity_at for inactivity timeout enforcement."""
        session = self.get_session_by_token_hash(token_hash)
        if session and session.revoked_at is None:
            session.last_activity_at = datetime.now(timezone.utc)
            session.updated_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(session)
            return session
        return None
