import { useMutation } from '@tanstack/react-query'
import { authService } from '../services/authService'
import { RegisterCredentials, AuthResponse } from '../types'

export const useRegister = () => {
  return useMutation({
    mutationFn: (credentials: RegisterCredentials) => authService.register(credentials),
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
      console.error('Register error:', error)
    }
  })
}
