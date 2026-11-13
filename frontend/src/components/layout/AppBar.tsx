/**
 * Application header/top bar component
 * Displays branding and user information
 */

import { useAuth } from '../../lib/auth-context'

export function AppBar() {
  const { user, logout } = useAuth()

  return (
    <header className="flex items-center justify-between h-16 px-6 bg-primary text-primary-contrast">
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-sm border-2 border-primary-contrast flex items-center justify-center font-bold text-sm tracking-wide">
          IAO
        </div>
        <div>
          <div className="text-[17px] font-bold">International Agreements & Origin</div>
          <div className="text-xs opacity-90">Abu Dhabi Customs · International Agreements & Origin section</div>
        </div>
      </div>
      
      <div className="flex items-center gap-4 text-[13px]">
        <span className="border border-white/60 rounded-sm px-2.5 py-0.5 text-[13px]">
          EN | <span lang="ar" dir="rtl">العربية</span>
        </span>
        
        {user && (
          <>
            <span>{user.email}</span>
            <span className="bg-primary-contrast text-primary rounded-full px-3 py-0.5 font-semibold text-xs">
              {user.role}
            </span>
            <button
              onClick={logout}
              className="text-primary-contrast hover:opacity-80 underline"
            >
              Sign out
            </button>
          </>
        )}
      </div>
    </header>
  )
}
