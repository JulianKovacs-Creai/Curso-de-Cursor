// ============================================================================
// SHARED TYPES - Common types used across the entire application
// ============================================================================

// Base entity interface
export interface BaseEntity {
  id: string
  createdAt: string
  updatedAt: string
}

// API Response types
export interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
  timestamp: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
    hasNext: boolean
    hasPrev: boolean
  }
}

export interface ApiError {
  message: string
  code: string
  details?: Record<string, any>
  timestamp: string
}

// User types
export interface User extends BaseEntity {
  email: string
  firstName: string
  lastName: string
  phone?: string
  avatar?: string
  role: UserRole
  isActive: boolean
  emailVerified: boolean
  lastLoginAt?: string
}

export interface UserProfile extends User {
  addresses: Address[]
  preferences: UserPreferences
  statistics: UserStatistics
}

export interface Address extends BaseEntity {
  userId: string
  type: AddressType
  street: string
  city: string
  state: string
  country: string
  zipCode: string
  isDefault: boolean
  coordinates?: {
    lat: number
    lng: number
  }
}

export interface UserPreferences {
  language: string
  currency: string
  timezone: string
  notifications: NotificationSettings
  privacy: PrivacySettings
}

export interface UserStatistics {
  totalOrders: number
  totalSpent: number
  averageOrderValue: number
  favoriteCategories: string[]
  lastOrderDate?: string
}

// Enums
export enum UserRole {
  CUSTOMER = 'customer',
  ADMIN = 'admin',
  MODERATOR = 'moderator',
  VENDOR = 'vendor'
}

export enum AddressType {
  HOME = 'home',
  WORK = 'work',
  BILLING = 'billing',
  SHIPPING = 'shipping'
}

export enum OrderStatus {
  PENDING = 'pending',
  CONFIRMED = 'confirmed',
  PROCESSING = 'processing',
  SHIPPED = 'shipped',
  DELIVERED = 'delivered',
  CANCELLED = 'cancelled',
  REFUNDED = 'refunded'
}

export enum PaymentStatus {
  PENDING = 'pending',
  PAID = 'paid',
  FAILED = 'failed',
  REFUNDED = 'refunded',
  PARTIALLY_REFUNDED = 'partially_refunded'
}

export enum PaymentMethod {
  CREDIT_CARD = 'credit_card',
  DEBIT_CARD = 'debit_card',
  PAYPAL = 'paypal',
  BANK_TRANSFER = 'bank_transfer',
  CASH_ON_DELIVERY = 'cash_on_delivery',
  CRYPTOCURRENCY = 'cryptocurrency'
}

// Notification settings
export interface NotificationSettings {
  email: {
    orderUpdates: boolean
    promotions: boolean
    newsletters: boolean
    security: boolean
  }
  push: {
    orderUpdates: boolean
    promotions: boolean
    security: boolean
  }
  sms: {
    orderUpdates: boolean
    security: boolean
  }
}

// Privacy settings
export interface PrivacySettings {
  profileVisibility: 'public' | 'private' | 'friends'
  dataSharing: boolean
  analytics: boolean
  marketing: boolean
}

// Common utility types
export type Status = 'active' | 'inactive' | 'pending' | 'suspended'
export type SortOrder = 'asc' | 'desc'
export type SortField<T> = keyof T

// Generic filter interface
export interface BaseFilter {
  search?: string
  status?: Status
  dateFrom?: string
  dateTo?: string
  page?: number
  limit?: number
  sortBy?: string
  sortOrder?: SortOrder
}

// File upload types
export interface FileUpload {
  id: string
  filename: string
  originalName: string
  mimeType: string
  size: number
  url: string
  uploadedAt: string
  uploadedBy: string
}

// Analytics types
export interface AnalyticsEvent {
  id: string
  userId?: string
  sessionId: string
  event: string
  properties: Record<string, any>
  timestamp: string
  page: string
  userAgent: string
  ip?: string
}

// Configuration types
export interface AppConfig {
  api: {
    baseUrl: string
    timeout: number
    retries: number
  }
  features: {
    enableAnalytics: boolean
    enableNotifications: boolean
    enableReviews: boolean
    enableWishlist: boolean
  }
  ui: {
    theme: 'light' | 'dark' | 'auto'
    language: string
    currency: string
  }
}

// Error types
export interface ValidationError {
  field: string
  message: string
  code: string
}

export interface BusinessError extends Error {
  code: string
  statusCode: number
  details?: Record<string, any>
}

// Form types
export interface FormState<T> {
  data: T
  errors: Record<keyof T, string>
  touched: Record<keyof T, boolean>
  isSubmitting: boolean
  isValid: boolean
}

// Component props types
export interface BaseComponentProps {
  className?: string
  id?: string
  'data-testid'?: string
}

export interface LoadingState {
  isLoading: boolean
  error?: string | null
}

// Search and filter types
export interface SearchFilters {
  query?: string
  category?: string
  priceRange?: {
    min: number
    max: number
  }
  rating?: number
  availability?: boolean
  tags?: string[]
}

// Pagination types
export interface PaginationParams {
  page: number
  limit: number
  offset?: number
}

export interface PaginationInfo {
  currentPage: number
  totalPages: number
  totalItems: number
  itemsPerPage: number
  hasNextPage: boolean
  hasPreviousPage: boolean
}