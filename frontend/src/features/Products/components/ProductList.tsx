import React from 'react'
import { Row, Col, Spin, Alert, Empty } from 'antd'
import ProductCard from './ProductCard'
import { Product } from '../types'

interface ProductListProps {
  products: Product[]
  loading?: boolean
  error?: string | null
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  className?: string
}

const ProductList: React.FC<ProductListProps> = ({
  products,
  loading = false,
  error,
  onAddToCart,
  onAddToWishlist,
  className
}) => {
  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
      </div>
    )
  }

  if (error) {
    return (
      <Alert
        message="Error"
        description={error}
        type="error"
        showIcon
        style={{ margin: '20px 0' }}
      />
    )
  }

  if (products.length === 0) {
    return (
      <Empty
        description="No se encontraron productos"
        style={{ margin: '50px 0' }}
      />
    )
  }

  return (
    <div className={className}>
      <Row gutter={[24, 24]}>
        {products.map((product) => (
          <Col key={product.id} xs={24} sm={12} md={8} lg={6}>
            <ProductCard
              product={product}
              onAddToCart={onAddToCart}
              onAddToWishlist={onAddToWishlist}
              loading={loading}
            />
          </Col>
        ))}
      </Row>
    </div>
  )
}

export default ProductList