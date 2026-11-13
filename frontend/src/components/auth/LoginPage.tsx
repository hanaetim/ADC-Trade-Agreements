/**
 * Login page component
 * Uses seed credentials from backend/app/seed.py
 */

import { useState, FormEvent } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../lib/auth-context'

export function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname || '/'

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await login({ email, password })
      navigate(from, { replace: true })
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-bg flex items-center justify-center p-6">
      <div className="w-full max-w-md">
        <div className="bg-surface border border-border rounded-md shadow-sm p-6">
          <div className="mb-6">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-9 h-9 bg-primary text-primary-contrast rounded-sm flex items-center justify-center font-bold text-sm">
                IAO
              </div>
              <h1 className="text-xl font-bold text-text">
                International Agreements & Origin
              </h1>
            </div>
            <p className="text-sm text-text-muted">
              Abu Dhabi Customs · Sign in to continue
            </p>
          </div>

          <form onSubmit={handleSubmit}>
            {error && (
              <div className="mb-4 p-3 bg-danger-bg border-2 border-danger-fg rounded-sm text-danger-fg text-sm">
                <strong className="block mb-1">Sign in failed</strong>
                {error}
              </div>
            )}

            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-semibold mb-1">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-border-strong rounded-sm bg-surface text-text"
                placeholder="external@example.com"
                required
                disabled={isLoading}
              />
            </div>

            <div className="mb-6">
              <label htmlFor="password" className="block text-sm font-semibold mb-1">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-border-strong rounded-sm bg-surface text-text"
                placeholder="External-pass-1"
                required
                disabled={isLoading}
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-2 px-4 bg-primary text-primary-contrast font-semibold rounded-sm hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Signing in...' : 'Sign in'}
            </button>
          </form>

          <div className="mt-6 p-3 bg-info-bg border border-info-fg rounded-sm text-sm">
            <strong className="text-info-fg block mb-2">Demo credentials</strong>
            <ul className="text-text-muted space-y-1 text-xs font-mono">
              <li>external@example.com / External-pass-1</li>
              <li>intake@example.com / Intake-pass-1</li>
              <li>specialist@example.com / Specialist-pass-1</li>
              <li>sectionhead@example.com / Section-pass-1</li>
              <li>policy@example.com / Policy-pass-1</li>
              <li>technical@example.com / Technical-pass-1</li>
              <li>auditor@example.com / Auditor-pass-1</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
