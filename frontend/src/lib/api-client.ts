/**
 * Centralized API client for all backend communication
 * Uses same-origin /api/v1 base with no hardcoded localhost URLs
 */

const API_BASE = import.meta.env.VITE_API_URL ?? '/api/v1'

export class ApiError extends Error {
  constructor(
    public status: number,
    public detail: string
  ) {
    super(detail)
    this.name = 'ApiError'
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = localStorage.getItem('access_token')
  const headers = new Headers(options.headers)
  
  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }
  
  if (options.body && !headers.has('Content-Type')) {
    headers.set('Content-Type', 'application/json')
  }

  const url = `${API_BASE}${path}`
  
  try {
    const response = await fetch(url, { ...options, headers })
    
    // Handle 401 Unauthorized
    if (response.status === 401) {
      // Only redirect if we had a token (i.e., we were logged in)
      // If there's no token, it's a failed login attempt, so just throw
      if (token) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
      
      let errorDetail: string
      try {
        const errorData = await response.json()
        errorDetail = errorData.detail || 'Unauthorized'
      } catch {
        errorDetail = 'Unauthorized'
      }
      throw new ApiError(401, errorDetail)
    }
    
    // Handle other errors
    if (!response.ok) {
      let errorDetail: string
      try {
        const errorData = await response.json()
        errorDetail = errorData.detail || 'Request failed'
      } catch {
        errorDetail = await response.text() || 'Request failed'
      }
      throw new ApiError(response.status, errorDetail)
    }
    
    // Handle 204 No Content
    if (response.status === 204) {
      return null as T
    }
    
    // Parse JSON response
    return response.json() as Promise<T>
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(500, 'Network error: ' + (error as Error).message)
  }
}

export const apiClient = {
  get<T>(path: string): Promise<T> {
    return request<T>(path, { method: 'GET' })
  },

  post<T>(path: string, data?: unknown): Promise<T> {
    return request<T>(path, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined,
    })
  },

  put<T>(path: string, data?: unknown): Promise<T> {
    return request<T>(path, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined,
    })
  },

  delete<T>(path: string): Promise<T> {
    return request<T>(path, { method: 'DELETE' })
  },
}
