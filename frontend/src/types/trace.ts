/**
 * Trace and audit types
 */

export interface AuditLog {
  id: string
  case_id: string | null
  event_category: string
  severity: string
  actor_id: string | null
  action: string
  correlation_id: string | null
  entity_type: string | null
  entity_id: string | null
  details_json: Record<string, unknown>
  occurred_at: string
  created_at: string
  updated_at: string
}

export interface Step {
  step_id: string
  step_status: string
  decision_source: string
  actor_label: string | null
  rationale_summary: string | null
  evidence_ref: string | null
  occurred_at: string
}

export interface ApprovalStage {
  stage_step_id: string
  stage_status: string
  required_role: string
  notes: string | null
}

export interface CaseStepDTO {
  step_id: string
  step_status: string
  decision_source: string
  actor_label: string | null
  rationale_summary: string | null
  evidence_ref: string | null
  occurred_at: string
}

export interface CaseEventDTO {
  event_id: string
  event_type: string
  step_id: string | null
  decision_source: string
  actor_type: string
  actor_id: string
  visible_to_external: boolean
  reason_code: string | null
  rationale_summary: string | null
  evidence_ref: string | null
  correlation_id: string
  occurred_at: string
}

export interface ApprovalStageDTO {
  stage_step_id: string
  stage_status: string
  required_role: string
  notes: string | null
}

export interface CaseTraceResponse {
  case_id: string
  case_reference: string
  workflow_type: string
  current_step_id: string
  case_state: string
  steps: CaseStepDTO[]
  events: CaseEventDTO[]
  approval_chain: ApprovalStageDTO[]
}
