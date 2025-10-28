# 🚀 E-commerce Development Setup

## Comandos para levantar el proyecto:

### **Opción 1: Script automático (Recomendado)**
```bash
./start-dev.sh
```

### **Opción 2: Manual paso a paso**

1. **Base de datos:**
   ```bash
   docker-compose -f docker-compose.dev.yml up -d
   ```

2. **Backend (Terminal 1):**
   ```bash
   cd backend
   python3 main_clean.py
   ```

3. **Frontend (Terminal 2):**
   ```bash
   cd frontend
   npm run dev
   ```

### **Para detener:**
```bash
./stop-dev.sh
```

## URLs de acceso:
- **Frontend**: http://localhost:3000 (o 3001/3002)
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Servicios incluidos:
- ✅ PostgreSQL (puerto 5432)
- ✅ Redis (puerto 6379)
- ✅ Backend FastAPI (puerto 8000)
- ✅ Frontend React (puerto 3000+)

## Notas:
- Se excluyen Prometheus y Grafana para evitar errores de montaje
- Solo se incluyen los servicios esenciales para desarrollo
- Los puertos se asignan automáticamente si están ocupados
