"""Unit tests for case registration service (FR-001, FR-002, FR-004)."""
import uuid

from app.models.workflow_taxonomy import WorkflowType
from app.schemas.case import CreateCaseRequest
from app.services.case_registration_service import CaseRegistrationService


def test_generate_case_reference(db_session):
    """Test case reference generation follows IAO-YYYY-NNNNNN format."""
    service = CaseRegistrationService(db_session)
    ref = service.generate_case_reference()

    assert ref.startswith("IAO-202")
    assert len(ref) == 15  # IAO-YYYY-NNNNNN (6 hex chars)
    assert ref[3] == "-"
    assert ref[8] == "-"


def test_register_case_origin_ruling(db_session):
    """Test successful origin ruling case registration with AGN1 orchestration."""
    service = CaseRegistrationService(db_session)

    command = CreateCaseRequest(
        submission_type=WorkflowType.ORIGIN_RULING,
        submission_channel="portal",
        applicant_reference="APP-2026-TEST01",
        applicant_name="Test Company Ltd.",
        goods_description="Electronic components",
        origin_country_code="CN",
        agreement_reference="FTA-GCC-RCEP",
        attachments=[],
    )

    result = service.register_case(command, correlation_id="test-001")

    assert result["case_reference"].startswith("IAO-202")
    assert result["workflow_type"] == "origin_ruling"
    assert result["case_state"] == "routed"
    # After AGN1 orchestration (ATS1→ATS2→ATS3), successful cases reach ATS3
    assert result["current_step_id"] == "ATS3"
    assert result["accountable_role"] == "intake_exception_handler"
    assert result["registration_sync_status"] in ["pending", "succeeded"]
    assert result["agent_execution"]["agent_id"] == "AGN1"
    assert result["agent_execution"]["agent_name"] == "Intake & Routing Agent"
    assert result["agent_execution"]["disposition"] == "completed"


def test_register_case_with_attachments(db_session):
    """Test case registration with attachments."""
    from app.schemas.case import AttachmentMetadata

    service = CaseRegistrationService(db_session)

    attachment_id = uuid.uuid4()
    command = CreateCaseRequest(
        submission_type=WorkflowType.INQUIRY,
        submission_channel="email_intake",
        applicant_reference="APP-2026-TEST02",
        applicant_name="Another Company",
        attachments=[
            AttachmentMetadata(
                attachment_id=attachment_id,
                file_name="document.pdf",
                media_type="application/pdf",
                storage_key="s3://bucket/key",
            )
        ],
    )

    result = service.register_case(command, correlation_id="test-002")

    assert result["case_id"] is not None
    assert result["case_reference"].startswith("IAO-202")

    # Verify attachment was created
    from app.repositories.case_attachment_repository import CaseAttachmentRepository

    repo = CaseAttachmentRepository(db_session)
    attachments = repo.list_by_case(result["case_id"])
    assert len(attachments) == 1
    assert attachments[0].file_name == "document.pdf"


def test_register_case_agreement_update(db_session):
    """Test agreement update workflow classification."""
    service = CaseRegistrationService(db_session)

    command = CreateCaseRequest(
        submission_type=WorkflowType.AGREEMENT_UPDATE,
        submission_channel="internal_entry",
        applicant_reference="INT-2026-001",
        applicant_name="Internal Team",
    )

    result = service.register_case(command, correlation_id="test-003")

    assert result["workflow_type"] == "agreement_update"
    assert result["case_state"] == "routed"


def test_register_case_dispute(db_session):
    """Test dispute workflow classification."""
    service = CaseRegistrationService(db_session)

    command = CreateCaseRequest(
        submission_type=WorkflowType.DISPUTE,
        submission_channel="portal",
        applicant_reference="APP-2026-DISP01",
        applicant_name="Disputing Party",
        goods_description="Contested origin determination",
    )

    result = service.register_case(command, correlation_id="test-004")

    assert result["workflow_type"] == "dispute"
    # After AGN1 orchestration (ATS1→ATS2→ATS3), successful cases reach ATS3
    assert result["current_step_id"] == "ATS3"
