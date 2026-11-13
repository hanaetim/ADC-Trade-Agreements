# TASK-4 Handoff: Backend Feature B2 - Intake Validation, Trace View, and Exception Actions

## Overview
This task implements the backend intake validation, orchestration, tracing, and audit capabilities (FR-002, FR-023, FR-024). AGN1 orchestrates ATS1-ATS3 intake workflow with deterministic validation, routing, and event capture. Case trace service assembles per-case timelines with visibility filtering. Exception actions endpoint allows manual intervention for blocked cases.

## API Endpoints Added

All endpoints are mounted under the `/api/v1` prefix as specified in the architecture contract.

### Trace Endpoint
**GET /api/v1/cases/{case_id}/trace**
- Returns complete case trace view with steps, events, and approval chain
- Response shape: `CaseTraceResponse`
  ```json
  {
    "case_id": "uuid",
    "case_reference": "IAO-2026-000001",
    "workflow_type": "origin_ruling",
    "current_step_id": "ATS3",
    "case_state": "routed",
    "steps": [
      {
        "step_id": "ATS1",
        "step_status": "completed",
        "decision_source": "deterministic_rule",
        "actor_label": "System",
        "rationale_summary": "All required fields present",
        "evidence_ref": null,
        "occurred_at": "2026-11-13T..."
      }
    ],
    "events": [
      {
        "event_id": "uuid",
        "event_type": "validation_completeness",
        "step_id": "ATS1",
        "decision_source": "deterministic_rule",
        "actor_type": "system",
        "actor_id": "DeterministicRuleEngine",
        "visible_to_external": true,
        "reason_code": null,
        "rationale_summary": "All required fields present",
        "evidence_ref": null,
        "correlation_id": "seed-IAO-2026-000001",
        "occurred_at": "2026-11-13T..."
      }
    ],
    "approval_chain": [
      {
        "stage_step_id": "ATS4",
        "stage_status": "future_visible_placeholder",
        "required_role": "specialist_reviewer",
        "notes": "Specialist fact review - deferred from MVP but preserved as visible governance gate"
      }
    ]
  }
  ```
- Visibility filtering applied: external applicants see only events where `visible_to_external=true`
- Returns 404 if case not found

### Exception Actions Endpoint
**POST /api/v1/cases/{case_id}/exception-actions**
- Allows intake_exception_handler to record manual actions for blocked/queued cases
- Request shape: `ExceptionActionRequest`
  ```json
  {
    "action_type": "request_correction | close_rejected | manual_route_resolution",
    "comment": "Required explanation for action",
    "resolved_workflow_type": "origin_ruling",  // Required for manual_route_resolution
    "resolved_next_step_id": "ATS3",  // Required for manual_route_resolution
    "resolved_accountable_role": "specialist_reviewer"  // Required for manual_route_resolution
  }
  ```
- Response shape: `ExceptionActionResponse`
  ```json
  {
    "case_id": "uuid",
    "case_state": "routed",
    "current_step_id": "ATS3",
    "accountable_role": "specialist_reviewer",
    "recorded_event_id": "uuid",
    "updated_at": "2026-11-13T..."
  }
  ```
- Returns 400 if case not in intake_blocked or queued_for_review state
- Returns 400 if manual_route_resolution missing required fields

## Updated Endpoint

**POST /api/v1/cases**
- Now invokes AGN1 orchestrator for ATS1-ATS3 intake workflow
- Response includes `agent_execution` summary with AGN1 disposition
- Response includes `trace_event_ids` array with recorded event IDs
- Case state updated based on validation outcome:
  - `intake_blocked` if completeness or eligibility fails
  - `routed` if validation passes and routing succeeds
  - `queued_for_review` if routing unresolved

## Seed Data

Updated seed data includes:
- 4 sample cases (IAO-2026-000001 through IAO-2026-000004)
- Each case has sample `case_events` showing completed ATS1-ATS3 steps
- Each case has sample `audit_logs` entry for case registration

### Seed Events Structure
Each seeded case includes:
1. **ATS1 Event**: Completeness validation (visible_to_external=true)
   - Passed cases: "All required fields present"
   - Blocked case (IAO-2026-000003): "Missing required fields: goods_description, origin_country_code"
2. **ATS2 Event**: Eligibility validation (visible_to_external=true, only if passed ATS1)
   - Rationale: "Workflow type {type} is eligible"
3. **ATS3 Event**: Routing resolution (visible_to_external=false, only if passed ATS2)
   - Rationale: "Classified as {workflow_type}, routed to {step_id}"

### Seed Credentials (from TASK-3)
- External applicant: `external@example.com` / `External-pass-1`
- Intake handler: `intake@example.com` / `Intake-pass-1`
- Specialist: `specialist@example.com` / `Specialist-pass-1`
- Section head: `sectionhead@example.com` / `Section-pass-1`
- Policy/legal: `policy@example.com` / `Policy-pass-1`
- Technical committee: `technical@example.com` / `Technical-pass-1`
- Auditor: `auditor@example.com` / `Auditor-pass-1`

## Backend Flows

