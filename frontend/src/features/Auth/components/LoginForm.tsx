import React, { useState } from 'react'
import { 
  Form, 
  Input, 
  Button, 
  Card, 
  Typography, 
  Space, 
  Divider,
  Checkbox,
  Alert,
  Row,
  Col
} from 'antd'
import { 
  UserOutlined, 
  LockOutlined, 
  EyeInvisibleOutlined,
  EyeTwoTone
} from '@ant-design/icons'
import { useNavigate, Link } from 'react-router-dom'
import { useLogin } from '../hooks/useLogin'
import { LoginCredentials } from '../types'

const { Title, Text } = Typography

interface LoginFormProps {
  onSuccess?: (user: any) => void
  onError?: (error: any) => void
  className?: string
}

const LoginForm: React.FC<LoginFormProps> = ({
  onSuccess,
  onError,
  className
}) => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [rememberMe, setRememberMe] = useState(false)

  const loginMutation = useLogin()

  const handleLogin = async (values: LoginCredentials) => {
    try {
      const result = await loginMutation.mutateAsync(values)
      onSuccess?.(result.user)
      navigate('/')
    } catch (error) {
      onError?.(error)
    }
  }

  return (
    <Card 
      className={className}
      style={{ 
        maxWidth: 400, 
        margin: '0 auto',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <Title level={2} style={{ margin: 0 }}>
          Iniciar Sesión
        </Title>
        <Text type="secondary">
          Accede a tu cuenta
        </Text>
      </div>

      {loginMutation.error && (
        <Alert
          message="Error en el login"
          description={
            (loginMutation.error as any)?.details?.detail || 
            loginMutation.error?.message || 
            'Credenciales inválidas. Verifica tu email y contraseña.'
          }
          type="error"
          showIcon
          style={{ marginBottom: 24 }}
        />
      )}

      <Form
        form={form}
        name="login"
        onFinish={handleLogin}
        layout="vertical"
        size="large"
      >
        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: 'Por favor ingresa tu email' },
            { type: 'email', message: 'Email inválido' }
          ]}
        >
          <Input 
            prefix={<UserOutlined />} 
            placeholder="tu@email.com" 
          />
        </Form.Item>

        <Form.Item
          name="password"
          label="Contraseña"
          rules={[
            { required: true, message: 'Por favor ingresa tu contraseña' }
          ]}
        >
          <Input.Password 
            prefix={<LockOutlined />} 
            placeholder="Tu contraseña"
            iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
          />
        </Form.Item>

        <Row justify="space-between" align="middle">
          <Col>
            <Checkbox
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
            >
              Recordarme
            </Checkbox>
          </Col>
          <Col>
            <Link to="/forgot-password">
              <Button type="link" style={{ padding: 0 }}>
                ¿Olvidaste tu contraseña?
              </Button>
            </Link>
          </Col>
        </Row>

        <Form.Item style={{ marginTop: 24 }}>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={loginMutation.isPending}
            block
            size="large"
          >
            Iniciar Sesión
          </Button>
        </Form.Item>
      </Form>

      <Divider>
        <Text type="secondary">O</Text>
      </Divider>

      <Space direction="vertical" style={{ width: '100%' }}>
        <Button 
          block 
          size="large"
          onClick={() => {/* Google OAuth */}}
        >
          Continuar con Google
        </Button>
        <Button 
          block 
          size="large"
          onClick={() => {/* Facebook OAuth */}}
        >
          Continuar con Facebook
        </Button>
      </Space>

      <div style={{ textAlign: 'center', marginTop: 24 }}>
        <Text type="secondary">
          ¿No tienes cuenta?{' '}
          <Link to="/register">
            <Button type="link" style={{ padding: 0 }}>
              Regístrate aquí
            </Button>
          </Link>
        </Text>
      </div>
    </Card>
  )
}

export default LoginForm
