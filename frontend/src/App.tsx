import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Layout, ConfigProvider } from 'antd'
import { QueryProvider } from '@shared/providers/QueryProvider'
import { AuthProvider } from '@features/Auth'
import AppHeader from '@shared/components/Layout/Header'
import HomePage from './pages/HomePage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

const { Content, Footer } = Layout

const App: React.FC = () => {
  return (
    <QueryProvider>
      <AuthProvider>
        <ConfigProvider
          theme={{
            token: {
              colorPrimary: '#1890ff',
              borderRadius: 6,
            },
          }}
        >
          <Router>
            <Layout style={{ minHeight: '100vh' }}>
              <AppHeader />
              
              <Content style={{ padding: '24px 50px' }}>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="/register" element={<RegisterPage />} />
                  {/* TODO: Add more routes */}
                </Routes>
              </Content>
              
              <Footer style={{ textAlign: 'center', background: '#f0f2f5' }}>
                E-commerce Evolution ©2024 - Learning Project
              </Footer>
            </Layout>
          </Router>
        </ConfigProvider>
      </AuthProvider>
    </QueryProvider>
  )
}

export default App
