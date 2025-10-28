// ============================================================================
// PRODUCTS FEATURE TYPES - Product management related types
// ============================================================================

import { BaseEntity, PaginationParams, SortOrder } from '@/shared/types'

// Product types
export interface Product extends BaseEntity {
  name: string
  description: string
  shortDescription?: string
  price: number
  compareAtPrice?: number
  costPrice?: number
  sku: string
  barcode?: string
  images: ProductImage[]
  category: ProductCategory
  brand?: ProductBrand
  tags: string[]
  attributes: ProductAttribute[]
  variants: ProductVariant[]
  inventory: ProductInventory
  seo: ProductSEO
  status: ProductStatus
  featured: boolean
  weight?: number
  dimensions?: ProductDimensions
  taxClass?: string
  shippingClass?: string
}

export interface ProductImage {
  id: string
  url: string
  alt: string
  order: number
  isPrimary: boolean
  thumbnail?: string
}

export interface ProductCategory extends BaseEntity {
  name: string
  slug: string
  description?: string
  image?: string
  parentId?: string
  level: number
  path: string
  isActive: boolean
  sortOrder: number
}

export interface ProductBrand extends BaseEntity {
  name: string
  slug: string
  description?: string
  logo?: string
  website?: string
  isActive: boolean
}

export interface ProductAttribute {
  id: string
  name: string
  type: AttributeType
  values: AttributeValue[]
  isRequired: boolean
  isFilterable: boolean
  sortOrder: number
}

export interface AttributeValue {
  id: string
  value: string
  displayValue: string
  color?: string
  image?: string
  sortOrder: number
}

export interface ProductVariant {
  id: string
  sku: string
  price: number
  compareAtPrice?: number
  costPrice?: number
  weight?: number
  dimensions?: ProductDimensions
  attributes: VariantAttribute[]
  inventory: ProductInventory
  images: ProductImage[]
  isActive: boolean
}

export interface VariantAttribute {
  attributeId: string
  attributeName: string
  valueId: string
  value: string
}

export interface ProductInventory {
  trackQuantity: boolean
  quantity: number
  allowBackorder: boolean
  lowStockThreshold: number
  sku: string
  barcode?: string
  weight?: number
  dimensions?: ProductDimensions
}

export interface ProductSEO {
  title?: string
  description?: string
  keywords?: string[]
  canonicalUrl?: string
  robots?: string
}

export interface ProductDimensions {
  length: number
  width: number
  height: number
  unit: 'cm' | 'in' | 'm'
}

// Enums
export enum ProductStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  INACTIVE = 'inactive',
  ARCHIVED = 'archived'
}

export enum AttributeType {
  TEXT = 'text',
  NUMBER = 'number',
  SELECT = 'select',
  MULTI_SELECT = 'multi_select',
  COLOR = 'color',
  IMAGE = 'image',
  BOOLEAN = 'boolean'
}

// Product filters and search
export interface ProductFilters extends PaginationParams {
  category?: string
  brand?: string
  minPrice?: number
  maxPrice?: number
  rating?: number
  inStock?: boolean
  featured?: boolean
  search?: string
  tags?: string[]
  attributes?: Record<string, string[]>
  sortBy?: ProductSortField
  sortOrder?: SortOrder
}

export interface ProductSortField {
  field: 'name' | 'price' | 'rating' | 'createdAt' | 'popularity' | 'relevance'
  order: SortOrder
}

