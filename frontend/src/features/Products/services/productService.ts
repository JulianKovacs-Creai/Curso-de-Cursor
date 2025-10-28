import { apiClient } from '@/shared/services/apiClient'
import { 
  Product, 
  ProductListResponse, 
  ProductFilters, 
  ProductCategory,
  ProductBrand,
  ProductReview,
  ProductSearchResult,
  ProductFormData,
  ProductAnalytics
} from '../types'

export const productService = {
  // Get all products with filters and pagination
  async getProducts(filters: ProductFilters = { page: 1, limit: 10 }): Promise<ProductListResponse> {
    const params = new URLSearchParams()
    
    // Pagination
    if (filters.page) params.append('page', filters.page.toString())
    if (filters.limit) params.append('limit', filters.limit.toString())
    
    // Filters
    if (filters.category) params.append('category', filters.category)
    if (filters.brand) params.append('brand', filters.brand)
    if (filters.minPrice) params.append('minPrice', filters.minPrice.toString())
    if (filters.maxPrice) params.append('maxPrice', filters.maxPrice.toString())
    if (filters.rating) params.append('rating', filters.rating.toString())
    if (filters.inStock !== undefined) params.append('inStock', filters.inStock.toString())
    if (filters.featured !== undefined) params.append('featured', filters.featured.toString())
    if (filters.search) params.append('search', filters.search)
    if (filters.tags?.length) params.append('tags', filters.tags.join(','))
    
    // Sorting
    if (filters.sortBy?.field) params.append('sortBy', filters.sortBy.field)
    if (filters.sortBy?.order) params.append('sortOrder', filters.sortBy.order)
    
    // Attributes
    if (filters.attributes) {
      Object.entries(filters.attributes).forEach(([key, values]) => {
        if (values.length) {
          params.append(`attributes[${key}]`, values.join(','))
        }
      })
    }

    const response = await apiClient.get<{ data: ProductListResponse }>(`/api/v1/products/?${params.toString()}`)
    return response.data
  },

  // Get single product by ID
  async getProduct(id: string): Promise<Product> {
    const response = await apiClient.get<{ data: Product }>(`/api/v1/products/${id}`)
    return response.data
  },

  // Create new product
  async createProduct(data: ProductFormData): Promise<Product> {
    const response = await apiClient.post<{ data: Product }>('/api/v1/products/', data)
    return response.data
  },

  // Update product
  async updateProduct(id: string, data: Partial<ProductFormData>): Promise<Product> {
    const response = await apiClient.put<{ data: Product }>(`/api/v1/products/${id}`, data)
    return response.data
  },

  // Delete product
  async deleteProduct(id: string): Promise<void> {
    await apiClient.delete(`/api/v1/products/${id}`)
  },

  // Get product categories
  async getCategories(): Promise<ProductCategory[]> {
    const response = await apiClient.get<{ data: ProductCategory[] }>('/api/v1/products/categories')
    return response.data
  },

  // Get product brands
  async getBrands(): Promise<ProductBrand[]> {
    const response = await apiClient.get<{ data: ProductBrand[] }>('/api/v1/products/brands')
    return response.data
  },

  // Get product reviews
  async getProductReviews(productId: string, page: number = 1, limit: number = 10): Promise<{
    reviews: ProductReview[]
    pagination: {
      page: number
      limit: number
      total: number
      totalPages: number
    }
  }> {
    const response = await apiClient.get<{ data: { reviews: ProductReview[]; pagination: { page: number; limit: number; total: number; totalPages: number } } }>(`/api/v1/products/${productId}/reviews?page=${page}&limit=${limit}`)
    return response.data
  },

  // Add product review
  async addProductReview(productId: string, review: Omit<ProductReview, 'id' | 'productId' | 'createdAt' | 'updatedAt'>): Promise<ProductReview> {
    const response = await apiClient.post<{ data: ProductReview }>(`/api/v1/products/${productId}/reviews`, review)
    return response.data
  },

  // Update product review
  async updateProductReview(productId: string, reviewId: string, review: Partial<Omit<ProductReview, 'id' | 'productId' | 'createdAt' | 'updatedAt'>>): Promise<ProductReview> {
    const response = await apiClient.put<{ data: ProductReview }>(`/api/v1/products/${productId}/reviews/${reviewId}`, review)
    return response.data
  },

  // Delete product review
  async deleteProductReview(productId: string, reviewId: string): Promise<void> {
    await apiClient.delete(`/api/v1/products/${productId}/reviews/${reviewId}`)
  },

  // Search products
  async searchProducts(query: string, filters?: ProductFilters): Promise<ProductSearchResult[]> {
    const params = new URLSearchParams()
    params.append('q', query)
    
    if (filters?.category) params.append('category', filters.category)
    if (filters?.brand) params.append('brand', filters.brand)
    if (filters?.minPrice) params.append('minPrice', filters.minPrice.toString())
    if (filters?.maxPrice) params.append('maxPrice', filters.maxPrice.toString())
    if (filters?.rating) params.append('rating', filters.rating.toString())
    if (filters?.inStock !== undefined) params.append('inStock', filters.inStock.toString())
    if (filters?.tags?.length) params.append('tags', filters.tags.join(','))

    const response = await apiClient.get<{ data: ProductSearchResult[] }>(`/api/v1/products/search?${params.toString()}`)
    return response.data
  },

  // Get related products
  async getRelatedProducts(productId: string, limit: number = 4): Promise<Product[]> {
    const response = await apiClient.get<{ data: Product[] }>(`/api/v1/products/${productId}/related?limit=${limit}`)
    return response.data
  },

  // Get featured products
  async getFeaturedProducts(limit: number = 8): Promise<Product[]> {
    const response = await apiClient.get<{ data: Product[] }>(`/api/v1/products/featured?limit=${limit}`)
    return response.data
  },

  // Get product analytics
  async getProductAnalytics(productId: string): Promise<ProductAnalytics> {
    const response = await apiClient.get<{ data: ProductAnalytics }>(`/api/v1/products/${productId}/analytics`)
    return response.data
  },

  // Upload product images
  async uploadProductImages(productId: string, files: File[]): Promise<{ images: string[] }> {
    const formData = new FormData()
    files.forEach(file => formData.append('images', file))
    
    const response = await apiClient.post<{ data: { images: string[] } }>(`/api/v1/products/${productId}/images`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Delete product image
  async deleteProductImage(productId: string, imageId: string): Promise<void> {
    await apiClient.delete(`/api/v1/products/${productId}/images/${imageId}`)
  },

  // Update product inventory
  async updateProductInventory(productId: string, inventory: {
    quantity: number
    trackQuantity: boolean
    allowBackorder: boolean
    lowStockThreshold: number
  }): Promise<Product> {
    const response = await apiClient.put<{ data: Product }>(`/api/v1/products/${productId}/inventory`, inventory)
    return response.data
  },

  // Bulk update products
  async bulkUpdateProducts(updates: Array<{
    id: string
    data: Partial<ProductFormData>
  }>): Promise<Product[]> {
    const response = await apiClient.put<{ data: Product[] }>('/api/v1/products/bulk', { updates })
    return response.data
  },

  // Get product variants
  async getProductVariants(productId: string): Promise<Product[]> {
    const response = await apiClient.get<{ data: Product[] }>(`/api/v1/products/${productId}/variants`)
    return response.data
  },

  // Create product variant
  async createProductVariant(productId: string, variant: {
    name: string
    sku: string
    price: number
    attributes: Record<string, string>
  }): Promise<Product> {
    const response = await apiClient.post<{ data: Product }>(`/api/v1/products/${productId}/variants`, variant)
    return response.data
  }
}
