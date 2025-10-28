import React from 'react'
import { Layout, Typography, App, Card, Button, Space, Avatar, Divider } from 'antd'
import { UserOutlined, LogoutOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useAuthState, useAuthActions } from '@features/Auth'
import { LoginForm } from '@features/Auth'

const { Content } = Layout
const { Title, Text } = Typography

const LoginPage: React.FC = () => {
  const navigate = useNavigate()
  const { user, isAuthenticated, isLoading } = useAuthState()
  const { logout } = useAuthActions()

  const handleSuccess = (user: any) => {
    console.log('Login successful:', user)
    navigate('/')
  }

  const handleError = (error: any) => {
    console.error('Login error:', error)
  }

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  // Si está cargando, mostrar loading
  if (isLoading) {
    return (
      <App>
        <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
          <Content style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            padding: '20px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <Title level={2}>Cargando...</Title>
            </div>
          </Content>
        </Layout>
      </App>
    )
  }

  // Si está autenticado, mostrar perfil
  if (isAuthenticated && user) {
    return (
      <App>
        <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
          <Content style={{ 
            display: 'flex', 
            justifyContent: 'center', 
            alignItems: 'center', 
            padding: '20px'
          }}>
            <div style={{ width: '100%', maxWidth: 500 }}>
              <div style={{ textAlign: 'center', marginBottom: 32 }}>
                <Title level={1}>E-commerce Evolution</Title>
                <Title level={3} type="secondary">
                  Bienvenido de vuelta
                </Title>
              </div>
              
              <Card style={{ boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }}>
                <div style={{ textAlign: 'center' }}>
                  <Avatar 
                    size={80} 
                    icon={<UserOutlined />} 
                    style={{ marginBottom: 16, backgroundColor: '#1890ff' }}
                  />
                  <Title level={3} style={{ margin: 0 }}>
                    {user.firstName} {user.lastName}
                  </Title>
                  <Text type="secondary" style={{ fontSize: 16 }}>
                    {user.email}
                  </Text>
                  
                  <Divider />
                  
                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div>
                      <Text strong>Estado de la cuenta:</Text>
                      <div style={{ marginTop: 8 }}>
                        <Text type={user.isActive ? 'success' : 'danger'}>
                          {user.isActive ? 'Activa' : 'Inactiva'}
                        </Text>
                      </div>
                      <div style={{ marginTop: 4 }}>
                        <Text type={user.emailVerified ? 'success' : 'warning'}>
                          {user.emailVerified ? 'Verificada' : 'Pendiente de verificación'}
                        </Text>
                      </div>
                    </div>
                    
                    <Button 
                      type="primary" 
                      size="large" 
                      block
                      onClick={() => navigate('/')}
                    >
                      Ir al Inicio
                    </Button>
                    
                    <Button 
                      icon={<LogoutOutlined />} 
                      size="large" 
                      block
                      onClick={handleLogout}
                    >
                      Cerrar Sesión
                    </Button>
                  </Space>
                </div>
              </Card>
            </div>
          </Content>
        </Layout>
      </App>
    )
  }

  // Si no está autenticado, mostrar formulario de login
  return (
    <App>
      <Layout style={{ minHeight: '100vh', background: '#f5f5f5' }}>
        <Content style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          padding: '20px'
        }}>
          <div style={{ width: '100%', maxWidth: 500 }}>
            <div style={{ textAlign: 'center', marginBottom: 32 }}>
              <Title level={1}>E-commerce Evolution</Title>
              <Title level={3} type="secondary">
                Inicia sesión en tu cuenta
              </Title>
            </div>
            
            <LoginForm
              onSuccess={handleSuccess}
              onError={handleError}
            />
          </div>
        </Content>
      </Layout>
    </App>
  )
}

export default LoginPage
