/**
 * Main layout component
 * Wraps pages with AppBar and AppNav
 */

import { ReactNode } from 'react'
import { AppBar } from './AppBar'
import { AppNav } from './AppNav'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-bg">
      <AppBar />
      <AppNav />
      <main className="w-full p-6">{children}</main>
    </div>
  )
}
