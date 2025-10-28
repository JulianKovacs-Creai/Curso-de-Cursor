#!/bin/bash

# Script completo para levantar el E-commerce
echo "🚀 INICIANDO E-COMMERCE COMPLETO"
echo "================================"
echo ""

# Función para mostrar el estado de los servicios
show_status() {
    echo "📊 ESTADO DE SERVICIOS:"
    echo "----------------------"
    echo "Backend:  http://localhost:8000"
    echo "Frontend: http://localhost:3000"
    echo "API Docs: http://localhost:8000/docs"
    echo "Health:   http://localhost:8000/health"
    echo ""
}

# Función para probar endpoints
test_endpoints() {
    echo "🧪 PROBANDO ENDPOINTS:"
    echo "--------------------"
    
    # Health check
    echo -n "Health Check: "
    if curl -s http://localhost:8000/health > /dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAIL"
    fi
    
    # API Root
    echo -n "API Root: "
    if curl -s http://localhost:8000/ > /dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAIL"
    fi
    
    # Frontend
    echo -n "Frontend: "
    if curl -s http://localhost:3000/ > /dev/null; then
        echo "✅ OK"
    else
        echo "❌ FAIL"
    fi
    
    echo ""
}

# Función para mostrar URLs importantes
show_urls() {
    echo "🌐 URLs IMPORTANTES:"
    echo "-------------------"
    echo "🏠 Frontend:     http://localhost:3000"
    echo "🔧 Backend API:  http://localhost:8000"
    echo "📚 API Docs:     http://localhost:8000/docs"
    echo "❤️  Health:      http://localhost:8000/health"
    echo "🔐 Auth:         http://localhost:8000/api/auth/"
    echo "🛍️  Products:     http://localhost:8000/api/products/"
    echo "🛒 Cart:         http://localhost:8000/api/cart/"
    echo "📦 Orders:       http://localhost:8000/api/orders/"
    echo ""
}

# Función para mostrar comandos útiles
show_commands() {
    echo "🛠️  COMANDOS ÚTILES:"
    echo "-------------------"
    echo "Ver logs backend:    docker logs ecommerce-backend -f"
    echo "Ver logs frontend:   docker logs ecommerce-frontend -f"
    echo "Ver logs nginx:      docker logs ecommerce-nginx -f"
    echo "Ver todos los logs:  docker-compose logs -f"
    echo "Detener servicios:   docker-compose down"
    echo "Reiniciar servicios: docker-compose restart"
    echo ""
}

# Función para mostrar endpoints de prueba
show_test_endpoints() {
    echo "🧪 ENDPOINTS DE PRUEBA:"
    echo "----------------------"
    echo ""
    echo "1. REGISTRO DE USUARIO:"
    echo "curl -X POST http://localhost:8000/api/auth/register \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"email\":\"test@example.com\",\"password\":\"test123\",\"first_name\":\"Test\",\"last_name\":\"User\"}'"
    echo ""
    echo "2. LOGIN DE USUARIO:"
    echo "curl -X POST http://localhost:8000/api/auth/login \\"
    echo "  -H 'Content-Type: application/json' \\"
    echo "  -d '{\"email\":\"test@example.com\",\"password\":\"test123\"}'"
    echo ""
    echo "3. OBTENER PRODUCTOS:"
    echo "curl http://localhost:8000/api/products/"
    echo ""
    echo "4. HEALTH CHECK:"
    echo "curl http://localhost:8000/health"
    echo ""
}

# Función principal
main() {
    echo "🔧 Configurando variables de entorno..."
    export DATABASE_URL="./ecommerce_clean.db"
    export SECRET_KEY="your-secret-key-here"
    export JWT_SECRET_KEY="your-jwt-secret-key"
    export ENVIRONMENT="development"
    export DEBUG="true"
    
    echo "✅ Variables configuradas"
    echo ""
    
    # Mostrar URLs importantes
    show_urls
    
    # Mostrar comandos útiles
    show_commands
    
    # Mostrar endpoints de prueba
    show_test_endpoints
    
    echo "🚀 INICIANDO SERVICIOS..."
    echo "========================="
    echo ""
    
    # Iniciar backend
    echo "🔧 Iniciando Backend..."
    cd /home/juliankovacs/curso-de-cursor/cursor-project-main/backend
    python3 main_clean.py &
    BACKEND_PID=$!
    echo "✅ Backend iniciado (PID: $BACKEND_PID)"
    
    # Esperar un momento para que el backend se inicie
    sleep 5
    
    # Iniciar frontend
    echo "🎨 Iniciando Frontend..."
    cd /home/juliankovacs/curso-de-cursor/cursor-project-main/frontend
    npm run dev &
    FRONTEND_PID=$!
    echo "✅ Frontend iniciado (PID: $FRONTEND_PID)"
    
    # Esperar un momento para que el frontend se inicie
    sleep 8
    
    # Mostrar estado
    show_status
    
    # Probar endpoints
    test_endpoints
    
    echo "🎉 E-COMMERCE INICIADO EXITOSAMENTE!"
    echo "===================================="
    echo ""
    echo "💡 Para detener los servicios, presiona Ctrl+C"
    echo "💡 Para ver logs en tiempo real, ejecuta: docker-compose logs -f"
    echo ""
    
    # Mantener el script ejecutándose
    echo "⏳ Servicios ejecutándose... (Presiona Ctrl+C para detener)"
    wait
}

# Ejecutar función principal
main
