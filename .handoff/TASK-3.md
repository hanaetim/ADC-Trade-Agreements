# Task 3 Handoff: Case Registration and Routing Backend

## Endpoints Implemented

All endpoints mounted under `/api/v1` prefix as required by architecture contract.

### POST /api/v1/cases
Register a new case with intake validation and routing.

**Request Body:**
```json
{
  "submission_type": "origin_ruling",
  "submission_channel": "portal",
  "applicant_reference": "APP-2026-00123",
  "applicant_name": "Example Company Ltd.",
  "goods_description": "Electronic components",
  "origin_country_code": "CN",
  "agreement_reference": "FTA-GCC-RCEP",
  "attachments": [],
  "intake_notes": null,
  "locale": "en"
}
```

**Response (201 Created):**
```json
{
  "case_id": "uuid",
  "case_reference": "IAO-2026-000123",
  "workflow_type": "origin_ruling",
  "current_step_id": "ATS2",
  "case_state": "routed",
  "accountable_role": "intake_exception_handler",
  "registration_sync_status": "succeeded",
  "reason_codes": [],
  "agent_execution": {
    "agent_id": "AGN1",
    "agent_name": "Intake & Routing Agent",
    "disposition": "completed"
  },
  "trace_event_ids": [],
  "created_at": "2026-11-13T...",
  "updated_at": "2026-11-13T..."
}
```

### GET /api/v1/cases
List cases with pagination and optional filters.

**Query Parameters:**
- `limit` (default 20): Page size
- `offset` (default 0): Pagination offset
- `workflow_type`: Filter by workflow type
- `case_state`: Filter by case state
- `assigned_role`: Filter by accountable role

**Response (200 OK):**
```json
{
  "items": [
    {
      "case_id": "uuid",
      "case_reference": "IAO-2026-000001",
      "workflow_type": "origin_ruling",
      "case_state": "registered",
      "current_step_id": "ATS2",
      "accountable_role": "intake_exception_handler",
      "latest_reason_code": null,
      "registration_sync_status": "succeeded",
      "created_at": "2026-11-13T...",
      "updated_at": "2026-11-13T..."
    }
  ],
  "total": 4,
  "page": 1,
  "page_size": 20
}
```

Note: List endpoint returns `{items, total, page, page_size}` pagination envelope, never bare arrays.

### GET /api/v1/cases/{case_id}
Get case detail by ID.

**Response (200 OK):**
```json
{
  "case_id": "uuid",
  "case_reference": "IAO-2026-000001",
  "workflow_type": "origin_ruling",
  "submission_channel": "portal",
  "applicant_reference": "APP-2026-00123",
  "case_state": "registered",
  "current_step_id": "ATS2",
  "accountable_role": "intake_exception_handler",
  "registration_sync_status": "succeeded",
  "visible_reason_codes": [],
  "created_at": "2026-11-13T...",
  "updated_at": "2026-11-13T..."
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Case not found"
}
```

## Seed Records

### Users
All users created with seed data (documented credentials):

| Email | Password | Role |
|-------|----------|------|
| applicant@example.com | Applicant123! | external_applicant |
| intake@example.com | Intake123! | intake_exception_handler |
| specialist@example.com | Specialist123! | specialist_reviewer |
| head@example.com | Head123! | section_head |
| policy@example.com | Policy123! | policy_legal_approver |
| committee@example.com | Committee123! | technical_committee |
| auditor@example.com | Auditor123! | auditor |

### Cases
Four sample cases created:

1. **IAO-2026-000001** - Origin Ruling (registered state)
2. **IAO-2026-000002** - Agreement Update (routed state)
3. **IAO-2026-000003** - Inquiry (intake_blocked state with INCOMPLETE_SUBMISSION reason)
4. **IAO-2026-000004** - Study (queued_for_review state)

## Backend Flows

### Case Registration Flow
1. Client sends POST request to `/api/v1/cases`
2. CaseRegistrationService generates unique case reference (IAO-YYYY-NNNNNN format)
3. RoutingService classifies workflow type from submission_type
4. RoutingService resolves next step (ATS1 → ATS2 for MVP intake)
5. RoutingService resolves accountable role (intake_exception_handler for all MVP steps)
6. IcosRegistrationAdapter performs mock registration sync (always succeeds in MVP)
7. CaseModel persisted with all metadata
8. CaseAttachmentModel records created for any attachments
9. Response includes AGN1 execution summary and correlation ID propagated

### List Cases Flow
1. Client sends GET request to `/api/v1/cases` with optional filters
2. CaseRepository queries database with filters and pagination
3. Response includes items array, total count, page number, and page size
4. Latest reason code extracted from reason_codes_json array for each item

### Get Case Detail Flow
1. Client sends GET request to `/api/v1/cases/{case_id}`
2. CaseRepository queries by UUID primary key
3. If not found, returns 404 with error detail
4. If found, returns case detail with visible reason codes filtered by viewer role (MVP shows all)

### Workflow Classification
- AGN1 (Intake & Routing Agent) is the active orchestrator for MVP
- Deterministic workflow classification based on submission_type enum
- Six workflow types supported: origin_ruling, agreement_update, inquiry, study, certificate_sampling, dispute
- All workflows route through ATS1 → ATS2 → ATS3 intake steps in MVP
- Unresolved routes trigger queued_for_review state

### ICOS Integration
- Mocked IcosRegistrationAdapter always returns success with generated ICOS reference
- Real implementation will POST to ICOS REST API in future
- Registration status tracked in case.registration_sync_status field

### Error Handling
- 400 Bad Request: Business validation failures
- 401 Unauthorized: Missing/invalid authentication (not enforced in MVP endpoints)
- 403 Forbidden: Insufficient permissions
- 404 Not Found: Resource not found
- 422 Unprocessable Entity: Schema validation failures (Pydantic)
- 500 Internal Server Error: Unhandled exceptions

All errors return consistent `{"detail": "message", "status_code": N}` shape.

## Architecture Notes

- Correlation IDs generated per request via CorrelationIdMiddleware
- All case operations are synchronous transactions in MVP
- Case references are unique constraints at database level
- Workflow taxonomy preserved for all six types but only intake routing implemented
- AGN2-AGN6 preserved as registered deferred components (not executable in MVP)
- Future HITL gates (ATS4, ATS6, ATS8, ATS11, ATS14) preserved as metadata only
