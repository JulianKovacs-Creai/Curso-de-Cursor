import React from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { Spin, Alert } from 'antd'
import { useAuthState } from '../context/AuthContext'
import { ProtectedRouteProps } from '../types'

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  requiredRole,
  requiredPermissions,
  fallback,
  redirectTo = '/login'
}) => {
  const { user, isAuthenticated, isLoading } = useAuthState()
  const location = useLocation()

  // Show loading state
  if (isLoading) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '50vh' 
      }}>
        <Spin size="large" />
      </div>
    )
  }

  // Redirect if not authenticated
  if (!isAuthenticated || !user) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />
  }

  // Check role requirement
  if (requiredRole && user.role !== requiredRole) {
    return (
      fallback || (
        <Alert
          message="Acceso Denegado"
          description="No tienes permisos para acceder a esta página."
          type="error"
          showIcon
          style={{ margin: '20px' }}
        />
      )
    )
  }

  // Check permissions requirement
  if (requiredPermissions && requiredPermissions.length > 0) {
    const hasPermission = requiredPermissions.some(permission => 
      user.permissions?.includes(permission)
    )
    
    if (!hasPermission) {
      return (
        fallback || (
          <Alert
            message="Acceso Denegado"
            description="No tienes los permisos necesarios para acceder a esta página."
            type="error"
            showIcon
            style={{ margin: '20px' }}
          />
        )
      )
    }
  }

  return <>{children}</>
}

export default ProtectedRoute
