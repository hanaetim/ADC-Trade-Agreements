"""Case request/response schemas (FR-001, FR-023, FR-024)."""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.workflow_taxonomy import WorkflowType


class AttachmentMetadata(BaseModel):
    """Attachment metadata for case submission."""

    attachment_id: uuid.UUID
    file_name: str
    media_type: str
    storage_key: str


class CreateCaseRequest(BaseModel):
    """Request payload for case registration (POST /api/v1/cases)."""

    submission_type: WorkflowType
    submission_channel: str = Field(..., max_length=32)
    applicant_reference: str = Field(..., max_length=128)
    applicant_name: str = Field(..., max_length=256)
    goods_description: Optional[str] = None
    origin_country_code: Optional[str] = Field(None, max_length=8)
    agreement_reference: Optional[str] = Field(None, max_length=64)
    attachments: list[AttachmentMetadata] = Field(default_factory=list)
    intake_notes: Optional[str] = None
    locale: Optional[str] = Field(None, max_length=2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "submission_type": "origin_ruling",
                "submission_channel": "portal",
                "applicant_reference": "APP-2026-00123",
                "applicant_name": "Example Company Ltd.",
                "goods_description": "Electronic components for industrial use",
                "origin_country_code": "CN",
                "agreement_reference": "FTA-GCC-RCEP",
                "attachments": [],
                "intake_notes": None,
                "locale": "en",
            }
        }
    )


class AgentExecutionSummary(BaseModel):
    """Agent execution summary for case registration response."""

    agent_id: str
    agent_name: str
    disposition: str


class CaseRecordResponse(BaseModel):
    """Response payload for case registration (FR-001)."""

    case_id: uuid.UUID
    case_reference: str
    workflow_type: str
    current_step_id: str
    case_state: str
    accountable_role: str
    registration_sync_status: str
    reason_codes: list[str]
    agent_execution: AgentExecutionSummary
    trace_event_ids: list[uuid.UUID]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseListItem(BaseModel):
    """Case summary for list view (FR-023)."""

    case_id: uuid.UUID
    case_reference: str
    workflow_type: str
    case_state: str
    current_step_id: str
    accountable_role: str
    latest_reason_code: Optional[str]
    registration_sync_status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CaseListResponse(BaseModel):
    """Paginated case list response."""

    items: list[CaseListItem]
    total: int
    page: int
    page_size: int

    model_config = ConfigDict(from_attributes=True)


class ReasonCodeDetail(BaseModel):
    """Reason code detail for case detail response."""

    reason_code: str
    rationale_summary: str
    decision_source: str


class CaseDetailResponse(BaseModel):
    """Case detail response (FR-001, FR-023)."""

    case_id: uuid.UUID
    case_reference: str
    workflow_type: str
    submission_channel: str
    applicant_reference: str
    applicant_name: Optional[str] = None
    case_state: str
    current_step_id: str
    accountable_role: str
    registration_sync_status: str
    visible_reason_codes: list[ReasonCodeDetail]
    locale: Optional[str] = None
    agent_execution: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
