import { User } from '../types'
import { UserRole } from '@/shared/types'

export const authUtils = {
  // Check if user has specific role
  hasRole: (user: User | null, role: UserRole): boolean => {
    if (!user) return false
    return user.role === role
  },

  // Check if user has any of the specified roles
  hasAnyRole: (user: User | null, roles: UserRole[]): boolean => {
    if (!user) return false
    return roles.includes(user.role)
  },

  // Check if user has all specified roles (for single role, this is the same as hasRole)
  hasAllRoles: (user: User | null, roles: UserRole[]): boolean => {
    if (!user) return false
    return roles.includes(user.role)
  },

  // Check if user has specific permission (placeholder - permissions not in User type)
  hasPermission: (user: User | null, _permission: string): boolean => {
    if (!user) return false
    // TODO: Add permissions to User type or implement permission checking logic
    return false
  },

  // Check if user has any of the specified permissions
  hasAnyPermission: (user: User | null, _permissions: string[]): boolean => {
    if (!user) return false
    // TODO: Add permissions to User type or implement permission checking logic
    return false
  },

  // Check if user has all specified permissions
  hasAllPermissions: (user: User | null, _permissions: string[]): boolean => {
    if (!user) return false
    // TODO: Add permissions to User type or implement permission checking logic
    return false
  },

  // Get user display name
  getDisplayName: (user: User | null): string => {
    if (!user) return 'Guest'
    if (user.firstName && user.lastName) {
      return `${user.firstName} ${user.lastName}`
    }
    if (user.firstName) return user.firstName
    return user.email
  },

  // Get user initials
  getInitials: (user: User | null): string => {
    if (!user) return 'G'
    if (user.firstName && user.lastName) {
      return `${user.firstName[0]}${user.lastName[0]}`.toUpperCase()
    }
    if (user.firstName) return user.firstName[0].toUpperCase()
    return user.email[0].toUpperCase()
  },

  // Check if user is admin
  isAdmin: (user: User | null): boolean => {
    return authUtils.hasRole(user, UserRole.ADMIN)
  },

  // Check if user is customer
  isCustomer: (user: User | null): boolean => {
    return authUtils.hasRole(user, UserRole.CUSTOMER)
  },

  // Check if user is seller
  isSeller: (user: User | null): boolean => {
    return authUtils.hasRole(user, UserRole.VENDOR)
  },

  // Check if user is guest
  isGuest: (user: User | null): boolean => {
    return !user
  },

  // Check if user is verified
  isVerified: (user: User | null): boolean => {
    return user?.emailVerified || false
  },

  // Check if user is active
  isActive: (user: User | null): boolean => {
    return user?.isActive || false
  },

  // Format user role for display
  formatRole: (role: UserRole): string => {
    const roleMap: Record<UserRole, string> = {
      [UserRole.ADMIN]: 'Administrador',
      [UserRole.CUSTOMER]: 'Cliente',
      [UserRole.MODERATOR]: 'Moderador',
      [UserRole.VENDOR]: 'Vendedor'
    }
    return roleMap[role] || role
  },

  // Get user role color for UI
  getRoleColor: (role: UserRole): string => {
    const colorMap: Record<UserRole, string> = {
      [UserRole.ADMIN]: 'red',
      [UserRole.CUSTOMER]: 'blue',
      [UserRole.MODERATOR]: 'orange',
      [UserRole.VENDOR]: 'green'
    }
    return colorMap[role] || 'default'
  },

  // Check if user can access admin panel
  canAccessAdmin: (user: User | null): boolean => {
    return authUtils.isAdmin(user) || authUtils.hasPermission(user, 'admin.access')
  },

  // Check if user can manage products
  canManageProducts: (user: User | null): boolean => {
    return authUtils.isAdmin(user) || 
           authUtils.isSeller(user) || 
           authUtils.hasPermission(user, 'products.manage')
  },

  // Check if user can manage orders
  canManageOrders: (user: User | null): boolean => {
    return authUtils.isAdmin(user) || 
           authUtils.isSeller(user) || 
           authUtils.hasPermission(user, 'orders.manage')
  },

  // Check if user can view analytics
  canViewAnalytics: (user: User | null): boolean => {
    return authUtils.isAdmin(user) || 
           authUtils.isSeller(user) || 
           authUtils.hasPermission(user, 'analytics.view')
  },

  // Get user avatar URL or fallback
  getAvatarUrl: (user: User | null, size: number = 40): string => {
    if (!user) return `https://ui-avatars.com/api/?name=Guest&size=${size}&background=random`
    if (user.avatar) return user.avatar
    return `https://ui-avatars.com/api/?name=${encodeURIComponent(authUtils.getDisplayName(user))}&size=${size}&background=random`
  },

  // Validate email format
  isValidEmail: (email: string): boolean => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return emailRegex.test(email)
  },

  // Validate password strength
  validatePassword: (password: string): { isValid: boolean; errors: string[] } => {
    const errors: string[] = []
    
    if (password.length < 8) {
      errors.push('La contraseña debe tener al menos 8 caracteres')
    }
    
    if (!/[A-Z]/.test(password)) {
      errors.push('La contraseña debe contener al menos una letra mayúscula')
    }
    
    if (!/[a-z]/.test(password)) {
      errors.push('La contraseña debe contener al menos una letra minúscula')
    }
    
    if (!/\d/.test(password)) {
      errors.push('La contraseña debe contener al menos un número')
    }
    
    if (!/[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]/.test(password)) {
      errors.push('La contraseña debe contener al menos un carácter especial')
    }
    
    return {
      isValid: errors.length === 0,
      errors
    }
  },

  // Generate random password
  generatePassword: (length: number = 12): string => {
    const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    let password = ''
    for (let i = 0; i < length; i++) {
      password += charset.charAt(Math.floor(Math.random() * charset.length))
    }
    return password
  },

  // Check if token is expired (basic check)
  isTokenExpired: (token: string | null): boolean => {
    if (!token) return true
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Math.floor(Date.now() / 1000)
      return payload.exp < currentTime
    } catch {
      return true
    }
  },

  // Get token expiration time
  getTokenExpiration: (token: string | null): Date | null => {
    if (!token) return null
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      return new Date(payload.exp * 1000)
    } catch {
      return null
    }
  }
}
