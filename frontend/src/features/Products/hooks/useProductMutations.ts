import { useMutation, useQueryClient } from '@tanstack/react-query'
import { productService } from '../services/productService'
import { productKeys } from './useProducts'
import { ProductFormData, ProductReview } from '../types'

// Hook for creating a product
export const useCreateProduct = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ProductFormData) => productService.createProduct(data),
    onSuccess: (newProduct) => {
      // Invalidate and refetch products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
      // Add the new product to cache
      queryClient.setQueryData(productKeys.detail(newProduct.id), newProduct)
    },
    onError: (error) => {
      console.error('Error creating product:', error)
    },
  })
}

// Hook for updating a product
export const useUpdateProduct = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<ProductFormData> }) =>
      productService.updateProduct(id, data),
    onSuccess: (updatedProduct) => {
      // Update the product in cache
      queryClient.setQueryData(productKeys.detail(updatedProduct.id), updatedProduct)
      // Invalidate products list to reflect changes
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
    },
    onError: (error) => {
      console.error('Error updating product:', error)
    },
  })
}

// Hook for deleting a product
export const useDeleteProduct = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (id: string) => productService.deleteProduct(id),
    onSuccess: (_, deletedId) => {
      // Remove product from cache
      queryClient.removeQueries({ queryKey: productKeys.detail(deletedId) })
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
    },
    onError: (error) => {
      console.error('Error deleting product:', error)
    },
  })
}

// Hook for adding a product review
export const useAddProductReview = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ 
      productId, 
      review 
    }: { 
      productId: string
      review: Omit<ProductReview, 'id' | 'productId' | 'createdAt' | 'updatedAt'>
    }) => productService.addProductReview(productId, review),
    onSuccess: (newReview, { productId }) => {
      // Invalidate product reviews
      queryClient.invalidateQueries({ queryKey: productKeys.reviews(productId) })
      // Invalidate product details to update rating
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
    onError: (error) => {
      console.error('Error adding product review:', error)
    },
  })
}

// Hook for updating a product review
export const useUpdateProductReview = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ 
      productId, 
      reviewId, 
      review 
    }: { 
      productId: string
      reviewId: string
      review: Partial<Omit<ProductReview, 'id' | 'productId' | 'createdAt' | 'updatedAt'>>
    }) => productService.updateProductReview(productId, reviewId, review),
    onSuccess: (updatedReview, { productId }) => {
      // Invalidate product reviews
      queryClient.invalidateQueries({ queryKey: productKeys.reviews(productId) })
      // Invalidate product details to update rating
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
    onError: (error) => {
      console.error('Error updating product review:', error)
    },
  })
}

// Hook for deleting a product review
export const useDeleteProductReview = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ productId, reviewId }: { productId: string; reviewId: string }) =>
      productService.deleteProductReview(productId, reviewId),
    onSuccess: (_, { productId }) => {
      // Invalidate product reviews
      queryClient.invalidateQueries({ queryKey: productKeys.reviews(productId) })
      // Invalidate product details to update rating
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
    onError: (error) => {
      console.error('Error deleting product review:', error)
    },
  })
}

// Hook for uploading product images
export const useUploadProductImages = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ productId, files }: { productId: string; files: File[] }) =>
      productService.uploadProductImages(productId, files),
    onSuccess: (_, { productId }) => {
      // Invalidate product details to show new images
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
    onError: (error) => {
      console.error('Error uploading product images:', error)
    },
  })
}

// Hook for deleting a product image
export const useDeleteProductImage = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ productId, imageId }: { productId: string; imageId: string }) =>
      productService.deleteProductImage(productId, imageId),
    onSuccess: (_, { productId }) => {
      // Invalidate product details to remove image
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
    },
    onError: (error) => {
      console.error('Error deleting product image:', error)
    },
  })
}

// Hook for updating product inventory
export const useUpdateProductInventory = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ 
      productId, 
      inventory 
    }: { 
      productId: string
      inventory: {
        quantity: number
        trackQuantity: boolean
        allowBackorder: boolean
        lowStockThreshold: number
      }
    }) => productService.updateProductInventory(productId, inventory),
    onSuccess: (updatedProduct) => {
      // Update product in cache
      queryClient.setQueryData(productKeys.detail(updatedProduct.id), updatedProduct)
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
    },
    onError: (error) => {
      console.error('Error updating product inventory:', error)
    },
  })
}

// Hook for bulk updating products
export const useBulkUpdateProducts = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (updates: Array<{ id: string; data: Partial<ProductFormData> }>) =>
      productService.bulkUpdateProducts(updates),
    onSuccess: (updatedProducts) => {
      // Update each product in cache
      updatedProducts.forEach(product => {
        queryClient.setQueryData(productKeys.detail(product.id), product)
      })
      // Invalidate products list
      queryClient.invalidateQueries({ queryKey: productKeys.lists() })
    },
    onError: (error) => {
      console.error('Error bulk updating products:', error)
    },
  })
}

// Hook for creating a product variant
export const useCreateProductVariant = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ 
      productId, 
      variant 
    }: { 
      productId: string
      variant: {
        name: string
        sku: string
        price: number
        attributes: Record<string, string>
      }
    }) => productService.createProductVariant(productId, variant),
    onSuccess: (newVariant, { productId }) => {
      // Invalidate product details to show new variant
      queryClient.invalidateQueries({ queryKey: productKeys.detail(productId) })
      // Invalidate product variants
      queryClient.invalidateQueries({ queryKey: [...productKeys.detail(productId), 'variants'] })
    },
    onError: (error) => {
      console.error('Error creating product variant:', error)
    },
  })
}
