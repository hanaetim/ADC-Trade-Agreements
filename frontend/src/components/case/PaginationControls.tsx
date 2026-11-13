/**
 * Pagination Controls Component
 * Implements pagination from wireframe_case_queue.html
 */

interface Props {
  currentPage: number
  pageSize: number
  total: number
  onPageChange: (page: number) => void
}

export function PaginationControls({ currentPage, pageSize, total, onPageChange }: Props) {
  const totalPages = Math.ceil(total / pageSize)
  const startItem = (currentPage - 1) * pageSize + 1
  const endItem = Math.min(currentPage * pageSize, total)

  const canGoPrevious = currentPage > 1
  const canGoNext = currentPage < totalPages

  return (
    <nav className="flex justify-between items-center px-5 py-4 text-sm text-gray-600" aria-label="Pagination">
      <span>
        Showing {startItem}–{endItem} of {total} · page {currentPage} · page size {pageSize} (limit and offset sent to the API)
      </span>
      <span className="flex gap-2 items-center">
        <button
          onClick={() => onPageChange(currentPage - 1)}
          disabled={!canGoPrevious}
          className={`min-w-[36px] h-9 inline-flex items-center justify-center border rounded px-2.5 font-semibold ${
            !canGoPrevious
              ? 'text-gray-600 bg-gray-100 border-gray-500 cursor-not-allowed'
              : 'text-gray-700 bg-white border-gray-500'
          }`}
        >
          Previous
        </button>
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => {
          // Show first, last, current, and pages around current
          if (
            page === 1 ||
            page === totalPages ||
            (page >= currentPage - 1 && page <= currentPage + 1)
          ) {
            return (
              <button
                key={page}
                onClick={() => onPageChange(page)}
                className={`min-w-[36px] h-9 inline-flex items-center justify-center border rounded px-2.5 font-semibold ${
                  page === currentPage
                    ? 'bg-blue-900 text-white border-blue-900'
                    : 'text-gray-700 bg-white border-gray-500'
                }`}
                aria-current={page === currentPage ? 'page' : undefined}
              >
                {page}
              </button>
            )
          } else if (page === currentPage - 2 || page === currentPage + 2) {
            return <span key={page} className="px-1">…</span>
          }
          return null
        })}
        <button
          onClick={() => onPageChange(currentPage + 1)}
          disabled={!canGoNext}
          className={`min-w-[36px] h-9 inline-flex items-center justify-center border rounded px-2.5 font-semibold ${
            !canGoNext
              ? 'text-gray-600 bg-gray-100 border-gray-500 cursor-not-allowed'
              : 'text-gray-700 bg-white border-gray-500'
          }`}
        >
          Next
        </button>
      </span>
    </nav>
  )
}
