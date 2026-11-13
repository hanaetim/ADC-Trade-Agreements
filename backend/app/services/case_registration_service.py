"""Case registration service coordinating intake flow (FR-001)."""
import uuid
from datetime import datetime, timezone
from typing import Any, Optional, cast

from sqlalchemy.orm import Session

from app.adapters.icos_registration import IcosRegistrationAdapter
from app.models.case import CaseModel
from app.models.case_attachment import CaseAttachmentModel
from app.repositories.case_attachment_repository import CaseAttachmentRepository
from app.repositories.case_repository import CaseRepository
from app.schemas.case import CreateCaseRequest
from app.services.agn1_orchestrator import Agn1Orchestrator
from app.services.routing_service import RoutingService


class CaseRegistrationService:
    """Service coordinating case registration flow (FR-001)."""

    def __init__(
        self,
        session: Session,
        icos_adapter: Optional[IcosRegistrationAdapter] = None,
        routing_service: Optional[RoutingService] = None,
        agn1_orchestrator: Optional[Agn1Orchestrator] = None,
    ):
        self.session = session
        self.case_repo = CaseRepository(session)
        self.attachment_repo = CaseAttachmentRepository(session)
        self.icos_adapter = icos_adapter or IcosRegistrationAdapter()
        self.routing_service = routing_service or RoutingService()
        self.agn1_orchestrator = agn1_orchestrator or Agn1Orchestrator(session)

    def generate_case_reference(self) -> str:
        """Generate unique case reference in format IAO-YYYY-NNNNNN."""
        from sqlalchemy import func

        year = datetime.now(timezone.utc).year

        # Count existing cases for current year to generate sequential number
        year_prefix = f"IAO-{year}-%"
        count = self.session.query(func.count(CaseModel.id)).filter(
            CaseModel.case_reference.like(year_prefix)
        ).scalar() or 0

        # Generate next sequential number (6 digits, zero-padded)
        next_number = count + 1
        return f"IAO-{year}-{next_number:06d}"

    def register_case(self, command: CreateCaseRequest, correlation_id: str) -> dict[str, Any]:
        """Register a new case with intake validation and routing.

        Steps (FR-001, FR-002, FR-004):
        1. Create provisional case record with generated case_reference
        2. Invoke ICOS registration adapter for sync
        3. Invoke AGN1 orchestrator for ATS1-ATS3 intake workflow
        4. Update case state based on AGN1 outcome
        5. Persist attachments
        6. Return response DTO
        """
        # Generate unique case reference
        case_reference = self.generate_case_reference()

        # Classify workflow type (initial seed)
        classification = self.routing_service.classify_workflow(
            {"submission_type": command.submission_type.value}
        )

        # Create provisional case record
        case = CaseModel(
            id=uuid.uuid4(),
            case_reference=case_reference,
            workflow_type=classification.workflow_type.value,
            submission_channel=command.submission_channel,
            applicant_reference=command.applicant_reference,
            applicant_name=command.applicant_name,
            goods_description=command.goods_description,
            origin_country_code=command.origin_country_code,
            agreement_reference=command.agreement_reference,
            case_state="submitted",
            current_step_id="ATS1",
            accountable_role="intake_exception_handler",
            registration_sync_status="pending",
            reason_codes_json=[],
            submitted_at=datetime.now(timezone.utc),
        )

        case = self.case_repo.create(case)

        # Invoke ICOS registration adapter
        icos_result = self.icos_adapter.register_case(
            {
                "case_id": str(case.id),
                "case_reference": case.case_reference,
                "workflow_type": case.workflow_type,
                "applicant_name": case.applicant_name,
            },
            correlation_id=correlation_id,
        )

        # Update sync status
        case.registration_sync_status = icos_result.status
        self.session.flush()

        # Invoke AGN1 orchestrator for ATS1-ATS3 intake workflow
        intake_payload = {
            "submission_type": command.submission_type.value,
            "submission_channel": command.submission_channel,
            "applicant_reference": command.applicant_reference,
            "applicant_name": command.applicant_name,
            "goods_description": command.goods_description,
            "origin_country_code": command.origin_country_code,
            "agreement_reference": command.agreement_reference,
        }
        intake_outcome = self.agn1_orchestrator.start_intake(
            case_id=case.id,
            payload=intake_payload,
            correlation_id=correlation_id,
        )

        # Update case based on AGN1 outcome
        case.case_state = intake_outcome.case_state
        case.current_step_id = intake_outcome.current_step_id
        case.accountable_role = intake_outcome.accountable_role
        # SQLAlchemy's JSON field accepts list but is typed as dict - use cast to satisfy mypy
        case.reason_codes_json = cast(dict, intake_outcome.reason_codes)
        self.session.flush()

        # Create attachments
        if command.attachments:
            attachment_models = [
                CaseAttachmentModel(
                    id=att.attachment_id,
                    case_id=case.id,
                    file_name=att.file_name,
                    media_type=att.media_type,
                    storage_key=att.storage_key,
                )
                for att in command.attachments
            ]
            self.attachment_repo.create_many(attachment_models)

        self.session.commit()
        self.session.refresh(case)

        # Build response
        return {
            "case_id": case.id,
            "case_reference": case.case_reference,
            "workflow_type": case.workflow_type,
            "current_step_id": case.current_step_id,
            "case_state": case.case_state,
            "accountable_role": case.accountable_role,
            "registration_sync_status": case.registration_sync_status,
            "reason_codes": case.reason_codes_json if isinstance(case.reason_codes_json, list) else [],
            "agent_execution": {
                "agent_id": "AGN1",
                "agent_name": "Intake & Routing Agent",
                "disposition": intake_outcome.agent_disposition,
            },
            "trace_event_ids": [str(eid) for eid in intake_outcome.event_ids],
            "created_at": case.created_at,
            "updated_at": case.updated_at,
        }
