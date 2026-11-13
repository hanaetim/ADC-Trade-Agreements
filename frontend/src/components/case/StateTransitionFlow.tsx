/**
 * State Transition Flow Component
 * Visual flow showing case progression through states
 */

interface StateTransitionFlowProps {
  caseState: string
}

export function StateTransitionFlow({ caseState }: StateTransitionFlowProps) {
  const getNodeClass = (state: string) => {
    if (state === 'submitted' || state === 'registered') {
      return 'flow-node visited'
    }
    if (state === caseState) {
      return 'flow-node current'
    }
    return 'flow-node possible'
  }

  return (
    <section className="card" aria-labelledby="flow-title">
      <div className="card-head">
        <div>
          <h2 id="flow-title">Where this case is in its life</h2>
          <p>The case moved from submitted to registered. Dashed states are possible next states.</p>
        </div>
      </div>
      <div className="card-body">
        <div className="flow" role="list">
          <div className={getNodeClass('submitted')} role="listitem">
            <span className="nm font-mono font-bold block">submitted</span>
            Case received
          </div>
          
          <span className="flow-arrow" aria-hidden="true">&rarr;</span>
          
          <div className={getNodeClass('registered')} role="listitem">
            <span className="nm font-mono font-bold block">registered</span>
            Case record created
          </div>
          
          <span className="flow-arrow" aria-hidden="true">&rarr;</span>
          
          <div 
            className={getNodeClass('intake_blocked')} 
            role="listitem"
            {...(caseState === 'intake_blocked' ? { 'aria-current': 'step' } : {})}
          >
            <span className="nm font-mono font-bold block">intake_blocked</span>
            {caseState === 'intake_blocked' ? (
              <strong>You are here</strong>
            ) : (
              'Rule check failed'
            )}
          </div>
          
          <span className="flow-arrow" aria-hidden="true">&rarr;</span>
          
          <div className="flow-branch flex flex-col gap-2">
            <div className={getNodeClass('queued_for_review')}>
              <span className="nm font-mono font-bold block">queued_for_review</span>
              After request_correction
            </div>
            <div className={getNodeClass('closed_rejected')}>
              <span className="nm font-mono font-bold block">closed_rejected</span>
              After close_rejected
            </div>
          </div>
          
          <span className="flow-arrow" aria-hidden="true">&rarr;</span>
          
          <div className={getNodeClass('routed')}>
            <span className="nm font-mono font-bold block">routed</span>
            After manual route resolution from queued_for_review
          </div>
        </div>
      </div>
    </section>
  )
}
