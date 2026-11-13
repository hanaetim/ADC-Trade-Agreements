/**
 * Case Detail Page
 * Implements wireframe_case_detail.html
 * Shows case summary, state flow, reason codes, agent execution, and exception actions
 */

import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { apiClient } from '../lib/api-client'
import { useAuth } from '../lib/auth-context'
import type { CaseDetailResponse } from '../types'
import { CaseDetailView } from '../components/case/CaseDetailView'
import { ExceptionActionForm } from '../components/case/ExceptionActionForm'

export function CaseDetailPage() {
  const { caseId } = useParams<{ caseId: string }>()
  const { user } = useAuth()
  const [caseDetail, setCaseDetail] = useState<CaseDetailResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const loadCase = async () => {
    if (!caseId) return
    
    setIsLoading(true)
    setError(null)
    
    try {
      const data = await apiClient.get<CaseDetailResponse>(`/cases/${caseId}`)
      setCaseDetail(data)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load case'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    loadCase()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [caseId])

  const handleActionSuccess = () => {
    // Reload case data after successful action
    loadCase()
  }

  if (isLoading) {
    return (
      <div className="w-full p-6">
        <div role="status" className="text-text-muted">Loading case…</div>
      </div>
    )
  }

  if (error || !caseDetail) {
    return (
      <div className="w-full p-6">
        <div className="alert alert-danger" role="alert">
          <div>
            <strong>Case not found (404)</strong>
            {error || 'The case does not exist or is not visible to you.'}
          </div>
          <Link to="/cases" className="btn btn-secondary btn-sm">Back to cases</Link>
        </div>
      </div>
    )
  }

  const canTakeAction = 
    user?.role === 'intake_exception_handler' &&
    (caseDetail.case_state === 'intake_blocked' || caseDetail.case_state === 'queued_for_review')

  return (
    <div className="w-full">
      {/* Breadcrumb */}
      <nav className="crumbs" aria-label="Breadcrumb">
        <ol>
          <li><Link to="/cases">Cases</Link></li>
          <li><span className="mono">{caseDetail.case_reference}</span></li>
          <li><span aria-current="page">Detail</span></li>
        </ol>
      </nav>

      {/* Main content */}
      <main className="p-6">
        {/* Page head */}
        <div className="page-head">
          <div>
            <h1 className="text-3xl font-bold flex items-center gap-3 flex-wrap">
              <span className="ref font-mono font-bold">{caseDetail.case_reference}</span>
              <span className={`badge st-${caseDetail.case_state.replace('_', '-')}`}>
                {caseDetail.case_state}
              </span>
              <span className={`badge sync-${caseDetail.registration_sync_status === 'succeeded' ? 'ok' : caseDetail.registration_sync_status}`}>
                {caseDetail.registration_sync_status === 'succeeded' ? 'sync succeeded' : `sync ${caseDetail.registration_sync_status}`}
              </span>
            </h1>
            <p className="desc mt-2 text-text-muted max-w-4xl">
              {caseDetail.applicant_name || 'Unknown applicant'} · <code>{caseDetail.workflow_type}</code> · 
              received through {caseDetail.submission_channel} on {new Date(caseDetail.created_at).toLocaleDateString()} at {new Date(caseDetail.created_at).toLocaleTimeString()} UTC.
            </p>
          </div>
        </div>

        {/* Case tabs */}
        <div className="case-tabs mt-5" role="navigation" aria-label="Case sections">
          <Link to={`/cases/${caseId}`} aria-current="page" className="text-primary border-b-4 border-primary">
            Case detail
          </Link>
          <Link to={`/cases/${caseId}/trace`} className="text-text-muted">
            Trace
          </Link>
        </div>

        {/* Two column layout */}
        <div className="two-col">
          {/* Left column - case detail view */}
          <CaseDetailView caseDetail={caseDetail} />

          {/* Right column - actions */}
          <aside aria-label="Actions and status">
            {canTakeAction ? (
              <ExceptionActionForm
                caseId={caseDetail.case_id}
                caseState={caseDetail.case_state}
                onSuccess={handleActionSuccess}
              />
            ) : (
              <section className="card">
                <div className="card-head">
                  <div>
                    <h2>Actions</h2>
                  </div>
                </div>
                <div className="card-body">
                  <p className="text-sm">
                    {caseDetail.case_state === 'routed' && 'This case has been routed to its next step.'}
                    {caseDetail.case_state === 'closed_rejected' && 'This case is closed and cannot be changed.'}
                    {caseDetail.case_state === 'registered' && 'Intake checks are still running.'}
                    {!['routed', 'closed_rejected', 'registered', 'intake_blocked', 'queued_for_review'].includes(caseDetail.case_state) && 
                      'No actions available for this case state.'}
                    {(caseDetail.case_state === 'intake_blocked' || caseDetail.case_state === 'queued_for_review') && 
                      user?.role !== 'intake_exception_handler' &&
                      'Read-only for your role. Exception actions are recorded by the intake exception handler.'}
                  </p>
                </div>
              </section>
            )}

            {/* Future stages */}
            <section className="card mt-5">
              <div className="card-head">
                <div>
                  <h2>Next stages (not available in this release)</h2>
                </div>
              </div>
              <div className="card-body">
                <div className="chip-row flex flex-wrap gap-2" role="list">
                  <span className="future-chip" role="listitem">
                    <strong className="font-mono text-sm">ATS4</strong>
                    Future review stage
                  </span>
                  <span className="future-chip" role="listitem">
                    <strong className="font-mono text-sm">ATS6</strong>
                    Future review stage
                  </span>
                  <span className="future-chip" role="listitem">
                    <strong className="font-mono text-sm">ATS8</strong>
                    Future review stage
                  </span>
                  <span className="future-chip" role="listitem">
                    <strong className="font-mono text-sm">ATS11</strong>
                    Future review stage
                  </span>
                  <span className="future-chip" role="listitem">
                    <strong className="font-mono text-sm">ATS14</strong>
                    Future review stage
                  </span>
                </div>
                <p className="hint text-xs text-text-muted mt-3">
                  Read-only future stages. No action can be taken on these stages. 
                  The full chain is on the <Link to={`/cases/${caseId}/trace`} className="text-primary underline">Trace</Link> tab.
                </p>
              </div>
            </section>

            {/* Case ownership */}
            <section className="card mt-5">
              <div className="card-head">
                <div>
                  <h2>Case ownership</h2>
                </div>
              </div>
              <div className="card-body">
                <p className="text-sm m-0">
                  Held by <strong>{caseDetail.accountable_role.replace(/_/g, ' ')}</strong>. 
                  Updated {new Date(caseDetail.updated_at).toLocaleString()} UTC.
                </p>
              </div>
            </section>
          </aside>
        </div>
      </main>
    </div>
  )
}
