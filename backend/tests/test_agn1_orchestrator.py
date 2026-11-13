"""Unit tests for AGN1 orchestrator (FR-002, FR-004)."""
import uuid

from app.services.agent_registry_service import AgentRegistryService
from app.services.agn1_orchestrator import Agn1Orchestrator
from app.services.audit_service import AuditService
from app.services.deterministic_rule_engine import DeterministicRuleEngine
from app.services.routing_service import RoutingService


def test_agn1_start_intake_success(db_session):
    """Test successful AGN1 intake orchestration (ATS1-ATS3)."""
    orchestrator = Agn1Orchestrator(
        session=db_session,
        agent_registry=AgentRegistryService(),
        rule_engine=DeterministicRuleEngine(),
        routing_service=RoutingService(),
        audit_service=AuditService(db_session),
    )

    case_id = uuid.uuid4()
    payload = {
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-TEST-001",
        "applicant_name": "Test Applicant",
        "goods_description": "Test goods",
        "origin_country_code": "CN",
    }
    correlation_id = "test-correlation-123"

    outcome = orchestrator.start_intake(case_id, payload, correlation_id)

    assert outcome.success is True
    assert outcome.case_state == "routed"
    assert outcome.current_step_id == "ATS3"
    assert outcome.accountable_role == "intake_exception_handler"
    assert outcome.agent_disposition == "completed"
    assert len(outcome.event_ids) == 3  # completeness, eligibility, routing
    assert outcome.reason_codes == []


def test_agn1_blocks_on_incomplete_submission(db_session):
    """Test AGN1 blocks case when completeness validation fails."""
    orchestrator = Agn1Orchestrator(session=db_session)

    case_id = uuid.uuid4()
    payload = {
        "submission_type": "origin_ruling",
        # Missing required fields: submission_channel, applicant_reference, applicant_name
    }
    correlation_id = "test-correlation-incomplete"

    outcome = orchestrator.start_intake(case_id, payload, correlation_id)

    assert outcome.success is False
    assert outcome.case_state == "intake_blocked"
    assert outcome.current_step_id == "ATS1"
    assert "INCOMPLETE_SUBMISSION" in outcome.reason_codes
    assert outcome.agent_disposition == "blocked"


def test_agn1_blocks_on_ineligible_workflow(db_session):
    """Test AGN1 blocks case when eligibility validation fails."""
    orchestrator = Agn1Orchestrator(session=db_session)

    case_id = uuid.uuid4()
    payload = {
        "submission_type": "invalid_workflow_type",
        "submission_channel": "portal",
        "applicant_reference": "APP-TEST-002",
        "applicant_name": "Test Applicant",
    }
    correlation_id = "test-correlation-ineligible"

    outcome = orchestrator.start_intake(case_id, payload, correlation_id)

    assert outcome.success is False
    assert outcome.case_state == "intake_blocked"
    assert outcome.current_step_id == "ATS2"
    assert "INELIGIBLE_WORKFLOW" in outcome.reason_codes
    assert outcome.agent_disposition == "blocked"


def test_agn1_records_events(db_session):
    """Test AGN1 records case events and audit logs."""
    orchestrator = Agn1Orchestrator(session=db_session)

    case_id = uuid.uuid4()
    payload = {
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-TEST-003",
        "applicant_name": "Test Applicant",
    }
    correlation_id = "test-correlation-events"

    orchestrator.start_intake(case_id, payload, correlation_id)

    # Verify events were recorded
    from app.repositories.case_event_repository import CaseEventRepository
    event_repo = CaseEventRepository(db_session)
    events = event_repo.list_by_case(str(case_id))

    assert len(events) >= 2  # At least completeness and eligibility
    assert any(e.event_type == "validation_completeness" for e in events)
    assert any(e.decision_source == "deterministic_rule" for e in events)
    assert all(e.correlation_id == correlation_id for e in events)
