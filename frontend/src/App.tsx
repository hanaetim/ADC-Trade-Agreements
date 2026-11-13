/**
 * Main application component
 * Sets up routing and authentication
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './lib/auth-context'
import { RequireAuth } from './components/auth/RequireAuth'
import { LoginPage } from './components/auth/LoginPage'
import { Layout } from './components/layout/Layout'
import { CaseQueuePage } from './pages/CaseQueuePage'
import { CaseSubmissionPage } from './pages/CaseSubmissionPage'
import { CaseDetailPage } from './pages/CaseDetailPage'
import { CaseTracePage } from './pages/CaseTracePage'

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route
            path="/cases"
            element={
              <RequireAuth>
                <Layout>
                  <CaseQueuePage />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/cases/new"
            element={
              <RequireAuth>
                <Layout>
                  <CaseSubmissionPage />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/cases/:caseId"
            element={
              <RequireAuth>
                <Layout>
                  <CaseDetailPage />
                </Layout>
              </RequireAuth>
            }
          />
          <Route
            path="/cases/:caseId/trace"
            element={
              <RequireAuth>
                <Layout>
                  <CaseTracePage />
                </Layout>
              </RequireAuth>
            }
          />
          <Route path="/" element={<Navigate to="/cases" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
