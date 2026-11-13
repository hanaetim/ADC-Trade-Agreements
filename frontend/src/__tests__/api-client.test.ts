/**
 * API client unit tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { apiClient, ApiError } from '../lib/api-client'

describe('API Client', () => {
  beforeEach(() => {
    // Clear localStorage before each test
    localStorage.clear()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  it('should make GET requests', async () => {
    const mockResponse = { data: 'test' }
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockResponse,
    })

    const result = await apiClient.get('/test')
    
    expect(result).toEqual(mockResponse)
    expect(global.fetch).toHaveBeenCalledWith(
      '/api/v1/test',
      expect.objectContaining({
        method: 'GET',
      })
    )
  })

  it('should include auth token when available', async () => {
    localStorage.setItem('access_token', 'test-token')
    
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({}),
    })

    await apiClient.get('/test')
    
    const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0]
    const headers = fetchCall?.[1]?.headers as Headers
    expect(headers?.get('Authorization')).toBe('Bearer test-token')
  })

  it('should handle 401 by clearing storage', async () => {
    localStorage.setItem('access_token', 'invalid-token')
    
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 401,
    })

    await expect(apiClient.get('/test')).rejects.toThrow(ApiError)
    expect(localStorage.getItem('access_token')).toBeNull()
  })

  it('should handle error responses', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({ detail: 'Bad request' }),
    })

    await expect(apiClient.get('/test')).rejects.toThrow('Bad request')
  })

  it('should make POST requests with JSON body', async () => {
    const mockData = { name: 'test' }
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 201,
      json: async () => mockData,
    })

    await apiClient.post('/test', mockData)
    
    const fetchCall = (global.fetch as ReturnType<typeof vi.fn>).mock.calls[0]
    expect(fetchCall?.[1]?.method).toBe('POST')
    expect(fetchCall?.[1]?.body).toBe(JSON.stringify(mockData))
  })

  it('should handle 204 No Content', async () => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 204,
    })

    const result = await apiClient.delete('/test')
    expect(result).toBeNull()
  })
})
