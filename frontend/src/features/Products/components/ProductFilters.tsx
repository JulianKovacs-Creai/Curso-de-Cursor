import React, { useState, useEffect } from 'react'
import { 
  Card, 
  Collapse, 
  Slider, 
  Checkbox, 
  Radio, 
  Input, 
  Button, 
  Space, 
  Tag,
  Select,
  Row,
  Col,
  Divider
} from 'antd'
import { 
  FilterOutlined, 
  ClearOutlined, 
  SearchOutlined,
  DownOutlined,
  UpOutlined
} from '@ant-design/icons'
import { useProductCategories, useProductBrands } from '../hooks/useProducts'
import { ProductFilters } from '../types'

const { Panel } = Collapse
const { Search } = Input
const { Option } = Select

interface ProductFiltersProps {
  filters: ProductFilters
  onFiltersChange: (filters: ProductFilters) => void
  onClearFilters: () => void
  className?: string
}

const ProductFiltersComponent: React.FC<ProductFiltersProps> = ({
  filters,
  onFiltersChange,
  onClearFilters,
  className
}) => {
  const [localFilters, setLocalFilters] = useState<ProductFilters>(filters)
  const [priceRange, setPriceRange] = useState<[number, number]>([
    filters.minPrice || 0,
    filters.maxPrice || 1000
  ])

  const { data: categories = [], isLoading: categoriesLoading } = useProductCategories()
  const { data: brands = [], isLoading: brandsLoading } = useProductBrands()

  useEffect(() => {
    setLocalFilters(filters)
    setPriceRange([filters.minPrice || 0, filters.maxPrice || 1000])
  }, [filters])

  const handleFilterChange = (key: keyof ProductFilters, value: any) => {
    const newFilters = { ...localFilters, [key]: value }
    setLocalFilters(newFilters)
    onFiltersChange(newFilters)
  }

  const handlePriceRangeChange = (value: [number, number]) => {
    setPriceRange(value)
    handleFilterChange('minPrice', value[0])
    handleFilterChange('maxPrice', value[1])
  }

  const handleClearFilters = () => {
    setLocalFilters({})
    setPriceRange([0, 1000])
    onClearFilters()
  }

  const hasActiveFilters = Object.keys(filters).length > 0

  return (
    <Card 
      title={
        <Space>
          <FilterOutlined />
          Filtros
          {hasActiveFilters && (
            <Tag color="blue" closable onClose={handleClearFilters}>
              {Object.keys(filters).length} activos
            </Tag>
          )}
        </Space>
      }
      extra={
        hasActiveFilters && (
          <Button 
            type="link" 
            icon={<ClearOutlined />} 
            onClick={handleClearFilters}
            size="small"
          >
            Limpiar
          </Button>
        )
      }
      className={className}
    >
      <Collapse 
        defaultActiveKey={['search', 'price', 'category']}
        ghost
        expandIcon={({ isActive }) => isActive ? <UpOutlined /> : <DownOutlined />}
      >
        {/* Search */}
        <Panel header="Búsqueda" key="search">
          <Search
            placeholder="Buscar productos..."
            value={localFilters.search || ''}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            onSearch={(value) => handleFilterChange('search', value)}
            allowClear
            enterButton={<SearchOutlined />}
          />
        </Panel>

        {/* Price Range */}
        <Panel header="Rango de Precio" key="price">
          <div style={{ padding: '0 16px' }}>
            <Slider
              range
              min={0}
              max={1000}
              step={10}
              value={priceRange}
              onChange={handlePriceRangeChange}
              marks={{
                0: '$0',
                250: '$250',
                500: '$500',
                750: '$750',
                1000: '$1000+'
              }}
            />
            <div style={{ marginTop: 16, textAlign: 'center' }}>
              <Tag color="blue">
                ${priceRange[0]} - ${priceRange[1]}
              </Tag>
            </div>
          </div>
        </Panel>

        {/* Category */}
        <Panel header="Categoría" key="category">
          <div style={{ maxHeight: 200, overflowY: 'auto' }}>
            {categoriesLoading ? (
              <div>Cargando categorías...</div>
            ) : (
              <Radio.Group
                value={localFilters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Radio value="">Todas las categorías</Radio>
                  {categories.map(category => (
                    <Radio key={category.id} value={category.id}>
                      {category.name}
                    </Radio>
                  ))}
                </Space>
              </Radio.Group>
            )}
          </div>
        </Panel>

        {/* Brand */}
        <Panel header="Marca" key="brand">
          <div style={{ maxHeight: 200, overflowY: 'auto' }}>
            {brandsLoading ? (
              <div>Cargando marcas...</div>
            ) : (
              <Radio.Group
                value={localFilters.brand}
                onChange={(e) => handleFilterChange('brand', e.target.value)}
                style={{ width: '100%' }}
              >
                <Space direction="vertical" style={{ width: '100%' }}>
                  <Radio value="">Todas las marcas</Radio>
                  {brands.map(brand => (
                    <Radio key={brand.id} value={brand.id}>
                      {brand.name}
                    </Radio>
                  ))}
                </Space>
              </Radio.Group>
            )}
          </div>
        </Panel>

        {/* Rating */}
        <Panel header="Calificación" key="rating">
          <Radio.Group
            value={localFilters.rating}
            onChange={(e) => handleFilterChange('rating', e.target.value)}
            style={{ width: '100%' }}
          >
            <Space direction="vertical" style={{ width: '100%' }}>
              <Radio value={undefined}>Cualquier calificación</Radio>
              <Radio value={4}>4+ estrellas</Radio>
              <Radio value={3}>3+ estrellas</Radio>
              <Radio value={2}>2+ estrellas</Radio>
              <Radio value={1}>1+ estrellas</Radio>
            </Space>
          </Radio.Group>
        </Panel>

        {/* Availability */}
        <Panel header="Disponibilidad" key="availability">
          <Checkbox
            checked={localFilters.inStock === true}
            onChange={(e) => handleFilterChange('inStock', e.target.checked ? true : undefined)}
          >
            Solo productos en stock
          </Checkbox>
        </Panel>

        {/* Featured */}
        <Panel header="Destacados" key="featured">
          <Checkbox
            checked={localFilters.featured === true}
            onChange={(e) => handleFilterChange('featured', e.target.checked ? true : undefined)}
          >
            Solo productos destacados
          </Checkbox>
        </Panel>

        {/* Sort */}
        <Panel header="Ordenar por" key="sort">
          <Select
            value={localFilters.sortBy?.field}
            onChange={(value) => handleFilterChange('sortBy', { 
              field: value, 
              order: localFilters.sortBy?.order || 'asc' 
            })}
            style={{ width: '100%' }}
            placeholder="Seleccionar orden"
          >
            <Option value="name">Nombre</Option>
            <Option value="price">Precio</Option>
            <Option value="rating">Calificación</Option>
            <Option value="createdAt">Fecha de creación</Option>
            <Option value="popularity">Popularidad</Option>
          </Select>
          
          <Divider />
          
          <Radio.Group
            value={localFilters.sortBy?.order}
            onChange={(e) => handleFilterChange('sortBy', { 
              field: localFilters.sortBy?.field || 'name', 
              order: e.target.value 
            })}
            style={{ width: '100%' }}
          >
            <Space>
              <Radio value="asc">Ascendente</Radio>
              <Radio value="desc">Descendente</Radio>
            </Space>
          </Radio.Group>
        </Panel>
      </Collapse>
    </Card>
  )
}

export default ProductFiltersComponent
