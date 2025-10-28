// ============================================================================
// MAIN TYPES EXPORT - Centralized type exports for the entire application
// ============================================================================

// Re-export all shared types
export * from '@/shared/types'

// Re-export all feature types
export * from '@/features/Products/types'
export * from '@/features/Auth/types'
export * from '@/features/Cart/types'
export * from '@/features/Orders/types'

// Global application types
export interface AppState {
  user: User | null
  cart: CartState
  theme: 'light' | 'dark' | 'auto'
  language: string
  currency: string
}

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
    enableComparison: boolean
  }
  ui: {
    theme: 'light' | 'dark' | 'auto'
    language: string
    currency: string
    dateFormat: string
    timeFormat: string
  }
  payment: {
    supportedMethods: PaymentMethod[]
    defaultCurrency: string
    taxRate: number
  }
  shipping: {
    freeShippingThreshold: number
    defaultMethod: string
    supportedRegions: string[]
  }
}

// Route types
export interface RouteConfig {
  path: string
  component: React.ComponentType<any>
  exact?: boolean
  protected?: boolean
  requiredRole?: UserRole
  requiredPermissions?: string[]
  layout?: React.ComponentType<any>
}

// Navigation types
export interface NavigationItem {
  id: string
  label: string
  path: string
  icon?: string
  children?: NavigationItem[]
  permissions?: string[]
  badge?: {
    text: string
    color: string
  }
}

// Theme types
export interface Theme {
  colors: {
    primary: string
    secondary: string
    success: string
    warning: string
    error: string
    info: string
    background: string
    surface: string
    text: string
    textSecondary: string
    border: string
  }
  spacing: {
    xs: string
    sm: string
    md: string
    lg: string
    xl: string
  }
  typography: {
    fontFamily: string
    fontSize: {
      xs: string
      sm: string
      md: string
      lg: string
      xl: string
    }
    fontWeight: {
      light: number
      normal: number
      medium: number
      semibold: number
      bold: number
    }
  }
  breakpoints: {
    xs: string
    sm: string
    md: string
    lg: string
    xl: string
  }
  shadows: {
    sm: string
    md: string
    lg: string
    xl: string
  }
  borderRadius: {
    sm: string
    md: string
    lg: string
    xl: string
  }
}

// API types
export interface ApiEndpoint {
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH'
  url: string
  headers?: Record<string, string>
  timeout?: number
}

export interface ApiRequest {
  endpoint: ApiEndpoint
  data?: any
  params?: Record<string, any>
  headers?: Record<string, string>
}

export interface ApiResponse<T = any> {
  data: T
  message?: string
  success: boolean
  timestamp: string
  pagination?: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

// Event types
export interface AppEvent {
  type: string
  payload: any
  timestamp: string
  userId?: string
  sessionId: string
}

export interface EventHandler {
  (event: AppEvent): void
}

// Store types
export interface StoreState {
  app: AppState
  auth: AuthState
  products: ProductState
  cart: CartState
  orders: OrderState
  ui: UIState
}

export interface ProductState {
  products: Product[]
  categories: ProductCategory[]
  brands: ProductBrand[]
  filters: ProductFilters
  loading: boolean
  error: string | null
}

export interface OrderState {
  orders: Order[]
  currentOrder: Order | null
  loading: boolean
  error: string | null
}

export interface UIState {
  theme: 'light' | 'dark' | 'auto'
  language: string
  currency: string
  sidebarOpen: boolean
  modalOpen: boolean
  modalType: string | null
  notifications: Notification[]
  loading: boolean
}

export interface Notification {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  title: string
  message: string
  duration?: number
  action?: {
    label: string
    onClick: () => void
  }
}

// Utility types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type Required<T, K extends keyof T> = T & { [P in K]-?: T[P] }
export type PartialExcept<T, K extends keyof T> = Partial<T> & Pick<T, K>
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Component utility types
export type ComponentProps<T> = T extends React.ComponentType<infer P> ? P : never
export type ComponentRef<T> = T extends React.ComponentType<any> 
  ? React.ComponentPropsWithRef<T>['ref'] 
  : never

// Form utility types
export type FormField<T> = {
  value: T
  error?: string
  touched: boolean
  dirty: boolean
}

export type FormState<T> = {
  [K in keyof T]: FormField<T[K]>
} & {
  isValid: boolean
  isSubmitting: boolean
  isDirty: boolean
  errors: Record<keyof T, string>
}

// Hook utility types
export type UseAsyncReturn<T> = {
  data: T | null
  loading: boolean
  error: string | null
  execute: (...args: any[]) => Promise<T>
  reset: () => void
}

export type UseFormReturn<T> = {
  values: T
  errors: Record<keyof T, string>
  touched: Record<keyof T, boolean>
  isValid: boolean
  isSubmitting: boolean
  setValue: (field: keyof T, value: T[keyof T]) => void
  setError: (field: keyof T, error: string) => void
  setTouched: (field: keyof T, touched: boolean) => void
  handleSubmit: (onSubmit: (values: T) => void) => (e: React.FormEvent) => void
  reset: () => void
}

// Generic types for common patterns
export type ID = string
export type Timestamp = string
export type Currency = string
export type Language = string
export type Theme = 'light' | 'dark' | 'auto'

// Common interface patterns
export interface Timestamped {
  createdAt: string
  updatedAt: string
}

export interface Identifiable {
  id: string
}

export interface Named {
  name: string
}

export interface Describable {
  description?: string
}

export interface Statused {
  status: string
}

export interface Owned {
  userId: string
}

// Type guards
export function isProduct(obj: any): obj is Product {
  return obj && typeof obj.id === 'string' && typeof obj.name === 'string'
}

export function isUser(obj: any): obj is User {
  return obj && typeof obj.id === 'string' && typeof obj.email === 'string'
}

export function isOrder(obj: any): obj is Order {
  return obj && typeof obj.id === 'string' && typeof obj.orderNumber === 'string'
}

// Type assertions
export function assertIsProduct(obj: any): asserts obj is Product {
  if (!isProduct(obj)) {
    throw new Error('Object is not a Product')
  }
}

export function assertIsUser(obj: any): asserts obj is User {
  if (!isUser(obj)) {
    throw new Error('Object is not a User')
  }
}

export function assertIsOrder(obj: any): asserts obj is Order {
  if (!isOrder(obj)) {
    throw new Error('Object is not an Order')
  }
}
