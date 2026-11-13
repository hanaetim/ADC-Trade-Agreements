/**
 * Exception Action Form Component
 * Allows intake exception handler to record actions on blocked/queued cases
 */

import { useState, FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { apiClient } from '../../lib/api-client'
import type { ExceptionActionRequest, ExceptionActionResponse } from '../../types'

interface ExceptionActionFormProps {
  caseId: string
  caseState: string
  onSuccess: () => void
}

export function ExceptionActionForm({ caseId, caseState, onSuccess }: ExceptionActionFormProps) {
  const [actionType, setActionType] = useState<'request_correction' | 'close_rejected' | 'manual_route_resolution'>('request_correction')
  const [comment, setComment] = useState('')
  const [resolvedWorkflowType, setResolvedWorkflowType] = useState('origin_ruling')
  const [resolvedNextStepId, setResolvedNextStepId] = useState('ATS3')
  const [resolvedAccountableRole, setResolvedAccountableRole] = useState('intake_exception_handler')
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState<ExceptionActionResponse | null>(null)
  const [validationError, setValidationError] = useState<string | null>(null)

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    
    // Validate comment
    if (!comment.trim()) {
      setValidationError('Enter a comment that explains this action.')
      return
    }
    
    setValidationError(null)
    setError(null)
    setSuccess(null)
    setIsSubmitting(true)

    try {
      const payload: ExceptionActionRequest = {
        action_type: actionType,
        comment: comment.trim(),
      }

      if (actionType === 'manual_route_resolution') {
        payload.resolved_workflow_type = resolvedWorkflowType
        payload.resolved_next_step_id = resolvedNextStepId
        payload.resolved_accountable_role = resolvedAccountableRole
      }

      const response = await apiClient.post<ExceptionActionResponse>(
        `/cases/${caseId}/exception-actions`,
        payload
      )
      
      setSuccess(response)
      setComment('')
      
      // Call onSuccess to refresh parent
      setTimeout(() => {
        onSuccess()
      }, 1500)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to record action'
      setError(message)
    } finally {
      setIsSubmitting(false)
    }
  }

  const isManualRoute = actionType === 'manual_route_resolution'
  const manualRouteEnabled = caseState === 'queued_for_review'

  return (
    <section className="card" style={{ border: '3px solid var(--color-primary)' }} aria-labelledby="act-title">
      <div className="card-head">
        <div>
          <h2 id="act-title">Record an exception action</h2>
          <p>
            Available because the case is in <code>{caseState}</code>. 
            Each action is recorded as a human decision.
          </p>
        </div>
      </div>
      <div className="card-body">
        {success && (
          <div className="alert alert-success" role="status">
            <div>
              <strong>Action recorded: {success.case_state}</strong>
              The case has been updated successfully.
            </div>
          </div>
        )}

        {error && (
          <div className="alert alert-danger" role="alert">
            <div>
              <strong>The action was not recorded</strong>
              {error}
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} aria-label="Record exception action">
          <fieldset>
            <legend>
              Action type <span className="fname mono">action_type</span>
            </legend>
            
            <label className="opt">
              <input
                type="radio"
                name="action_type"
                value="request_correction"
                checked={actionType === 'request_correction'}
                onChange={() => setActionType('request_correction')}
              />
              <span>
                <span className="code">request_correction</span> · Ask the applicant to correct the submission
                <span className="on">Result: the case moves to <code>queued_for_review</code> while the correction is awaited.</span>
              </span>
            </label>

            <label className="opt">
              <input
                type="radio"
                name="action_type"
                value="close_rejected"
                checked={actionType === 'close_rejected'}
                onChange={() => setActionType('close_rejected')}
              />
              <span>
                <span className="code">close_rejected</span> · Close the case as not accepted
                <span className="on">Result: the case moves to <code>closed_rejected</code>.</span>
              </span>
            </label>

            <label className="opt">
              <input
                type="radio"
                name="action_type"
                value="manual_route_resolution"
                checked={actionType === 'manual_route_resolution'}
                onChange={() => setActionType('manual_route_resolution')}
                disabled={!manualRouteEnabled}
              />
              <span>
                <span className="code">manual_route_resolution</span> · Resolve the route yourself
                <span className="on">
                  {manualRouteEnabled
                    ? 'Result: the case moves to routed.'
                    : `Not available now. It applies to cases in queued_for_review (current: ${caseState}).`}
                </span>
              </span>
            </label>
          </fieldset>

          {isManualRoute && manualRouteEnabled && (
            <div className="space-y-4 mt-4">
              <div className="field">
                <label htmlFor="rwt">
                  Resolved workflow type
                  <span className="fname">resolved_workflow_type</span>
                </label>
                <select
                  id="rwt"
                  value={resolvedWorkflowType}
                  onChange={(e) => setResolvedWorkflowType(e.target.value)}
                >
                  <option value="origin_ruling">origin_ruling</option>
                  <option value="agreement_update">agreement_update</option>
                  <option value="inquiry">inquiry</option>
                  <option value="study">study</option>
                  <option value="certificate_sampling">certificate_sampling</option>
                  <option value="dispute">dispute</option>
                </select>
              </div>

              <div className="field">
                <label htmlFor="rns">
                  Resolved next step
                  <span className="fname">resolved_next_step_id</span>
                </label>
                <select
                  id="rns"
                  value={resolvedNextStepId}
                  onChange={(e) => setResolvedNextStepId(e.target.value)}
                >
                  <option value="ATS3">ATS3 · Classify and route</option>
                  <option value="ATS4">ATS4 · Next stage in the full workflow</option>
                </select>
              </div>

              <div className="field">
                <label htmlFor="rar">
                  Resolved accountable role
                  <span className="fname">resolved_accountable_role</span>
                </label>
                <select
                  id="rar"
                  value={resolvedAccountableRole}
                  onChange={(e) => setResolvedAccountableRole(e.target.value)}
                >
                  <option value="intake_exception_handler">intake_exception_handler</option>
                  <option value="specialist_reviewer">specialist_reviewer</option>
                </select>
              </div>
            </div>
          )}

          <div className={`field mt-4 ${validationError ? 'field-error' : ''}`}>
            <label htmlFor="comment">
              Comment (required)
              <span className="fname">comment</span>
            </label>
            <textarea
              id="comment"
              name="comment"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              aria-describedby={validationError ? 'comment-err-msg' : 'comment-hint'}
              aria-invalid={!!validationError}
            />
            {validationError ? (
              <div className="err-msg" id="comment-err-msg">{validationError}</div>
            ) : (
              <div className="hint" id="comment-hint">
                Explain the action. The comment is stored with the case and shown to internal reviewers only.
              </div>
            )}
          </div>

          <div className="btn-row">
            {isSubmitting ? (
              <span className="btn btn-primary" role="status">Recording action…</span>
            ) : (
              <button type="submit" className="btn btn-primary">
                Record action
              </button>
            )}
            <Link to="/cases" className="btn btn-secondary">Back to cases</Link>
          </div>
          
          <p className="hint text-xs mt-3">POST /api/v1/cases/{'{case_id}'}/exception-actions</p>
        </form>
      </div>
    </section>
  )
}
