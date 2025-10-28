import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import { ApiError } from '@shared/types'

// ❌ PROBLEMA: API Client muy básico sin features empresariales
// ❌ PROBLEMA: No retry logic para failed requests
// ❌ PROBLEMA: No request caching
// ❌ PROBLEMA: No request deduplication
class ApiClient {
  private client: AxiosInstance

  // ❌ PROBLEMA: Constructor muy básico sin configuración avanzada
  // ❌ PROBLEMA: BaseURL hardcodeada - should come from env
  // ❌ PROBLEMA: No configuración de diferentes environments
  constructor(baseURL: string = 'http://localhost:8000') {
    this.client = axios.create({
      baseURL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
      // ❌ PROBLEMA: No configuración de:
      // - withCredentials
      // - maxRedirects
      // - validateStatus
      // - transformRequest/transformResponse
    })

    this.setupInterceptors()
  }

  // ❌ PROBLEMA: Interceptors básicos sin features avanzadas
  private setupInterceptors(): void {
    // ❌ PROBLEMA: Request interceptor muy simple
    this.client.interceptors.request.use(
      (config) => {
        // ❌ PROBLEMA: Token management muy básico
        // ❌ PROBLEMA: No token refresh logic
        // ❌ PROBLEMA: No token expiry check
        const token = localStorage.getItem('auth_token')
        if (token) {
          config.headers.Authorization = `Bearer ${token}`
        }
        
        // ❌ PROBLEMA: No request ID generation para tracing
        // ❌ PROBLEMA: No request timing
        // ❌ PROBLEMA: No request logging
        
        return config
      },
      (error) => {
        // ❌ PROBLEMA: No error logging en request interceptor
        return Promise.reject(error)
      }
    )

    // ❌ PROBLEMA: Response interceptor sin features avanzadas
    this.client.interceptors.response.use(
      (response: AxiosResponse) => {
        // ❌ PROBLEMA: No response transformation
        // ❌ PROBLEMA: No response caching
        // ❌ PROBLEMA: No response validation
        return response
      },
      (error) => {
        // ❌ PROBLEMA: Error handling muy básico
        const apiError: ApiError = {
          message: error.response?.data?.detail || error.message || 'Unknown error',
          status: error.response?.status || 500,
          details: error.response?.data
        }

        // ❌ PROBLEMA: Error handling muy simple
        if (apiError.status === 401) {
          // ❌ PROBLEMA: Token cleanup muy básico
          localStorage.removeItem('auth_token')
          // ❌ PROBLEMA: Hard redirect - should use router
          // window.location.href = '/login'
          console.log('Unauthorized - token cleared')
        }

        // ❌ PROBLEMA: No retry logic para network errors
        // ❌ PROBLEMA: No exponential backoff
        // ❌ PROBLEMA: No error reporting to service (Sentry, etc.)
        
        return Promise.reject(apiError)
      }
    )
  }

  // ❌ PROBLEMA: Generic request methods sin features avanzadas
  // ❌ PROBLEMA: No request cancellation support
  // ❌ PROBLEMA: No upload progress tracking
  // ❌ PROBLEMA: No download progress tracking
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }

  // ❌ PROBLEMA: Utility methods muy básicos
  // ❌ PROBLEMA: No token refresh mechanism
  // ❌ PROBLEMA: No secure token storage (should use httpOnly cookies)
  setAuthToken(token: string): void {
    localStorage.setItem('auth_token', token)
    // ❌ PROBLEMA: No token expiry management
    // ❌ PROBLEMA: No automatic header update
  }

  removeAuthToken(): void {
    localStorage.removeItem('auth_token')
    // ❌ PROBLEMA: No cleanup de headers pendientes
  }

  getAuthToken(): string | null {
    return localStorage.getItem('auth_token')
  }

  // ❌ PROBLEMA: No métodos para:
  // - File uploads con progress
  // - Request cancellation
  // - Batch requests
  // - Request caching
  // - Request retry con exponential backoff
  // - Network status detection
  // - Request/response logging
  // - Request metrics collection
}

// ❌ PROBLEMA: Singleton pattern sin lazy loading
// ❌ PROBLEMA: No configuración per-environment
// ❌ PROBLEMA: No múltiples instancias para diferentes APIs
export const apiClient = new ApiClient()
export default apiClient