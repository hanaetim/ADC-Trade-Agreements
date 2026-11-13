"""Case ORM model - canonical formal case record."""
import uuid
from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, String, Uuid, text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CaseModel(Base):
    """Cases table - canonical formal case record (FR-001, FR-002, FR-004)."""

    __tablename__ = "cases"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    case_reference: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    workflow_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    submission_channel: Mapped[str] = mapped_column(String(32), nullable=False)
    applicant_reference: Mapped[str] = mapped_column(String(128), nullable=False)
    applicant_name: Mapped[str] = mapped_column(String(256), nullable=False)
    goods_description: Mapped[str | None] = mapped_column(String, nullable=True)
    origin_country_code: Mapped[str | None] = mapped_column(String(8), nullable=True)
    agreement_reference: Mapped[str | None] = mapped_column(String(64), nullable=True)
    case_state: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    current_step_id: Mapped[str] = mapped_column(String(16), nullable=False)
    accountable_role: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    registration_sync_status: Mapped[str] = mapped_column(String(16), nullable=False)
    reason_codes_json: Mapped[dict] = mapped_column(
        JSON().with_variant(JSONB(), "postgresql"), nullable=False, server_default=text("'[]'")
    )
    submitted_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
