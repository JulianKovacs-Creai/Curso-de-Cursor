// ============================================================================
// AUTH FEATURE TYPES - Authentication and authorization related types
// ============================================================================

import { User, UserRole, BaseEntity } from '@/shared/types'

// Re-export shared types
export type { User, UserRole, BaseEntity }

// Authentication types
export interface AuthState {
  user: User | null
  token: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

export interface LoginCredentials {
  email: string
  password: string
  rememberMe?: boolean
}

export interface RegisterCredentials {
  email: string
  password: string
  confirmPassword: string
  firstName: string
  lastName: string
  phone?: string
  acceptTerms: boolean
  marketingOptIn?: boolean
}

export interface AuthResponse {
  user: User
  accessToken: string
  refreshToken: string
  expiresIn: number
  tokenType: string
}

export interface RefreshTokenResponse {
  accessToken: string
  refreshToken: string
  expiresIn: number
}

// Password management
export interface PasswordResetRequest {
  email: string
}

export interface PasswordResetConfirm {
  token: string
  password: string
  confirmPassword: string
}

export interface ChangePasswordRequest {
  currentPassword: string
  newPassword: string
  confirmPassword: string
}

// Email verification
export interface EmailVerificationRequest {
  email: string
}

export interface EmailVerificationConfirm {
  token: string
}

// Two-factor authentication
export interface TwoFactorSetup {
  secret: string
  qrCode: string
  backupCodes: string[]
}

export interface TwoFactorVerify {
  code: string
  backupCode?: string
}

// Social authentication
export interface SocialAuthProvider {
  name: string
  displayName: string
  icon: string
  url: string
}

export interface SocialAuthResponse {
  provider: string
  accessToken: string
  userInfo: SocialUserInfo
}

export interface SocialUserInfo {
  id: string
  email: string
  firstName: string
  lastName: string
  avatar?: string
  provider: string
}

// Session management
export interface Session {
  id: string
  userId: string
  deviceInfo: DeviceInfo
  ipAddress: string
  userAgent: string
  isActive: boolean
  lastActivity: string
  createdAt: string
  expiresAt: string
}

export interface DeviceInfo {
  type: 'desktop' | 'mobile' | 'tablet'
  os: string
  browser: string
  version: string
}

// Permission and role management
export interface Permission {
  id: string
  name: string
  resource: string
  action: string
  description: string
}

export interface RolePermission {
  roleId: string
  permissionId: string
  granted: boolean
}

export interface UserPermission {
  userId: string
  permission: Permission
  granted: boolean
  grantedBy: string
  grantedAt: string
}

// Auth hooks types
export interface UseAuthReturn {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  login: (credentials: LoginCredentials) => Promise<void>
  register: (credentials: RegisterCredentials) => Promise<void>
  logout: () => Promise<void>
  refreshToken: () => Promise<void>
  resetPassword: (request: PasswordResetRequest) => Promise<void>
  changePassword: (request: ChangePasswordRequest) => Promise<void>
  verifyEmail: (token: string) => Promise<void>
  resendVerification: () => Promise<void>
}

export interface UseLoginReturn {
  login: (credentials: LoginCredentials) => Promise<void>
  isLoading: boolean
  error: string | null
}

export interface UseRegisterReturn {
  register: (credentials: RegisterCredentials) => Promise<void>
  isLoading: boolean
  error: string | null
}

// Form validation types
export interface LoginFormData {
  email: string
  password: string
  rememberMe: boolean
}

export interface RegisterFormData {
  email: string
  password: string
  confirmPassword: string
  firstName: string
  lastName: string
  phone: string
  acceptTerms: boolean
  marketingOptIn: boolean
}

// Auth context types
export interface AuthContextType {
  // User data
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: Error | null

  // Actions
  login: (credentials: LoginCredentials) => Promise<AuthResponse>
  register: (credentials: RegisterCredentials) => Promise<AuthResponse>
  logout: () => Promise<void>
  refreshToken: () => Promise<RefreshTokenResponse>

  // Mutation states
  isLoggingIn: boolean
  isRegistering: boolean
  isLoggingOut: boolean
  isRefreshing: boolean

  // Mutation errors
  loginError: Error | null
  registerError: Error | null
  logoutError: Error | null
  refreshError: Error | null

  // Reset functions
  resetLoginError: () => void
  resetRegisterError: () => void
  resetLogoutError: () => void
  resetRefreshError: () => void
}

// Protected route types
export interface ProtectedRouteProps {
  children: React.ReactNode
  requiredRole?: UserRole
  requiredPermissions?: string[]
  fallback?: React.ReactNode
  redirectTo?: string
}

// Auth service types
export interface AuthService {
  login(credentials: LoginCredentials): Promise<AuthResponse>
  register(credentials: RegisterCredentials): Promise<AuthResponse>
  logout(): Promise<void>
  refreshToken(): Promise<RefreshTokenResponse>
  resetPassword(request: PasswordResetRequest): Promise<void>
  changePassword(request: ChangePasswordRequest): Promise<void>
  verifyEmail(token: string): Promise<void>
  resendVerification(): Promise<void>
  getCurrentUser(): Promise<User>
  updateProfile(updates: Partial<User>): Promise<User>
  deleteAccount(): Promise<void>
}

// Auth utility types
export interface AuthUtils {
  isTokenExpired(token: string): boolean
  getTokenExpiration(token: string): Date | null
  parseJWT(token: string): any
  hasPermission(user: User, permission: string): boolean
  hasRole(user: User, role: UserRole): boolean
  canAccess(user: User, resource: string, action: string): boolean
}

// Auth error types
export interface AuthError {
  code: string
  message: string
  field?: string
  details?: Record<string, any>
}

export enum AuthErrorCode {
  INVALID_CREDENTIALS = 'INVALID_CREDENTIALS',
  EMAIL_NOT_VERIFIED = 'EMAIL_NOT_VERIFIED',
  ACCOUNT_LOCKED = 'ACCOUNT_LOCKED',
  TOKEN_EXPIRED = 'TOKEN_EXPIRED',
  INVALID_TOKEN = 'INVALID_TOKEN',
  EMAIL_ALREADY_EXISTS = 'EMAIL_ALREADY_EXISTS',
  WEAK_PASSWORD = 'WEAK_PASSWORD',
  INVALID_EMAIL = 'INVALID_EMAIL',
  RATE_LIMITED = 'RATE_LIMITED',
  TWO_FACTOR_REQUIRED = 'TWO_FACTOR_REQUIRED',
  INVALID_TWO_FACTOR_CODE = 'INVALID_TWO_FACTOR_CODE'
}
