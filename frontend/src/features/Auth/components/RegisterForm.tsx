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
  MailOutlined,
  PhoneOutlined,
  EyeInvisibleOutlined,
  EyeTwoTone
} from '@ant-design/icons'
import { useNavigate, Link } from 'react-router-dom'
import { useRegister } from '../hooks/useRegister'
import { RegisterCredentials } from '../types'

const { Title, Text } = Typography

interface RegisterFormProps {
  onSuccess?: (user: any) => void
  onError?: (error: any) => void
  className?: string
}

const RegisterForm: React.FC<RegisterFormProps> = ({
  onSuccess,
  onError,
  className
}) => {
  const navigate = useNavigate()
  const [form] = Form.useForm()
  const [acceptTerms, setAcceptTerms] = useState(false)
  const [acceptMarketing, setAcceptMarketing] = useState(false)

  const registerMutation = useRegister()

  const handleRegister = async (values: RegisterCredentials) => {
    try {
      const result = await registerMutation.mutateAsync(values)
      onSuccess?.(result.user)
      navigate('/')
    } catch (error) {
      onError?.(error)
    }
  }

  const handleSubmit = (values: any) => {
    if (!acceptTerms) {
      form.setFields([
        {
          name: 'terms',
          errors: ['Debes aceptar los términos y condiciones']
        }
      ])
      return
    }

    handleRegister(values)
  }

  return (
    <Card 
      className={className}
      style={{ 
        maxWidth: 500, 
        margin: '0 auto',
        boxShadow: '0 4px 12px rgba(0,0,0,0.1)' 
      }}
    >
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <Title level={2} style={{ margin: 0 }}>
          Crear Cuenta
        </Title>
        <Text type="secondary">
          Únete a nuestra plataforma
        </Text>
      </div>

      {registerMutation.error && (
        <Alert
          message="Error en el registro"
          description={
            (registerMutation.error as any)?.details?.detail === "User with this email already exists" 
              ? "Este email ya está registrado. ¿Ya tienes cuenta? Inicia sesión aquí."
              : (registerMutation.error as any)?.details?.detail || 
                registerMutation.error?.message || 
                'Ha ocurrido un error inesperado. Inténtalo de nuevo.'
          }
          type="error"
          showIcon
          style={{ marginBottom: 24 }}
          action={
            (registerMutation.error as any)?.details?.detail === "User with this email already exists" ? (
              <Link to="/login">
                <Button type="link" size="small">
                  Iniciar sesión
                </Button>
              </Link>
            ) : null
          }
        />
      )}

      <Form
        form={form}
        name="register"
        onFinish={handleSubmit}
        layout="vertical"
        size="large"
        scrollToFirstError
      >
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item
              name="firstName"
              label="Nombre"
              rules={[
                { required: true, message: 'Por favor ingresa tu nombre' },
                { min: 2, message: 'El nombre debe tener al menos 2 caracteres' }
              ]}
            >
              <Input 
                prefix={<UserOutlined />} 
                placeholder="Tu nombre" 
              />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item
              name="lastName"
              label="Apellido"
              rules={[
                { required: true, message: 'Por favor ingresa tu apellido' },
                { min: 2, message: 'El apellido debe tener al menos 2 caracteres' }
              ]}
            >
              <Input 
                prefix={<UserOutlined />} 
                placeholder="Tu apellido" 
              />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item
          name="email"
          label="Email"
          rules={[
            { required: true, message: 'Por favor ingresa tu email' },
            { type: 'email', message: 'Email inválido' }
          ]}
        >
          <Input 
            prefix={<MailOutlined />} 
            placeholder="tu@email.com" 
          />
        </Form.Item>

        <Form.Item
          name="phone"
          label="Teléfono (Opcional)"
          rules={[
            { pattern: /^[+]?[\d\s\-\(\)]+$/, message: 'Formato de teléfono inválido' }
          ]}
        >
          <Input 
            prefix={<PhoneOutlined />} 
            placeholder="+1 234 567 8900" 
          />
        </Form.Item>

        <Form.Item
          name="password"
          label="Contraseña"
          rules={[
            { required: true, message: 'Por favor ingresa tu contraseña' },
            { min: 8, message: 'La contraseña debe tener al menos 8 caracteres' },
            { 
              pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/, 
              message: 'La contraseña debe contener al menos una mayúscula, una minúscula y un número' 
            }
          ]}
        >
          <Input.Password 
            prefix={<LockOutlined />} 
            placeholder="Tu contraseña"
            iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
          />
        </Form.Item>

        <Form.Item
          name="confirmPassword"
          label="Confirmar Contraseña"
          dependencies={['password']}
          rules={[
            { required: true, message: 'Por favor confirma tu contraseña' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve()
                }
                return Promise.reject(new Error('Las contraseñas no coinciden'))
              },
            }),
          ]}
        >
          <Input.Password 
            prefix={<LockOutlined />} 
            placeholder="Confirma tu contraseña"
            iconRender={(visible) => (visible ? <EyeTwoTone /> : <EyeInvisibleOutlined />)}
          />
        </Form.Item>

        <Form.Item name="terms" valuePropName="checked">
          <Checkbox
            checked={acceptTerms}
            onChange={(e) => setAcceptTerms(e.target.checked)}
          >
            Acepto los{' '}
            <a href="/terms" target="_blank" rel="noopener noreferrer">
              términos y condiciones
            </a>{' '}
            y la{' '}
            <a href="/privacy" target="_blank" rel="noopener noreferrer">
              política de privacidad
            </a>
          </Checkbox>
        </Form.Item>

        <Form.Item name="marketing" valuePropName="checked">
          <Checkbox
            checked={acceptMarketing}
            onChange={(e) => setAcceptMarketing(e.target.checked)}
          >
            Quiero recibir ofertas y novedades por email
          </Checkbox>
        </Form.Item>

        <Form.Item>
          <Button 
            type="primary" 
            htmlType="submit" 
            loading={registerMutation.isPending}
            block
            size="large"
          >
            Crear Cuenta
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
          ¿Ya tienes cuenta?{' '}
          <Link to="/login">
            <Button type="link" style={{ padding: 0 }}>
              Inicia sesión aquí
            </Button>
          </Link>
        </Text>
      </div>
    </Card>
  )
}

export default RegisterForm
