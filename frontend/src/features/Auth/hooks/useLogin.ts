import { useMutation } from '@tanstack/react-query'
import { authService } from '../services/authService'
import { LoginCredentials, AuthResponse } from '../types'

export const useLogin = () => {
  return useMutation({
    mutationFn: (credentials: LoginCredentials) => authService.login(credentials),
    onSuccess: (data: AuthResponse) => {
      // Store tokens
      if (data.accessToken) {
        localStorage.setItem('auth_token', data.accessToken)
      }
      if (data.refreshToken) {
        localStorage.setItem('refresh_token', data.refreshToken)
      }
    },
    onError: (error) => {
      console.error('Login error:', error)
    }
  })
}
