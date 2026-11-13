"""Unit tests for Case Trace Service (FR-023, FR-024)."""
import uuid
from datetime import datetime, timezone

from app.models.case import CaseModel
from app.models.case_event import CaseEventModel
from app.repositories.case_repository import CaseRepository
from app.services.case_trace_service import CaseTraceService


def test_get_case_trace_assembles_steps_and_events(db_session):
    """Test trace service assembles steps and events from case_events."""
    # Create case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-TEST01",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-TEST",
        applicant_name="Test Applicant",
        case_state="routed",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)

    # Create events
    events = [
        CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type="validation_completeness",
            step_id="ATS1",
            decision_source="deterministic_rule",
            actor_type="system",
            actor_id="DeterministicRuleEngine",
            visible_to_external=True,
            correlation_id="test-corr-01",
            payload_json={"outcome": "passed"},
            occurred_at=datetime.now(timezone.utc),
        ),
        CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type="validation_eligibility",
            step_id="ATS2",
            decision_source="deterministic_rule",
            actor_type="system",
            actor_id="DeterministicRuleEngine",
            visible_to_external=True,
            correlation_id="test-corr-01",
            payload_json={"outcome": "passed"},
            occurred_at=datetime.now(timezone.utc),
        ),
        CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type="route_resolved",
            step_id="ATS3",
            decision_source="agent",
            actor_type="agent",
            actor_id="AGN1",
            visible_to_external=False,
            correlation_id="test-corr-01",
            payload_json={"workflow_type": "origin_ruling"},
            occurred_at=datetime.now(timezone.utc),
        ),
    ]
    for event in events:
        db_session.add(event)
    db_session.commit()

    # Get trace
    trace_service = CaseTraceService(db_session)
    trace = trace_service.get_case_trace(case_id, viewer_role="auditor")

    assert trace.case_id == case_id
    assert trace.case_reference == "IAO-2026-TEST01"
    assert len(trace.steps) == 3
    assert len(trace.events) == 3
    assert len(trace.approval_chain) == 5  # ATS4, ATS6, ATS8, ATS11, ATS14


def test_get_case_trace_filters_for_external_applicant(db_session):
    """Test visibility policy filters events for external applicants."""
    # Create case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-TEST02",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-TEST",
        applicant_name="Test Applicant",
        case_state="routed",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)

    # Create mixed visibility events
    events = [
        CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type="validation_completeness",
            step_id="ATS1",
            decision_source="deterministic_rule",
            actor_type="system",
            actor_id="DeterministicRuleEngine",
            visible_to_external=True,  # External visible
            correlation_id="test-corr-02",
            payload_json={},
            occurred_at=datetime.now(timezone.utc),
        ),
        CaseEventModel(
            id=uuid.uuid4(),
            case_id=case_id,
            event_type="route_resolved",
            step_id="ATS3",
            decision_source="agent",
            actor_type="agent",
            actor_id="AGN1",
            visible_to_external=False,  # Internal only
            correlation_id="test-corr-02",
            payload_json={},
            occurred_at=datetime.now(timezone.utc),
        ),
    ]
    for event in events:
        db_session.add(event)
    db_session.commit()

    # Get trace as external applicant
    trace_service = CaseTraceService(db_session)
    trace = trace_service.get_case_trace(case_id, viewer_role="external_applicant")

    # Should only see external-visible events
    assert len(trace.events) == 1
    assert trace.events[0].visible_to_external is True
    assert trace.events[0].event_type == "validation_completeness"


def test_get_case_trace_includes_approval_placeholders(db_session):
    """Test trace includes future HITL approval gate placeholders."""
    # Create minimal case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-TEST03",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-TEST",
        applicant_name="Test Applicant",
        case_state="routed",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)

    # Get trace
    trace_service = CaseTraceService(db_session)
    trace = trace_service.get_case_trace(case_id, viewer_role="auditor")

    # Verify approval chain placeholders
    assert len(trace.approval_chain) == 5
    stage_ids = {stage.stage_step_id for stage in trace.approval_chain}
    assert stage_ids == {"ATS4", "ATS6", "ATS8", "ATS11", "ATS14"}

    for stage in trace.approval_chain:
        assert stage.stage_status == "future_visible_placeholder"
        # Check case-insensitive match for "deferred" and "MVP"
        assert "deferred" in stage.notes.lower()
        assert "mvp" in stage.notes.lower()
