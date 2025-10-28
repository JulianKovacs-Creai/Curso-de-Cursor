import React, { useState, useCallback, useEffect } from 'react'
import { Layout, Drawer, Button, Space, Typography, notification } from 'antd'
import { FilterOutlined, SearchOutlined } from '@ant-design/icons'
import { useProductCategories, useProductBrands } from '../hooks/useProducts'
import { useCreateProduct, useUpdateProduct, useDeleteProduct } from '../hooks/useProductMutations'
import ProductGrid from './ProductGrid'
import ProductFilters from './ProductFilters'
import ProductSearch from './ProductSearch'
import { ProductFilters as ProductFiltersType, Product } from '../types'

const { Content, Sider } = Layout
const { Title } = Typography

interface ProductsPageProps {
  onProductClick?: (product: Product) => void
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  showFilters?: boolean
  showSearch?: boolean
  useInfiniteScroll?: boolean
  className?: string
}

const ProductsPageComponent: React.FC<ProductsPageProps> = ({
  onProductClick,
  onAddToCart,
  onAddToWishlist,
  showFilters = true,
  showSearch = true,
  useInfiniteScroll = false,
  className
}) => {
  // State management
  const [filters, setFilters] = useState<ProductFiltersType>({ page: 1, limit: 10 })
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid')
  const [filtersVisible, setFiltersVisible] = useState(false)
  const [isMobile, setIsMobile] = useState(false)

  // Hooks
  useProductCategories()
  useProductBrands()
  
  // Mutations
  const createProductMutation = useCreateProduct()
  const updateProductMutation = useUpdateProduct()
  const deleteProductMutation = useDeleteProduct()

  // Handle responsive design
  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    handleResize()
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  // Handle filters change
  const handleFiltersChange = useCallback((newFilters: ProductFiltersType) => {
    setFilters(newFilters)
  }, [])

  // Handle search
  const handleSearch = useCallback((_query: string, searchFilters?: ProductFiltersType) => {
    if (searchFilters) {
      setFilters(searchFilters)
    }
  }, [])

  // Handle clear filters
  const handleClearFilters = useCallback(() => {
    setFilters({ page: 1, limit: 10 })
  }, [])

  // Handle product actions
  const handleProductClick = useCallback((product: Product) => {
    onProductClick?.(product)
  }, [onProductClick])

  const handleAddToCart = useCallback((product: Product) => {
    onAddToCart?.(product)
    notification.success({
      message: 'Producto agregado',
      description: `${product.name} ha sido agregado al carrito`,
      placement: 'topRight',
    })
  }, [onProductClick])

  const handleAddToWishlist = useCallback((product: Product) => {
    onAddToWishlist?.(product)
    notification.success({
      message: 'Agregado a favoritos',
      description: `${product.name} ha sido agregado a tu lista de deseos`,
      placement: 'topRight',
    })
  }, [onAddToWishlist])

  // Handle view mode change
  const handleViewModeChange = useCallback((mode: 'grid' | 'list') => {
    setViewMode(mode)
  }, [])

  // Handle filters toggle
  const handleFiltersToggle = useCallback(() => {
    setFiltersVisible(!filtersVisible)
  }, [filtersVisible])

  // Error handling for mutations
  useEffect(() => {
    if (createProductMutation.error) {
      notification.error({
        message: 'Error al crear producto',
        description: 'No se pudo crear el producto. Inténtalo de nuevo.',
        placement: 'topRight',
      })
    }
  }, [createProductMutation.error])

  useEffect(() => {
    if (updateProductMutation.error) {
      notification.error({
        message: 'Error al actualizar producto',
        description: 'No se pudo actualizar el producto. Inténtalo de nuevo.',
        placement: 'topRight',
      })
    }
  }, [updateProductMutation.error])

  useEffect(() => {
    if (deleteProductMutation.error) {
      notification.error({
        message: 'Error al eliminar producto',
        description: 'No se pudo eliminar el producto. Inténtalo de nuevo.',
        placement: 'topRight',
      })
    }
  }, [deleteProductMutation.error])

  // Render filters sidebar for desktop
  const renderFiltersSidebar = () => {
    if (!showFilters) return null

    return (
      <Sider
        width={300}
        style={{
          background: '#fff',
          borderRight: '1px solid #f0f0f0',
        }}
        breakpoint="lg"
        collapsedWidth="0"
      >
        <ProductFilters
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onClearFilters={handleClearFilters}
        />
      </Sider>
    )
  }

  // Render filters drawer for mobile
  const renderFiltersDrawer = () => {
    if (!showFilters || !isMobile) return null

    return (
      <Drawer
        title="Filtros"
        placement="right"
        onClose={handleFiltersToggle}
        open={filtersVisible}
        width={300}
        bodyStyle={{ padding: 0 }}
      >
        <ProductFilters
          filters={filters}
          onFiltersChange={handleFiltersChange}
          onClearFilters={handleClearFilters}
        />
      </Drawer>
    )
  }

  // Render search bar
  const renderSearch = () => {
    if (!showSearch) return null

    return (
      <div style={{ marginBottom: 16 }}>
        <ProductSearch
          onSearch={handleSearch}
          onFiltersChange={handleFiltersChange}
          placeholder="Buscar productos..."
          showFilters={isMobile}
          showSort={true}
        />
      </div>
    )
  }

  // Render mobile filters button
  const renderMobileFiltersButton = () => {
    if (!showFilters || !isMobile) return null

    return (
      <Button
        icon={<FilterOutlined />}
        onClick={handleFiltersToggle}
        style={{ marginBottom: 16 }}
      >
        Filtros
        {Object.keys(filters).length > 0 && (
          <span style={{ marginLeft: 4, color: '#1890ff' }}>
            ({Object.keys(filters).length})
          </span>
        )}
      </Button>
    )
  }

  return (
    <div className={className}>
      <Layout style={{ minHeight: '100vh', background: '#fff' }}>
        {/* Desktop sidebar */}
        {!isMobile && renderFiltersSidebar()}

        <Layout>
          <Content style={{ padding: '24px' }}>
            {/* Page header */}
            <div style={{ marginBottom: 24 }}>
              <Title level={2} style={{ margin: 0 }}>
                Productos
              </Title>
              <Space style={{ marginTop: 8 }}>
                <Button
                  icon={<SearchOutlined />}
                  onClick={() => {/* Focus search */}}
                  size="small"
                >
                  Buscar
                </Button>
                {isMobile && (
                  <Button
                    icon={<FilterOutlined />}
                    onClick={handleFiltersToggle}
                    size="small"
                  >
                    Filtros
                  </Button>
                )}
              </Space>
            </div>

            {/* Search bar */}
            {renderSearch()}

            {/* Mobile filters button */}
            {renderMobileFiltersButton()}

            {/* Products grid */}
            <ProductGrid
              filters={filters}
              onFiltersChange={handleFiltersChange}
              onProductClick={handleProductClick}
              onAddToCart={handleAddToCart}
              onAddToWishlist={handleAddToWishlist}
              viewMode={viewMode}
              onViewModeChange={handleViewModeChange}
              showFilters={false} // Handled by sidebar/drawer
              showPagination={!useInfiniteScroll}
              useInfiniteScroll={useInfiniteScroll}
            />
          </Content>
        </Layout>
      </Layout>

      {/* Mobile filters drawer */}
      {renderFiltersDrawer()}
    </div>
  )
}

export default ProductsPageComponent
