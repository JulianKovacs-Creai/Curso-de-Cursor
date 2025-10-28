import { apiClient } from '@/shared/services/apiClient'
import { 
  LoginCredentials, 
  RegisterCredentials, 
  AuthResponse, 
  User,
  RefreshTokenResponse,
  PasswordResetRequest,
  PasswordResetConfirm,
  ChangePasswordRequest,
  EmailVerificationRequest,
  EmailVerificationConfirm
} from '../types'

export const authService = {
  // Authentication
  async login(credentials: LoginCredentials): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/login', credentials)
    
    // Store tokens
    if (response.accessToken) {
      localStorage.setItem('auth_token', response.accessToken)
    }
    if (response.refreshToken) {
      localStorage.setItem('refresh_token', response.refreshToken)
    }
    
    return response
  },

  async register(credentials: RegisterCredentials): Promise<AuthResponse> {
    const response = await apiClient.post<AuthResponse>('/api/v1/auth/register', credentials)
    
    // Store tokens
    if (response.accessToken) {
      localStorage.setItem('auth_token', response.accessToken)
    }
    if (response.refreshToken) {
      localStorage.setItem('refresh_token', response.refreshToken)
    }
    
    return response
  },

  async logout(): Promise<void> {
    try {
      await apiClient.post('/api/v1/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('refresh_token')
    }
  },

  async getCurrentUser(): Promise<User> {
    const token = localStorage.getItem('auth_token')
    if (!token) {
      throw new Error('No authentication token')
    }
    
    const response = await apiClient.get<User>('/api/v1/auth/me')
    return response
  },

  async refreshToken(): Promise<RefreshTokenResponse> {
    const refreshToken = localStorage.getItem('refresh_token')
    if (!refreshToken) {
      throw new Error('No refresh token available')
    }

    const response = await apiClient.post<RefreshTokenResponse>(
      '/api/v1/auth/refresh',
      { refresh_token: refreshToken }
    )
    
    // Update tokens
    if (response.accessToken) {
      localStorage.setItem('auth_token', response.accessToken)
    }
    if (response.refreshToken) {
      localStorage.setItem('refresh_token', response.refreshToken)
    }
    
    return response
  },

  // Password management
  async resetPassword(request: PasswordResetRequest): Promise<void> {
    await apiClient.post('/api/v1/auth/password/reset', request)
  },

  async confirmPasswordReset(request: PasswordResetConfirm): Promise<void> {
    await apiClient.post('/api/v1/auth/password/reset/confirm', request)
  },

  async changePassword(request: ChangePasswordRequest): Promise<void> {
    await apiClient.post('/api/v1/auth/password/change', request)
  },

  // Email verification
  async requestEmailVerification(request: EmailVerificationRequest): Promise<void> {
    await apiClient.post('/api/v1/auth/email/verify', request)
  },

  async confirmEmailVerification(request: EmailVerificationConfirm): Promise<void> {
    await apiClient.post('/api/v1/auth/email/verify/confirm', request)
  },

  // Token management
  getToken(): string | null {
    return localStorage.getItem('auth_token')
  },

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token')
  },

  isAuthenticated(): boolean {
    return !!this.getToken()
  },

  clearTokens(): void {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('refresh_token')
  }
}
