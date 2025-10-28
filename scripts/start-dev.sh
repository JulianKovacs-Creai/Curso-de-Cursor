#!/bin/bash

echo "🚀 Iniciando E-commerce Development Environment"
echo "=============================================="

# 1. Levantar solo PostgreSQL y Redis (sin Prometheus/Grafana)
echo "📦 Iniciando base de datos..."
docker-compose -f docker-compose.dev.yml up -d

# Esperar a que las bases de datos estén listas
echo "⏳ Esperando que las bases de datos estén listas..."
sleep 5

# 2. Verificar que las bases de datos estén funcionando
echo "🔍 Verificando servicios..."
docker-compose -f docker-compose.dev.yml ps

# 3. Iniciar Backend
echo "🐍 Iniciando Backend (FastAPI)..."
cd backend
python3 main_clean.py &
BACKEND_PID=$!

# Esperar a que el backend esté listo
echo "⏳ Esperando que el backend esté listo..."
sleep 8

# 4. Verificar Backend
echo "🔍 Verificando Backend..."
curl -s http://localhost:8000/health > /dev/null && echo "✅ Backend funcionando" || echo "❌ Backend no responde"

# 5. Iniciar Frontend
echo "⚛️  Iniciando Frontend (React)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

# Esperar a que el frontend esté listo
echo "⏳ Esperando que el frontend esté listo..."
sleep 5

echo ""
echo "🎉 ¡Aplicación iniciada!"
echo "======================="
echo "🌐 Frontend: http://localhost:3000 (o 3001/3002)"
echo "🔧 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "❤️  Health:  http://localhost:8000/health"
echo ""
echo "Para detener: Ctrl+C o ejecutar ./stop-dev.sh"
echo ""

# Mantener el script corriendo
wait
