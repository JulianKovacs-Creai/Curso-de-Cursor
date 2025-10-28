import { useState, useEffect } from 'react'
import { productService } from '../services/productService'
import { Product } from '../types'

export const useProduct = (id: string) => {
  const [product, setProduct] = useState<Product | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchProduct = async () => {
    if (!id) return
    
    try {
      setLoading(true)
      setError(null)
      const result = await productService.getProduct(id)
      setProduct(result)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Error fetching product')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchProduct()
  }, [id])

  return {
    product,
    loading,
    error,
    refetch: fetchProduct
  }
}
