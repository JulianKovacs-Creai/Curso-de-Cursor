import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authService } from '../services/authService'
import { 
  LoginCredentials, 
  RegisterCredentials, 
  AuthResponse, 
  PasswordResetRequest,
  PasswordResetConfirm,
  ChangePasswordRequest,
  EmailVerificationRequest,
  EmailVerificationConfirm
} from '../types'

// Query keys for consistent caching
export const authKeys = {
  all: ['auth'] as const,
  user: () => [...authKeys.all, 'user'] as const,
  sessions: () => [...authKeys.all, 'sessions'] as const,
}

// Hook for getting current user
export const useAuth = () => {
  const queryClient = useQueryClient()

  const { data: user, isLoading, error } = useQuery({
    queryKey: authKeys.user(),
    queryFn: authService.getCurrentUser,
    enabled: !!localStorage.getItem('auth_token'), // Only try if there's a token
    staleTime: 5 * 60 * 1000, // 5 minutes
    retry: (failureCount, error: any) => {
      if (error?.status === 401) {
        return false
      }
      return failureCount < 3
    }
  })

  const loginMutation = useMutation({
    mutationFn: (credentials: LoginCredentials) => authService.login(credentials),
    onSuccess: (data: AuthResponse) => {
      // Update user data in cache
      queryClient.setQueryData(authKeys.user(), data.user)
      // Invalidate user query to refetch
      queryClient.invalidateQueries({ queryKey: authKeys.user() })
    },
    onError: (error) => {
      console.error('Login error:', error)
    }
  })

  const registerMutation = useMutation({
    mutationFn: (credentials: RegisterCredentials) => authService.register(credentials),
    onSuccess: (data: AuthResponse) => {
      // Update user data in cache
      queryClient.setQueryData(authKeys.user(), data.user)
      // Invalidate user query to refetch
      queryClient.invalidateQueries({ queryKey: authKeys.user() })
    },
    onError: (error) => {
      console.error('Register error:', error)
    }
  })

  const logoutMutation = useMutation({
    mutationFn: () => authService.logout(),
    onSuccess: () => {
      // Clear user data from cache
      queryClient.removeQueries({ queryKey: authKeys.user() })
      // Clear all auth-related queries
      queryClient.removeQueries({ queryKey: authKeys.all })
    },
    onError: (error) => {
      console.error('Logout error:', error)
    }
  })

  const refreshTokenMutation = useMutation({
    mutationFn: () => authService.refreshToken(),
    onSuccess: () => {
      // Invalidate user query to refetch with new token
      queryClient.invalidateQueries({ queryKey: authKeys.user() })
    },
    onError: () => {
      // If refresh fails, logout user
      queryClient.removeQueries({ queryKey: authKeys.all })
    }
  })

  return {
    // User data
    user,
    isAuthenticated: !!user,
    isLoading,
    error,

    // Actions
    login: loginMutation.mutateAsync,
    register: registerMutation.mutateAsync,
    logout: logoutMutation.mutateAsync,
    refreshToken: refreshTokenMutation.mutateAsync,

    // Mutation states
    isLoggingIn: loginMutation.isPending,
    isRegistering: registerMutation.isPending,
    isLoggingOut: logoutMutation.isPending,
    isRefreshing: refreshTokenMutation.isPending,

    // Mutation errors
    loginError: loginMutation.error,
    registerError: registerMutation.error,
    logoutError: logoutMutation.error,
    refreshError: refreshTokenMutation.error,

    // Reset functions
    resetLoginError: loginMutation.reset,
    resetRegisterError: registerMutation.reset,
    resetLogoutError: logoutMutation.reset,
    resetRefreshError: refreshTokenMutation.reset
  }
}

// Hook for password management
export const usePasswordManagement = () => {
  const resetPasswordMutation = useMutation({
    mutationFn: (request: PasswordResetRequest) => authService.resetPassword(request)
  })

  const confirmPasswordResetMutation = useMutation({
    mutationFn: (request: PasswordResetConfirm) => authService.confirmPasswordReset(request)
  })

  const changePasswordMutation = useMutation({
    mutationFn: (request: ChangePasswordRequest) => authService.changePassword(request)
  })

  return {
    resetPassword: resetPasswordMutation.mutateAsync,
    confirmPasswordReset: confirmPasswordResetMutation.mutateAsync,
    changePassword: changePasswordMutation.mutateAsync,
    
    isResettingPassword: resetPasswordMutation.isPending,
    isConfirmingReset: confirmPasswordResetMutation.isPending,
    isChangingPassword: changePasswordMutation.isPending,
    
    resetPasswordError: resetPasswordMutation.error,
    confirmResetError: confirmPasswordResetMutation.error,
    changePasswordError: changePasswordMutation.error,
    
    resetResetPasswordError: resetPasswordMutation.reset,
    resetConfirmResetError: confirmPasswordResetMutation.reset,
    resetChangePasswordError: changePasswordMutation.reset
  }
}

// Hook for email verification
export const useEmailVerification = () => {
  const requestVerificationMutation = useMutation({
    mutationFn: (request: EmailVerificationRequest) => authService.requestEmailVerification(request)
  })

  const confirmVerificationMutation = useMutation({
    mutationFn: (request: EmailVerificationConfirm) => authService.confirmEmailVerification(request)
  })

  return {
    requestVerification: requestVerificationMutation.mutateAsync,
    confirmVerification: confirmVerificationMutation.mutateAsync,
    
    isRequestingVerification: requestVerificationMutation.isPending,
    isConfirmingVerification: confirmVerificationMutation.isPending,
    
    requestVerificationError: requestVerificationMutation.error,
    confirmVerificationError: confirmVerificationMutation.error,
    
    resetRequestVerificationError: requestVerificationMutation.reset,
    resetConfirmVerificationError: confirmVerificationMutation.reset
  }
}
