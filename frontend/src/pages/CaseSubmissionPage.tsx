/**
 * Case Submission Page
 * Implements the case submission page from wireframe_case_submission.html
 */

import { useNavigate } from 'react-router-dom'
import { CaseSubmissionForm } from '../components/case/CaseSubmissionForm'

export function CaseSubmissionPage() {
  const navigate = useNavigate()

  const handleSuccess = (caseId: string) => {
    // Navigate to the case detail page after successful submission
    navigate(`/cases/${caseId}`)
  }

  return (
    <div className="p-6">
      <div className="mb-6 flex justify-between items-start gap-6">
        <div>
          <h1 className="text-3xl font-bold">Submit a new case</h1>
          <p className="text-gray-600 mt-2 max-w-3xl">
            Create a formal case with the International Agreements & Origin section. When you submit, the case is registered, checked for completeness and eligibility, and routed automatically. You will see the result immediately.
          </p>
        </div>
        <div className="flex gap-2 flex-wrap">
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700 border border-gray-300">
            Route /cases/new
          </span>
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-gray-200 text-gray-700 border border-gray-300">
            Sample data
          </span>
          <span className="inline-block px-3 py-1 rounded text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-800">
            Wireframe · MVP release
          </span>
        </div>
      </div>

      <div className="grid grid-cols-[minmax(0,1fr)_400px] gap-6 items-start">
        <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="form-title">
          <div className="p-5 border-b border-gray-300">
            <h2 id="form-title" className="text-lg font-bold">Case details</h2>
            <p className="text-sm text-gray-600 mt-1">
              Fields marked required must be completed before the case can be registered. Small monospace names show the matching API field.
            </p>
          </div>
          <div className="p-6">
            <CaseSubmissionForm onSuccess={handleSuccess} />
          </div>
        </section>

        <aside className="flex flex-col gap-6" aria-label="Submission guidance and build notes">
          <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="what-happens">
            <div className="p-4 border-b border-gray-300">
              <h2 id="what-happens" className="text-lg font-bold">What happens on submit</h2>
              <p className="text-sm text-gray-600 mt-1">Three automatic steps run in order, in one request.</p>
            </div>
            <div className="p-5">
              <ol className="list-none p-0 m-0">
                {[
                  {
                    id: 'ATS1',
                    title: 'Register case',
                    meta: 'System · formal case number issued and registration synced with the system of record',
                    source: 'system'
                  },
                  {
                    id: 'ATS2',
                    title: 'Validate completeness and eligibility',
                    meta: 'Deterministic Rule Engine · any failure is reported with its exact reason, never silently dropped',
                    source: 'rule'
                  },
                  {
                    id: 'ATS3',
                    title: 'Classify and route',
                    meta: 'AGN1 Intake & Routing Agent · proposes the workflow, next step and accountable role; the route is checked by rule before it is accepted',
                    source: 'agent'
                  }
                ].map((step, index) => (
                  <li key={step.id} className={`grid grid-cols-[56px_1fr] gap-3 py-3 ${index < 2 ? 'border-b border-gray-300' : ''}`}>
                    <span className="font-mono font-bold text-sm bg-blue-900 text-white rounded text-center py-0.5 h-6">
                      {step.id}
                    </span>
                    <div>
                      <div className="font-semibold">{step.title}</div>
                      <div className="text-xs text-gray-600 mt-0.5">
                        <span className={`inline-flex items-center gap-1.5 font-semibold text-xs ${
                          step.source === 'system' ? 'text-gray-700' : 'text-blue-900'
                        }`}>
                          <span className={`w-2.5 h-2.5 border-2 border-blue-900 ${
                            step.source === 'rule' ? 'bg-blue-900' :
                            step.source === 'agent' ? 'rotate-45 bg-blue-50' :
                            'rounded-full bg-transparent'
                          }`}></span>
                        </span>
                        {step.meta}
                      </div>
                    </div>
                  </li>
                ))}
              </ol>
              <p className="mt-3 p-3 border-2 border-dashed border-gray-500 rounded text-sm text-gray-500 bg-gray-50">
                Later review stages (ATS4, ATS6, ATS8, ATS11, ATS14) are not part of this release.
              </p>
            </div>
          </section>

          <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="who-sees">
            <div className="p-4 border-b border-gray-300">
              <h2 id="who-sees" className="text-lg font-bold">What you see as an applicant</h2>
            </div>
            <div className="p-5">
              <ul className="list-disc pl-6 text-sm space-y-1">
                <li>A plain-language reason whenever your submission is held or rejected.</li>
                <li>Your case reference, current state, current step and the role responsible for the next action.</li>
                <li>Rule internals and internal rationale are not shown to applicants.</li>
                <li>Staff entering a case see the internal entry variant, and can see full reason codes on the case detail page.</li>
              </ul>
            </div>
          </section>

          <section className="bg-white border border-gray-300 rounded-lg" aria-labelledby="build-notes">
            <div className="p-4 border-b border-gray-300">
              <h2 id="build-notes" className="text-lg font-bold">Build notes</h2>
            </div>
            <div className="p-5">
              <dl className="grid grid-cols-[110px_1fr] gap-x-3 gap-y-1.5 text-sm">
                <dt className="text-gray-600">Page</dt>
                <dd><code className="font-mono text-xs">CaseSubmissionPage</code></dd>
                <dt className="text-gray-600">Route</dt>
                <dd><code className="font-mono text-xs">/cases/new</code> (signed-in users only)</dd>
                <dt className="text-gray-600">API call</dt>
                <dd className="font-mono text-xs">POST /api/v1/cases</dd>
                <dt className="text-gray-600">Errors</dt>
                <dd className="text-xs">400 shown as a banner, 422 shown on the field, 401 returns to sign-in</dd>
                <dt className="text-gray-600">Field names</dt>
                <dd className="text-xs">Snake_case, matching the response types one for one</dd>
              </dl>
            </div>
          </section>
        </aside>
      </div>
    </div>
  )
}
