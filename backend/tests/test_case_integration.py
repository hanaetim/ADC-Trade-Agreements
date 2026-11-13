"""Integration tests for case registration flow (FR-001, FR-002, FR-004)."""
import uuid

from app.models.case import CaseModel
from app.models.workflow_taxonomy import WorkflowType
from app.schemas.case import CreateCaseRequest
from app.services.case_registration_service import CaseRegistrationService


def test_full_registration_flow_with_database(db_session):
    """Test complete registration flow against real database."""
    service = CaseRegistrationService(db_session)

    command = CreateCaseRequest(
        submission_type=WorkflowType.ORIGIN_RULING,
        submission_channel="portal",
        applicant_reference="APP-2026-INT01",
        applicant_name="Integration Test Company",
        goods_description="Test goods",
        origin_country_code="US",
        agreement_reference="FTA-TEST",
    )

    result = service.register_case(command, correlation_id="int-test-001")

    # Verify case was persisted
    from sqlalchemy import select

    stmt = select(CaseModel).where(CaseModel.id == result["case_id"])
    case = db_session.execute(stmt).scalar_one()

    assert case.case_reference == result["case_reference"]
    assert case.workflow_type == "origin_ruling"
    assert case.applicant_name == "Integration Test Company"
    assert case.case_state == "routed"
    assert case.registration_sync_status in ["pending", "succeeded"]


def test_case_repository_list_with_filters(db_session):
    """Test case repository list with various filters."""
    from app.repositories.case_repository import CaseRepository

    # Create test cases
    service = CaseRegistrationService(db_session)

    for i in range(5):
        command = CreateCaseRequest(
            submission_type=WorkflowType.ORIGIN_RULING if i < 3 else WorkflowType.INQUIRY,
            submission_channel="portal",
            applicant_reference=f"APP-2026-LIST{i:02d}",
            applicant_name=f"Test Company {i}",
        )
        service.register_case(command, correlation_id=f"list-test-{i}")

    repo = CaseRepository(db_session)

    # Test workflow filter
    cases, total = repo.list_cases(workflow_type="origin_ruling")
    assert total == 3
    assert all(c.workflow_type == "origin_ruling" for c in cases)

    # Test pagination
    cases, total = repo.list_cases(limit=2, offset=0)
    assert len(cases) == 2
    assert total == 5

    cases, total = repo.list_cases(limit=2, offset=2)
    assert len(cases) == 2


def test_routing_service_workflow_classification(db_session):
    """Test routing service workflow classification logic."""
    from app.services.routing_service import RoutingService

    service = RoutingService()

    # Test each workflow type
    for workflow_type in WorkflowType:
        classification = service.classify_workflow({"submission_type": workflow_type.value})
        assert classification.workflow_type == workflow_type
        assert classification.confidence == "high"

    # Test missing submission type
    classification = service.classify_workflow({})
    assert classification.workflow_type == WorkflowType.INQUIRY
    assert classification.confidence == "low"


def test_routing_service_step_resolution(db_session):
    """Test routing service step resolution for MVP intake flow."""
    from app.services.routing_service import RoutingService

    service = RoutingService()

    # ATS1 → ATS2
    resolution = service.resolve_next_step(WorkflowType.ORIGIN_RULING, current_step="ATS1")
    assert resolution.next_step_id == "ATS2"
    assert resolution.resolved is True

    # ATS2 → ATS3
    resolution = service.resolve_next_step(WorkflowType.ORIGIN_RULING, current_step="ATS2")
    assert resolution.next_step_id == "ATS3"
    assert resolution.resolved is True

    # ATS3 stays at ATS3 for MVP
    resolution = service.resolve_next_step(WorkflowType.ORIGIN_RULING, current_step="ATS3")
    assert resolution.next_step_id == "ATS3"
    assert resolution.resolved is True


def test_icos_adapter_mock_registration(db_session):
    """Test ICOS adapter mock returns expected result."""
    from app.adapters.icos_registration import IcosRegistrationAdapter

    adapter = IcosRegistrationAdapter()
    result = adapter.register_case(
        {"case_id": str(uuid.uuid4()), "case_reference": "IAO-2026-TEST"},
        correlation_id="test-icos",
    )

    assert result.status == "succeeded"
    assert result.icos_reference_id is not None
    assert result.icos_reference_id.startswith("ICOS-")
