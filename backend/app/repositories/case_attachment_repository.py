"""Case attachment repository for database operations (FR-001)."""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.case_attachment import CaseAttachmentModel


class CaseAttachmentRepository:
    """Repository for case attachment persistence operations."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, attachment: CaseAttachmentModel) -> CaseAttachmentModel:
        """Create a new case attachment record."""
        self.session.add(attachment)
        self.session.flush()
        self.session.refresh(attachment)
        return attachment

    def create_many(self, attachments: list[CaseAttachmentModel]) -> list[CaseAttachmentModel]:
        """Create multiple case attachment records."""
        self.session.add_all(attachments)
        self.session.flush()
        for attachment in attachments:
            self.session.refresh(attachment)
        return attachments

    def list_by_case(self, case_id: uuid.UUID) -> list[CaseAttachmentModel]:
        """List all attachments for a case."""
        stmt = select(CaseAttachmentModel).where(CaseAttachmentModel.case_id == case_id)
        result = self.session.execute(stmt)
        return list(result.scalars().all())
