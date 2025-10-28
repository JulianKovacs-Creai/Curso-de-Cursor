import { apiClient } from './apiClient'

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  first_name?: string
  last_name?: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  user: {
    id: string
    email: string
    first_name?: string
    last_name?: string
    full_name: string
  }
}

export interface User {
  id: string
  email: string
  first_name?: string
  last_name?: string
  full_name: string
  is_active: boolean
  is_verified: boolean
}

class AuthService {
  private readonly TOKEN_KEY = 'auth_token'
  private readonly REFRESH_TOKEN_KEY = 'refresh_token'

  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post<{ data: AuthResponse }>('/api/v1/auth/login', credentials)
    
    // Store tokens
    this.setTokens(response.data.access_token, response.data.refresh_token)
    
    return response.data
  }

  async register(userData: RegisterRequest): Promise<{ message: string }> {
    const response = await apiClient.post<{ data: { message: string } }>('/api/v1/auth/register', userData)
    return response.data
  }

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<{ data: User }>('/api/v1/auth/me')
    return response.data
  }

  async refreshToken(): Promise<{ access_token: string; refresh_token: string; token_type: string }> {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await apiClient.post<{ data: { access_token: string; refresh_token: string; token_type: string } }>(
      '/api/v1/auth/refresh',
      { refresh_token: refreshToken }
    )
    
    // Update tokens
    this.setTokens(response.data.access_token, response.data.refresh_token)
    
    return response.data
  }

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/v1/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      this.clearTokens()
    }
  }

  setTokens(accessToken: string, refreshToken: string): void {
    localStorage.setItem(this.TOKEN_KEY, accessToken)
    localStorage.setItem(this.REFRESH_TOKEN_KEY, refreshToken)
  }

  getToken(): string | null {
    return localStorage.getItem(this.TOKEN_KEY)
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(this.REFRESH_TOKEN_KEY)
  }

  clearTokens(): void {
    localStorage.removeItem(this.TOKEN_KEY)
    localStorage.removeItem(this.REFRESH_TOKEN_KEY)
  }

  isAuthenticated(): boolean {
    return !!this.getToken()
  }
}

export const authService = new AuthService()
