import { Product, ProductFilters } from '../types'

export const productUtils = {
  // Format price with currency
  formatPrice: (price: number, currency: string = 'USD'): string => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(price)
  },

  // Calculate discount percentage
  calculateDiscount: (originalPrice: number, salePrice: number): number => {
    if (originalPrice <= 0) return 0
    return Math.round(((originalPrice - salePrice) / originalPrice) * 100)
  },

  // Check if product is on sale
  isOnSale: (product: Product, salePrice?: number): boolean => {
    return salePrice !== undefined && salePrice < product.price
  },

  // Get product availability status
  getAvailabilityStatus: (stock: number): { status: string; color: string } => {
    if (stock === 0) return { status: 'Sin stock', color: 'red' }
    if (stock < 10) return { status: 'Pocas unidades', color: 'orange' }
    return { status: 'Disponible', color: 'green' }
  },

  // Filter products by search term
  filterBySearch: (products: Product[], searchTerm: string): Product[] => {
    if (!searchTerm.trim()) return products
    
    const term = searchTerm.toLowerCase()
    return products.filter(product => 
      product.name.toLowerCase().includes(term) ||
      product.description.toLowerCase().includes(term) ||
      product.category.toLowerCase().includes(term)
    )
  },

  // Sort products
  sortProducts: (products: Product[], field: keyof Product, order: 'asc' | 'desc'): Product[] => {
    return [...products].sort((a, b) => {
      const aValue = a[field]
      const bValue = b[field]
      
      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return order === 'asc' 
          ? aValue.localeCompare(bValue)
          : bValue.localeCompare(aValue)
      }
      
      if (typeof aValue === 'number' && typeof bValue === 'number') {
        return order === 'asc' ? aValue - bValue : bValue - aValue
      }
      
      return 0
    })
  },

  // Apply filters to products
  applyFilters: (products: Product[], filters: ProductFilters): Product[] => {
    let filtered = [...products]

    if (filters.category) {
      filtered = filtered.filter(p => p.category === filters.category)
    }

    if (filters.minPrice !== undefined) {
      filtered = filtered.filter(p => p.price >= filters.minPrice!)
    }

    if (filters.maxPrice !== undefined) {
      filtered = filtered.filter(p => p.price <= filters.maxPrice!)
    }

    if (filters.rating !== undefined) {
      filtered = filtered.filter(p => p.rating >= filters.rating!)
    }

    if (filters.inStock) {
      filtered = filtered.filter(p => p.stock > 0)
    }

    if (filters.search) {
      filtered = this.filterBySearch(filtered, filters.search)
    }

    return filtered
  },

  // Generate product slug
  generateSlug: (name: string): string => {
    return name
      .toLowerCase()
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .trim()
  },

  // Validate product data
  validateProduct: (product: Partial<Product>): string[] => {
    const errors: string[] = []

    if (!product.name || product.name.trim().length === 0) {
      errors.push('El nombre del producto es requerido')
    }

    if (!product.description || product.description.trim().length === 0) {
      errors.push('La descripción del producto es requerida')
    }

    if (product.price === undefined || product.price <= 0) {
      errors.push('El precio debe ser mayor a 0')
    }

    if (product.stock === undefined || product.stock < 0) {
      errors.push('El stock no puede ser negativo')
    }

    if (product.rating !== undefined && (product.rating < 0 || product.rating > 5)) {
      errors.push('La calificación debe estar entre 0 y 5')
    }

    return errors
  },

  // Convert mock product to Product type
  convertMockToProduct: (mockProduct: any): Product => {
    return {
      id: mockProduct.id.toString(),
      name: mockProduct.name,
      description: mockProduct.description,
      price: mockProduct.price,
      image: mockProduct.image,
      category: mockProduct.category,
      stock: 10, // Default stock for mock data
      rating: 4.5, // Default rating for mock data
      reviews: Math.floor(Math.random() * 100), // Random reviews for mock data
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  }
}