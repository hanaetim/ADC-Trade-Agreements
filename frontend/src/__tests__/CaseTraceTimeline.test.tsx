/**
 * Case Trace Timeline Unit Tests
 */

import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { CaseTraceTimeline } from '../components/case/CaseTraceTimeline'
import type { CaseStepDTO } from '../types'

describe('CaseTraceTimeline', () => {
  const mockSteps: CaseStepDTO[] = [
    {
      step_id: 'ATS1',
      step_status: 'completed',
      decision_source: 'deterministic_rule',
      actor_label: 'System',
      rationale_summary: 'All required fields present',
      evidence_ref: null,
      occurred_at: '2026-11-13T08:14:02Z',
    },
    {
      step_id: 'ATS2',
      step_status: 'completed',
      decision_source: 'deterministic_rule',
      actor_label: 'System',
      rationale_summary: 'Workflow type origin_ruling is eligible',
      evidence_ref: null,
      occurred_at: '2026-11-13T08:14:02Z',
    },
    {
      step_id: 'ATS3',
      step_status: 'current',
      decision_source: 'agent',
      actor_label: 'AGN1',
      rationale_summary: 'Classified as origin_ruling, routed to ATS4',
      evidence_ref: null,
      occurred_at: '2026-11-13T08:14:03Z',
    },
  ]

  it('renders steps table with correct headers', () => {
    render(<CaseTraceTimeline steps={mockSteps} />)

    expect(screen.getByText('Atomic steps')).toBeInTheDocument()
    expect(screen.getByText('Step ID')).toBeInTheDocument()
    expect(screen.getByText('Status')).toBeInTheDocument()
    expect(screen.getByText('Decision Source')).toBeInTheDocument()
    expect(screen.getByText('Actor')).toBeInTheDocument()
    expect(screen.getByText('Rationale Summary')).toBeInTheDocument()
    expect(screen.getByText('Evidence Ref')).toBeInTheDocument()
    expect(screen.getByText('Occurred At')).toBeInTheDocument()
  })

  it('renders all steps with correct data', () => {
    render(<CaseTraceTimeline steps={mockSteps} />)

    // Check step IDs
    expect(screen.getByText('ATS1')).toBeInTheDocument()
    expect(screen.getByText('ATS2')).toBeInTheDocument()
    expect(screen.getByText('ATS3')).toBeInTheDocument()

    // Check rationale summaries
    expect(screen.getByText('All required fields present')).toBeInTheDocument()
    expect(screen.getByText('Workflow type origin_ruling is eligible')).toBeInTheDocument()
    expect(screen.getByText('Classified as origin_ruling, routed to ATS4')).toBeInTheDocument()
  })

  it('applies correct status badge classes', () => {
    const { container } = render(<CaseTraceTimeline steps={mockSteps} />)

    const completedBadges = container.querySelectorAll('.st-routed')
    expect(completedBadges.length).toBeGreaterThan(0)

    const currentBadges = container.querySelectorAll('.st-registered')
    expect(currentBadges.length).toBeGreaterThan(0)
  })

  it('renders decision source indicators', () => {
    const { container } = render(<CaseTraceTimeline steps={mockSteps} />)

    const ruleSources = container.querySelectorAll('.src-rule')
    expect(ruleSources.length).toBe(2) // ATS1 and ATS2

    const agentSources = container.querySelectorAll('.src-agent')
    expect(agentSources.length).toBe(1) // ATS3
  })

  it('shows empty state when no steps provided', () => {
    render(<CaseTraceTimeline steps={[]} />)

    expect(screen.getByText('No steps recorded yet')).toBeInTheDocument()
  })

  it('displays em dash for null values', () => {
    const stepWithNulls: CaseStepDTO = {
      step_id: 'ATS99',
      step_status: 'pending',
      decision_source: 'system',
      actor_label: null,
      rationale_summary: null,
      evidence_ref: null,
      occurred_at: '2026-11-13T08:14:03Z',
    }

    render(<CaseTraceTimeline steps={[stepWithNulls]} />)

    // Count em dashes - should be 3 (actor, rationale, evidence)
    const emDashes = screen.getAllByText('—')
    expect(emDashes).toHaveLength(3)
  })

  it('formats dates correctly', () => {
    render(<CaseTraceTimeline steps={mockSteps} />)

    // Check that dates are displayed (exact format depends on locale)
    const datePattern = /\d{1,2}\/\d{1,2}\/\d{4}/
    const cells = screen.getAllByRole('cell')
    const dateCells = cells.filter(cell => datePattern.test(cell.textContent || ''))
    
    expect(dateCells.length).toBeGreaterThan(0)
  })
})
