import React, { useState } from 'react'
import { Button, Space, Typography, Card, Row, Col, notification } from 'antd'
import { 
  ProductsPage,
  useProducts,
  useCreateProduct,
  useUpdateProduct,
  useDeleteProduct,
  Product
} from '../index'
import { ProductFilters as ProductFiltersType } from '../types'

const { Title, Text } = Typography

/**
 * Example component demonstrating the complete Products feature
 * with API integration, React Query, and modern components
 */
const ProductsExample: React.FC = () => {
  const [filters] = useState<ProductFiltersType>({ page: 1, limit: 10 })
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null)

  // Query hooks
  const { data: productsData, isLoading, error, refetch } = useProducts(filters)
  
  // Mutation hooks
  const createProductMutation = useCreateProduct()
  const updateProductMutation = useUpdateProduct()
  const deleteProductMutation = useDeleteProduct()

  // Handle product selection
  const handleProductClick = (product: Product) => {
    setSelectedProduct(product)
    notification.info({
      message: 'Producto seleccionado',
      description: `Has seleccionado: ${product.name}`,
      placement: 'topRight',
    })
  }

  // Handle add to cart
  const handleAddToCart = (product: Product) => {
    notification.success({
      message: 'Agregado al carrito',
      description: `${product.name} ha sido agregado al carrito`,
      placement: 'topRight',
    })
  }

  // Handle add to wishlist
  const handleAddToWishlist = (product: Product) => {
    notification.success({
      message: 'Agregado a favoritos',
      description: `${product.name} ha sido agregado a tu lista de deseos`,
      placement: 'topRight',
    })
  }

  // Handle create product
  const handleCreateProduct = async () => {
    try {
      const newProduct = await createProductMutation.mutateAsync({
        name: 'Nuevo Producto',
        description: 'Descripción del nuevo producto',
        price: 99.99,
        sku: 'NP-001',
        categoryId: '1',
        tags: ['nuevo', 'destacado'],
        status: 'active' as any,
        featured: true,
        weight: 1.5,
        seo: {
          title: 'Nuevo Producto',
          description: 'Descripción SEO'
        }
      })
      
      notification.success({
        message: 'Producto creado',
        description: `Producto ${newProduct.name} creado exitosamente`,
        placement: 'topRight',
      })
    } catch (error) {
      notification.error({
        message: 'Error al crear producto',
        description: 'No se pudo crear el producto',
        placement: 'topRight',
      })
    }
  }

  // Handle update product
  const handleUpdateProduct = async (productId: string) => {
    try {
      const updatedProduct = await updateProductMutation.mutateAsync({
        id: productId,
        data: {
          name: 'Producto Actualizado',
          price: 149.99
        }
      })
      
      notification.success({
        message: 'Producto actualizado',
        description: `Producto ${updatedProduct.name} actualizado exitosamente`,
        placement: 'topRight',
      })
    } catch (error) {
      notification.error({
        message: 'Error al actualizar producto',
        description: 'No se pudo actualizar el producto',
        placement: 'topRight',
      })
    }
  }

  // Handle delete product
  const handleDeleteProduct = async (productId: string) => {
    try {
      await deleteProductMutation.mutateAsync(productId)
      
      notification.success({
        message: 'Producto eliminado',
        description: 'Producto eliminado exitosamente',
        placement: 'topRight',
      })
    } catch (error) {
      notification.error({
        message: 'Error al eliminar producto',
        description: 'No se pudo eliminar el producto',
        placement: 'topRight',
      })
    }
  }

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>Products Feature - Complete Example</Title>
      
      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>API Integration Status</Title>
        <Row gutter={16}>
          <Col span={8}>
            <Text strong>Loading:</Text> {isLoading ? 'Yes' : 'No'}
          </Col>
          <Col span={8}>
            <Text strong>Error:</Text> {error ? 'Yes' : 'No'}
          </Col>
          <Col span={8}>
            <Text strong>Products:</Text> {productsData?.products.length || 0}
          </Col>
        </Row>
        
        <Space style={{ marginTop: 16 }}>
          <Button onClick={() => refetch()}>
            Refetch Data
          </Button>
          <Button 
            type="primary" 
            onClick={handleCreateProduct}
            loading={createProductMutation.isPending}
          >
            Create Product
          </Button>
        </Space>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>Mutation Status</Title>
        <Row gutter={16}>
          <Col span={8}>
            <Text strong>Create:</Text> {createProductMutation.isPending ? 'Pending' : 'Ready'}
          </Col>
          <Col span={8}>
            <Text strong>Update:</Text> {updateProductMutation.isPending ? 'Pending' : 'Ready'}
          </Col>
          <Col span={8}>
            <Text strong>Delete:</Text> {deleteProductMutation.isPending ? 'Pending' : 'Ready'}
          </Col>
        </Row>
      </Card>

      <Card style={{ marginBottom: 24 }}>
        <Title level={4}>Selected Product</Title>
        {selectedProduct ? (
          <div>
            <Text strong>Name:</Text> {selectedProduct.name}<br/>
            <Text strong>Price:</Text> ${selectedProduct.price}<br/>
            <Text strong>SKU:</Text> {selectedProduct.sku}<br/>
            <Space style={{ marginTop: 8 }}>
              <Button 
                size="small"
                onClick={() => handleUpdateProduct(selectedProduct.id)}
                loading={updateProductMutation.isPending}
              >
                Update
              </Button>
              <Button 
                size="small"
                danger
                onClick={() => handleDeleteProduct(selectedProduct.id)}
                loading={deleteProductMutation.isPending}
              >
                Delete
              </Button>
            </Space>
          </div>
        ) : (
          <Text type="secondary">No product selected</Text>
        )}
      </Card>

      {/* Complete Products Page */}
      <ProductsPage
        onProductClick={handleProductClick}
        onAddToCart={handleAddToCart}
        onAddToWishlist={handleAddToWishlist}
        showFilters={true}
        showSearch={true}
        useInfiniteScroll={false}
      />
    </div>
  )
}

export default ProductsExample
