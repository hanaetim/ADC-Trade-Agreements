"""Case management API endpoints (FR-001, FR-023, FR-024)."""
import uuid
from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user
from app.repositories.case_repository import CaseRepository
from app.schemas.auth import AuthUser
from app.schemas.case import (
    CaseDetailResponse,
    CaseListItem,
    CaseListResponse,
    CaseRecordResponse,
    CreateCaseRequest,
    ReasonCodeDetail,
)
from app.schemas.trace import ExceptionActionRequest, ExceptionActionResponse
from app.services.audit_service import AuditService
from app.services.case_registration_service import CaseRegistrationService

router = APIRouter(prefix="/v1/cases", tags=["cases"])


@router.post("", response_model=CaseRecordResponse, status_code=status.HTTP_201_CREATED)
def register_case(
    request: Request,
    command: CreateCaseRequest,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> CaseRecordResponse:
    """Register a new case with intake validation and routing (FR-001, FR-002, FR-004).

    Steps:
    1. Create unique case record with generated case_reference
    2. Invoke ICOS registration adapter for sync
    3. Invoke AGN1 orchestrator for ATS1-ATS3 intake workflow
    4. Return case record response

    Requires authentication.
    """
    # Get correlation ID from middleware
    correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))

    try:
        service = CaseRegistrationService(db)
        result = service.register_case(command, correlation_id)

        return CaseRecordResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=CaseListResponse)
def list_cases(
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    workflow_type: Optional[str] = None,
    case_state: Optional[str] = None,
    assigned_role: Optional[str] = None,
) -> CaseListResponse:
    """List cases with pagination and optional filters (FR-023).

    Query Parameters:
    - limit: Page size (default 20)
    - offset: Offset for pagination (default 0)
    - workflow_type: Filter by workflow type
    - case_state: Filter by case state
    - assigned_role: Filter by accountable role

    Requires authentication.
    """
    repo = CaseRepository(db)
    cases, total = repo.list_cases(
        limit=limit,
        offset=offset,
        workflow_type=workflow_type,
        case_state=case_state,
        assigned_role=assigned_role,
    )

    # Build list items
    items = []
    for case in cases:
        # Extract latest reason code
        reason_codes: list[str] = case.reason_codes_json if isinstance(case.reason_codes_json, list) else []
        latest_reason_code = reason_codes[-1] if reason_codes else None

        items.append(
            CaseListItem(
                case_id=case.id,
                case_reference=case.case_reference,
                workflow_type=case.workflow_type,
                case_state=case.case_state,
                current_step_id=case.current_step_id,
                accountable_role=case.accountable_role,
                latest_reason_code=latest_reason_code,
                registration_sync_status=case.registration_sync_status,
                created_at=case.created_at,
                updated_at=case.updated_at,
            )
        )

    # Calculate page number
    page = (offset // limit) + 1 if limit > 0 else 1

    return CaseListResponse(
        items=items,
        total=total,
        page=page,
        page_size=limit,
    )


@router.get("/{case_id}", response_model=CaseDetailResponse)
def get_case(
    case_id: uuid.UUID,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> CaseDetailResponse:
    """Get case detail by ID (FR-001, FR-023).

    Returns case summary with visibility rules appropriate to caller role.

    Requires authentication.
    """
    repo = CaseRepository(db)
    case = repo.get_by_id(case_id)

    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    # Build visible reason codes from case events
    from app.repositories.case_event_repository import CaseEventRepository
    
    event_repo = CaseEventRepository(db)
    events = event_repo.list_by_case(case_id)
    
    reason_code_details: list[ReasonCodeDetail] = []
    for event in events:
        if event.reason_code:
            reason_code_details.append(
                ReasonCodeDetail(
                    reason_code=event.reason_code,
                    rationale_summary=event.rationale_summary or "",
                    decision_source=event.decision_source,
                )
            )

    return CaseDetailResponse(
        case_id=case.id,
        case_reference=case.case_reference,
        workflow_type=case.workflow_type,
        submission_channel=case.submission_channel,
        applicant_reference=case.applicant_reference,
        applicant_name=case.applicant_name,
        case_state=case.case_state,
        current_step_id=case.current_step_id,
        accountable_role=case.accountable_role,
        registration_sync_status=case.registration_sync_status,
        visible_reason_codes=reason_code_details,
        locale=getattr(case, 'locale', None),
        agent_execution=None,  # TODO: Build from case events for AGN1 execution
        created_at=case.created_at,
        updated_at=case.updated_at,
    )


@router.post("/{case_id}/exception-actions", response_model=ExceptionActionResponse)
def record_exception_action(
    request: Request,
    case_id: uuid.UUID,
    action: ExceptionActionRequest,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> ExceptionActionResponse:
    """Record intake exception action (FR-002, FR-004).

    Allows intake_exception_handler role to record:
    - Manual correction request
    - Eligibility override rejection
    - Manual routing resolution

    Requires:
    - Case must be in intake_blocked or queued_for_review state
    - Caller must have intake_exception_handler role
    - Manual route resolution requires resolved_* fields

    Requires authentication and intake_exception_handler role.
    """
    # Check role authorization
    if current_user.role != "intake_exception_handler":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Required role: intake_exception_handler",
        )

    # Get correlation ID from middleware
    correlation_id = getattr(request.state, "correlation_id", str(uuid.uuid4()))

    # Load case
    repo = CaseRepository(db)
    case = repo.get_by_id(case_id)
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found")

    # Validate case state
    if case.case_state not in ("intake_blocked", "queued_for_review"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Exception actions not allowed for cases in state {case.case_state}",
        )

    # Validate action type requirements
    if action.action_type == "manual_route_resolution":
        if not all([action.resolved_workflow_type, action.resolved_next_step_id, action.resolved_accountable_role]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="manual_route_resolution requires resolved_workflow_type, resolved_next_step_id, and resolved_accountable_role",
            )

    # Update case based on action type
    audit_service = AuditService(db)

    if action.action_type == "close_rejected":
        case.case_state = "closed_rejected"
        event_type = "exception_close_rejected"
    elif action.action_type == "manual_route_resolution":
        case.case_state = "routed"
        case.workflow_type = action.resolved_workflow_type or case.workflow_type
        case.current_step_id = action.resolved_next_step_id or case.current_step_id
        case.accountable_role = action.resolved_accountable_role or case.accountable_role
        event_type = "exception_manual_route"
    else:  # request_correction
        case.case_state = "queued_for_review"
        event_type = "exception_request_correction"

    case.updated_at = datetime.now(timezone.utc)
    db.flush()

    # Record event
    event_id = audit_service.record_case_event(
        case_id=case.id,
        event_type=event_type,
        step_id=case.current_step_id,
        decision_source="human",
        actor_type="human",
        actor_id=str(current_user.user_id),
        correlation_id=correlation_id,
        visible_to_external=False,
        rationale_summary=action.comment,
        payload={
            "action_type": action.action_type,
            "resolved_workflow_type": action.resolved_workflow_type,
            "resolved_next_step_id": action.resolved_next_step_id,
            "resolved_accountable_role": action.resolved_accountable_role,
        },
    )

    db.commit()
    db.refresh(case)

    return ExceptionActionResponse(
        case_id=case.id,
        case_state=case.case_state,
        current_step_id=case.current_step_id,
        accountable_role=case.accountable_role,
        recorded_event_id=event_id,
        updated_at=case.updated_at,
    )
