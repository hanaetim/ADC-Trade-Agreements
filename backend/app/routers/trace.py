"""Trace router - case trace and approval chain endpoint (FR-023, FR-024)."""
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user
from app.schemas.auth import AuthUser
from app.schemas.trace import CaseTraceResponse
from app.services.case_trace_service import CaseTraceService

router = APIRouter()


@router.get("/{case_id}/trace", response_model=CaseTraceResponse)
def get_case_trace(
    case_id: UUID,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> CaseTraceResponse:
    """Get complete case trace view with steps, events, and approval chain (FR-023, FR-024).

    Returns:
    - Ordered atomic-step visibility records
    - Detailed visible event stream
    - Future HITL approval gate placeholders

    Visibility filtering applied based on viewer role:
    - External applicants see only events where visible_to_external=True
    - Internal reviewers see all events

    Requires authentication.
    """
    # Get viewer role from authenticated user
    viewer_role = current_user.role

    try:
        trace_service = CaseTraceService(db)
        return trace_service.get_case_trace(case_id, viewer_role)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
