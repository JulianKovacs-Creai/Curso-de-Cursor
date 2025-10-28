// ============================================================================
// CART FEATURE TYPES - Shopping cart related types
// ============================================================================

import { BaseEntity } from '@/shared/types'

// Cart item types
export interface CartItem extends BaseEntity {
  productId: string
  userId: string
  quantity: number
  price: number
  totalPrice: number
  productSnapshot: ProductSnapshot
  selectedOptions?: CartProductOption[]
  notes?: string
}

export interface ProductSnapshot {
  id: string
  name: string
  description: string
  image: string
  price: number
  category: string
  brand?: string
  sku: string
  weight?: number
  dimensions?: {
    length: number
    width: number
    height: number
  }
}

export interface CartProductOption {
  id: string
  name: string
  value: string
  priceAdjustment: number
  type: 'color' | 'size' | 'material' | 'style' | 'other'
}

// Cart state types
export interface CartState {
  items: CartItem[]
  totalItems: number
  totalPrice: number
  totalWeight: number
  isLoading: boolean
  error: string | null
  lastUpdated: string
}

export interface CartSummary {
  subtotal: number
  tax: number
  shipping: number
  discount: number
  total: number
  currency: string
}

// Cart operations
export interface AddToCartRequest {
  productId: string
  quantity: number
  options?: CartProductOption[]
  notes?: string
}

export interface UpdateCartItemRequest {
  itemId: string
  quantity: number
  options?: CartProductOption[]
  notes?: string
}

export interface RemoveFromCartRequest {
  itemId: string
}

export interface ClearCartRequest {
  userId: string
}

// Cart validation
export interface CartValidationResult {
  isValid: boolean
  errors: CartValidationError[]
  warnings: CartValidationWarning[]
}

export interface CartValidationError {
  itemId: string
  field: string
  message: string
  code: string
}

export interface CartValidationWarning {
  itemId: string
  message: string
  code: string
}

// Cart hooks types
export interface UseCartReturn {
  cart: CartState
  addItem: (request: AddToCartRequest) => Promise<void>
  updateItem: (request: UpdateCartItemRequest) => Promise<void>
  removeItem: (itemId: string) => Promise<void>
  clearCart: () => Promise<void>
  validateCart: () => Promise<CartValidationResult>
  getCartSummary: () => CartSummary
  isLoading: boolean
  error: string | null
}

export interface UseCartItemsReturn {
  items: CartItem[]
  totalItems: number
  totalPrice: number
  addItem: (request: AddToCartRequest) => Promise<void>
  updateItem: (request: UpdateCartItemRequest) => Promise<void>
  removeItem: (itemId: string) => Promise<void>
  isLoading: boolean
  error: string | null
}

// Cart service types
export interface CartService {
  getCart(userId: string): Promise<CartItem[]>
  addItem(userId: string, request: AddToCartRequest): Promise<CartItem>
  updateItem(userId: string, request: UpdateCartItemRequest): Promise<CartItem>
  removeItem(userId: string, itemId: string): Promise<void>
  clearCart(userId: string): Promise<void>
  validateCart(userId: string): Promise<CartValidationResult>
  getCartSummary(userId: string): Promise<CartSummary>
  mergeCarts(guestCart: CartItem[], userCart: CartItem[]): Promise<CartItem[]>
  saveForLater(userId: string, itemId: string): Promise<void>
  moveToCart(userId: string, itemId: string): Promise<void>
}

// Cart persistence
export interface CartPersistence {
  saveCart(cart: CartState): void
  loadCart(): CartState | null
  clearCart(): void
  saveGuestCart(cart: CartState): void
  loadGuestCart(): CartState | null
  clearGuestCart(): void
}

// Cart calculations
export interface CartCalculations {
  calculateSubtotal(items: CartItem[]): number
  calculateTax(subtotal: number, taxRate: number): number
  calculateShipping(items: CartItem[], shippingMethod: ShippingMethod): number
  calculateDiscount(subtotal: number, discountCode?: string): number
  calculateTotal(subtotal: number, tax: number, shipping: number, discount: number): number
}

// Shipping types
export interface ShippingMethod {
  id: string
  name: string
  description: string
  cost: number
  estimatedDays: number
  freeThreshold?: number
  availableRegions: string[]
}

export interface ShippingAddress {
  firstName: string
  lastName: string
  company?: string
  address1: string
  address2?: string
  city: string
  state: string
  country: string
  zipCode: string
  phone?: string
}

// Discount types
export interface DiscountCode {
  code: string
  type: 'percentage' | 'fixed'
  value: number
  minOrderAmount?: number
  maxDiscountAmount?: number
  validFrom: string
  validUntil: string
  usageLimit?: number
  usedCount: number
  isActive: boolean
}

export interface AppliedDiscount {
  code: string
  type: 'percentage' | 'fixed'
  value: number
  discountAmount: number
  description: string
}

// Cart events
export interface CartEvent {
  type: 'item_added' | 'item_updated' | 'item_removed' | 'cart_cleared' | 'cart_merged'
  itemId?: string
  productId?: string
  quantity?: number
  timestamp: string
  userId: string
}

// Cart analytics
export interface CartAnalytics {
  sessionId: string
  userId?: string
  events: CartEvent[]
  cartAbandonment: boolean
  timeToCheckout: number
  conversionRate: number
}

// Cart components props
export interface CartItemProps {
  item: CartItem
  onUpdate: (request: UpdateCartItemRequest) => void
  onRemove: (itemId: string) => void
  onSaveForLater?: (itemId: string) => void
  isLoading?: boolean
}

export interface CartListProps {
  items: CartItem[]
  onUpdateItem: (request: UpdateCartItemRequest) => void
  onRemoveItem: (itemId: string) => void
  onSaveForLater?: (itemId: string) => void
  isLoading?: boolean
  error?: string | null
}

export interface CartSummaryProps {
  summary: CartSummary
  onCheckout: () => void
  onApplyDiscount?: (code: string) => void
  appliedDiscounts?: AppliedDiscount[]
  isLoading?: boolean
}

// Cart form types
export interface CartFormData {
  items: CartItem[]
  shippingAddress: ShippingAddress
  billingAddress: ShippingAddress
  shippingMethod: string
  paymentMethod: string
  discountCode?: string
  notes?: string
}

// Cart validation codes
export enum CartValidationCode {
  OUT_OF_STOCK = 'OUT_OF_STOCK',
  INSUFFICIENT_STOCK = 'INSUFFICIENT_STOCK',
  PRICE_CHANGED = 'PRICE_CHANGED',
  PRODUCT_UNAVAILABLE = 'PRODUCT_UNAVAILABLE',
  INVALID_OPTIONS = 'INVALID_OPTIONS',
  EXPIRED_DISCOUNT = 'EXPIRED_DISCOUNT',
  INVALID_DISCOUNT = 'INVALID_DISCOUNT',
  MIN_ORDER_NOT_MET = 'MIN_ORDER_NOT_MET',
  MAX_QUANTITY_EXCEEDED = 'MAX_QUANTITY_EXCEEDED'
}
