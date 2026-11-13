/**
 * Quick Filter Chips Component
 * Implements quick filter shortcuts from wireframe_case_queue.html
 */

interface QuickFilter {
  id: string
  label: string
  active: boolean
}

interface Props {
  filters: QuickFilter[]
  onFilterClick: (id: string) => void
}

export function QuickFilterChips({ filters, onFilterClick }: Props) {
  return (
    <div className="flex flex-wrap gap-2 items-center px-5 pb-4" role="group" aria-label="Case state shortcuts">
      <span className="text-sm font-semibold mr-2">Quick filters:</span>
      {filters.map((filter) => (
        <button
          key={filter.id}
          type="button"
          onClick={() => onFilterClick(filter.id)}
          className={`inline-flex items-center gap-1.5 px-3.5 py-1 rounded-full text-sm font-semibold ${
            filter.active
              ? 'bg-blue-900 text-white border border-blue-900'
              : 'bg-white text-gray-700 border border-gray-500'
          }`}
          aria-pressed={filter.active}
        >
          {filter.label}
        </button>
      ))}
    </div>
  )
}
