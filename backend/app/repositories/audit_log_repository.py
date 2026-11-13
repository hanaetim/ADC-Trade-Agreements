"""Audit Log Repository - append-only audit trail (FR-023, FR-024)."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLogModel


class AuditLogRepository:
    """Repository for audit_logs table - append-only access pattern."""

    def __init__(self, session: Session):
        self.session = session

    def append(self, log_entry: AuditLogModel) -> AuditLogModel:
        """Append a new entry to the audit log.

        No UPDATE or DELETE operations allowed - append-only enforcement.
        """
        self.session.add(log_entry)
        self.session.flush()
        return log_entry

    def list_by_case(self, case_id: str | uuid.UUID, order_by_occurred: bool = True) -> list[AuditLogModel]:
        """Retrieve all audit logs for a case, ordered by occurred_at."""
        # Convert to UUID if string
        if isinstance(case_id, str):
            case_id = uuid.UUID(case_id)

        query = select(AuditLogModel).where(AuditLogModel.case_id == case_id)
        if order_by_occurred:
            query = query.order_by(AuditLogModel.occurred_at)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def list_by_correlation(self, correlation_id: str) -> list[AuditLogModel]:
        """Retrieve all audit logs for a correlation ID."""
        result = self.session.execute(
            select(AuditLogModel).where(AuditLogModel.correlation_id == correlation_id).order_by(AuditLogModel.occurred_at)
        )
        return list(result.scalars().all())
