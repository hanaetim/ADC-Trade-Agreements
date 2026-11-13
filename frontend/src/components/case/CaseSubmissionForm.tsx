/**
 * Case Submission Form Component
 * Implements the case submission form from wireframe_case_submission.html
 */

import { useState, FormEvent } from 'react'
import { apiClient, ApiError } from '../../lib/api-client'

interface AttachmentMetadata {
  file_name: string
  media_type: string
  storage_key?: string
}

interface CreateCaseRequest {
  submission_type: string
  submission_channel: string
  applicant_reference: string
  applicant_name: string
  goods_description?: string
  origin_country_code?: string
  agreement_reference?: string
  attachments?: AttachmentMetadata[]
  intake_notes?: string
  locale?: string
}

interface ValidationError {
  loc: (string | number)[]
  msg: string
  type: string
}

interface CreateCaseResponse {
  case_id: string
  case_reference: string
  workflow_type: string
  current_step_id: string
  case_state: string
  accountable_role: string
  registration_sync_status: string
  reason_codes: string[]
  agent_execution: {
    agent_id: string
    agent_name: string
    disposition: string
  }
  trace_event_ids: string[]
  created_at: string
  updated_at: string
}

interface Props {
  onSuccess: (caseId: string) => void
}

export function CaseSubmissionForm({ onSuccess }: Props) {
  // Form state
  const [submissionType, setSubmissionType] = useState('origin_ruling')
  const [submissionChannel] = useState('portal')
  const [applicantName, setApplicantName] = useState('')
  const [applicantReference, setApplicantReference] = useState('')
  const [goodsDescription, setGoodsDescription] = useState('')
  const [originCountryCode, setOriginCountryCode] = useState('')
  const [agreementReference, setAgreementReference] = useState('')
  const [locale, setLocale] = useState('en')
  const [attachments, setAttachments] = useState<AttachmentMetadata[]>([])

  // UI state
  const [submitting, setSubmitting] = useState(false)
  const [errorSummary, setErrorSummary] = useState<string | null>(null)
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({})

  const workflowTypes = [
    { value: 'origin_ruling', label: 'Origin ruling request', note: null },
    { value: 'agreement_update', label: 'Agreement update', note: 'Registered at intake; downstream workflow not yet available in MVP' },
    { value: 'inquiry', label: 'Inquiry', note: 'Registered at intake; downstream workflow not yet available in MVP' },
    { value: 'study', label: 'Study', note: 'Registered at intake; downstream workflow not yet available in MVP' },
    { value: 'certificate_sampling', label: 'Certificate sampling', note: 'Registered at intake; downstream workflow not yet available in MVP' },
    { value: 'dispute', label: 'Dispute', note: 'Registered at intake; downstream workflow not yet available in MVP' }
  ]

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    
    setSubmitting(true)
    setErrorSummary(null)
    setFieldErrors({})

    const request: CreateCaseRequest = {
      submission_type: submissionType,
      submission_channel: submissionChannel,
      applicant_reference: applicantReference,
      applicant_name: applicantName,
      goods_description: goodsDescription || undefined,
      origin_country_code: originCountryCode || undefined,
      agreement_reference: agreementReference || undefined,
      attachments: attachments.length > 0 ? attachments : undefined,
      locale
    }

    try {
      const response = await apiClient.post<CreateCaseResponse>('/cases', request)
      onSuccess(response.case_id)
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.status === 422) {
          // Validation errors
          try {
            const detail = JSON.parse(err.detail)
            if (Array.isArray(detail)) {
              const errors: Record<string, string> = {}
              detail.forEach((item: ValidationError) => {
                const field = item.loc[item.loc.length - 1]
                const fieldKey = typeof field === 'string' ? field : String(field)
                errors[fieldKey] = item.msg
              })
              setFieldErrors(errors)
              setErrorSummary('1 or more fields need attention before you can submit')
            } else {
              setErrorSummary(err.detail)
            }
          } catch {
            setErrorSummary(err.detail)
          }
        } else if (err.status === 400) {
          // Business rejection
          setErrorSummary(err.detail)
        } else {
          setErrorSummary(`Request failed: ${err.detail}`)
        }
      } else {
        setErrorSummary('Network error occurred')
      }
    } finally {
      setSubmitting(false)
    }
  }

  const handleAddAttachment = () => {
    // In MVP, just add a placeholder attachment
    const fileName = prompt('Enter file name:')
    if (fileName) {
      setAttachments([
        ...attachments,
        {
          file_name: fileName,
          media_type: 'application/pdf',
          storage_key: `placeholder-${Date.now()}`
        }
      ])
    }
  }

  const handleRemoveAttachment = (index: number) => {
    setAttachments(attachments.filter((_, i) => i !== index))
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      {errorSummary && (
        <div className="border-2 border-red-600 bg-red-100 text-red-700 rounded px-4 py-3 mb-6" role="alert">
          <strong className="block">{fieldErrors && Object.keys(fieldErrors).length > 0 ? `${Object.keys(fieldErrors).length} field(s) need attention before you can submit` : 'Submission error'}</strong>
          {errorSummary && <p className="mt-1">{errorSummary}</p>}
        </div>
      )}

      {/* 1. Request type */}
      <fieldset className="mb-6">
        <legend className="text-base font-bold mb-3">1. Request type</legend>
        <p className="text-sm text-gray-600 mb-3">
          Origin ruling requests are processed end to end in this release. Other request types are registered at intake so a formal case exists; their downstream workflow is not yet available.
        </p>
        <div className="grid grid-cols-2 gap-3" role="radiogroup" aria-label="Request type (submission_type)">
          {workflowTypes.map((type) => (
            <label
              key={type.value}
              className={`flex gap-3 items-start border rounded px-4 py-3 cursor-pointer ${
                submissionType === type.value
                  ? 'border-2 border-blue-900 bg-blue-50'
                  : 'border border-gray-500 bg-white'
              }`}
            >
              <input
                type="radio"
                name="submission_type"
                value={type.value}
                checked={submissionType === type.value}
                onChange={(e) => setSubmissionType(e.target.value)}
                className="mt-1"
              />
              <span>
                <span className="block font-semibold">{type.label}</span>
                <span className="block font-mono text-xs text-gray-600">{type.value}</span>
                {type.note && <span className="block text-xs text-gray-500 mt-0.5">{type.note}</span>}
              </span>
            </label>
          ))}
        </div>
      </fieldset>

      {/* 2. Applicant and channel */}
      <fieldset className="mb-6">
        <legend className="text-base font-bold mb-3">2. Applicant and channel</legend>
        <div className="grid grid-cols-2 gap-4">
          <div className="mb-4">
            <label htmlFor="applicant_name" className="block font-semibold mb-1">
              Applicant name<span className="text-red-700 font-semibold text-xs ml-1">required</span>
              <span className="font-mono text-xs font-normal text-gray-600 ml-2">applicant_name</span>
            </label>
            <input
              type="text"
              id="applicant_name"
              name="applicant_name"
              value={applicantName}
              onChange={(e) => setApplicantName(e.target.value)}
              className={`w-full px-3 py-2 border rounded ${
                fieldErrors.applicant_name
                  ? 'border-2 border-red-700 bg-red-100'
                  : 'border border-gray-500'
              }`}
              aria-invalid={!!fieldErrors.applicant_name}
              aria-describedby={fieldErrors.applicant_name ? 'applicant_name-error' : undefined}
            />
            {fieldErrors.applicant_name && (
              <p className="mt-1 text-red-700 text-sm font-semibold" id="applicant_name-error">
                {fieldErrors.applicant_name}
              </p>
            )}
          </div>
          <div className="mb-4">
            <label htmlFor="applicant_reference" className="block font-semibold mb-1">
              Applicant reference<span className="text-red-700 font-semibold text-xs ml-1">required</span>
              <span className="font-mono text-xs font-normal text-gray-600 ml-2">applicant_reference</span>
            </label>
            <input
              type="text"
              id="applicant_reference"
              name="applicant_reference"
              value={applicantReference}
              onChange={(e) => setApplicantReference(e.target.value)}
              className={`w-full px-3 py-2 border rounded ${
                fieldErrors.applicant_reference
                  ? 'border-2 border-red-700 bg-red-100'
                  : 'border border-gray-500'
              }`}
              aria-invalid={!!fieldErrors.applicant_reference}
              aria-describedby={fieldErrors.applicant_reference ? 'applicant_reference-error' : undefined}
            />
            {fieldErrors.applicant_reference && (
              <p className="mt-1 text-red-700 text-sm font-semibold" id="applicant_reference-error">
                {fieldErrors.applicant_reference}
              </p>
            )}
            <p className="mt-1 text-xs text-gray-600">Your trade licence or customs account reference.</p>
          </div>
        </div>
        <div className="mb-4">
          <label htmlFor="submission_channel" className="block font-semibold mb-1">
            Submission channel<span className="text-red-700 font-semibold text-xs ml-1">required</span>
            <span className="font-mono text-xs font-normal text-gray-600 ml-2">submission_channel</span>
          </label>
          <select
            id="submission_channel"
            name="submission_channel"
            value={submissionChannel}
            disabled
            className="w-full px-3 py-2 border border-gray-500 rounded bg-gray-50 text-gray-600"
          >
            <option>portal</option>
          </select>
          <p className="mt-1 text-xs text-gray-600">
            Applicants always submit through the portal channel. Staff entering a case for an applicant also see email_intake and internal_entry.
          </p>
        </div>
      </fieldset>

      {/* 3. Goods and origin */}
      <fieldset className="mb-6">
        <legend className="text-base font-bold mb-3">3. Goods and origin</legend>
        <div className="mb-4">
          <label htmlFor="goods_description" className="block font-semibold mb-1">
            Goods description<span className="text-gray-600 font-normal text-xs ml-1">optional</span>
            <span className="font-mono text-xs font-normal text-gray-600 ml-2">goods_description</span>
          </label>
          <textarea
            id="goods_description"
            name="goods_description"
            value={goodsDescription}
            onChange={(e) => setGoodsDescription(e.target.value)}
            className="w-full px-3 py-2 border border-gray-500 rounded resize-none"
            style={{ minHeight: '84px' }}
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div className="mb-4">
            <label htmlFor="origin_country_code" className="block font-semibold mb-1">
              Country of origin code<span className="text-gray-600 font-normal text-xs ml-1">optional</span>
              <span className="font-mono text-xs font-normal text-gray-600 ml-2">origin_country_code</span>
            </label>
            <input
              type="text"
              id="origin_country_code"
              name="origin_country_code"
              value={originCountryCode}
              onChange={(e) => setOriginCountryCode(e.target.value)}
              className={`w-full px-3 py-2 border rounded ${
                fieldErrors.origin_country_code
                  ? 'border-2 border-red-700 bg-red-100'
                  : 'border border-gray-500'
              }`}
              aria-invalid={!!fieldErrors.origin_country_code}
              aria-describedby={fieldErrors.origin_country_code ? 'origin_country_code-error' : undefined}
            />
            {fieldErrors.origin_country_code && (
              <p className="mt-1 text-red-700 text-sm font-semibold" id="origin_country_code-error">
                {fieldErrors.origin_country_code}
              </p>
            )}
          </div>
          <div className="mb-4">
            <label htmlFor="agreement_reference" className="block font-semibold mb-1">
              Agreement reference<span className="text-gray-600 font-normal text-xs ml-1">optional</span>
              <span className="font-mono text-xs font-normal text-gray-600 ml-2">agreement_reference</span>
            </label>
            <input
              type="text"
              id="agreement_reference"
              name="agreement_reference"
              value={agreementReference}
              onChange={(e) => setAgreementReference(e.target.value)}
              className="w-full px-3 py-2 border border-gray-500 rounded"
            />
            <p className="mt-1 text-xs text-gray-600">
              The trade agreement you are asking the ruling to be based on, if known.
            </p>
          </div>
        </div>
      </fieldset>

      {/* 4. Attachments */}
      <fieldset className="mb-6">
        <legend className="text-base font-bold mb-3">4. Attachments</legend>
        <p className="text-sm text-gray-600 mb-3">
          Supporting documents are recorded by file name and type. Add the documents that support your request.
        </p>
        {attachments.length > 0 && (
          <table className="w-full border-collapse mb-3 text-sm">
            <caption className="text-left text-xs text-gray-600 pb-2">
              Attached files (attachments[].file_name, attachments[].media_type)
            </caption>
            <thead>
              <tr>
                <th className="text-left px-3 py-2 border-b border-gray-300 bg-gray-50 text-xs">File name</th>
                <th className="text-left px-3 py-2 border-b border-gray-300 bg-gray-50 text-xs">Media type</th>
                <th className="text-left px-3 py-2 border-b border-gray-300 bg-gray-50 text-xs">Action</th>
              </tr>
            </thead>
            <tbody>
              {attachments.map((attachment, index) => (
                <tr key={index}>
                  <td className="px-3 py-2 border-b border-gray-300">{attachment.file_name}</td>
                  <td className="px-3 py-2 border-b border-gray-300 font-mono text-xs">{attachment.media_type}</td>
                  <td className="px-3 py-2 border-b border-gray-300">
                    <button
                      type="button"
                      onClick={() => handleRemoveAttachment(index)}
                      className="text-blue-900 underline"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        <button
          type="button"
          onClick={handleAddAttachment}
          className="px-5 py-2 bg-white text-blue-900 border-2 border-blue-900 rounded font-semibold"
        >
          Add attachment
        </button>
      </fieldset>

      {/* 5. Preferences */}
      <fieldset className="mb-6">
        <legend className="text-base font-bold mb-3">5. Preferences</legend>
        <div className="mb-4">
          <span className="label block font-semibold mb-1" id="locale-label">
            Preferred language for notifications<span className="text-gray-600 font-normal text-xs ml-1">optional</span>
            <span className="font-mono text-xs font-normal text-gray-600 ml-2">locale</span>
          </span>
          <div className="flex gap-6" role="radiogroup" aria-labelledby="locale-label">
            <label className="inline-flex gap-2 items-center">
              <input
                type="radio"
                name="locale"
                value="en"
                checked={locale === 'en'}
                onChange={(e) => setLocale(e.target.value)}
              />
              <span>English (en)</span>
            </label>
            <label className="inline-flex gap-2 items-center">
              <input
                type="radio"
                name="locale"
                value="ar"
                checked={locale === 'ar'}
                onChange={(e) => setLocale(e.target.value)}
              />
              <span lang="ar" dir="rtl">العربية</span> (ar)
            </label>
          </div>
          <p className="mt-1 text-xs text-gray-600">
            Language preference is recorded with the case. The full Arabic interface is not part of this release.
          </p>
        </div>
      </fieldset>

      {/* Submit actions */}
      <div className="flex items-center gap-4 pt-4 border-t border-gray-300">
        <button
          type="submit"
          disabled={submitting}
          className={`px-5 py-2 border-2 border-blue-900 rounded font-semibold inline-flex items-center gap-2 ${
            submitting
              ? 'bg-gray-300 text-gray-600 border-gray-500 cursor-default'
              : 'bg-blue-900 text-white'
          }`}
          aria-disabled={submitting}
        >
          {submitting && (
            <span className="inline-block w-3.5 h-3.5 border-3 border-gray-500 border-t-gray-600 rounded-full animate-spin" aria-hidden="true"></span>
          )}
          {submitting ? 'Submitting case…' : 'Submit case'}
        </button>
        <a href="/cases" className="px-5 py-2 bg-white text-blue-900 border-2 border-blue-900 rounded font-semibold">
          Cancel
        </a>
        <span className="text-sm text-gray-600">There is no draft saving. The case is registered when you submit.</span>
      </div>
    </form>
  )
}