### AGN1 Intake Orchestration (ATS1-ATS3)
1. **ATS1 - Completeness Validation**
   - DeterministicRuleEngine checks mandatory fields: `submission_type`, `submission_channel`, `applicant_reference`, `applicant_name`
   - Blocking outcome: case state → `intake_blocked`, reason_code → `INCOMPLETE_SUBMISSION`
   - Passing outcome: continue to ATS2

2. **ATS2 - Eligibility Validation**
   - DeterministicRuleEngine validates workflow type is in allowed taxonomy
   - Blocking outcome: case state → `intake_blocked`, reason_code → `INELIGIBLE_WORKFLOW`
   - Passing outcome: continue to ATS3

3. **ATS3 - Workflow Classification and Routing**
   - RoutingService classifies workflow type
   - RoutingService resolves next step and accountable role
   - Resolved outcome: case state → `routed`, agent disposition → `completed`
   - Unresolved outcome: case state → `queued_for_review`, reason_code → `UNRESOLVED_ROUTE`

### Event Recording
All transitions recorded via AuditService:
- `case_events` table: Append-only with correlation_id, decision_source, actor identity
- `audit_logs` table: Security/operational audit entries
- No UPDATE or DELETE operations allowed on event/audit tables

### Trace Assembly
CaseTraceService builds trace from canonical `case_events`:
1. Query events ordered by `occurred_at`
2. Group events by `step_id` to build steps array
3. Apply visibility policy based on viewer role
4. Append approval_chain placeholders (ATS4, ATS6, ATS8, ATS11, ATS14)

### Visibility Policy
- **External applicants**: See only events where `visible_to_external=true`
- **Internal reviewers**: See all events
- Restricted reasoning text masked for external viewers

## Agent Registry
All six agents preserved in registry:
- **AGN1** (Intake & Routing Agent): `executable_in_mvp=true`, responsible for ATS1-ATS3
- **AGN2** (Request Comprehension Agent): `executable_in_mvp=false`, responsible for ATS4
- **AGN3** (Origin Determination Agent): `executable_in_mvp=false`, responsible for ATS5-ATS7
- **AGN4** (Decision Drafting Agent): `executable_in_mvp=false`, responsible for ATS8-ATS9
- **AGN5** (Approval & Issuance Agent): `executable_in_mvp=false`, responsible for ATS10-ATS13
- **AGN6** (Dispute Adjudication Agent): `executable_in_mvp=false`, responsible for ATS14

## Key Services Implemented

### Agn1Orchestrator
- Executes ATS1-ATS3 intake workflow
- Invokes DeterministicRuleEngine for validation
- Invokes RoutingService for classification
- Records events via AuditService
- Returns IntakeOutcome with case state, step, role, reason codes

### DeterministicRuleEngine
- `evaluate_completeness()`: Checks mandatory field presence
- `evaluate_eligibility()`: Validates workflow type
- `evaluate_routing_constraints()`: Validates routing targets
- Returns RuleDecision with outcome, blocking flag, reason_code, rationale

### CaseTraceService
- `get_case_trace()`: Assembles complete trace from case_events
- Groups events by step_id to build steps array
- Applies VisibilityPolicyService filtering
- Includes approval_chain placeholders for future HITL gates

### AuditService
- `record_case_event()`: Append-only case event recording
- `record_security_audit()`: Append-only audit log recording
- Enforces immutability (no UPDATE or DELETE operations)

## Database Tables

### case_events
Append-only event stream with:
- `id`, `case_id`, `event_type`, `step_id`
- `decision_source` (agent | deterministic_rule | human | system)
- `actor_type`, `actor_id`
- `visible_to_external` (boolean)
- `reason_code`, `rationale_summary`, `evidence_ref`
- `correlation_id`, `payload_json`
- `occurred_at`, `created_at`, `updated_at`

### audit_logs
Compliance/security audit with:
- `id`, `case_id`, `event_category`, `severity`
- `actor_id`, `action`, `correlation_id`
- `entity_type`, `entity_id`, `details_json`
- `occurred_at`, `created_at`, `updated_at`

## Testing

All test files pass:
- `tests/test_agn1_orchestrator.py` - AGN1 orchestration logic
- `tests/test_deterministic_rule_engine.py` - Rule validation logic
- `tests/test_trace_service.py` - Trace assembly and visibility filtering
- `tests/test_trace_integration.py` - Full intake flow integration
- `tests/test_trace_acceptance.py` - API endpoint acceptance tests

## Dependencies
This task depends on:
- TASK-3: Case registration service, repositories, routing service foundation
- Existing models: CaseModel, CaseEventModel, AuditLogModel
- Existing middleware: CorrelationIdMiddleware

## Notes for UI Implementation
- Trace endpoint provides structured timeline for case history visualization
- Steps array shows workflow progress (completed, current, blocked, pending)
- Events array provides detailed audit trail with actor identification
- Approval chain placeholders indicate future governance gates (deferred from MVP)
- Exception actions require intake_exception_handler role (enforce in UI)
- External applicants should only see events where `visible_to_external=true`
