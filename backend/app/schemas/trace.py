"""Trace and visibility response schemas (FR-023, FR-024)."""
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CaseStepDTO(BaseModel):
    """Single atomic step in case timeline."""

    step_id: str
    step_status: str  # completed, current, blocked, pending, deferred_placeholder
    decision_source: str  # agent, deterministic_rule, human, system
    actor_label: str
    rationale_summary: Optional[str] = None
    evidence_ref: Optional[str] = None
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseEventDTO(BaseModel):
    """Detailed event stream entry."""

    event_id: UUID
    event_type: str
    step_id: str
    decision_source: str
    actor_type: str
    actor_id: str
    visible_to_external: bool
    reason_code: Optional[str] = None
    rationale_summary: Optional[str] = None
    evidence_ref: Optional[str] = None
    correlation_id: str
    occurred_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ApprovalStageDTO(BaseModel):
    """Future HITL approval gate placeholder."""

    stage_step_id: str  # ATS4, ATS6, ATS8, ATS11, ATS14
    stage_status: str  # not_in_scope, future_visible_placeholder
    required_role: str
    notes: str  # Why visible but not executable in MVP

    model_config = ConfigDict(from_attributes=True)


class CaseTraceResponse(BaseModel):
    """Complete case trace view (FR-023, FR-024)."""

    case_id: UUID
    case_reference: str
    workflow_type: str
    current_step_id: str
    case_state: str
    steps: list[CaseStepDTO] = Field(default_factory=list)
    events: list[CaseEventDTO] = Field(default_factory=list)
    approval_chain: list[ApprovalStageDTO] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)


class ExceptionActionRequest(BaseModel):
    """Request body for intake exception action (FR-002, FR-004)."""

    action_type: str  # request_correction, close_rejected, manual_route_resolution
    comment: str
    resolved_workflow_type: Optional[str] = None
    resolved_next_step_id: Optional[str] = None
    resolved_accountable_role: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ExceptionActionResponse(BaseModel):
    """Response after recording exception action."""

    case_id: UUID
    case_state: str
    current_step_id: str
    accountable_role: str
    recorded_event_id: UUID
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
