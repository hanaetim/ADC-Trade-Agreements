/**
 * Application navigation component
 * Primary navigation links
 */

import { NavLink } from 'react-router-dom'

export function AppNav() {
  return (
    <nav className="flex gap-2 px-6 bg-surface border-b border-border" aria-label="Primary">
      <NavLink
        to="/cases/new"
        className={({ isActive }) =>
          `inline-block px-4 py-3.5 no-underline font-medium border-b-[3px] transition-colors ${
            isActive
              ? 'text-primary font-bold border-primary'
              : 'text-text-muted border-transparent hover:text-text'
          }`
        }
      >
        New case
      </NavLink>
      <NavLink
        to="/cases"
        className={({ isActive }) =>
          `inline-block px-4 py-3.5 no-underline font-medium border-b-[3px] transition-colors ${
            isActive
              ? 'text-primary font-bold border-primary'
              : 'text-text-muted border-transparent hover:text-text'
          }`
        }
      >
        Cases
      </NavLink>
    </nav>
  )
}
