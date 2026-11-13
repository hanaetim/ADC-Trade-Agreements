/**
 * Case Trace Page
 * Implements wireframe_case_trace.html
 * Shows complete case trace with steps, events, and approval chain
 */

import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiClient } from '../lib/api-client'
import { useAuth } from '../lib/auth-context'
import type { CaseTraceResponse } from '../types'
import { CaseTraceTimeline } from '../components/case/CaseTraceTimeline'
import { DetailedEventStream } from '../components/case/DetailedEventStream'
import { ApprovalChainDisplay } from '../components/case/ApprovalChainDisplay'
import { AgentRegistryPanel } from '../components/case/AgentRegistryPanel'

export function CaseTracePage() {
  const { caseId } = useParams<{ caseId: string }>()
  const { user } = useAuth()
  const [trace, setTrace] = useState<CaseTraceResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const loadTrace = async () => {
      if (!caseId) return
      
      setIsLoading(true)
      setError(null)
      
      try {
        const data = await apiClient.get<CaseTraceResponse>(`/cases/${caseId}/trace`)
        setTrace(data)
      } catch (err) {
        const message = err instanceof Error ? err.message : 'Failed to load trace'
        setError(message)
      } finally {
        setIsLoading(false)
      }
    }

    loadTrace()
  }, [caseId])

  if (isLoading) {
    return (
      <div className="w-full p-6">
        <div role="status" className="text-text-muted">Loading trace…</div>
      </div>
    )
  }

  if (error || !trace) {
    return (
      <div className="w-full p-6">
        <div className="alert alert-danger" role="alert">
          <div>
            <strong>Trace not found (404)</strong>
            {error || 'The case trace does not exist or is not visible to you.'}
          </div>
          <Link to="/cases" className="btn btn-secondary btn-sm">Back to cases</Link>
        </div>
      </div>
    )
  }

  return (
    <div className="w-full">
      {/* Breadcrumb */}
      <nav className="crumbs" aria-label="Breadcrumb">
        <ol>
          <li><Link to="/cases">Cases</Link></li>
          <li><span className="mono">{trace.case_reference}</span></li>
          <li><span aria-current="page">Trace</span></li>
        </ol>
      </nav>

      {/* Main content */}
      <main className="p-6">
        {/* Page head */}
        <div className="page-head">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3 flex-wrap">
              <span className="ref font-mono font-bold">{trace.case_reference}</span>
              <span className={`badge st-${trace.case_state.replace('_', '-')}`}>
                {trace.case_state}
              </span>
            </h1>
            <p className="desc mt-2 text-text-muted max-w-4xl">
              Trace &amp; Approval Chain · <code>{trace.workflow_type}</code> · 
              Current step: <code>{trace.current_step_id}</code>
            </p>
          </div>
        </div>

        {/* Case tabs */}
        <div className="case-tabs mt-5" role="navigation" aria-label="Case sections">
          <Link to={`/cases/${caseId}`} className="text-text-muted">
            Case detail
          </Link>
          <Link to={`/cases/${caseId}/trace`} aria-current="page" className="text-primary border-b-4 border-primary">
            Trace
          </Link>
        </div>

        {/* Facts strip */}
        <div className="card mb-5">
          <div className="card-body">
            <div className="grid grid-cols-5 gap-4">
              <div>
                <div className="text-xs text-text-muted font-semibold">Case reference</div>
                <div className="font-mono font-bold">{trace.case_reference}</div>
              </div>
              <div>
                <div className="text-xs text-text-muted font-semibold">Workflow type</div>
                <div><code>{trace.workflow_type}</code></div>
              </div>
              <div>
                <div className="text-xs text-text-muted font-semibold">Case state</div>
                <div>
                  <span className={`badge st-${trace.case_state.replace('_', '-')}`}>
                    {trace.case_state}
                  </span>
                </div>
              </div>
              <div>
                <div className="text-xs text-text-muted font-semibold">Current step</div>
                <div><code>{trace.current_step_id}</code></div>
              </div>
              <div>
                <div className="text-xs text-text-muted font-semibold">Accountable role</div>
                <div className="text-sm">{trace.current_step_id}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Atomic steps section */}
        <CaseTraceTimeline steps={trace.steps} />

        {/* Detailed event stream */}
        <DetailedEventStream events={trace.events} viewerRole={user?.role || 'external_applicant'} />

        {/* Approval chain visibility */}
        <ApprovalChainDisplay approvalChain={trace.approval_chain} />

        {/* Agent registry */}
        <AgentRegistryPanel />

        {/* Legend */}
        <section className="card">
          <div className="card-head">
            <div>
              <h2>Legend</h2>
            </div>
          </div>
          <div className="card-body">
            <div className="grid grid-cols-2 gap-6">
              <div>
                <h3 className="text-base font-semibold mb-2">Badge shapes</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="badge st-routed">completed</span>
                    <span>Circle = completed state</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="badge st-blocked">blocked</span>
                    <span>Square = blocked state</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="badge st-queued">pending</span>
                    <span>Diamond = pending state</span>
                  </div>
                </div>
              </div>
              <div>
                <h3 className="text-base font-semibold mb-2">Decision source indicators</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2">
                    <span className="src src-rule">Rule</span>
                    <span>Filled square = deterministic rule</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="src src-agent">Agent</span>
                    <span>Diamond = agent decision</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="src src-human">Human</span>
                    <span>Filled circle = human action</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="src src-system">System</span>
                    <span>Hollow circle = system event</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
