import React from 'react'
import { Typography, Row, Col, Tag } from 'antd'
import { ProjectTimelineProps, TimelineItem } from '../types'

const { Title } = Typography

const ProjectTimeline: React.FC<ProjectTimelineProps> = ({ className }) => {
  const timelineItems: TimelineItem[] = [
    {
      id: 'day1',
      title: 'Day 1: Clean Architecture (Backend)',
      status: 'completed',
      description: 'Backend structure and API setup'
    },
    {
      id: 'day2',
      title: 'Day 2: Products Feature (Frontend)',
      status: 'current',
      description: 'Product listing and management'
    },
    {
      id: 'day3',
      title: 'Day 3: Orders & Cart',
      status: 'upcoming',
      description: 'Shopping cart and order management'
    },
    {
      id: 'day4',
      title: 'Day 4: Authentication',
      status: 'upcoming',
      description: 'User authentication and authorization'
    }
  ]

  const getTagColor = (status: TimelineItem['status']) => {
    switch (status) {
      case 'completed':
        return 'success'
      case 'current':
        return 'processing'
      case 'upcoming':
        return 'default'
      default:
        return 'default'
    }
  }

  return (
    <div 
      className={className}
      style={{ 
        marginTop: '60px', 
        padding: '40px',
        background: 'white',
        borderRadius: '8px',
        textAlign: 'center'
      }}
    >
      <Title level={3}>Project Evolution Timeline</Title>
      <Row gutter={[24, 16]} style={{ marginTop: '32px' }}>
        {timelineItems.map((item) => (
          <Col span={6} key={item.id}>
            <Tag 
              color={getTagColor(item.status)} 
              style={{ padding: '8px 16px', fontSize: '14px' }}
            >
              {item.title}
            </Tag>
          </Col>
        ))}
      </Row>
    </div>
  )
}

export default ProjectTimeline
