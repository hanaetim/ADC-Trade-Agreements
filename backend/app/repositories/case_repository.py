"""Case repository for database operations (FR-001)."""
import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case import CaseModel


class CaseRepository:
    """Repository for case persistence operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, case: CaseModel) -> CaseModel:
        """Create a new case record."""
        self.session.add(case)
        self.session.flush()
        self.session.refresh(case)
        return case

    def get_by_id(self, case_id: uuid.UUID) -> Optional[CaseModel]:
        """Retrieve a case by ID."""
        return self.session.get(CaseModel, case_id)

    def get_by_reference(self, case_reference: str) -> Optional[CaseModel]:
        """Retrieve a case by case_reference."""
        stmt = select(CaseModel).where(CaseModel.case_reference == case_reference)
        result = self.session.execute(stmt)
        return result.scalar_one_or_none()

    def list_cases(
        self,
        limit: int = 20,
        offset: int = 0,
        workflow_type: Optional[str] = None,
        case_state: Optional[str] = None,
        assigned_role: Optional[str] = None,
    ) -> tuple[list[CaseModel], int]:
        """List cases with optional filters and pagination."""
        stmt = select(CaseModel)

        if workflow_type:
            stmt = stmt.where(CaseModel.workflow_type == workflow_type)
        if case_state:
            stmt = stmt.where(CaseModel.case_state == case_state)
        if assigned_role:
            stmt = stmt.where(CaseModel.accountable_role == assigned_role)

        # Count total
        count_stmt = stmt.with_only_columns(CaseModel.id)
        total = len(self.session.execute(count_stmt).all())

        # Apply pagination
        stmt = stmt.order_by(CaseModel.created_at.desc()).limit(limit).offset(offset)

        result = self.session.execute(stmt)
        cases = result.scalars().all()

        return list(cases), total

    def update_status(self, case_id: uuid.UUID, case_state: str, current_step_id: str, accountable_role: str) -> Optional[CaseModel]:
        """Update case status and routing fields."""
        case = self.get_by_id(case_id)
        if case:
            case.case_state = case_state
            case.current_step_id = current_step_id
            case.accountable_role = accountable_role
            self.session.flush()
            self.session.refresh(case)
        return case
