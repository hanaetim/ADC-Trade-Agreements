/**
 * Tests for CaseSubmissionForm component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { CaseSubmissionForm } from '../components/case/CaseSubmissionForm'
import { apiClient } from '../lib/api-client'

// Mock the API client
vi.mock('../lib/api-client', () => ({
  apiClient: {
    post: vi.fn()
  },
  ApiError: class ApiError extends Error {
    constructor(public status: number, public detail: string) {
      super(detail)
      this.name = 'ApiError'
    }
  }
}))

describe('CaseSubmissionForm', () => {
  const mockOnSuccess = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders all form sections', () => {
    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    expect(screen.getByText('1. Request type')).toBeInTheDocument()
    expect(screen.getByText('2. Applicant and channel')).toBeInTheDocument()
    expect(screen.getByText('3. Goods and origin')).toBeInTheDocument()
    expect(screen.getByText('4. Attachments')).toBeInTheDocument()
    expect(screen.getByText('5. Preferences')).toBeInTheDocument()
  })

  it('defaults to origin_ruling workflow type', () => {
    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    const originRulingRadio = screen.getByDisplayValue('origin_ruling')
    expect(originRulingRadio).toBeChecked()
  })

  it('allows changing workflow type', () => {
    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    const inquiryRadio = screen.getByDisplayValue('inquiry')
    fireEvent.click(inquiryRadio)

    expect(inquiryRadio).toBeChecked()
    expect(screen.getByDisplayValue('origin_ruling')).not.toBeChecked()
  })

  it('submits form with valid data', async () => {
    const mockResponse = {
      case_id: 'test-case-id',
      case_reference: 'IAO-2026-000001',
      workflow_type: 'origin_ruling',
      current_step_id: 'ATS3',
      case_state: 'routed',
      accountable_role: 'intake_exception_handler',
      registration_sync_status: 'succeeded',
      reason_codes: [],
      agent_execution: {
        agent_id: 'AGN1',
        agent_name: 'Intake & Routing Agent',
        disposition: 'completed'
      },
      trace_event_ids: [],
      created_at: '2026-11-13T10:00:00Z',
      updated_at: '2026-11-13T10:00:00Z'
    }

    vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse)

    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    // Fill in required fields
    fireEvent.change(screen.getByLabelText(/Applicant name/), {
      target: { value: 'Test Company' }
    })
    fireEvent.change(screen.getByLabelText(/Applicant reference/), {
      target: { value: 'TEST-123' }
    })

    // Submit form
    const submitButton = screen.getByRole('button', { name: /Submit case/ })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/cases', expect.objectContaining({
        submission_type: 'origin_ruling',
        submission_channel: 'portal',
        applicant_name: 'Test Company',
        applicant_reference: 'TEST-123',
        locale: 'en'
      }))
    })

    expect(mockOnSuccess).toHaveBeenCalledWith('test-case-id')
  })

  it('displays validation errors for 422 response', async () => {
    const ApiError = (await import('../lib/api-client')).ApiError
    const validationError = new ApiError(422, JSON.stringify([
      {
        loc: ['body', 'origin_country_code'],
        msg: 'string should have at most 2 characters',
        type: 'string_too_long'
      }
    ]))

    vi.mocked(apiClient.post).mockRejectedValueOnce(validationError)

    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    fireEvent.change(screen.getByLabelText(/Applicant name/), {
      target: { value: 'Test Company' }
    })
    fireEvent.change(screen.getByLabelText(/Applicant reference/), {
      target: { value: 'TEST-123' }
    })
    fireEvent.change(screen.getByLabelText(/Country of origin code/), {
      target: { value: 'INVALID' }
    })

    const submitButton = screen.getByRole('button', { name: /Submit case/ })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/field\(s\) need attention/i)).toBeInTheDocument()
    })
  })

  it('displays business error for 400 response', async () => {
    const ApiError = (await import('../lib/api-client')).ApiError
    const businessError = new ApiError(400, 'Applicant reference is not linked to a registered trade account')

    vi.mocked(apiClient.post).mockRejectedValueOnce(businessError)

    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    fireEvent.change(screen.getByLabelText(/Applicant name/), {
      target: { value: 'Test Company' }
    })
    fireEvent.change(screen.getByLabelText(/Applicant reference/), {
      target: { value: 'INVALID-REF' }
    })

    const submitButton = screen.getByRole('button', { name: /Submit case/ })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Applicant reference is not linked to a registered trade account/)).toBeInTheDocument()
    })
  })

  it('shows loading state during submission', async () => {
    let resolvePost: (value: unknown) => void
    const postPromise = new Promise((resolve) => {
      resolvePost = resolve
    })

    vi.mocked(apiClient.post).mockReturnValueOnce(postPromise as Promise<unknown>)

    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    fireEvent.change(screen.getByLabelText(/Applicant name/), {
      target: { value: 'Test Company' }
    })
    fireEvent.change(screen.getByLabelText(/Applicant reference/), {
      target: { value: 'TEST-123' }
    })

    const submitButton = screen.getByRole('button', { name: /Submit case/ })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/Submitting case/)).toBeInTheDocument()
    })

    // Resolve the promise to clean up
    resolvePost!({
      case_id: 'test-id',
      case_reference: 'IAO-2026-000001',
      workflow_type: 'origin_ruling',
      current_step_id: 'ATS3',
      case_state: 'routed',
      accountable_role: 'intake_exception_handler',
      registration_sync_status: 'succeeded',
      reason_codes: [],
      agent_execution: { agent_id: 'AGN1', agent_name: 'Intake & Routing Agent', disposition: 'completed' },
      trace_event_ids: [],
      created_at: '2026-11-13T10:00:00Z',
      updated_at: '2026-11-13T10:00:00Z'
    })
  })

  it('includes optional fields when provided', async () => {
    const mockResponse = {
      case_id: 'test-case-id',
      case_reference: 'IAO-2026-000001',
      workflow_type: 'origin_ruling',
      current_step_id: 'ATS3',
      case_state: 'routed',
      accountable_role: 'intake_exception_handler',
      registration_sync_status: 'succeeded',
      reason_codes: [],
      agent_execution: {
        agent_id: 'AGN1',
        agent_name: 'Intake & Routing Agent',
        disposition: 'completed'
      },
      trace_event_ids: [],
      created_at: '2026-11-13T10:00:00Z',
      updated_at: '2026-11-13T10:00:00Z'
    }

    vi.mocked(apiClient.post).mockResolvedValueOnce(mockResponse)

    render(<CaseSubmissionForm onSuccess={mockOnSuccess} />)

    fireEvent.change(screen.getByLabelText(/Applicant name/), {
      target: { value: 'Test Company' }
    })
    fireEvent.change(screen.getByLabelText(/Applicant reference/), {
      target: { value: 'TEST-123' }
    })
    fireEvent.change(screen.getByLabelText(/Goods description/), {
      target: { value: 'Test goods description' }
    })
    fireEvent.change(screen.getByLabelText(/Country of origin code/), {
      target: { value: 'EG' }
    })
    fireEvent.change(screen.getByLabelText(/Agreement reference/), {
      target: { value: 'FTA-TEST' }
    })

    const submitButton = screen.getByRole('button', { name: /Submit case/ })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(apiClient.post).toHaveBeenCalledWith('/cases', expect.objectContaining({
        goods_description: 'Test goods description',
        origin_country_code: 'EG',
        agreement_reference: 'FTA-TEST'
      }))
    })
  })
})
