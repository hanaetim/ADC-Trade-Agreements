/**
 * Case Detail View Component
 * Shows case summary, state transition flow, reason codes, and agent execution
 */

import type { CaseDetailResponse } from '../../types'
import { StateTransitionFlow } from './StateTransitionFlow'
import { AgentExecutionPanel } from './AgentExecutionPanel'

interface CaseDetailViewProps {
  caseDetail: CaseDetailResponse
}

export function CaseDetailView({ caseDetail }: CaseDetailViewProps) {
  return (
    <div>
      {/* Summary card */}
      <section className="card" aria-labelledby="sum-title">
        <div className="card-head">
          <div>
            <h2 id="sum-title">Case summary</h2>
            <p>Record content as received at intake.</p>
          </div>
          <span className="tag">GET /api/v1/cases/{'{case_id}'}</span>
        </div>
        <div className="card-body">
          <dl className="facts">
            <dt>
              Case reference
              <span className="fname">case_reference</span>
            </dt>
            <dd className="ref font-mono font-bold">{caseDetail.case_reference}</dd>

            <dt>
              Workflow type
              <span className="fname">workflow_type</span>
            </dt>
            <dd><code>{caseDetail.workflow_type}</code></dd>

            <dt>
              Submission channel
              <span className="fname">submission_channel</span>
            </dt>
            <dd><code>{caseDetail.submission_channel}</code></dd>

            <dt>
              Applicant reference
              <span className="fname">applicant_reference</span>
            </dt>
            <dd><code>{caseDetail.applicant_reference}</code></dd>

            <dt>
              Applicant
              <span className="fname">applicant_name</span>
            </dt>
            <dd>{caseDetail.applicant_name || 'Not provided'}</dd>

            <dt>
              Case state
              <span className="fname">case_state</span>
            </dt>
            <dd>
              <span className={`badge st-${caseDetail.case_state.replace('_', '-')}`}>
                {caseDetail.case_state}
              </span>
            </dd>

            <dt>
              Current step
              <span className="fname">current_step_id</span>
            </dt>
            <dd><code>{caseDetail.current_step_id}</code></dd>

            <dt>
              Accountable role
              <span className="fname">accountable_role</span>
            </dt>
            <dd>
              {caseDetail.accountable_role.replace(/_/g, ' ')}
              <span className="sub-line mono">{caseDetail.accountable_role}</span>
            </dd>

            <dt>
              Created
              <span className="fname">created_at</span>
            </dt>
            <dd className="mono">{caseDetail.created_at}</dd>

            <dt>
              Updated
              <span className="fname">updated_at</span>
            </dt>
            <dd className="mono">{caseDetail.updated_at}</dd>

            <dt>
              Registration sync
              <span className="fname">registration_sync_status</span>
            </dt>
            <dd>
              <span className={`badge sync-${caseDetail.registration_sync_status === 'succeeded' ? 'ok' : caseDetail.registration_sync_status}`}>
                {caseDetail.registration_sync_status}
              </span>
              <span className="sub-line">
                {caseDetail.registration_sync_status === 'succeeded' 
                  ? 'Recorded in the system of record'
                  : 'Sync status: ' + caseDetail.registration_sync_status}
              </span>
            </dd>

            {caseDetail.locale && (
              <>
                <dt>
                  Preferred language
                  <span className="fname">locale</span>
                </dt>
                <dd><code>{caseDetail.locale}</code></dd>
              </>
            )}
          </dl>
        </div>
      </section>

      {/* State-transition flow */}
      <StateTransitionFlow caseState={caseDetail.case_state} />

      {/* Why this state */}
      {caseDetail.visible_reason_codes && caseDetail.visible_reason_codes.length > 0 && (
        <section className="card" aria-labelledby="why-title">
          <div className="card-head">
            <div>
              <h2 id="why-title">Why this state</h2>
              <p>Reason codes and routing basis recorded for this case.</p>
            </div>
            <span className="tag">visible_reason_codes</span>
          </div>
          <div className="card-body">
            {caseDetail.visible_reason_codes.map((reason, index) => (
              <div key={index} className="reason-box mb-4">
                <strong className="block text-base">
                  <code>{reason.reason_code}</code>
                </strong>
                {reason.rationale_summary}
                <div className="mt-2">
                  <span className={`src src-${reason.decision_source.replace('_', '-')}`}>
                    {reason.decision_source.replace('_', ' ')}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Agent execution panel */}
      {caseDetail.agent_execution && (
        <AgentExecutionPanel agentExecution={caseDetail.agent_execution} />
      )}
    </div>
  )
}
