"""Case Event Repository - append-only event stream (FR-023, FR-024)."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_event import CaseEventModel


class CaseEventRepository:
    """Repository for case_events table - append-only access pattern."""

    def __init__(self, session: Session):
        self.session = session

    def append(self, event: CaseEventModel) -> CaseEventModel:
        """Append a new event to the case event stream.

        No UPDATE or DELETE operations allowed - append-only enforcement.
        """
        self.session.add(event)
        self.session.flush()
        return event

    def list_by_case(self, case_id: str | uuid.UUID, order_by_occurred: bool = True) -> list[CaseEventModel]:
        """Retrieve all events for a case, ordered by occurred_at."""
        # Convert to UUID if string
        if isinstance(case_id, str):
            case_id = uuid.UUID(case_id)

        query = select(CaseEventModel).where(CaseEventModel.case_id == case_id)
        if order_by_occurred:
            query = query.order_by(CaseEventModel.occurred_at)
        result = self.session.execute(query)
        return list(result.scalars().all())

    def get_by_id(self, event_id: str | uuid.UUID) -> CaseEventModel | None:
        """Retrieve a single event by ID."""
        # Convert to UUID if string
        if isinstance(event_id, str):
            event_id = uuid.UUID(event_id)

        result = self.session.execute(
            select(CaseEventModel).where(CaseEventModel.id == event_id)
        )
        return result.scalar_one_or_none()
