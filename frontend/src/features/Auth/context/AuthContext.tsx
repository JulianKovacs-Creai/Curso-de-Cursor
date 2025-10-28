import React, { createContext, useContext, ReactNode } from 'react'
import { useAuth } from '../hooks/useAuth'
import { AuthContextType } from '../types'

const AuthContext = createContext<AuthContextType | undefined>(undefined)

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  try {
    const auth = useAuth()
    
    // Convert User | undefined to User | null to match interface
    const authWithNullUser = {
      ...auth,
      user: auth.user ?? null
    }

    return (
      <AuthContext.Provider value={authWithNullUser}>
        {children}
      </AuthContext.Provider>
    )
  } catch (error) {
    console.error('AuthProvider error:', error)
    // Return a fallback context value
    const fallbackAuth: AuthContextType = {
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: error as Error,
      login: async () => { throw new Error('Auth not available') },
      register: async () => { throw new Error('Auth not available') },
      logout: async () => { throw new Error('Auth not available') },
      refreshToken: async () => { throw new Error('Auth not available') },
      isLoggingIn: false,
      isRegistering: false,
      isLoggingOut: false,
      isRefreshing: false,
      loginError: null,
      registerError: null,
      logoutError: null,
      refreshError: null,
      resetLoginError: () => {},
      resetRegisterError: () => {},
      resetLogoutError: () => {},
      resetRefreshError: () => {}
    }

    return (
      <AuthContext.Provider value={fallbackAuth}>
        {children}
      </AuthContext.Provider>
    )
  }
}

export const useAuthContext = (): AuthContextType => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}

// Hook for easy access to auth state
export const useAuthState = () => {
  const { user, isAuthenticated, isLoading, error } = useAuthContext()
  return { user, isAuthenticated, isLoading, error }
}

// Hook for easy access to auth actions
export const useAuthActions = () => {
  const { 
    login, 
    register, 
    logout, 
    refreshToken,
    isLoggingIn,
    isRegistering,
    isLoggingOut,
    isRefreshing
  } = useAuthContext()
  
  return { 
    login, 
    register, 
    logout, 
    refreshToken,
    isLoggingIn,
    isRegistering,
    isLoggingOut,
    isRefreshing
  }
}

// Hook for easy access to auth errors
export const useAuthErrors = () => {
  const { 
    loginError, 
    registerError, 
    logoutError, 
    refreshError,
    resetLoginError,
    resetRegisterError,
    resetLogoutError,
    resetRefreshError
  } = useAuthContext()
  
  return { 
    loginError, 
    registerError, 
    logoutError, 
    refreshError,
    resetLoginError,
    resetRegisterError,
    resetLogoutError,
    resetRefreshError
  }
}
