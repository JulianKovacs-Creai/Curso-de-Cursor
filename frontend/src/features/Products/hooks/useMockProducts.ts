import { useState, useEffect, useCallback } from 'react'
import { Product } from '../types'
import { productUtils } from '../utils/productUtils'

// Mock data - in real app this would come from API
const mockProductsData = [
  {
    id: 1,
    name: 'Laptop HP Pavilion',
    price: 899.99,
    category: 'Electronics',
    description: 'High performance laptop perfect for work and entertainment'
  },
  {
    id: 2,
    name: 'iPhone 15 Pro',
    price: 999.99,
    category: 'Electronics', 
    description: 'Latest iPhone model with advanced camera system'
  },
  {
    id: 3,
    name: 'Coffee Maker Deluxe',
    price: 159.99,
    category: 'Home',
    description: 'Premium coffee maker for the perfect morning brew'
  },
  {
    id: 4,
    name: 'Running Shoes Pro',
    price: 129.99,
    category: 'Sports',
    description: 'Comfortable running shoes for professional athletes'
  },
  {
    id: 5,
    name: 'Wireless Headphones',
    price: 79.99,
    category: 'Electronics',
    description: 'Premium sound quality with noise cancellation'
  },
  {
    id: 6,
    name: 'Smart Watch',
    price: 249.99,
    category: 'Electronics',
    description: 'Track your fitness and stay connected'
  }
]

export const useMockProducts = () => {
  const [products, setProducts] = useState<Product[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchMockProducts = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Simulate API delay
      await new Promise(resolve => setTimeout(resolve, 500))
      
      const convertedProducts = mockProductsData.map(productUtils.convertMockToProduct)
      setProducts(convertedProducts)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error loading products')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchMockProducts()
  }, [fetchMockProducts])

  const handleAddToCart = useCallback((product: Product) => {
    console.log('Add to cart:', product.id)
    // TODO: Implement cart functionality
  }, [])

  const handleAddToWishlist = useCallback((product: Product) => {
    console.log('Add to wishlist:', product.id)
    // TODO: Implement wishlist functionality
  }, [])

  return {
    products,
    loading,
    error,
    refetch: fetchMockProducts,
    handleAddToCart,
    handleAddToWishlist
  }
}