export interface ProductListResponse {
  products: Product[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
  filters: ProductFilters
  facets: ProductFacets
}

export interface ProductFacets {
  categories: CategoryFacet[]
  brands: BrandFacet[]
  priceRanges: PriceRangeFacet[]
  attributes: AttributeFacet[]
}

export interface CategoryFacet {
  category: ProductCategory
  count: number
}

export interface BrandFacet {
  brand: ProductBrand
  count: number
}

export interface PriceRangeFacet {
  min: number
  max: number
  count: number
}

export interface AttributeFacet {
  attribute: ProductAttribute
  values: AttributeValueFacet[]
}

export interface AttributeValueFacet {
  value: AttributeValue
  count: number
}

// Product reviews and ratings
export interface ProductReview extends BaseEntity {
  productId: string
  userId: string
  userName: string
  userAvatar?: string
  rating: number
  title?: string
  comment: string
  images?: string[]
  helpful: number
  verified: boolean
  response?: ReviewResponse
}

export interface ReviewResponse {
  id: string
  comment: string
  respondedBy: string
  respondedAt: string
}

export interface ProductRating {
  average: number
  count: number
  distribution: {
    1: number
    2: number
    3: number
    4: number
    5: number
  }
}

// Product comparison
export interface ProductComparison {
  products: Product[]
  attributes: ComparisonAttribute[]
}

export interface ComparisonAttribute {
  name: string
  values: Record<string, string>
}

// Product wishlist
export interface ProductWishlist {
  id: string
  userId: string
  productId: string
  product: Product
  addedAt: string
}

// Product search
export interface ProductSearchResult {
  product: Product
  relevanceScore: number
  matchedFields: string[]
  highlights: SearchHighlight[]
}

export interface SearchHighlight {
  field: string
  value: string
  matched: boolean
}

// Product analytics
export interface ProductAnalytics {
  productId: string
  views: number
  clicks: number
  conversions: number
  revenue: number
  averageRating: number
  reviewCount: number
  popularityScore: number
  trends: ProductTrend[]
}

export interface ProductTrend {
  date: string
  views: number
  sales: number
  revenue: number
}

// Product components props
export interface ProductCardProps {
  product: Product
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  onViewDetails?: (product: Product) => void
  loading?: boolean
  showActions?: boolean
  variant?: 'default' | 'compact' | 'detailed'
}

export interface ProductListProps {
  products: Product[]
  loading?: boolean
  error?: string | null
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  onViewDetails?: (product: Product) => void
  className?: string
  showFilters?: boolean
  showSort?: boolean
}

export interface ProductDetailsProps {
  product: Product
  onAddToCart?: (product: Product, variant?: ProductVariant) => void
  onAddToWishlist?: (product: Product) => void
  onWriteReview?: (product: Product) => void
  reviews?: ProductReview[]
  rating?: ProductRating
  relatedProducts?: Product[]
}

// Product forms
export interface ProductFormData {
  name: string
  description: string
  shortDescription?: string
  price: number
  compareAtPrice?: number
  sku: string
  categoryId: string
  brandId?: string
  tags: string[]
  status: ProductStatus
  featured: boolean
  weight?: number
  dimensions?: ProductDimensions
  seo: ProductSEO
}

// Product service types
export interface ProductService {
  getProducts(filters: ProductFilters): Promise<ProductListResponse>
  getProduct(id: string): Promise<Product>
  createProduct(data: ProductFormData): Promise<Product>
  updateProduct(id: string, data: Partial<ProductFormData>): Promise<Product>
  deleteProduct(id: string): Promise<void>
  getCategories(): Promise<ProductCategory[]>
  getBrands(): Promise<ProductBrand[]>
  searchProducts(query: string, filters?: ProductFilters): Promise<ProductSearchResult[]>
  getRelatedProducts(productId: string, limit?: number): Promise<Product[]>
  getProductReviews(productId: string): Promise<ProductReview[]>
  addProductReview(productId: string, review: Omit<ProductReview, 'id' | 'productId' | 'createdAt' | 'updatedAt'>): Promise<ProductReview>
}

// Mock data types for legacy compatibility
export interface MockProduct {
  id: number
  name: string
  price: number
  category: string
  description: string
  image: string
}

// Homepage specific types
export interface HomePageProps {
  className?: string
}

export interface HeroSectionProps {
  title: string
  subtitle: string
  description: string
  className?: string
}

export interface FeaturedProductsProps {
  products: Product[]
  loading?: boolean
  error?: string | null
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  className?: string
}

export interface ProjectTimelineProps {
  className?: string
}

export interface TimelineItem {
  id: string
  title: string
  status: 'completed' | 'current' | 'upcoming'
  description?: string
}