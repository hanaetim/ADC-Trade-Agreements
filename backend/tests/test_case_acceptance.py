"""Acceptance tests for case API endpoints (FR-001, FR-023)."""
import uuid


def test_post_cases_creates_case(auth_client, db_session):
    """Test POST /api/v1/cases creates a new case record with AGN1 orchestration."""
    payload = {
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-2026-ACC01",
        "applicant_name": "Acceptance Test Company",
        "goods_description": "Test goods for acceptance",
        "origin_country_code": "DE",
        "agreement_reference": "FTA-EU",
        "attachments": [],
        "locale": "en",
    }

    response = auth_client.post("/api/v1/cases", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "case_id" in data
    assert data["case_reference"].startswith("IAO-202")
    assert data["workflow_type"] == "origin_ruling"
    assert data["case_state"] == "routed"
    # After AGN1 orchestration (ATS1→ATS2→ATS3), successful cases reach ATS3
    assert data["current_step_id"] == "ATS3"
    assert data["accountable_role"] == "intake_exception_handler"
    assert data["registration_sync_status"] in ["pending", "succeeded"]
    assert data["agent_execution"]["agent_id"] == "AGN1"
    assert data["agent_execution"]["disposition"] == "completed"
    assert "created_at" in data
    assert "updated_at" in data


def test_post_cases_with_attachments(auth_client, db_session):
    """Test POST /api/v1/cases with attachments."""
    attachment_id = str(uuid.uuid4())
    payload = {
        "submission_type": "inquiry",
        "submission_channel": "email_intake",
        "applicant_reference": "APP-2026-ACC02",
        "applicant_name": "Company With Attachments",
        "attachments": [
            {
                "attachment_id": attachment_id,
                "file_name": "evidence.pdf",
                "media_type": "application/pdf",
                "storage_key": "s3://test-bucket/evidence.pdf",
            }
        ],
    }

    response = auth_client.post("/api/v1/cases", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["workflow_type"] == "inquiry"


def test_get_cases_returns_paginated_list(auth_client, db_session):
    """Test GET /api/v1/cases returns paginated case list."""
    # Create test cases
    for i in range(3):
        payload = {
            "submission_type": "origin_ruling",
            "submission_channel": "portal",
            "applicant_reference": f"APP-2026-LIST{i:02d}",
            "applicant_name": f"List Test Company {i}",
        }
        auth_client.post("/api/v1/cases", json=payload)

    response = auth_client.get("/api/v1/cases")

    assert response.status_code == 200
    data = response.json()

    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "page_size" in data
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_get_cases_with_filters(auth_client, db_session):
    """Test GET /api/v1/cases with filters."""
    # Create cases with different workflow types
    auth_client.post("/api/v1/cases", json={
        "submission_type": "origin_ruling",
        "submission_channel": "portal",
        "applicant_reference": "APP-F1",
        "applicant_name": "Filter Test 1",
    })
    auth_client.post("/api/v1/cases", json={
        "submission_type": "inquiry",
        "submission_channel": "portal",
        "applicant_reference": "APP-F2",
        "applicant_name": "Filter Test 2",
    })

    # Filter by workflow type
    response = auth_client.get("/api/v1/cases?workflow_type=origin_ruling")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["workflow_type"] == "origin_ruling"


def test_get_cases_with_pagination(auth_client, db_session):
    """Test GET /api/v1/cases pagination."""
    # Create 5 test cases
    for i in range(5):
        auth_client.post("/api/v1/cases", json={
            "submission_type": "inquiry",
            "submission_channel": "portal",
            "applicant_reference": f"APP-P{i:02d}",
            "applicant_name": f"Pagination Test {i}",
        })

    # Get first page
    response = auth_client.get("/api/v1/cases?limit=2&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["total"] == 5
    assert data["page"] == 1

    # Get second page
    response = auth_client.get("/api/v1/cases?limit=2&offset=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2
    assert data["page"] == 2


def test_get_case_by_id(auth_client, db_session):
    """Test GET /api/v1/cases/{case_id} returns case detail."""
    # Create a case
    create_response = auth_client.post("/api/v1/cases", json={
        "submission_type": "study",
        "submission_channel": "internal_entry",
        "applicant_reference": "INT-001",
        "applicant_name": "Internal Study",
    })
    assert create_response.status_code == 201
    case_id = create_response.json()["case_id"]

    # Get case detail
    response = auth_client.get(f"/api/v1/cases/{case_id}")

    assert response.status_code == 200
    data = response.json()

    assert data["case_id"] == case_id
    assert data["workflow_type"] == "study"
    assert data["submission_channel"] == "internal_entry"
    assert data["applicant_reference"] == "INT-001"
    assert "visible_reason_codes" in data


def test_get_case_not_found(auth_client, db_session):
    """Test GET /api/v1/cases/{case_id} returns 404 for non-existent case."""
    non_existent_id = str(uuid.uuid4())
    response = auth_client.get(f"/api/v1/cases/{non_existent_id}")

    assert response.status_code == 404
    assert "detail" in response.json()


def test_post_cases_invalid_workflow_type(auth_client, db_session):
    """Test POST /api/v1/cases rejects invalid workflow type."""
    payload = {
        "submission_type": "invalid_workflow",
        "submission_channel": "portal",
        "applicant_reference": "APP-BAD",
        "applicant_name": "Bad Request Test",
    }

    response = auth_client.post("/api/v1/cases", json=payload)

    # Should be 422 (validation error) for invalid enum
    assert response.status_code == 422
