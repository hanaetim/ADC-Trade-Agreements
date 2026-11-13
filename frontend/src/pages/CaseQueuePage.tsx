/**
 * Case Queue Page
 * Implements the case queue from wireframe_case_queue.html
 */

import { useState, useEffect } from 'react'
import { apiClient } from '../lib/api-client'
import { useAuth } from '../lib/auth-context'
import { SummaryStripWidget } from '../components/case/SummaryStripWidget'
import { FilterBar, FilterValues } from '../components/case/FilterBar'
import { QuickFilterChips } from '../components/case/QuickFilterChips'
import { CaseListTable } from '../components/case/CaseListTable'
import { PaginationControls } from '../components/case/PaginationControls'

interface CaseListItem {
  case_id: string
  case_reference: string
  workflow_type: string
  case_state: string
  current_step_id: string
  accountable_role: string
  latest_reason_code: string | null
  registration_sync_status: string
  created_at: string
  updated_at: string
  applicant_name?: string
}

interface CasesResponse {
  items: CaseListItem[]
  total: number
  page: number
  page_size: number
}

export function CaseQueuePage() {
  const { user } = useAuth()
  const [cases, setCases] = useState<CaseListItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [total, setTotal] = useState(0)
  const [currentPage, setCurrentPage] = useState(1)
  const [pageSize] = useState(10)

  // Filter state
  const [filters, setFilters] = useState<FilterValues>({})
  const [activeQuickFilter, setActiveQuickFilter] = useState('all')

  // Summary metrics (hardcoded for MVP as per wireframe)
  const summaryItems = [
    { count: 4, label: 'Blocked at intake', code: 'intake_blocked', color: 'blocked' as const },
    { count: 2, label: 'Queued for review', code: 'queued_for_review', color: 'queued' as const },
    { count: 1, label: 'Registration sync failed', code: 'failed', color: 'failed' as const },
    { count: 9, label: 'Routed in the last 7 days', code: 'routed', color: 'routed' as const }
  ]

  // Quick filters
  const quickFilters = [
    { id: 'needs_attention', label: 'Needs attention (intake_blocked + queued_for_review)', active: false },
    { id: 'intake_blocked', label: 'intake_blocked', active: false },
    { id: 'queued_for_review', label: 'queued_for_review', active: false },
    { id: 'all', label: 'All states', active: activeQuickFilter === 'all' }
  ].map(f => ({ ...f, active: f.id === activeQuickFilter }))

  useEffect(() => {
    loadCases()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filters, currentPage])

  const loadCases = async () => {
    try {
      setLoading(true)
      setError(null)

      // Build query params
      const params = new URLSearchParams()
      params.set('limit', pageSize.toString())
      params.set('offset', ((currentPage - 1) * pageSize).toString())
      
      if (filters.workflow_type) params.set('workflow_type', filters.workflow_type)
      if (filters.case_state) params.set('case_state', filters.case_state)
      if (filters.assigned_role) params.set('assigned_role', filters.assigned_role)

      const response = await apiClient.get<CasesResponse>(`/cases?${params.toString()}`)
      setCases(response.items)
      setTotal(response.total)
    } catch (err) {
      setError('Failed to load cases')
      console.error('Failed to load cases:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (newFilters: FilterValues) => {
    setFilters(newFilters)
    setCurrentPage(1)
    setActiveQuickFilter('all')
  }

  const handleClearFilters = () => {
    setFilters({})
    setCurrentPage(1)
    setActiveQuickFilter('all')
  }

  const handleQuickFilter = (filterId: string) => {
    setActiveQuickFilter(filterId)
    setCurrentPage(1)

    switch (filterId) {
      case 'needs_attention':
        setFilters({ case_state: 'intake_blocked' }) // Would ideally support OR conditions
        break
      case 'intake_blocked':
        setFilters({ case_state: 'intake_blocked' })
        break
      case 'queued_for_review':
        setFilters({ case_state: 'queued_for_review' })
        break
      case 'all':
        setFilters({})
        break
    }
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-start gap-6">
        <div>
          <h1 className="text-3xl font-bold">Cases</h1>
          <p className="text-lg font-semibold text-blue-900 mt-1">
            {user?.role === 'intake_exception_handler' ? 'Intake exception queue' : 'My cases'}
          </p>
          <p className="text-gray-600 mt-2 max-w-3xl">
            {user?.role === 'intake_exception_handler'
              ? 'Cases that the deterministic checks or the intake routing could not move forward are held here for you. Open a case to see why it is held and to record an exception action.'
              : 'View and track the status of your submitted cases.'}
          </p>
        </div>
        <div className="flex gap-2 flex-wrap">
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700 border border-gray-300">
            Route /cases
          </span>
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700 border border-gray-300">
            Sample data
          </span>
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-800">
            Internal handler view
          </span>
        </div>
      </div>

      <SummaryStripWidget items={summaryItems} />

      <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="queue-title">
        <div className="p-5 border-b border-gray-300 flex justify-between items-center">
          <div>
            <h2 id="queue-title" className="text-lg font-bold">Case list</h2>
            <p className="text-sm text-gray-600 mt-1">
              Cases visible to your role. Use the case state shortcuts for your queue (intake_blocked and queued_for_review), or set the assigned role filter to intake_exception_handler.
            </p>
          </div>
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700 border border-gray-300">
            GET /api/v1/cases
          </span>
        </div>

        <FilterBar
          filters={filters}
          onFilterChange={handleFilterChange}
          onClear={handleClearFilters}
        />

        <QuickFilterChips
          filters={quickFilters}
          onFilterClick={handleQuickFilter}
        />

        <CaseListTable
          cases={cases}
          loading={loading}
          error={error}
          onRetry={loadCases}
        />

        {!loading && !error && cases.length > 0 && (
          <PaginationControls
            currentPage={currentPage}
            pageSize={pageSize}
            total={total}
            onPageChange={handlePageChange}
          />
        )}
      </section>

      {/* Legend section */}
      <div className="grid grid-cols-3 gap-6 mt-6">
        <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="leg-state">
          <div className="p-5">
            <h3 id="leg-state" className="text-base font-bold mb-3">Case state labels</h3>
            <ul className="list-none p-0 m-0 text-sm">
              {[
                { state: 'registered', label: 'registered', desc: 'Case record created' },
                { state: 'intake_blocked', label: 'intake_blocked', desc: 'A rule check failed' },
                { state: 'queued_for_review', label: 'queued_for_review', desc: 'Waiting for a person' },
                { state: 'routed', label: 'routed', desc: 'Sent to next role' },
                { state: 'closed_rejected', label: 'closed_rejected', desc: 'Closed, not accepted' }
              ].map((item, index, arr) => (
                <li
                  key={item.state}
                  className={`flex justify-between gap-3 py-1.5 ${index < arr.length - 1 ? 'border-b border-gray-300' : ''} items-center`}
                >
                  <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-semibold leading-5 whitespace-nowrap bg-gray-100 text-gray-700">
                    <span className="w-2 h-2 rounded-full bg-current"></span>
                    {item.label}
                  </span>
                  <span className="text-gray-600 text-right">{item.desc}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="leg-src">
          <div className="p-5">
            <h3 id="leg-src" className="text-base font-bold mb-3">Where a reason came from</h3>
            <ul className="list-none p-0 m-0 text-sm">
              {[
                { label: 'Deterministic Rule', desc: 'Fixed rule check' },
                { label: 'AGN1 routing', desc: 'Intake & Routing Agent output' },
                { label: 'Human action', desc: 'Recorded by a person' },
                { label: 'System', desc: 'Automatic system event' }
              ].map((item, index, arr) => (
                <li
                  key={item.label}
                  className={`flex justify-between gap-3 py-1.5 ${index < arr.length - 1 ? 'border-b border-gray-300' : ''} items-center`}
                >
                  <span className="inline-flex items-center gap-1.5 font-semibold text-xs text-gray-700">
                    <span className="w-2.5 h-2.5 border-2 border-blue-900 bg-blue-900"></span>
                    {item.label}
                  </span>
                  <span className="text-gray-600 text-right">{item.desc}</span>
                </li>
              ))}
            </ul>
          </div>
        </section>

        <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="leg-sync">
          <div className="p-5">
            <h3 id="leg-sync" className="text-base font-bold mb-3">Registration sync</h3>
            <ul className="list-none p-0 m-0 text-sm">
              {[
                { status: 'succeeded', label: 'succeeded', desc: 'Recorded in the system of record' },
                { status: 'pending', label: 'pending', desc: 'Not yet confirmed' },
                { status: 'failed', label: 'failed', desc: 'Needs follow-up' }
              ].map((item, index, arr) => (
                <li
                  key={item.status}
                  className={`flex justify-between gap-3 py-1.5 ${index < arr.length - 1 ? 'border-b border-gray-300' : ''} items-center`}
                >
                  <span className="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-semibold leading-5 whitespace-nowrap bg-gray-100 text-gray-700">
                    <span className="w-2 h-2 rounded-full bg-current"></span>
                    {item.label}
                  </span>
                  <span className="text-gray-600 text-right">{item.desc}</span>
                </li>
              ))}
            </ul>
            <p className="text-xs text-gray-600 mt-3">
              This list shows status only. Retrying a sync is not available in this release.
            </p>
          </div>
        </section>
      </div>
    </div>
  )
}
