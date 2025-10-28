import { useQuery, useInfiniteQuery } from '@tanstack/react-query'
import { productService } from '../services/productService'
import { ProductFilters } from '../types'

// Query keys for consistent caching
export const productKeys = {
  all: ['products'] as const,
  lists: () => [...productKeys.all, 'list'] as const,
  list: (filters: ProductFilters) => [...productKeys.lists(), filters] as const,
  details: () => [...productKeys.all, 'detail'] as const,
  detail: (id: string) => [...productKeys.details(), id] as const,
  categories: () => [...productKeys.all, 'categories'] as const,
  brands: () => [...productKeys.all, 'brands'] as const,
  reviews: (productId: string) => [...productKeys.detail(productId), 'reviews'] as const,
  search: (query: string, filters?: ProductFilters) => [...productKeys.all, 'search', query, filters] as const,
  featured: () => [...productKeys.all, 'featured'] as const,
  related: (productId: string) => [...productKeys.detail(productId), 'related'] as const,
  analytics: (productId: string) => [...productKeys.detail(productId), 'analytics'] as const,
}

// Hook for fetching products with filters
export const useProducts = (filters: ProductFilters = {}) => {
  return useQuery({
    queryKey: productKeys.list(filters),
    queryFn: () => productService.getProducts(filters),
    staleTime: 5 * 60 * 1000, // 5 minutes
    enabled: true,
  })
}

// Hook for infinite scroll products
export const useInfiniteProducts = (filters: ProductFilters = {}) => {
  return useInfiniteQuery({
    queryKey: productKeys.list(filters),
    queryFn: ({ pageParam = 1 }) => 
      productService.getProducts({ ...filters, page: pageParam }),
    getNextPageParam: (lastPage) => {
      const { pagination } = lastPage
      return pagination.page < pagination.totalPages 
        ? pagination.page + 1 
        : undefined
    },
    initialPageParam: 1,
    staleTime: 5 * 60 * 1000,
  })
}

// Hook for single product
export const useProduct = (id: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: productKeys.detail(id),
    queryFn: () => productService.getProduct(id),
    enabled: enabled && !!id,
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}

// Hook for product categories
export const useProductCategories = () => {
  return useQuery({
    queryKey: productKeys.categories(),
    queryFn: productService.getCategories,
    staleTime: 30 * 60 * 1000, // 30 minutes
  })
}

// Hook for product brands
export const useProductBrands = () => {
  return useQuery({
    queryKey: productKeys.brands(),
    queryFn: productService.getBrands,
    staleTime: 30 * 60 * 1000, // 30 minutes
  })
}

// Hook for product reviews
export const useProductReviews = (productId: string, page: number = 1, limit: number = 10) => {
  return useQuery({
    queryKey: productKeys.reviews(productId),
    queryFn: () => productService.getProductReviews(productId, page, limit),
    enabled: !!productId,
    staleTime: 5 * 60 * 1000,
  })
}

// Hook for product search
export const useProductSearch = (query: string, filters?: ProductFilters, enabled: boolean = true) => {
  return useQuery({
    queryKey: productKeys.search(query, filters),
    queryFn: () => productService.searchProducts(query, filters),
    enabled: enabled && !!query.trim(),
    staleTime: 2 * 60 * 1000, // 2 minutes
  })
}

// Hook for featured products
export const useFeaturedProducts = (limit: number = 8) => {
  return useQuery({
    queryKey: [...productKeys.featured(), limit],
    queryFn: () => productService.getFeaturedProducts(limit),
    staleTime: 10 * 60 * 1000, // 10 minutes
  })
}

// Hook for related products
export const useRelatedProducts = (productId: string, limit: number = 4) => {
  return useQuery({
    queryKey: [...productKeys.related(productId), limit],
    queryFn: () => productService.getRelatedProducts(productId, limit),
    enabled: !!productId,
    staleTime: 15 * 60 * 1000, // 15 minutes
  })
}

// Hook for product analytics
export const useProductAnalytics = (productId: string, enabled: boolean = true) => {
  return useQuery({
    queryKey: productKeys.analytics(productId),
    queryFn: () => productService.getProductAnalytics(productId),
    enabled: enabled && !!productId,
    staleTime: 5 * 60 * 1000,
  })
}