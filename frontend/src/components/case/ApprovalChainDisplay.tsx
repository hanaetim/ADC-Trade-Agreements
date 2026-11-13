/**
 * Approval Chain Display Component
 * Shows future HITL approval gates as placeholders
 */

import type { ApprovalStageDTO } from '../../types'

interface ApprovalChainDisplayProps {
  approvalChain: ApprovalStageDTO[]
}

export function ApprovalChainDisplay({ approvalChain }: ApprovalChainDisplayProps) {
  const gateLabels: Record<string, string> = {
    'ATS4': 'Specialist Fact Review',
    'ATS6': 'Specialist Determination Verification',
    'ATS8': 'Section Head Decision Review',
    'ATS11': 'Final Approval',
    'ATS14': 'Technical Committee Adjudication',
  }

  return (
    <section className="card mb-5" aria-labelledby="approval-title">
      <div className="card-head">
        <div>
          <h2 id="approval-title">Approval chain visibility</h2>
          <p>Future HITL approval gates preserved as visible governance checkpoints (deferred from MVP).</p>
        </div>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-5 gap-4">
          {approvalChain.map((stage) => (
            <div 
              key={stage.stage_step_id} 
              className="card border-2 border-dashed border-border-strong bg-surface-alt"
              style={{ borderStyle: 'dashed' }}
            >
              <div className="card-body p-4">
                <div className="flex items-center gap-2 mb-2">
                  <span className="font-mono text-xl font-bold text-future-fg">
                    {stage.stage_step_id}
                  </span>
                  <span className="gate-tag badge st-queued text-xs">gate</span>
                </div>
                <div className="text-sm font-semibold mb-1">
                  {gateLabels[stage.stage_step_id] || 'Future stage'}
                </div>
                <div className="text-xs text-text-muted mb-2">
                  Role: {stage.required_role.replace(/_/g, ' ')}
                </div>
                <div className="text-xs text-text-muted mb-2">
                  Status: <span className="italic">{stage.stage_status}</span>
                </div>
                {stage.notes && (
                  <div className="text-xs italic text-text-muted mt-2">
                    {stage.notes}
                  </div>
                )}
                <div className="text-center mt-3">
                  <svg className="inline-block w-5 h-5 text-text-muted" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
            </div>
          ))}
        </div>
        <p className="hint text-xs mt-4">
          These approval gates are preserved in the design but not executable in this release. 
          They will become active decision points in future phases.
        </p>
      </div>
    </section>
  )
}
