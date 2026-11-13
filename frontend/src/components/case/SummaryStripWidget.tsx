/**
 * Summary Strip Widget Component
 * Displays summary metrics for case queue from wireframe_case_queue.html
 */

interface SummaryItem {
  count: number
  label: string
  code: string
  color: 'blocked' | 'queued' | 'failed' | 'routed'
}

interface Props {
  items: SummaryItem[]
}

export function SummaryStripWidget({ items }: Props) {
  const colorClasses = {
    blocked: 'border-l-red-700',
    queued: 'border-l-yellow-600',
    failed: 'border-l-gray-600',
    routed: 'border-l-green-700'
  }

  return (
    <section className="grid grid-cols-4 gap-4 mb-6" aria-label="Queue summary for the current filter">
      {items.map((item, index) => (
        <div
          key={index}
          className={`bg-white border border-gray-300 rounded-lg p-4 border-l-[6px] ${colorClasses[item.color]}`}
        >
          <div className="text-3xl font-bold leading-tight">{item.count}</div>
          <div className="text-sm text-gray-600 mt-1">
            {item.label} <code className="font-mono text-xs">{item.code}</code>
          </div>
        </div>
      ))}
    </section>
  )
}
