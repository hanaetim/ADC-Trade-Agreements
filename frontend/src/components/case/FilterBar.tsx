/**
 * Filter Bar Component
 * Implements filter controls from wireframe_case_queue.html
 */

import { FormEvent } from 'react'

export interface FilterValues {
  workflow_type?: string
  case_state?: string
  assigned_role?: string
}

interface Props {
  filters: FilterValues
  onFilterChange: (filters: FilterValues) => void
  onClear: () => void
}

export function FilterBar({ filters, onFilterChange, onClear }: Props) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    // Filters are already updated via onChange, form submit just triggers apply
  }

  const handleChange = (field: keyof FilterValues, value: string) => {
    onFilterChange({ ...filters, [field]: value === 'all' ? undefined : value })
  }

  return (
    <form
      className="grid grid-cols-[1fr_1fr_1fr_auto] gap-4 items-end p-5"
      onSubmit={handleSubmit}
      aria-label="Filter cases"
    >
      <div>
        <label htmlFor="f-workflow" className="block font-semibold text-sm mb-1">
          Workflow type<span className="font-mono text-xs font-normal text-gray-600 ml-2">workflow_type</span>
        </label>
        <select
          id="f-workflow"
          name="workflow_type"
          value={filters.workflow_type || 'all'}
          onChange={(e) => handleChange('workflow_type', e.target.value)}
          className="w-full px-3 py-2 border border-gray-500 rounded"
        >
          <option value="all">All workflow types</option>
          <option value="origin_ruling">origin_ruling</option>
          <option value="agreement_update">agreement_update</option>
          <option value="inquiry">inquiry</option>
          <option value="study">study</option>
          <option value="certificate_sampling">certificate_sampling</option>
          <option value="dispute">dispute</option>
        </select>
      </div>

      <div>
        <label htmlFor="f-state" className="block font-semibold text-sm mb-1">
          Case state<span className="font-mono text-xs font-normal text-gray-600 ml-2">case_state</span>
        </label>
        <select
          id="f-state"
          name="case_state"
          value={filters.case_state || 'all'}
          onChange={(e) => handleChange('case_state', e.target.value)}
          className="w-full px-3 py-2 border border-gray-500 rounded"
        >
          <option value="all">All states</option>
          <option value="submitted">submitted</option>
          <option value="registered">registered</option>
          <option value="intake_blocked">intake_blocked</option>
          <option value="queued_for_review">queued_for_review</option>
          <option value="routed">routed</option>
          <option value="closed_rejected">closed_rejected</option>
        </select>
      </div>

      <div>
        <label htmlFor="f-role" className="block font-semibold text-sm mb-1">
          Assigned role<span className="font-mono text-xs font-normal text-gray-600 ml-2">assigned_role</span>
        </label>
        <select
          id="f-role"
          name="assigned_role"
          value={filters.assigned_role || 'all'}
          onChange={(e) => handleChange('assigned_role', e.target.value)}
          className="w-full px-3 py-2 border border-gray-500 rounded"
        >
          <option value="all">All roles</option>
          <option value="intake_exception_handler">intake_exception_handler</option>
          <option value="external_applicant">external_applicant</option>
          <option value="specialist_reviewer">specialist_reviewer</option>
          <option value="section_head">section_head</option>
          <option value="policy_legal_approver">policy_legal_approver</option>
          <option value="technical_committee">technical_committee</option>
          <option value="auditor">auditor</option>
        </select>
      </div>

      <div className="flex gap-3 items-center">
        <button
          type="submit"
          className="px-5 py-2 bg-blue-900 text-white border-2 border-blue-900 rounded font-semibold"
        >
          Apply filters
        </button>
        <button
          type="button"
          onClick={onClear}
          className="px-5 py-2 bg-white text-blue-900 border-2 border-blue-900 rounded font-semibold"
        >
          Clear filters
        </button>
      </div>
    </form>
  )
}
