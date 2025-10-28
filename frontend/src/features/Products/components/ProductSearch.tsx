import React, { useState, useEffect, useCallback } from 'react'
import { Input, Button, Space, Tag, AutoComplete, Dropdown, Menu } from 'antd'
import { 
  SearchOutlined, 
  ClearOutlined, 
  HistoryOutlined,
  FilterOutlined,
  SortAscendingOutlined,
  SortDescendingOutlined
} from '@ant-design/icons'
import { useProductSearch } from '../hooks/useProducts'
import { ProductFilters, ProductSearchResult } from '../types'

const { Search } = Input

interface ProductSearchProps {
  onSearch: (query: string, filters?: ProductFilters) => void
  onFiltersChange?: (filters: ProductFilters) => void
  placeholder?: string
  className?: string
  showFilters?: boolean
  showSort?: boolean
}

const ProductSearchComponent: React.FC<ProductSearchProps> = ({
  onSearch,
  onFiltersChange,
  placeholder = "Buscar productos...",
  className,
  showFilters = true,
  showSort = true
}) => {
  const [query, setQuery] = useState('')
  const [filters, setFilters] = useState<ProductFilters>({})
  const [searchHistory, setSearchHistory] = useState<string[]>([])
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc')

  // Debounced search
  const { data: searchResults = [], isLoading } = useProductSearch(
    query, 
    filters, 
    query.length >= 2
  )

  // Load search history from localStorage
  useEffect(() => {
    const history = localStorage.getItem('product-search-history')
    if (history) {
      setSearchHistory(JSON.parse(history))
    }
  }, [])

  // Save search to history
  const saveToHistory = useCallback((searchQuery: string) => {
    if (searchQuery.trim() && !searchHistory.includes(searchQuery)) {
      const newHistory = [searchQuery, ...searchHistory].slice(0, 10) // Keep last 10
      setSearchHistory(newHistory)
      localStorage.setItem('product-search-history', JSON.stringify(newHistory))
    }
  }, [searchHistory])

  const handleSearch = (searchQuery: string) => {
    if (searchQuery.trim()) {
      saveToHistory(searchQuery)
      onSearch(searchQuery, filters)
    }
  }

  const handleQueryChange = (value: string) => {
    setQuery(value)
  }

  const handleFiltersChange = (newFilters: ProductFilters) => {
    setFilters(newFilters)
    onFiltersChange?.(newFilters)
  }

  const handleSortChange = (field: string) => {
    const newFilters = {
      ...filters,
      sortBy: {
        field: field as any,
        order: sortOrder
      }
    }
    handleFiltersChange(newFilters)
  }

  const handleSortOrderChange = (order: 'asc' | 'desc') => {
    setSortOrder(order)
    if (filters.sortBy) {
      const newFilters = {
        ...filters,
        sortBy: {
          ...filters.sortBy,
          order
        }
      }
      handleFiltersChange(newFilters)
    }
  }

  const clearSearch = () => {
    setQuery('')
    setFilters({})
    onSearch('', {})
  }

  const handleHistoryClick = (historyItem: string) => {
    setQuery(historyItem)
    handleSearch(historyItem)
  }

  const handleSuggestionClick = (suggestion: ProductSearchResult) => {
    setQuery(suggestion.product.name)
    handleSearch(suggestion.product.name)
  }

  // AutoComplete options
  const autocompleteOptions = [
    ...searchHistory.map(item => ({
      value: item,
      label: (
        <Space>
          <HistoryOutlined />
          {item}
        </Space>
      )
    })),
    ...searchResults.slice(0, 5).map(result => ({
      value: result.product.name,
      label: (
        <Space>
          <SearchOutlined />
          {result.product.name}
        </Space>
      )
    }))
  ]

  // Sort menu
  const sortMenu = (
    <Menu
      onClick={({ key }) => handleSortChange(key)}
      selectedKeys={filters.sortBy?.field ? [filters.sortBy.field] : []}
    >
      <Menu.Item key="name">Nombre</Menu.Item>
      <Menu.Item key="price">Precio</Menu.Item>
      <Menu.Item key="rating">Calificación</Menu.Item>
      <Menu.Item key="createdAt">Fecha</Menu.Item>
      <Menu.Item key="popularity">Popularidad</Menu.Item>
    </Menu>
  )

  return (
    <div className={className}>
      <Space.Compact style={{ width: '100%' }}>
        <AutoComplete
          value={query}
          onChange={handleQueryChange}
          onSearch={handleSearch}
          options={autocompleteOptions}
          style={{ flex: 1 }}
          onSelect={(value) => {
            setQuery(value)
            handleSearch(value)
          }}
        >
          <Search
            placeholder={placeholder}
            enterButton={<SearchOutlined />}
            size="large"
            loading={isLoading}
            onSearch={handleSearch}
            allowClear
          />
        </AutoComplete>

        {showSort && (
          <Dropdown overlay={sortMenu} trigger={['click']}>
            <Button 
              icon={sortOrder === 'asc' ? <SortAscendingOutlined /> : <SortDescendingOutlined />}
              size="large"
            >
              Ordenar
            </Button>
          </Dropdown>
        )}

        {showFilters && (
          <Button 
            icon={<FilterOutlined />}
            size="large"
            type={Object.keys(filters).length > 0 ? 'primary' : 'default'}
          >
            Filtros
            {Object.keys(filters).length > 0 && (
              <Tag color="blue" style={{ marginLeft: 4 }}>
                {Object.keys(filters).length}
              </Tag>
            )}
          </Button>
        )}

        {(query || Object.keys(filters).length > 0) && (
          <Button 
            icon={<ClearOutlined />}
            size="large"
            onClick={clearSearch}
            title="Limpiar búsqueda"
          />
        )}
      </Space.Compact>

      {/* Active filters display */}
      {Object.keys(filters).length > 0 && (
        <div style={{ marginTop: 8 }}>
          <Space wrap>
            {filters.search && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, search: undefined })}>
                Búsqueda: {filters.search}
              </Tag>
            )}
            {filters.category && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, category: undefined })}>
                Categoría: {filters.category}
              </Tag>
            )}
            {filters.brand && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, brand: undefined })}>
                Marca: {filters.brand}
              </Tag>
            )}
            {filters.minPrice !== undefined && filters.maxPrice !== undefined && (
              <Tag closable onClose={() => handleFiltersChange({ 
                ...filters, 
                minPrice: undefined, 
                maxPrice: undefined 
              })}>
                Precio: ${filters.minPrice} - ${filters.maxPrice}
              </Tag>
            )}
            {filters.rating && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, rating: undefined })}>
                Calificación: {filters.rating}+ estrellas
              </Tag>
            )}
            {filters.inStock && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, inStock: undefined })}>
                En stock
              </Tag>
            )}
            {filters.featured && (
              <Tag closable onClose={() => handleFiltersChange({ ...filters, featured: undefined })}>
                Destacados
              </Tag>
            )}
          </Space>
        </div>
      )}

      {/* Search suggestions */}
      {searchResults.length > 0 && query && (
        <div style={{ marginTop: 8 }}>
          <Space wrap>
            <span style={{ color: '#666', fontSize: '12px' }}>Sugerencias:</span>
            {searchResults.slice(0, 3).map((result, index) => (
              <Tag 
                key={index}
                style={{ cursor: 'pointer' }}
                onClick={() => handleSuggestionClick(result)}
              >
                {result.product.name}
              </Tag>
            ))}
          </Space>
        </div>
      )}
    </div>
  )
}

export default ProductSearchComponent
