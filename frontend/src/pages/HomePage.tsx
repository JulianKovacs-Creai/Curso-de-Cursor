import React from 'react'
import { Typography } from 'antd'
import { 
  HeroSection, 
  ProductList, 
  useMockProducts,
  type HomePageProps 
} from '@features/Products'

const { Title } = Typography

const HomePage: React.FC<HomePageProps> = ({ className }) => {
  const {
    products,
    loading,
    error,
    handleAddToCart,
    handleAddToWishlist
  } = useMockProducts()

  return (
    <div className={className}>
      <HeroSection
        title="Welcome to E-commerce Evolution"
        subtitle="This is the base project that will evolve into a full-featured e-commerce platform"
        description="🚀 Day 2: We'll connect these products with the real API"
      />

      <Title level={2} style={{ marginBottom: '24px' }}>
        Featured Products
      </Title>
      
      <ProductList
        products={products}
        loading={loading}
        error={error}
        onAddToCart={handleAddToCart}
        onAddToWishlist={handleAddToWishlist}
      />
    </div>
  )
}

export default HomePage