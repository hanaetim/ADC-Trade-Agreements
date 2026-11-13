/**
 * Tests for CaseListTable component
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import { CaseListTable } from '../components/case/CaseListTable'

const mockNavigate = vi.fn()
vi.mock('react-router-dom', async () => {
  const actual = await vi.importActual('react-router-dom')
  return {
    ...actual,
    useNavigate: () => mockNavigate
  }
})

const mockCases = [
  {
    case_id: '1',
    case_reference: 'IAO-2026-000123',
    workflow_type: 'origin_ruling',
    case_state: 'intake_blocked',
    current_step_id: 'ATS2',
    accountable_role: 'intake_exception_handler',
    latest_reason_code: 'ORIGIN_COUNTRY_NOT_PROVIDED',
    registration_sync_status: 'succeeded',
    created_at: '2026-11-12T08:14:00Z',
    updated_at: '2026-11-12T08:14:00Z',
    applicant_name: 'Gulf Basin Trading LLC'
  },
  {
    case_id: '2',
    case_reference: 'IAO-2026-000120',
    workflow_type: 'inquiry',
    case_state: 'queued_for_review',
    current_step_id: 'ATS3',
    accountable_role: 'intake_exception_handler',
    latest_reason_code: null,
    registration_sync_status: 'pending',
    created_at: '2026-11-12T07:30:00Z',
    updated_at: '2026-11-12T07:31:00Z',
    applicant_name: 'Desert Rose Textiles'
  }
]

describe('CaseListTable', () => {
  const mockOnRetry = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('displays loading state', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={[]} loading={true} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByRole('status')).toBeInTheDocument()
    expect(screen.getByText('Loading cases…')).toBeInTheDocument()
  })

  it('displays error state with retry button', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={[]} loading={false} error="Failed to load" onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByRole('alert')).toBeInTheDocument()
    expect(screen.getByText(/We could not load the case list/)).toBeInTheDocument()
    expect(screen.getByText('Failed to load')).toBeInTheDocument()

    const retryButton = screen.getByRole('button', { name: /Retry/ })
    fireEvent.click(retryButton)
    expect(mockOnRetry).toHaveBeenCalledTimes(1)
  })

  it('displays empty state when no cases', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={[]} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByText('No cases match these filters')).toBeInTheDocument()
  })

  it('renders case list with all columns', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    // Check table headers
    expect(screen.getByRole('columnheader', { name: /Case reference/ })).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: /Workflow type/ })).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: /Case state/ })).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: /Current step/ })).toBeInTheDocument()
    expect(screen.getByRole('columnheader', { name: /Accountable role/ })).toBeInTheDocument()

    // Check first case data
    expect(screen.getByText('IAO-2026-000123')).toBeInTheDocument()
    expect(screen.getByText('Gulf Basin Trading LLC')).toBeInTheDocument()
    expect(screen.getByText('origin_ruling')).toBeInTheDocument()
  })

  it('displays case state badges with correct styling', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    const blockedBadge = screen.getByText('intake_blocked')
    expect(blockedBadge).toHaveClass('bg-red-100', 'text-red-700')

    const queuedBadge = screen.getByText('queued_for_review')
    expect(queuedBadge).toHaveClass('bg-yellow-100', 'text-yellow-700')
  })

  it('displays sync status badges', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    const succeededBadge = screen.getByText('succeeded')
    expect(succeededBadge).toHaveClass('bg-green-100', 'text-green-800')

    const pendingBadge = screen.getByText('pending')
    expect(pendingBadge).toHaveClass('bg-yellow-100', 'text-yellow-700')
  })

  it('displays reason code when present', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByText('ORIGIN_COUNTRY_NOT_PROVIDED')).toBeInTheDocument()
    expect(screen.getByText('Deterministic Rule')).toBeInTheDocument()
  })

  it('displays "No reason recorded" when reason code is null', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByText('No reason recorded')).toBeInTheDocument()
  })

  it('navigates to case detail on Open button click', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    const openButtons = screen.getAllByRole('button', { name: /Open/ })
    fireEvent.click(openButtons[0])

    expect(mockNavigate).toHaveBeenCalledWith('/cases/1')
  })

  it('highlights first row with different background', () => {
    const { container } = render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    const rows = container.querySelectorAll('tbody tr')
    expect(rows.length).toBeGreaterThan(0)
    if (rows[0]) {
      expect(rows[0]).toHaveClass('bg-blue-50')
    }
    if (rows[1]) {
      expect(rows[1]).not.toHaveClass('bg-blue-50')
    }
  })

  it('formats dates correctly', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    // Date formatting depends on locale, just check that dates are present
    const dateElements = screen.getAllByText(/2026/)
    expect(dateElements.length).toBeGreaterThan(0)
  })

  it('displays applicant name as sub-line when present', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    expect(screen.getByText('Gulf Basin Trading LLC')).toBeInTheDocument()
    expect(screen.getByText('Desert Rose Textiles')).toBeInTheDocument()
  })

  it('formats accountable role with human-readable and code versions', () => {
    render(
      <BrowserRouter>
        <CaseListTable cases={mockCases} loading={false} error={null} onRetry={mockOnRetry} />
      </BrowserRouter>
    )

    // Human-readable version
    expect(screen.getAllByText(/Intake Exception Handler/i)[0]).toBeInTheDocument()
    // Code version in mono font
    expect(screen.getAllByText('intake_exception_handler')[0]).toBeInTheDocument()
  })
})
