/**
 * Case Trace Timeline Component
 * Shows atomic steps table with status badges
 */

import type { CaseStepDTO } from '../../types'

interface CaseTraceTimelineProps {
  steps: CaseStepDTO[]
}

export function CaseTraceTimeline({ steps }: CaseTraceTimelineProps) {
  const getStatusBadgeClass = (status: string) => {
    const statusMap: Record<string, string> = {
      'ss-completed': 'st-routed',
      'ss-current': 'st-registered',
      'ss-blocked': 'st-blocked',
      'ss-pending': 'st-queued',
      'ss-deferred': 'st-queued',
      'completed': 'st-routed',
      'current': 'st-registered',
      'blocked': 'st-blocked',
      'pending': 'st-queued',
      'deferred': 'st-queued',
    }
    return statusMap[status] || 'st-queued'
  }

  const getDecisionSourceClass = (source: string) => {
    const sourceMap: Record<string, string> = {
      'deterministic_rule': 'src-rule',
      'agent': 'src-agent',
      'human': 'src-human',
      'system': 'src-system',
    }
    return `src ${sourceMap[source] || 'src-system'}`
  }

  return (
    <section className="card mb-5" aria-labelledby="steps-title">
      <div className="card-head">
        <div>
          <h2 id="steps-title">Atomic steps</h2>
          <p>Each row is one step in the workflow. Status colors show progress.</p>
        </div>
      </div>
      <div className="card-body">
        <table className="mini w-full">
          <thead>
            <tr>
              <th scope="col">Step ID</th>
              <th scope="col">Status</th>
              <th scope="col">Decision Source</th>
              <th scope="col">Actor</th>
              <th scope="col">Rationale Summary</th>
              <th scope="col">Evidence Ref</th>
              <th scope="col">Occurred At</th>
            </tr>
          </thead>
          <tbody>
            {steps.length === 0 ? (
              <tr>
                <td colSpan={7} className="text-center text-text-muted">
                  No steps recorded yet
                </td>
              </tr>
            ) : (
              steps.map((step) => (
                <tr key={step.step_id}>
                  <td className="font-mono">{step.step_id}</td>
                  <td>
                    <span className={`badge ${getStatusBadgeClass(step.step_status)}`}>
                      {step.step_status}
                    </span>
                  </td>
                  <td>
                    <span className={getDecisionSourceClass(step.decision_source)}>
                      {step.decision_source.replace('_', ' ')}
                    </span>
                  </td>
                  <td>{step.actor_label || '—'}</td>
                  <td>{step.rationale_summary || '—'}</td>
                  <td className="font-mono text-xs">{step.evidence_ref || '—'}</td>
                  <td className="font-mono text-xs">
                    {new Date(step.occurred_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
