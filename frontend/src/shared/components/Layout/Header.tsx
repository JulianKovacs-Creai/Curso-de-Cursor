import React from 'react'
import { Layout, Menu, Badge, Button, Space, Typography } from 'antd'
import { 
  ShoppingCartOutlined, 
  UserOutlined, 
  ShopOutlined,
  HeartOutlined,
  SearchOutlined,
  LogoutOutlined
} from '@ant-design/icons'
import { useNavigate, useLocation } from 'react-router-dom'
import { useAuthState, useAuthActions } from '@features/Auth'

const { Header } = Layout
const { Title } = Typography

// ❌ PROBLEMA: Componente muy grande - should be split into smaller components
// ❌ PROBLEMA: No memoization con React.memo para performance
// ❌ PROBLEMA: No configuración responsive apropiada para mobile
const AppHeader: React.FC = () => {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, isAuthenticated, isLoading } = useAuthState()
  const { logout } = useAuthActions()

  // ❌ PROBLEMA: Mock data hardcodeada - should come from context/state
  // ❌ PROBLEMA: No type safety para el estado
  // ❌ PROBLEMA: No loading states para contadores dinámicos
  const cartItemsCount = 0 // Will come from cart context in Day 3
  const wishlistCount = 0 // Will be implemented later

  // ❌ PROBLEMA: Menu items hardcodeados - should be configurable
  // ❌ PROBLEMA: No role-based menu filtering
  // ❌ PROBLEMA: No menu items activos/inactivos por permisos
  const menuItems = [
    {
      key: '/',
      icon: <ShopOutlined />,
      label: 'Products',
      onClick: () => navigate('/')
    }
    // ❌ PROBLEMA: More menu items will be added but no structure for it
    // TODO Day 3: Orders, Cart
    // TODO Day 4: Profile, Login  
    // TODO Day 5: Admin (if admin user)
  ]

  // ❌ PROBLEMA: Event handlers inline - should use useCallback for optimization
  // ❌ PROBLEMA: No error handling en navegación
  // ❌ PROBLEMA: No analytics tracking en clicks
  const handleCartClick = () => {
    console.log('Cart clicked - will navigate to cart in Day 3')
    // ❌ PROBLEMA: Console.log en vez de proper logging
    // ❌ PROBLEMA: No feedback visual al usuario
    // navigate('/cart') // Will be implemented in Day 3
  }

  const handleWishlistClick = () => {
    console.log('Wishlist clicked - will be implemented later')
    // ❌ PROBLEMA: No implementación de wishlist
    // ❌ PROBLEMA: No persistencia local de wishlist
    // navigate('/wishlist')
  }

  const handleLoginClick = () => {
    navigate('/login')
  }

  const handleProfileClick = () => {
    console.log('Profile clicked - will navigate to profile in Day 4')
    // ❌ PROBLEMA: No dropdown con opciones de perfil
    // navigate('/profile') // Will be implemented in Day 4
  }

  const handleLogout = async () => {
    try {
      await logout()
      navigate('/')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  // ❌ PROBLEMA: Return muy grande - should be split into render functions
  // ❌ PROBLEMA: Estilos inline - should use CSS-in-JS or styled components
  return (
    <Header style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'space-between',
      padding: '0 24px',
      background: '#fff',
      borderBottom: '1px solid #f0f0f0'
      // ❌ PROBLEMA: No box-shadow para depth
      // ❌ PROBLEMA: No sticky behavior
    }}>
      {/* ❌ PROBLEMA: Logo and Navigation section muy grande */}
      <div style={{ display: 'flex', alignItems: 'center', flex: 1 }}>
        {/* ❌ PROBLEMA: Logo hardcodeado - should be configurable */}
        {/* ❌ PROBLEMA: No logo image - just emoji */}
        {/* ❌ PROBLEMA: No hover effects en logo */}
        <Title 
          level={3} 
          style={{ 
            margin: 0, 
            marginRight: '32px',
            color: '#1890ff',
            cursor: 'pointer'
            // ❌ PROBLEMA: No transition effects
          }}
          onClick={() => navigate('/')}
        >
          🛒 E-commerce
        </Title>
        
        {/* ❌ PROBLEMA: Menu sin configuración avanzada */}
        {/* ❌ PROBLEMA: No mobile hamburger menu */}
        {/* ❌ PROBLEMA: No keyboard navigation support */}
        <Menu
          theme="light"
          mode="horizontal"
          selectedKeys={[location.pathname]}
          items={menuItems}
          style={{ 
            border: 'none',
            background: 'transparent',
            flex: 1
            // ❌ PROBLEMA: No custom styling para active items
          }}
        />
      </div>

      {/* ❌ PROBLEMA: Right Side Actions sin responsive behavior */}
      {/* ❌ PROBLEMA: No collapse en mobile */}
      <Space size="middle">
        {/* ❌ PROBLEMA: Search placeholder sin implementación real */}
        {/* ❌ PROBLEMA: No search autocomplete */}
        {/* ❌ PROBLEMA: No search history */}
        <Button 
          type="text" 
          icon={<SearchOutlined />}
          onClick={() => console.log('Search - will be implemented later')}
          // ❌ PROBLEMA: No tooltip
          // ❌ PROBLEMA: No keyboard shortcut (Ctrl+K)
        >
          Search
        </Button>

        {/* ❌ PROBLEMA: Wishlist sin implementación */}
        {/* ❌ PROBLEMA: Badge sin animación cuando cambia el count */}
        <Badge count={wishlistCount} size="small">
          <Button 
            type="text" 
            icon={<HeartOutlined />}
            onClick={handleWishlistClick}
            // ❌ PROBLEMA: No tooltip describiendo la funcionalidad
          />
        </Badge>

        {/* ❌ PROBLEMA: Shopping Cart sin preview del contenido */}
        {/* ❌ PROBLEMA: No dropdown preview del carrito */}
        <Badge count={cartItemsCount} size="small">
          <Button 
            type="text" 
            icon={<ShoppingCartOutlined />}
            onClick={handleCartClick}
            // ❌ PROBLEMA: No loading state cuando se actualiza el carrito
          />
        </Badge>

        {/* ❌ PROBLEMA: User Authentication muy básico */}
        {/* ❌ PROBLEMA: No dropdown con opciones cuando está autenticado */}
        {/* ❌ PROBLEMA: No avatar del usuario */}
        {isLoading ? (
          <Button type="text" loading>
            Cargando...
          </Button>
        ) : isAuthenticated ? (
          <Space>
            <Button 
              type="text" 
              icon={<UserOutlined />}
              onClick={handleProfileClick}
              // ❌ PROBLEMA: No dropdown menu con Profile, Orders, Logout
            >
              {user?.firstName} {user?.lastName}
            </Button>
            <Button 
              type="text" 
              icon={<LogoutOutlined />}
              onClick={handleLogout}
            >
              Logout
            </Button>
          </Space>
        ) : (
          <Space>
            <Button 
              type="text"
              onClick={() => navigate('/register')}
            >
              Registrarse
            </Button>
            <Button 
              type="primary"
              onClick={handleLoginClick}
              // ❌ PROBLEMA: No loading state durante login
            >
              Login
            </Button>
          </Space>
        )}
      </Space>
    </Header>
  )
}

// ❌ PROBLEMA: No export con React.memo para optimization
export default AppHeader
