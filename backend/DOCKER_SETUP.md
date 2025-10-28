# 🐳 Docker Setup Guide - E-commerce Project

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 4GB RAM available
- At least 10GB free disk space

## 🚀 Quick Start

### Development Environment

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v
```

### Production Environment

```bash
# Build and start production services
docker-compose -f docker-compose.prod.yml up -d --build

# Scale backend workers
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop all services
docker-compose -f docker-compose.prod.yml down
```

## 📦 Services

| Service | Port | Description |
|---------|------|-------------|
| **Frontend** | 3000 | React application with Vite |
| **Backend** | 8000 | FastAPI REST API |
| **PostgreSQL** | 5432 | Database |
| **Redis** | 6379 | Cache & sessions |
| **Nginx** | 80, 443 | Reverse proxy |
| **Prometheus** | 9090 | Metrics collection |
| **Grafana** | 3001 | Monitoring dashboards |

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Database
POSTGRES_DB=ecommerce
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=your_secure_password_here

# Redis
REDIS_PASSWORD=your_redis_password_here

# Backend
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
DATABASE_URL=postgresql://ecommerce_user:your_secure_password_here@postgres:5432/ecommerce
REDIS_URL=redis://:your_redis_password_here@redis:6379/0

# Frontend
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENVIRONMENT=development

# Monitoring
GF_SECURITY_ADMIN_PASSWORD=your_grafana_password_here
```

## 🏗️ Building Images

### Build all images

```bash
docker-compose build
```

### Build specific service

```bash
docker-compose build backend
docker-compose build frontend
```

### Build with no cache

```bash
docker-compose build --no-cache
```

## 🔍 Health Checks

Check service health:

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000/health

# Nginx
curl http://localhost/health

# All services status
docker-compose ps
```

## 📊 Monitoring

### Prometheus
- URL: http://localhost:9090
- View metrics and queries

### Grafana
- URL: http://localhost:3001
- Default credentials: admin/admin
- Pre-configured dashboards available

## 🐛 Troubleshooting

### View service logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Restart a service

```bash
docker-compose restart backend
docker-compose restart frontend
```

### Rebuild a service

```bash
docker-compose up -d --build backend
```

### Access container shell

```bash
# Backend
docker-compose exec backend sh

# Frontend
docker-compose exec frontend sh

# Database
docker-compose exec postgres psql -U ecommerce_user -d ecommerce
```

### Check resource usage

```bash
docker stats
```

### Clean up Docker system

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove all unused objects
docker system prune -a
```

## 🔐 Security Best Practices

1. **Never commit `.env` files** - Use `.env.example` as template
2. **Change default passwords** - Update all passwords in production
3. **Use secrets management** - For production, use Docker secrets or vault
4. **Keep images updated** - Regularly update base images
5. **Scan images for vulnerabilities** - Use `docker scan`
6. **Use non-root users** - All images run as non-root by default
7. **Limit resources** - Set memory and CPU limits in production

## 📈 Performance Optimization

### Backend

- Workers configured based on CPU cores
- Connection pooling enabled
- Redis caching enabled
- Gzip compression enabled

### Frontend

- Multi-stage build reduces image size
- Nginx serves static files
- Asset caching configured
- Gzip compression enabled

### Database

- Persistent volumes for data
- Connection pooling
- Index optimization
- Regular backups recommended

## 🧪 Testing

### Run tests in containers

```bash
# Backend tests
docker-compose -f docker-compose.yml -f docker-compose.test.yml run backend-test

# Frontend tests
docker-compose -f docker-compose.yml -f docker-compose.test.yml run frontend-test
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Nginx Documentation](https://nginx.org/en/docs/)

## ✅ Verification Checklist

After setup, verify:

- [ ] All containers are running: `docker-compose ps`
- [ ] Backend health check passes: `curl http://localhost:8000/health`
- [ ] Frontend is accessible: `curl http://localhost:3000`
- [ ] Database connection works
- [ ] Redis connection works
- [ ] Nginx reverse proxy works
- [ ] Monitoring dashboards accessible
- [ ] Logs are being generated
- [ ] No error messages in logs

## 🎯 Next Steps

1. Configure environment variables
2. Initialize database schema
3. Load seed data (optional)
4. Configure monitoring alerts
5. Set up CI/CD pipeline
6. Configure SSL certificates for production
7. Set up automated backups

For more detailed information, see the main README.md file.
