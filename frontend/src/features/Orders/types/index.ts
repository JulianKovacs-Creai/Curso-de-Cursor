// ============================================================================
// ORDERS FEATURE TYPES - Order management related types
// ============================================================================

import { BaseEntity, User, PaginationParams } from '@/shared/types'
import { CartItem, ShippingAddress, AppliedDiscount, CartProductOption } from '@/features/Cart/types'
import { Product } from '@/features/Products/types'

// Order types
export interface Order extends BaseEntity {
  orderNumber: string
  userId: string
  user: User
  status: OrderStatus   
  paymentStatus: PaymentStatus
  items: OrderItem[]
  shippingAddress: OrderAddress
  billingAddress: OrderAddress
  paymentMethod: PaymentMethod
  shippingMethod: ShippingMethod
  subtotal: number
  tax: number
  shipping: number
  discount: number
  total: number
  currency: string
  notes?: string
  trackingNumber?: string
  estimatedDelivery?: string
  deliveredAt?: string
  cancelledAt?: string
  refundedAt?: string
  refundAmount?: number
}

export interface OrderItem extends BaseEntity {
  orderId: string
  productId: string
  productSnapshot: ProductSnapshot
  quantity: number
  unitPrice: number
  totalPrice: number
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


export interface OrderAddress {
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

// Order status and payment
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

// Shipping types
export interface ShippingMethod {
  id: string
  name: string
  description: string
  cost: number
  estimatedDays: number
  freeThreshold?: number
  availableRegions: string[]
  trackingUrl?: string
}

export interface ShippingInfo {
  method: ShippingMethod
  trackingNumber?: string
  carrier?: string
  estimatedDelivery?: string
  actualDelivery?: string
  status: ShippingStatus
}

export enum ShippingStatus {
  PENDING = 'pending',
  PROCESSING = 'processing',
  IN_TRANSIT = 'in_transit',
  OUT_FOR_DELIVERY = 'out_for_delivery',
  DELIVERED = 'delivered',
  FAILED = 'failed',
  RETURNED = 'returned'
}

// Order creation
export interface CreateOrderRequest {
  userId: string
  items: CreateOrderItem[]
  shippingAddress: OrderAddress
  billingAddress: OrderAddress
  paymentMethod: PaymentMethod
  shippingMethod: string
  discountCode?: string
  notes?: string
}

export interface CreateOrderItem {
  productId: string
  quantity: number
  selectedOptions?: CartProductOption[]
  notes?: string
}

export interface CreateOrderResponse {
  order: Order
  paymentIntent?: PaymentIntent
  confirmationUrl?: string
}

// Payment types
export interface PaymentIntent {
  id: string
  amount: number
  currency: string
  status: PaymentStatus
  clientSecret?: string
  paymentMethod?: string
  confirmationUrl?: string
}

export interface PaymentResult {
  success: boolean
  transactionId?: string
  error?: string
  requiresAction?: boolean
  actionUrl?: string
}

// Order updates
export interface UpdateOrderStatusRequest {
  orderId: string
  status: OrderStatus
  notes?: string
}

export interface UpdateShippingRequest {
  orderId: string
  trackingNumber: string
  carrier: string
  estimatedDelivery?: string
}

export interface CancelOrderRequest {
  orderId: string
  reason: string
  refundAmount?: number
}

export interface RefundOrderRequest {
  orderId: string
  amount: number
  reason: string
  refundItems?: string[]
}

// Order queries and filters
export interface OrderFilters extends PaginationParams {
  userId?: string
  status?: OrderStatus
  paymentStatus?: PaymentStatus
  dateFrom?: string
  dateTo?: string
  orderNumber?: string
  search?: string
}

export interface OrderListResponse {
  orders: Order[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

// Order hooks types
export interface UseOrdersReturn {
  orders: Order[]
  loading: boolean
  error: string | null
  fetchOrders: (filters?: OrderFilters) => Promise<void>
  createOrder: (request: CreateOrderRequest) => Promise<CreateOrderResponse>
  updateOrderStatus: (request: UpdateOrderStatusRequest) => Promise<void>
  cancelOrder: (request: CancelOrderRequest) => Promise<void>
  refundOrder: (request: RefundOrderRequest) => Promise<void>
}

export interface UseOrderReturn {
  order: Order | null
  loading: boolean
  error: string | null
  fetchOrder: (orderId: string) => Promise<void>
  updateShipping: (request: UpdateShippingRequest) => Promise<void>
  trackOrder: () => Promise<ShippingInfo>
}

// Order service types
export interface OrderService {
  getOrders(filters: OrderFilters): Promise<OrderListResponse>
  getOrder(orderId: string): Promise<Order>
  createOrder(request: CreateOrderRequest): Promise<CreateOrderResponse>
  updateOrderStatus(request: UpdateOrderStatusRequest): Promise<void>
  updateShipping(request: UpdateShippingRequest): Promise<void>
  cancelOrder(request: CancelOrderRequest): Promise<void>
  refundOrder(request: RefundOrderRequest): Promise<void>
  getOrderHistory(orderId: string): Promise<OrderHistoryItem[]>
  getOrderTracking(orderId: string): Promise<ShippingInfo>
}

// Order history and tracking
export interface OrderHistoryItem {
  id: string
  orderId: string
  status: OrderStatus
  timestamp: string
  notes?: string
  updatedBy: string
}

export interface OrderTracking {
  orderId: string
  status: OrderStatus
  shippingInfo: ShippingInfo
  history: OrderHistoryItem[]
  estimatedDelivery?: string
  actualDelivery?: string
}

// Order components props
export interface OrderCardProps {
  order: Order
  onViewDetails: (orderId: string) => void
  onTrackOrder?: (orderId: string) => void
  onCancelOrder?: (orderId: string) => void
  onReorder?: (orderId: string) => void
  showActions?: boolean
}

export interface OrderListProps {
  orders: Order[]
  loading?: boolean
  error?: string | null
  onViewDetails: (orderId: string) => void
  onTrackOrder?: (orderId: string) => void
  onCancelOrder?: (orderId: string) => void
  onReorder?: (orderId: string) => void
  showActions?: boolean
}

export interface OrderDetailsProps {
  order: Order
  onUpdateStatus?: (request: UpdateOrderStatusRequest) => void
  onUpdateShipping?: (request: UpdateShippingRequest) => void
  onCancelOrder?: (request: CancelOrderRequest) => void
  onRefundOrder?: (request: RefundOrderRequest) => void
  isAdmin?: boolean
}

// Order analytics
export interface OrderAnalytics {
  totalOrders: number
  totalRevenue: number
  averageOrderValue: number
  conversionRate: number
  orderStatusDistribution: Record<OrderStatus, number>
  paymentMethodDistribution: Record<PaymentMethod, number>
  monthlyTrends: OrderTrend[]
}

export interface OrderTrend {
  month: string
  orders: number
  revenue: number
  averageOrderValue: number
}

// Order notifications
export interface OrderNotification {
  orderId: string
  type: OrderNotificationType
  message: string
  timestamp: string
  read: boolean
}

export enum OrderNotificationType {
  ORDER_CONFIRMED = 'order_confirmed',
  ORDER_SHIPPED = 'order_shipped',
  ORDER_DELIVERED = 'order_delivered',
  ORDER_CANCELLED = 'order_cancelled',
  PAYMENT_FAILED = 'payment_failed',
  PAYMENT_REFUNDED = 'payment_refunded'
}

// Order utilities
export interface OrderUtils {
  generateOrderNumber(): string
  calculateOrderTotal(items: OrderItem[], shipping: number, tax: number, discount: number): number
  formatOrderStatus(status: OrderStatus): string
  getOrderStatusColor(status: OrderStatus): string
  canCancelOrder(order: Order): boolean
  canRefundOrder(order: Order): boolean
  getEstimatedDeliveryDate(order: Order): string
}

// Order validation
export interface OrderValidationResult {
  isValid: boolean
  errors: OrderValidationError[]
  warnings: OrderValidationWarning[]
}

export interface OrderValidationError {
  field: string
  message: string
  code: string
}

export interface OrderValidationWarning {
  field: string
  message: string
  code: string
}

export enum OrderValidationCode {
  INSUFFICIENT_STOCK = 'INSUFFICIENT_STOCK',
  INVALID_ADDRESS = 'INVALID_ADDRESS',
  PAYMENT_METHOD_INVALID = 'PAYMENT_METHOD_INVALID',
  SHIPPING_METHOD_UNAVAILABLE = 'SHIPPING_METHOD_UNAVAILABLE',
  DISCOUNT_CODE_INVALID = 'DISCOUNT_CODE_INVALID',
  MIN_ORDER_AMOUNT_NOT_MET = 'MIN_ORDER_AMOUNT_NOT_MET',
  MAX_ORDER_AMOUNT_EXCEEDED = 'MAX_ORDER_AMOUNT_EXCEEDED'
}
