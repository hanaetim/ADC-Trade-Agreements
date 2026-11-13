"""Acceptance tests for trace and exception action API endpoints (FR-023, FR-024)."""
import uuid
from datetime import datetime, timezone

from app.models.case import CaseModel
from app.repositories.case_repository import CaseRepository


def test_get_case_trace_endpoint(auth_client, db_session):
    """Test GET /api/v1/cases/{case_id}/trace endpoint."""
    # Create case with events (via seed-like setup)
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC01",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-001",
        applicant_name="Acceptance Test Applicant",
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

    # Call trace endpoint
    response = auth_client.get(f"/api/v1/cases/{case_id}/trace")

    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert data["case_id"] == str(case_id)
    assert data["case_reference"] == "IAO-2026-ACC01"
    assert data["workflow_type"] == "origin_ruling"
    assert "steps" in data
    assert "events" in data
    assert "approval_chain" in data
    assert len(data["approval_chain"]) == 5  # ATS4, ATS6, ATS8, ATS11, ATS14


def test_get_case_trace_not_found(auth_client, db_session):
    """Test trace endpoint returns 404 for non-existent case."""
    non_existent_id = uuid.uuid4()
    response = auth_client.get(f"/api/v1/cases/{non_existent_id}/trace")

    assert response.status_code == 404


def test_exception_action_request_correction(auth_client, db_session):
    """Test POST /api/v1/cases/{case_id}/exception-actions for correction request."""
    # Create blocked case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC02",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-002",
        applicant_name="Blocked Applicant",
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

    # Submit exception action
    response = auth_client.post(
        f"/api/v1/cases/{case_id}/exception-actions",
        json={
            "action_type": "request_correction",
            "comment": "Please provide missing goods description and origin country code",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == str(case_id)
    assert data["case_state"] == "queued_for_review"
    assert "recorded_event_id" in data
    assert "updated_at" in data


def test_exception_action_close_rejected(auth_client, db_session):
    """Test exception action to close case as rejected."""
    # Create blocked case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC03",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-003",
        applicant_name="Rejected Applicant",
        case_state="intake_blocked",
        current_step_id="ATS2",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=["INELIGIBLE_WORKFLOW"],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Submit rejection action
    response = auth_client.post(
        f"/api/v1/cases/{case_id}/exception-actions",
        json={
            "action_type": "close_rejected",
            "comment": "Workflow type not supported for this jurisdiction",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == str(case_id)
    assert data["case_state"] == "closed_rejected"


def test_exception_action_manual_route_resolution(auth_client, db_session):
    """Test exception action for manual routing resolution."""
    # Create unresolved case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC04",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-004",
        applicant_name="Manual Route Applicant",
        case_state="queued_for_review",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Submit manual route resolution
    response = auth_client.post(
        f"/api/v1/cases/{case_id}/exception-actions",
        json={
            "action_type": "manual_route_resolution",
            "comment": "Manually routing to specialist reviewer",
            "resolved_workflow_type": "origin_ruling",
            "resolved_next_step_id": "ATS3",
            "resolved_accountable_role": "specialist_reviewer",
        },
    )

    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == str(case_id)
    assert data["case_state"] == "routed"
    assert data["accountable_role"] == "specialist_reviewer"


def test_exception_action_validation_error(auth_client, db_session):
    """Test exception action validation fails without required fields."""
    # Create case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC05",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-005",
        applicant_name="Validation Test",
        case_state="queued_for_review",
        current_step_id="ATS3",
        accountable_role="intake_exception_handler",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Submit manual route without required fields
    response = auth_client.post(
        f"/api/v1/cases/{case_id}/exception-actions",
        json={
            "action_type": "manual_route_resolution",
            "comment": "Attempting manual route without resolution fields",
            # Missing: resolved_workflow_type, resolved_next_step_id, resolved_accountable_role
        },
    )

    assert response.status_code == 400
    assert "resolved_workflow_type" in response.json()["detail"]


def test_exception_action_wrong_state(auth_client, db_session):
    """Test exception action fails for cases not in blocked/queued state."""
    # Create routed case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC06",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-006",
        applicant_name="Wrong State Test",
        case_state="routed",  # Not blocked or queued
        current_step_id="ATS3",
        accountable_role="specialist_reviewer",
        registration_sync_status="succeeded",
        reason_codes_json=[],
        submitted_at=datetime.now(timezone.utc),
    )
    repo = CaseRepository(db_session)
    repo.create(case)
    db_session.commit()

    # Attempt exception action on routed case
    response = auth_client.post(
        f"/api/v1/cases/{case_id}/exception-actions",
        json={
            "action_type": "request_correction",
            "comment": "Should not work on routed case",
        },
    )

    assert response.status_code == 400
    assert "not allowed" in response.json()["detail"]


def test_trace_endpoint_includes_all_required_fields(auth_client, db_session):
    """Test trace response includes all required fields per LLD."""
    # Create case
    case_id = uuid.uuid4()
    case = CaseModel(
        id=case_id,
        case_reference="IAO-2026-ACC07",
        workflow_type="origin_ruling",
        submission_channel="portal",
        applicant_reference="APP-ACC-007",
        applicant_name="Complete Response Test",
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

    response = auth_client.get(f"/api/v1/cases/{case_id}/trace")

    assert response.status_code == 200
    data = response.json()

    # Verify all required top-level fields
    required_fields = [
        "case_id",
        "case_reference",
        "workflow_type",
        "current_step_id",
        "case_state",
        "steps",
        "events",
        "approval_chain",
    ]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Verify approval chain structure
    for stage in data["approval_chain"]:
        assert "stage_step_id" in stage
        assert "stage_status" in stage
        assert "required_role" in stage
        assert "notes" in stage
