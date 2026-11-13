"""Integration tests for trace visibility and exception actions (FR-023, FR-024)."""
import uuid
from datetime import datetime, timezone

from app.models.case import CaseModel
from app.repositories.case_repository import CaseRepository
from app.services.agn1_orchestrator import Agn1Orchestrator
from app.services.audit_service import AuditService
from app.services.case_trace_service import CaseTraceService


def test_full_intake_flow_generates_trace(db_session):
    """Test complete intake flow generates proper trace records."""
    # Create case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-INT01",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-INT-001",
        applicant_name="Integration Test Applicant",
        case_state="submitted",
        current_step_id="ATS1",
        accountable_role="intake_exception_handler",
        registration_sync_status="pending",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Run AGN1 intake orchestration
    orchestrator = Agn1Orchestrator(session=db_session)
    payload = {
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-INT-001",
        "applicant_name": "Integration Test Applicant",
        "goods_description": "Test goods",
        "origin_country_code": "CN",
    }
    outcome = orchestrator.start_intake(case_id, payload, "integration-test-001")

    # Update case state based on outcome
    case.case_state = outcome.case_state
    case.current_step_id = outcome.current_step_id
    case.accountable_role = outcome.accountable_role
    db_session.commit()

    # Retrieve trace
    trace_service = CaseTraceService(db_session)
    trace = trace_service.get_case_trace(case_id, viewer_role="auditor")

    # Verify trace structure
    assert trace.case_id == case_id
    assert len(trace.events) >= 2  # At least completeness and eligibility
    assert len(trace.steps) >= 2
    assert len(trace.approval_chain) == 5

    # Verify event types
    event_types = {e.event_type for e in trace.events}
    assert "validation_completeness" in event_types
    assert "validation_eligibility" in event_types


def test_exception_action_records_event(db_session):
    """Test exception action recording via audit service."""
    # Create blocked case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-INT02",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-INT-002",
        applicant_name="Blocked Test Applicant",
        case_state="intake_blocked",
        current_step_id="ATS1",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=["INCOMPLETE_SUBMISSION"],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Record exception action
    audit_service = AuditService(db_session)
    audit_service.record_case_event(
        case_id=case_id,
        event_type="exception_request_correction",
        step_id="ATS1",
        decision_source="human",
        actor_type="human",
        actor_id="intake_exception_handler",
        correlation_id="exception-test-001",
        visible_to_external=False,
        rationale_summary="Requesting applicant to provide missing goods description",
        payload={
            "action_type": "request_correction",
            "comment": "Please provide goods description",
        },
    )
    db_session.commit()

    # Verify event was recorded
    from app.repositories.case_event_repository import CaseEventRepository
    event_repo = CaseEventRepository(db_session)
    events = event_repo.list_by_case(str(case_id))

    assert len(events) == 1
    assert events[0].event_type == "exception_request_correction"
    assert events[0].decision_source == "human"
    assert events[0].actor_type == "human"


def test_trace_visibility_for_different_roles(db_session):
    """Test trace visibility differs by viewer role."""
    # Create case with mixed visibility events
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-INT03",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-INT-003",
        applicant_name="Visibility Test Applicant",
        case_state="routed",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Create events with different visibility
    audit_service = AuditService(db_session)
    audit_service.record_case_event(
        case_id=case_id,
        event_type="validation_completeness",
        step_id="ATS1",
        decision_source="deterministic_rule",
        actor_type="system",
        actor_id="DeterministicRuleEngine",
        correlation_id="visibility-test-001",
        visible_to_external=True,
        payload={},
    )
    audit_service.record_case_event(
        case_id=case_id,
        event_type="route_resolved",
        step_id="ATS3",
        decision_source="agent",
        actor_type="agent",
        actor_id="AGN1",
        correlation_id="visibility-test-001",
        visible_to_external=False,
        payload={},
    )
    db_session.commit()

    # Get trace as external applicant
    trace_service = CaseTraceService(db_session)
    external_trace = trace_service.get_case_trace(case_id, viewer_role="external_applicant")
    internal_trace = trace_service.get_case_trace(case_id, viewer_role="auditor")

    # External sees only visible events
    assert len(external_trace.events) == 1
    assert external_trace.events[0].visible_to_external is True

    # Internal sees all events
    assert len(internal_trace.events) == 2
