/**
 * Detailed Event Stream Component
 * Shows all case events with visibility filtering
 */

import type { CaseEventDTO } from '../../types'

interface DetailedEventStreamProps {
  events: CaseEventDTO[]
  viewerRole: string
}

export function DetailedEventStream({ events, viewerRole }: DetailedEventStreamProps) {
  const isExternalRole = viewerRole === 'external_applicant'
  
  // Filter events based on viewer role
  const visibleEvents = isExternalRole
    ? events.filter(event => event.visible_to_external)
    : events

  const getDecisionSourceClass = (source: string) => {
    const sourceMap: Record<string, string> = {
      'deterministic_rule': 'src-rule',
      'agent': 'src-agent',
      'human': 'src-human',
      'system': 'src-system',
    }
    return `src ${sourceMap[source] || 'src-system'}`
  }

  return (
    <section className="card mb-5" aria-labelledby="events-title">
      <div className="card-head">
        <div>
          <h2 id="events-title">Detailed event stream</h2>
          <p>
            Complete audit trail of all case transitions and decisions. 
            {isExternalRole && ' (Filtered to externally visible events only)'}
          </p>
        </div>
      </div>
      <div className="card-body">
        <table className="mini w-full">
          <thead>
            <tr>
              <th scope="col">Event ID</th>
              <th scope="col">Event Type</th>
              <th scope="col">Step</th>
              <th scope="col">Source</th>
              <th scope="col">Actor Type</th>
              <th scope="col">Actor ID</th>
              <th scope="col">Visible to External</th>
              <th scope="col">Reason Code</th>
              <th scope="col">Rationale</th>
              <th scope="col">Correlation ID</th>
              <th scope="col">Occurred At</th>
            </tr>
          </thead>
          <tbody>
            {visibleEvents.length === 0 ? (
              <tr>
                <td colSpan={11} className="text-center text-text-muted">
                  No events visible
                </td>
              </tr>
            ) : (
              visibleEvents.map((event) => (
                <tr key={event.event_id}>
                  <td className="font-mono text-xs">{event.event_id.substring(0, 8)}...</td>
                  <td className="font-mono">{event.event_type}</td>
                  <td className="font-mono">{event.step_id || '—'}</td>
                  <td>
                    <span className={getDecisionSourceClass(event.decision_source)}>
                      {event.decision_source.replace('_', ' ')}
                    </span>
                  </td>
                  <td>{event.actor_type}</td>
                  <td className="font-mono text-xs">{event.actor_id}</td>
                  <td>
                    <span className={`badge ${event.visible_to_external ? 'st-routed' : 'st-blocked'}`}>
                      {event.visible_to_external ? 'yes' : 'no'}
                    </span>
                  </td>
                  <td className="font-mono text-xs">{event.reason_code || '—'}</td>
                  <td className="text-sm">{event.rationale_summary || '—'}</td>
                  <td className="font-mono text-xs">{event.correlation_id}</td>
                  <td className="font-mono text-xs">
                    {new Date(event.occurred_at).toLocaleString()}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
        {isExternalRole && events.length > visibleEvents.length && (
          <p className="hint text-xs mt-3">
            Showing {visibleEvents.length} of {events.length} events (externally visible only)
          </p>
        )}
      </div>
    </section>
  )
}
