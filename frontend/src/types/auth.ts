/**
 * Authentication types
 */

export interface User {
  user_id: string
  email: string
  role: string
  is_active: boolean
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: User
  expires_at: string
}

export interface AuthSession {
  id: string
  user_id: string
  token_hash: string
  issued_at: string
  expires_at: string
  last_activity_at: string
  revoked_at: string | null
}
