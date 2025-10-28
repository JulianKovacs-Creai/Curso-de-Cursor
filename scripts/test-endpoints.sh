#!/bin/bash

# Script para probar todos los endpoints del e-commerce

echo "🧪 Probando Endpoints del E-commerce"
echo "===================================="
echo ""

# Función para probar endpoint
test_endpoint() {
    local name="$1"
    local method="$2"
    local url="$3"
    local data="$4"
    local expected_status="$5"
    
    echo -n "Testing $name: "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" "$url")
        status_code="${response: -3}"
        body="${response%???}"
    else
        response=$(curl -s -w "%{http_code}" -X "$method" -H "Content-Type: application/json" -d "$data" "$url")
        status_code="${response: -3}"
        body="${response%???}"
    fi
    
    if [ "$status_code" = "$expected_status" ]; then
        echo "✅ OK ($status_code)"
        if [ "$body" != "" ]; then
            echo "   Response: $(echo "$body" | head -c 100)..."
        fi
    else
        echo "❌ FAIL (Expected: $expected_status, Got: $status_code)"
        if [ "$body" != "" ]; then
            echo "   Response: $body"
        fi
    fi
    echo ""
}

echo "🔍 Probando Endpoints Básicos:"
echo "=============================="

# Probar endpoints básicos
test_endpoint "Health Check" "GET" "http://localhost:8000/health" "" "200"
test_endpoint "API Root" "GET" "http://localhost:8000/" "" "200"
test_endpoint "API Docs" "GET" "http://localhost:8000/docs" "" "200"
test_endpoint "Frontend" "GET" "http://localhost:3000/" "" "200"

echo "🔐 Probando Endpoints de Autenticación:"
echo "======================================"

# Probar registro
test_endpoint "User Registration" "POST" "http://localhost:8000/api/v1/auth/register" '{"email":"test@example.com","password":"TestPassword123!","first_name":"Test","last_name":"User"}' "201"

# Probar login
echo "🔑 Obteniendo token de autenticación..."
login_response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPassword123!"}')

if echo "$login_response" | grep -q "access_token"; then
    echo "✅ Token obtenido exitosamente"
else
    echo "❌ No se pudo obtener token"
fi

echo "🛍️  Probando Endpoints de Productos:"
echo "==================================="

# Probar endpoints de productos
test_endpoint "Get Products" "GET" "http://localhost:8000/api/v1/products/" "" "200"

echo "🎉 Pruebas completadas!"
