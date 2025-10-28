// Export all components
export { default as LoginForm } from './components/LoginForm'
export { default as RegisterForm } from './components/RegisterForm'
export { default as ProtectedRoute } from './components/ProtectedRoute'

// Export all hooks
export { 
  useAuth,
  usePasswordManagement,
  useEmailVerification,
  authKeys
} from './hooks/useAuth'

export { useLogin } from './hooks/useLogin'
export { useRegister } from './hooks/useRegister'

// Export context
export { 
  AuthProvider, 
  useAuthContext, 
  useAuthState, 
  useAuthActions, 
  useAuthErrors 
} from './context/AuthContext'

// Export all services
export { authService } from './services/authService'

// Export all types
export type {
  User,
  LoginCredentials,
  RegisterCredentials,
  AuthResponse,
  RefreshTokenResponse,
  PasswordResetRequest,
  PasswordResetConfirm,
  ChangePasswordRequest,
  EmailVerificationRequest,
  EmailVerificationConfirm,
  AuthState,
  AuthContextType,
  ProtectedRouteProps
} from './types'

// Export all utils
export { authUtils } from './utils/authUtils'
