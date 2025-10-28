import React from 'react'
import { Typography } from 'antd'
import { HeroSectionProps } from '../types'

const { Title, Paragraph, Text } = Typography

const HeroSection: React.FC<HeroSectionProps> = ({
  title,
  subtitle,
  description,
  className
}) => {
  return (
    <div 
      className={className}
      style={{ 
        background: 'linear-gradient(135deg, #1890ff 0%, #096dd9 100%)', 
        padding: '60px 0',
        borderRadius: '8px',
        marginBottom: '40px',
        color: 'white',
        textAlign: 'center'
      }}
    >
      <Title level={1} style={{ color: 'white', margin: 0 }}>
        {title}
      </Title>
      <Paragraph style={{ fontSize: '18px', color: 'white', margin: '16px 0' }}>
        {subtitle}
      </Paragraph>
      <Text style={{ color: 'white', opacity: 0.9 }}>
        {description}
      </Text>
    </div>
  )
}

export default HeroSection
