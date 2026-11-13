/**
 * Case types matching backend Pydantic schemas
 */

export interface CaseAttachment {
  id: string
  case_id: string
  file_name: string
  media_type: string
  storage_key: string
  created_at: string
  updated_at: string
}

export interface CaseModel {
  id: string
  case_reference: string
  workflow_type: string
  submission_channel: string
  applicant_reference: string
  applicant_name: string
  goods_description: string | null
  origin_country_code: string | null
  agreement_reference: string | null
  case_state: string
  current_step_id: string
  accountable_role: string
  registration_sync_status: string
  reason_codes_json: Record<string, unknown>
  submitted_at: string
  created_at: string
  updated_at: string
}

export interface CaseEvent {
  id: string
  case_id: string
  event_type: string
  step_id: string
  decision_source: string
  actor_type: string
  actor_id: string
  visible_to_external: boolean
  reason_code: string | null
  rationale_summary: string | null
  evidence_ref: string | null
  correlation_id: string
  payload_json: Record<string, unknown>
  occurred_at: string
  created_at: string
  updated_at: string
}

export interface AgentExecutionSummary {
  agent_id: string
  agent_name: string
  disposition: string
}

export interface CaseDetailResponse {
  case_id: string
  case_reference: string
  workflow_type: string
  submission_channel: string
  applicant_reference: string
  case_state: string
  current_step_id: string
  accountable_role: string
  registration_sync_status: string
  visible_reason_codes: Array<{
    reason_code: string
    rationale_summary: string
    decision_source: string
  }>
  applicant_name?: string
  goods_description?: string
  origin_country_code?: string
  agreement_reference?: string
  locale?: string
  agent_execution?: AgentExecutionSummary
  created_at: string
  updated_at: string
}

export interface ExceptionActionRequest {
  action_type: 'request_correction' | 'close_rejected' | 'manual_route_resolution'
  comment: string
  resolved_workflow_type?: string
  resolved_next_step_id?: string
  resolved_accountable_role?: string
}

export interface ExceptionActionResponse {
  case_id: string
  case_state: string
  current_step_id: string
  accountable_role: string
  recorded_event_id: string
  updated_at: string
}
