import React, { useState, useCallback } from 'react'
import { 
  Row, 
  Col, 
  Spin, 
  Alert, 
  Empty, 
  Pagination, 
  Button,
  Space,
  Typography,
  Card,
  Tooltip
} from 'antd'
import { 
  AppstoreOutlined, 
  UnorderedListOutlined,
  ReloadOutlined,
  FilterOutlined
} from '@ant-design/icons'
import { useProducts, useInfiniteProducts } from '../hooks/useProducts'
import ProductCard from './ProductCard'
import { ProductFilters, Product } from '../types'

const { Title, Text } = Typography

interface ProductGridProps {
  filters: ProductFilters
  onFiltersChange?: (filters: ProductFilters) => void
  onProductClick?: (product: Product) => void
  onAddToCart?: (product: Product) => void
  onAddToWishlist?: (product: Product) => void
  viewMode?: 'grid' | 'list'
  onViewModeChange?: (mode: 'grid' | 'list') => void
  showFilters?: boolean
  showPagination?: boolean
  useInfiniteScroll?: boolean
  className?: string
}

const ProductGridComponent: React.FC<ProductGridProps> = ({
  filters,
  onFiltersChange,
  onProductClick,
  onAddToCart,
  onAddToWishlist,
  viewMode = 'grid',
  onViewModeChange,
  showFilters = true,
  showPagination = true,
  useInfiniteScroll = false,
  className
}) => {
  const [currentPage, setCurrentPage] = useState(1)
  const [isRefreshing, setIsRefreshing] = useState(false)

  // Use infinite query if enabled, otherwise regular query
  const infiniteQuery = useInfiniteProducts(filters)
  const regularQuery = useProducts({ ...filters, page: currentPage })

  const query = useInfiniteScroll ? infiniteQuery : regularQuery

  const {
    data,
    isLoading,
    error,
    refetch,
    isFetching,
    isFetchingNextPage,
    hasNextPage,
    fetchNextPage
  } = query

  // Handle refresh
  const handleRefresh = useCallback(async () => {
    setIsRefreshing(true)
    try {
      await refetch()
    } finally {
      setIsRefreshing(false)
    }
  }, [refetch])

  // Handle page change
  const handlePageChange = useCallback((page: number) => {
    setCurrentPage(page)
    if (onFiltersChange) {
      onFiltersChange({ ...filters, page })
    }
  }, [filters, onFiltersChange])

  // Handle load more for infinite scroll
  const handleLoadMore = useCallback(() => {
    if (hasNextPage && !isFetchingNextPage) {
      fetchNextPage()
    }
  }, [hasNextPage, isFetchingNextPage, fetchNextPage])

  // Get products from query
  const getProducts = () => {
    if (useInfiniteScroll && infiniteQuery.data) {
      return infiniteQuery.data.pages.flatMap(page => page.products)
    }
    return data?.products || []
  }

  // Get pagination info
  const getPaginationInfo = () => {
    if (useInfiniteScroll && infiniteQuery.data) {
      const lastPage = infiniteQuery.data.pages[infiniteQuery.data.pages.length - 1]
      return lastPage.pagination
    }
    return data?.pagination
  }

  const products = getProducts()
  const pagination = getPaginationInfo()

  // Loading state
  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', padding: '50px' }}>
        <Spin size="large" />
        <div style={{ marginTop: 16 }}>
          <Text>Cargando productos...</Text>
        </div>
      </div>
    )
  }

  // Error state
  if (error) {
    return (
      <Alert
        message="Error al cargar productos"
        description={error.message || 'Ha ocurrido un error inesperado'}
        type="error"
        showIcon
        action={
          <Button size="small" onClick={handleRefresh} loading={isRefreshing}>
            Reintentar
          </Button>
        }
        style={{ margin: '20px 0' }}
      />
    )
  }

  // Empty state
  if (products.length === 0) {
    return (
      <Empty
        image={Empty.PRESENTED_IMAGE_SIMPLE}
        description="No se encontraron productos"
        style={{ margin: '50px 0' }}
      >
        <Button type="primary" onClick={handleRefresh}>
          Recargar
        </Button>
      </Empty>
    )
  }

  return (
    <div className={className}>
      {/* Header with controls */}
      <Card 
        size="small" 
        style={{ marginBottom: 16 }}
        bodyStyle={{ padding: '12px 16px' }}
      >
        <Row justify="space-between" align="middle">
          <Col>
            <Space>
              <Title level={5} style={{ margin: 0 }}>
                {pagination?.total || products.length} productos encontrados
              </Title>
              {isFetching && (
                <Spin size="small" />
              )}
            </Space>
          </Col>
          
          <Col>
            <Space>
              {/* View mode toggle */}
              {onViewModeChange && (
                <Button.Group>
                  <Button
                    icon={<AppstoreOutlined />}
                    type={viewMode === 'grid' ? 'primary' : 'default'}
                    onClick={() => onViewModeChange('grid')}
                    size="small"
                  />
                  <Button
                    icon={<UnorderedListOutlined />}
                    type={viewMode === 'list' ? 'primary' : 'default'}
                    onClick={() => onViewModeChange('list')}
                    size="small"
                  />
                </Button.Group>
              )}

              {/* Refresh button */}
              <Tooltip title="Actualizar">
                <Button
                  icon={<ReloadOutlined />}
                  onClick={handleRefresh}
                  loading={isRefreshing}
                  size="small"
                />
              </Tooltip>

              {/* Filters button */}
              {showFilters && onFiltersChange && (
                <Tooltip title="Filtros">
                  <Button
                    icon={<FilterOutlined />}
                    onClick={() => {/* Open filters modal/sidebar */}}
                    size="small"
                  />
                </Tooltip>
              )}
            </Space>
          </Col>
        </Row>
      </Card>

      {/* Products grid */}
      <Row gutter={[16, 16]}>
        {products.map((product) => (
          <Col 
            key={product.id} 
            xs={24} 
            sm={12} 
            md={viewMode === 'list' ? 24 : 8} 
            lg={viewMode === 'list' ? 24 : 6}
            xl={viewMode === 'list' ? 24 : 4}
          >
            <ProductCard
              product={product}
              onAddToCart={onAddToCart}
              onAddToWishlist={onAddToWishlist}
              onViewDetails={onProductClick}
              loading={isFetching}
              variant={viewMode === 'list' ? 'detailed' : 'default'}
            />
          </Col>
        ))}
      </Row>

      {/* Load more button for infinite scroll */}
      {useInfiniteScroll && hasNextPage && (
        <div style={{ textAlign: 'center', marginTop: 24 }}>
          <Button
            type="primary"
            loading={isFetchingNextPage}
            onClick={handleLoadMore}
            size="large"
          >
            Cargar más productos
          </Button>
        </div>
      )}

      {/* Pagination */}
      {showPagination && !useInfiniteScroll && pagination && pagination.totalPages > 1 && (
        <div style={{ textAlign: 'center', marginTop: 32 }}>
          <Pagination
            current={pagination.page}
            total={pagination.total}
            pageSize={pagination.limit}
            onChange={handlePageChange}
            showSizeChanger={false}
            showQuickJumper
            showTotal={(total, range) => 
              `${range[0]}-${range[1]} de ${total} productos`
            }
          />
        </div>
      )}

      {/* Loading overlay for infinite scroll */}
      {useInfiniteScroll && isFetchingNextPage && (
        <div style={{ textAlign: 'center', marginTop: 16 }}>
          <Spin />
          <div style={{ marginTop: 8 }}>
            <Text type="secondary">Cargando más productos...</Text>
          </div>
        </div>
      )}
    </div>
  )
}

export default ProductGridComponent
