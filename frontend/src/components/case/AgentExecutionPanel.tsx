/**
 * Agent Execution Panel Component
 * Shows agent execution summary
 */

import { Link } from 'react-router-dom'
import type { AgentExecutionSummary } from '../../types'

interface AgentExecutionPanelProps {
  agentExecution: AgentExecutionSummary
}

export function AgentExecutionPanel({ agentExecution }: AgentExecutionPanelProps) {
  return (
    <section className="card" aria-labelledby="agn-title">
      <div className="card-head">
        <div>
          <h2 id="agn-title">Agent at work on this case</h2>
          <p>Only the intake agent and the rule engine run in this release.</p>
        </div>
        <Link to="trace" className="btn btn-secondary btn-sm">Open full trace</Link>
      </div>
      <div className="card-body">
        <div className="agent-box">
          <div>
            <span className="k block text-xs text-text-muted font-semibold">Agent</span>
            <span className="src src-agent">
              {agentExecution.agent_id} · {agentExecution.agent_name}
            </span>
            <span className="sub-line mono">agent_id={agentExecution.agent_id}</span>
          </div>
          <div>
            <span className="k block text-xs text-text-muted font-semibold">Disposition</span>
            <span className={`badge st-${agentExecution.disposition.replace('_', '-')}`}>
              {agentExecution.disposition}
            </span>
            <span className="sub-line mono">disposition={agentExecution.disposition}</span>
          </div>
          <div>
            <span className="k block text-xs text-text-muted font-semibold">Authority</span>
            {agentExecution.disposition === 'blocked' ? (
              <>
                <span className="src src-rule">Deterministic Rule Engine</span>
                <span className="sub-line">The rule result decided the outcome, not the agent.</span>
              </>
            ) : (
              <>
                <span className="src src-agent">{agentExecution.agent_name}</span>
                <span className="sub-line">Agent orchestration completed successfully.</span>
              </>
            )}
          </div>
        </div>
      </div>
    </section>
  )
}
