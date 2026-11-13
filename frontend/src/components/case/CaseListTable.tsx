/**
 * Case List Table Component
 * Implements the case table from wireframe_case_queue.html
 */

import { useNavigate } from 'react-router-dom'

interface CaseItem {
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

interface Props {
  cases: CaseItem[]
  loading: boolean
  error: string | null
  onRetry: () => void
}

export function CaseListTable({ cases, loading, error, onRetry }: Props) {
  const navigate = useNavigate()

  const getBadgeClasses = (state: string) => {
    const baseClasses = 'inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-semibold leading-5 whitespace-nowrap'
    
    switch (state) {
      case 'routed':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'intake_blocked':
        return `${baseClasses} bg-red-100 text-red-700`
      case 'queued_for_review':
        return `${baseClasses} bg-yellow-100 text-yellow-700`
      case 'closed_rejected':
      case 'closed':
        return `${baseClasses} bg-gray-200 text-gray-700`
      case 'registered':
        return `${baseClasses} bg-blue-100 text-blue-800`
      default:
        return `${baseClasses} bg-gray-100 text-gray-600`
    }
  }

  const getBadgeShape = (state: string) => {
    switch (state) {
      case 'routed':
        return 'w-2 h-2 rounded-full bg-current'
      case 'intake_blocked':
        return 'w-2 h-2 bg-current'
      case 'queued_for_review':
        return 'w-2 h-2 bg-current transform rotate-45'
      case 'closed_rejected':
      case 'closed':
        return 'w-2.5 h-0.5 bg-current'
      case 'registered':
        return 'w-2 h-2 rounded-full bg-transparent border-2 border-current'
      default:
        return 'w-2 h-2 rounded-full bg-current'
    }
  }

  const getSyncBadgeClasses = (status: string) => {
    const baseClasses = 'inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full text-xs font-semibold leading-5 whitespace-nowrap'
    
    switch (status) {
      case 'succeeded':
        return `${baseClasses} bg-green-100 text-green-800`
      case 'pending':
        return `${baseClasses} bg-yellow-100 text-yellow-700`
      case 'failed':
        return `${baseClasses} bg-red-100 text-red-700`
      default:
        return `${baseClasses} bg-gray-100 text-gray-600`
    }
  }

  const getSyncBadgeShape = (status: string) => {
    switch (status) {
      case 'succeeded':
        return 'w-2 h-2 rounded-full bg-current'
      case 'pending':
        return 'w-2 h-2 rounded-full bg-transparent border-2 border-current'
      case 'failed':
        return 'w-2 h-2 bg-current'
      default:
        return 'w-2 h-2 rounded-full bg-current'
    }
  }

  const formatDate = (isoString: string) => {
    try {
      const date = new Date(isoString)
      return date.toLocaleDateString('en-GB', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        timeZoneName: 'short'
      }).replace(',', '')
    } catch {
      return isoString
    }
  }

  if (loading) {
    return (
      <div className="p-6" role="status">
        <p>Loading cases…</p>
        <div aria-hidden="true" className="mt-4 space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="grid grid-cols-[130px_110px_120px_70px_150px_1fr] gap-3 py-2 border-b border-gray-300">
              {[1, 2, 3, 4, 5, 6].map((j) => (
                <div key={j} className="h-3.5 rounded bg-gray-200"></div>
              ))}
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="flex justify-between items-center gap-4 border-2 border-red-700 bg-red-100 text-red-700 rounded px-4 py-3" role="alert">
          <div>
            <strong className="block mb-1">We could not load the case list</strong>
            <p>{error}</p>
          </div>
          <button
            onClick={onRetry}
            className="px-4 py-1 bg-white text-blue-900 border-2 border-blue-900 rounded font-semibold text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (cases.length === 0) {
    return (
      <div className="p-6 text-center">
        <div className="border border-gray-300 rounded bg-gray-50 p-6">
          <strong className="block text-base mb-1">No cases match these filters</strong>
          <span className="text-gray-600">Nothing is waiting in the intake exception queue. Clear the filters to see all cases visible to your role.</span>
        </div>
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full border-collapse text-sm cases" data-testid="case-table">
        <caption className="text-left px-5 py-3 text-sm text-gray-600 border-b border-gray-300">
          Showing {cases.length} matching cases · sorted by most recently updated · all values are illustrative sample data
        </caption>
        <thead>
          <tr className="bg-gray-50">
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Case reference
              <span className="block font-mono font-normal text-[10px]">case_reference</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Workflow type
              <span className="block font-mono font-normal text-[10px]">workflow_type</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Case state
              <span className="block font-mono font-normal text-[10px]">case_state</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Current step
              <span className="block font-mono font-normal text-[10px]">current_step_id</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Accountable role
              <span className="block font-mono font-normal text-[10px]">accountable_role</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Latest reason
              <span className="block font-mono font-normal text-[10px]">latest_reason_code</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Registration sync
              <span className="block font-mono font-normal text-[10px]">registration_sync_status</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Created
              <span className="block font-mono font-normal text-[10px]">created_at</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Updated
              <span className="block font-mono font-normal text-[10px]">updated_at</span>
            </th>
            <th scope="col" className="text-left text-xs font-bold text-gray-600 px-3 py-3 border-b border-gray-300 whitespace-nowrap">
              Action
            </th>
          </tr>
        </thead>
        <tbody>
          {cases.map((caseItem, index) => (
            <tr
              key={caseItem.case_id}
              className={index === 0 ? 'bg-blue-50' : undefined}
            >
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <span className="font-mono font-bold text-sm">{caseItem.case_reference}</span>
                {caseItem.applicant_name && (
                  <span className="block text-xs text-gray-600 mt-0.5">{caseItem.applicant_name}</span>
                )}
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <code className="text-sm">{caseItem.workflow_type}</code>
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <span className={`badge ${getBadgeClasses(caseItem.case_state)}`}>
                  <span className={getBadgeShape(caseItem.case_state)}></span>
                  {caseItem.case_state}
                </span>
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <code className="text-sm">{caseItem.current_step_id}</code>
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                {caseItem.accountable_role.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                <span className="block font-mono text-xs text-gray-600 mt-0.5">
                  {caseItem.accountable_role}
                </span>
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                {caseItem.latest_reason_code ? (
                  <>
                    <code className="text-sm">{caseItem.latest_reason_code}</code>
                    <br />
                    <span className="inline-flex items-center gap-1.5 font-semibold text-xs text-gray-700 mt-0.5">
                      <span className="w-2.5 h-2.5 border-2 border-blue-900 bg-blue-900"></span>
                      Deterministic Rule
                    </span>
                  </>
                ) : (
                  <span className="text-xs text-gray-600">No reason recorded</span>
                )}
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <span className={getSyncBadgeClasses(caseItem.registration_sync_status)}>
                  <span className={getSyncBadgeShape(caseItem.registration_sync_status)}></span>
                  {caseItem.registration_sync_status}
                </span>
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top font-mono text-sm">
                {formatDate(caseItem.created_at)}
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top font-mono text-sm">
                {formatDate(caseItem.updated_at)}
              </td>
              <td className="px-3 py-3 border-b border-gray-300 align-top">
                <button
                  onClick={() => navigate(`/cases/${caseItem.case_id}`)}
                  className="px-4 py-1 bg-white text-blue-900 border-2 border-blue-900 rounded font-semibold text-sm"
                >
                  Open
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
