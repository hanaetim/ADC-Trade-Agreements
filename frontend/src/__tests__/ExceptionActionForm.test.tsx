/**
 * Exception Action Form Unit Tests
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { ExceptionActionForm } from '../components/case/ExceptionActionForm'
import * as apiClientModule from '../lib/api-client'

// Mock the API client
vi.mock('../lib/api-client', () => ({
  apiClient: {
    post: vi.fn(),
  },
}))

const renderForm = (props = {}) => {
  const defaultProps = {
    caseId: 'test-case-id',
    caseState: 'intake_blocked',
    onSuccess: vi.fn(),
  }

  return render(
    <BrowserRouter>
      <ExceptionActionForm {...defaultProps} {...props} />
    </BrowserRouter>
  )
}

describe('ExceptionActionForm', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders form with action type options', () => {
    renderForm()

    expect(screen.getByText(/Record an exception action/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/request_correction/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/close_rejected/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/manual_route_resolution/i)).toBeInTheDocument()
  })

  it('submits request_correction action successfully', async () => {
    const mockOnSuccess = vi.fn()
    const mockResponse = {
      case_id: 'test-case-id',
      case_state: 'queued_for_review',
      current_step_id: 'ATS2',
      accountable_role: 'intake_exception_handler',
      recorded_event_id: 'event-123',
      updated_at: '2026-11-13T10:00:00Z',
    }

    vi.mocked(apiClientModule.apiClient.post).mockResolvedValueOnce(mockResponse)

    renderForm({ onSuccess: mockOnSuccess })

    // Fill in comment field
    const commentField = screen.getByLabelText(/Comment \(required\)/i)
    fireEvent.change(commentField, { target: { value: 'Requesting applicant to provide missing information' } })

    const submitButton = screen.getByRole('button', { name: /Record action/i })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(apiClientModule.apiClient.post).toHaveBeenCalledWith(
        '/cases/test-case-id/exception-actions',
        {
          action_type: 'request_correction',
          comment: 'Requesting applicant to provide missing information',
        }
      )
    })

    await waitFor(() => {
      expect(screen.getByText(/Action recorded/i)).toBeInTheDocument()
    })
  })

  it('submits close_rejected action successfully', async () => {
    const mockOnSuccess = vi.fn()
    const mockResponse = {
      case_id: 'test-case-id',
      case_state: 'closed_rejected',
      current_step_id: 'ATS2',
      accountable_role: 'intake_exception_handler',
      recorded_event_id: 'event-124',
      updated_at: '2026-11-13T10:00:00Z',
    }

    vi.mocked(apiClientModule.apiClient.post).mockResolvedValueOnce(mockResponse)

    renderForm({ onSuccess: mockOnSuccess })

    // Select close_rejected
    const closeRejectedRadio = screen.getByLabelText(/close_rejected/i)
    fireEvent.click(closeRejectedRadio)

    const commentField = screen.getByLabelText(/Comment \(required\)/i)
    fireEvent.change(commentField, { target: { value: 'Case does not meet eligibility criteria' } })

    const submitButton = screen.getByRole('button', { name: /Record action/i })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(apiClientModule.apiClient.post).toHaveBeenCalledWith(
        '/cases/test-case-id/exception-actions',
        {
          action_type: 'close_rejected',
          comment: 'Case does not meet eligibility criteria',
        }
      )
    })
  })

  it('disables manual_route_resolution when case state is intake_blocked', () => {
    renderForm({ caseState: 'intake_blocked' })

    const manualRouteRadio = screen.getByLabelText(/manual_route_resolution/i) as HTMLInputElement
    expect(manualRouteRadio.disabled).toBe(true)
  })

  it('enables manual_route_resolution when case state is queued_for_review', () => {
    renderForm({ caseState: 'queued_for_review' })

    const manualRouteRadio = screen.getByLabelText(/manual_route_resolution/i) as HTMLInputElement
    expect(manualRouteRadio.disabled).toBe(false)
  })

  it('shows additional fields for manual_route_resolution', async () => {
    renderForm({ caseState: 'queued_for_review' })

    const manualRouteRadio = screen.getByLabelText(/manual_route_resolution/i)
    fireEvent.click(manualRouteRadio)

    await waitFor(() => {
      expect(screen.getByLabelText(/Resolved workflow type/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/Resolved next step/i)).toBeInTheDocument()
      expect(screen.getByLabelText(/Resolved accountable role/i)).toBeInTheDocument()
    })
  })

  it('displays error message when submission fails', async () => {
    vi.mocked(apiClientModule.apiClient.post).mockRejectedValueOnce(
      new Error('Network error')
    )

    renderForm()

    const commentField = screen.getByLabelText(/Comment \(required\)/i)
    fireEvent.change(commentField, { target: { value: 'Test comment' } })

    const submitButton = screen.getByRole('button', { name: /Record action/i })
    fireEvent.click(submitButton)

    await waitFor(() => {
      expect(screen.getByText(/The action was not recorded/i)).toBeInTheDocument()
      expect(screen.getByText(/Network error/i)).toBeInTheDocument()
    })
  })

  it('validates empty comment field shows error message', async () => {
    renderForm()

    const commentField = screen.getByLabelText(/Comment \(required\)/i) as HTMLTextAreaElement
    
    // Make sure comment is empty
    fireEvent.change(commentField, { target: { value: '' } })
    
    // Try to submit
    const submitButton = screen.getByRole('button', { name: /Record action/i })
    fireEvent.submit(submitButton.closest('form')!)

    // Wait for validation error to appear
    await waitFor(() => {
      const errorElement = screen.queryByText(/Enter a comment that explains this action/i)
      expect(errorElement).toBeInTheDocument()
    })
  })
})
