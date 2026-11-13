"""Agent Definition model - preserves agent registry for MVP and future agents."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AgentDefinitionModel(Base):
    """Agent definitions table - registry of AGN1 (active) and AGN2-AGN6 (deferred)."""

    __tablename__ = "agent_definitions"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[str] = mapped_column(String(16), unique=True, nullable=False, index=True)
    agent_name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(String(512), nullable=False)
    executable_in_mvp: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    responsible_steps: Mapped[str] = mapped_column(String(256), nullable=False)  # Comma-separated ATS IDs
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
