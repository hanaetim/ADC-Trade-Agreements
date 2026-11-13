"""Audit Service - immutable event and audit log capture (FR-023, FR-024, REQ-DOMAIN-005)."""
import uuid
from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLogModel
from app.models.case_event import CaseEventModel
from app.repositories.audit_log_repository import AuditLogRepository
from app.repositories.case_event_repository import CaseEventRepository


class AuditService:
    """Service for recording immutable operational and compliance events (FR-023, FR-024)."""

    def __init__(self, session: Session):
        self.session = session
        self.case_event_repo = CaseEventRepository(session)
        self.audit_log_repo = AuditLogRepository(session)

    def record_case_event(
        self,
        case_id: uuid.UUID,
        event_type: str,
        step_id: str,
        decision_source: str,
        actor_type: str,
        actor_id: str,
        correlation_id: str,
        visible_to_external: bool = False,
        reason_code: str | None = None,
        rationale_summary: str | None = None,
        evidence_ref: str | None = None,
        payload: dict[str, Any] | None = None,
    ) -> uuid.UUID:
        """Record a case event (append-only, immutable).

        Returns the event ID for tracing.
        """
        event = CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type=event_type,
            step_id=step_id,
            decision_source=decision_source,
            actor_type=actor_type,
            actor_id=actor_id,
            visible_to_external=visible_to_external,
            reason_code=reason_code,
            rationale_summary=rationale_summary,
            evidence_ref=evidence_ref,
            correlation_id=correlation_id,
            payload_json=payload or {},
            occurred_at=datetime.now(timezone.utc),
        )
        self.case_event_repo.append(event)
        return event.id

    def record_security_audit(
        self,
        event_category: str,
        severity: str,
        actor_id: str,
        action: str,
        correlation_id: str,
        entity_type: str,
        entity_id: str,
        details: dict[str, Any],
        case_id: uuid.UUID | None = None,
    ) -> uuid.UUID:
        """Record a security/operational audit entry (append-only, immutable)."""
        audit_entry = AuditLogModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_category=event_category,
            severity=severity,
            actor_id=actor_id,
            action=action,
            correlation_id=correlation_id,
            entity_type=entity_type,
            entity_id=entity_id,
            details_json=details,
            occurred_at=datetime.now(timezone.utc),
        )
        self.audit_log_repo.append(audit_entry)
        return audit_entry.id
