// Export all components
export { default as ProductCard } from './components/ProductCard'
export { default as ProductList } from './components/ProductList'
export { default as ProductGrid } from './components/ProductGrid'
export { default as ProductFiltersComponent } from './components/ProductFilters'
export { default as ProductSearch } from './components/ProductSearch'
export { default as ProductsPage } from './components/ProductsPage'
export { default as HeroSection } from './components/HeroSection'
export { default as ProjectTimeline } from './components/ProjectTimeline'

// Export all hooks
export { 
  useProducts, 
  useInfiniteProducts,
  useProduct, 
  useProductCategories,
  useProductBrands,
  useProductReviews,
  useProductSearch,
  useFeaturedProducts,
  useRelatedProducts,
  useProductAnalytics,
  productKeys
} from './hooks/useProducts'

export { 
  useCreateProduct,
  useUpdateProduct,
  useDeleteProduct,
  useAddProductReview,
  useUpdateProductReview,
  useDeleteProductReview,
  useUploadProductImages,
  useDeleteProductImage,
  useUpdateProductInventory,
  useBulkUpdateProducts,
  useCreateProductVariant
} from './hooks/useProductMutations'

export { useMockProducts } from './hooks/useMockProducts'

// Export all services
export { productService } from './services/productService'

// Export all types
export type {
  Product,
  ProductCategory,
  ProductBrand,
  ProductFilters,
  ProductSortField,
  ProductListResponse,
  ProductReview,
  ProductSearchResult,
  ProductFormData,
  ProductAnalytics,
  ProductCardProps,
  ProductListProps,
  ProductDetailsProps,
  MockProduct,
  HomePageProps,
  HeroSectionProps,
  FeaturedProductsProps,
  ProjectTimelineProps,
  TimelineItem
} from './types'

// Export all utils
export { productUtils } from './utils/productUtils'