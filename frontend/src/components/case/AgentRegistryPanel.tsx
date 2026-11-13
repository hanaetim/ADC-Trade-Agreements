/**
 * Agent Registry Panel Component
 * Shows registered agents with their status
 */

export function AgentRegistryPanel() {
  const agents = [
    { id: 'AGN1', name: 'Intake & Routing Agent', active: true },
    { id: 'AGN2', name: 'Request Comprehension Agent', active: false },
    { id: 'AGN3', name: 'Origin Determination Agent', active: false },
    { id: 'AGN4', name: 'Decision Drafting Agent', active: false },
    { id: 'AGN5', name: 'Approval & Issuance Agent', active: false },
    { id: 'AGN6', name: 'Dispute Adjudication Agent', active: false },
  ]

  return (
    <section className="card mb-5" aria-labelledby="agent-title">
      <div className="card-head">
        <div>
          <h2 id="agent-title">Agent registry</h2>
          <p>All six agents registered. Only AGN1 is executable in this release.</p>
        </div>
      </div>
      <div className="card-body">
        <div className="grid grid-cols-4 gap-4">
          {agents.map((agent) => (
            <div
              key={agent.id}
              className={`card p-4 ${
                agent.active
                  ? 'border-success-fg border-4'
                  : 'border-2 border-dashed border-border-strong'
              }`}
            >
              <div className="font-mono text-lg font-bold mb-1">
                {agent.id}
              </div>
              <div className="text-sm mb-2">
                {agent.name}
              </div>
              <div>
                <span className={`badge ${agent.active ? 'st-routed' : 'st-queued'} text-xs`}>
                  {agent.active ? 'active' : 'registered'}
                </span>
              </div>
            </div>
          ))}
        </div>
        <p className="hint text-xs mt-4">
          AGN1 (active, green border) executes ATS1–ATS3 intake workflow. 
          AGN2–AGN6 (registered, dashed border) are preserved for future phases.
        </p>
      </div>
    </section>
  )
}
