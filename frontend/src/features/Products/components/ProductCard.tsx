import React, { memo, useCallback } from 'react'
import { Card, Rate, Button, Tag, Space } from 'antd'
import { ShoppingCartOutlined, HeartOutlined } from '@ant-design/icons'
import { Product } from '../types'
import { productUtils } from '../utils/productUtils'
import styles from './ProductCard.module.css'

interface ProductCardProps {
  product: Product
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  loading?: boolean
}

const ProductCard: React.FC<ProductCardProps> = ({ 
  product, 
  onAddToCart, 
  onAddToWishlist,
  loading = false
}) => {
  const handleAddToCart = useCallback(() => {
    onAddToCart?.(product)
  }, [onAddToCart, product])

  const handleAddToWishlist = useCallback(() => {
    onAddToWishlist?.(product)
  }, [onAddToWishlist, product])

  const availability = productUtils.getAvailabilityStatus(product.inventory?.quantity || 0)
  const isOutOfStock = (product.inventory?.quantity || 0) === 0

  return (
    <Card
      hoverable
      loading={loading}
      className={`${styles.card} ${isOutOfStock ? styles.outOfStock : ''}`}
      actions={[
        <Button 
          key="wishlist" 
          icon={<HeartOutlined />} 
          onClick={handleAddToWishlist}
          loading={loading}
          className={styles.wishlistButton}
          aria-label={`Agregar ${product.name} a favoritos`}
        >
          Wishlist
        </Button>,
        <Button 
          key="cart" 
          type="primary" 
          icon={<ShoppingCartOutlined />} 
          onClick={handleAddToCart}
          disabled={isOutOfStock}
          loading={loading}
          className={styles.cartButton}
          aria-label={`Agregar ${product.name} al carrito`}
        >
          {isOutOfStock ? 'Sin stock' : 'Agregar'}
        </Button>
      ]}
    >
      <Card.Meta
        title={
          <div className={styles.titleContainer}>
            <div>{product.name}</div>
            <Tag color="blue" className={styles.categoryTag}>
              {product.category?.name || 'Sin categoría'}
            </Tag>
          </div>
        }
        description={
          <Space direction="vertical" size="small" style={{ width: '100%' }}>
            <p className={styles.description}>
              {product.description}
            </p>
            <div className={styles.ratingContainer}>
              <Rate 
                disabled 
                value={4.5} 
                style={{ fontSize: 14 }} 
                allowHalf
              />
              <span className={styles.ratingCount}>(0)</span>
            </div>
            <div className={styles.priceContainer}>
              <div>
                <span className={styles.price}>
                  {productUtils.formatPrice(product.price)}
                </span>
                {product.compareAtPrice && product.compareAtPrice > product.price && (
                  <span className={styles.compareAtPrice}>
                    {productUtils.formatPrice(product.compareAtPrice)}
                  </span>
                )}
              </div>
              <Tag 
                color={availability.color} 
                className={styles.availabilityTag}
              >
                {availability.status}
              </Tag>
            </div>
          </Space>
        }
      />
    </Card>
  )
}

export default memo(ProductCard)