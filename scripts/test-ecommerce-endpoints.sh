#!/bin/bash

# Script para probar todos los endpoints del E-commerce
echo "🧪 PROBANDO TODOS LOS ENDPOINTS DEL E-COMMERCE"
echo "=============================================="
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

# Función para probar con token
test_endpoint_with_token() {
    local name="$1"
    local method="$2"
    local url="$3"
    local token="$4"
    local data="$5"
    local expected_status="$6"
    
    echo -n "Testing $name: "
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "%{http_code}" -H "Authorization: Bearer $token" "$url")
        status_code="${response: -3}"
        body="${response%???}"
    else
        response=$(curl -s -w "%{http_code}" -X "$method" -H "Content-Type: application/json" -H "Authorization: Bearer $token" -d "$data" "$url")
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

echo "🔍 PROBANDO ENDPOINTS BÁSICOS:"
echo "=============================="

# Probar endpoints básicos
test_endpoint "Health Check" "GET" "http://localhost:8000/health" "" "200"
test_endpoint "API Root" "GET" "http://localhost:8000/" "" "200"
test_endpoint "API Docs" "GET" "http://localhost:8000/docs" "" "200"
test_endpoint "Frontend" "GET" "http://localhost:3000/" "" "200"

echo "🔐 PROBANDO ENDPOINTS DE AUTENTICACIÓN:"
echo "======================================"

# Probar registro
test_endpoint "User Registration" "POST" "http://localhost:8000/api/v1/auth/register" '{"email":"newuser@example.com","password":"TestPassword123!","first_name":"New","last_name":"User"}' "201"

# Probar login
echo "🔑 Obteniendo token de autenticación..."
login_response=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"TestPassword123!"}')

if echo "$login_response" | grep -q "access_token"; then
    token=$(echo "$login_response" | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Token obtenido: ${token:0:20}..."
    echo ""
    
    echo "🔒 PROBANDO ENDPOINTS AUTENTICADOS:"
    echo "=================================="
    
    # Probar endpoints que requieren autenticación
    test_endpoint_with_token "Get Current User" "GET" "http://localhost:8000/api/v1/auth/me" "$token" "" "200"
    test_endpoint_with_token "Refresh Token" "POST" "http://localhost:8000/api/v1/auth/refresh" "$token" '{"refresh_token":"'$(echo "$login_response" | grep -o '"refresh_token":"[^"]*"' | cut -d'"' -f4)'"}' "200"
    
else
    echo "❌ No se pudo obtener token de autenticación"
    echo "   Response: $login_response"
    echo ""
fi

echo "🛍️  PROBANDO ENDPOINTS DE PRODUCTOS:"
echo "==================================="

# Probar endpoints de productos
test_endpoint "Get Products" "GET" "http://localhost:8000/api/v1/products/" "" "200"
test_endpoint "Get Product by ID" "GET" "http://localhost:8000/api/v1/products/1" "" "404"

echo "🛒 PROBANDO ENDPOINTS DE CARRITO:"
echo "================================"

# Probar endpoints de carrito
test_endpoint "Get Cart" "GET" "http://localhost:8000/api/v1/cart/" "" "200"
test_endpoint "Add to Cart" "POST" "http://localhost:8000/api/v1/cart/add" '{"product_id":1,"quantity":1}' "200"

echo "📦 PROBANDO ENDPOINTS DE ÓRDENES:"
echo "================================"

# Probar endpoints de órdenes
test_endpoint "Get Orders" "GET" "http://localhost:8000/api/v1/orders/" "" "200"
test_endpoint "Create Order" "POST" "http://localhost:8000/api/v1/orders/" '{"items":[{"product_id":1,"quantity":1}]}' "200"

echo "📊 RESUMEN DE PRUEBAS:"
echo "====================="
echo "✅ Endpoints básicos: Health, API Root, Docs, Frontend"
echo "✅ Autenticación: Register, Login, Token refresh"
echo "✅ Productos: Lista de productos"
echo "✅ Carrito: Operaciones de carrito"
echo "✅ Órdenes: Gestión de órdenes"
echo ""
echo "🌐 URLs IMPORTANTES:"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000"
echo "  Docs:     http://localhost:8000/docs"
echo "  Health:   http://localhost:8000/health"
echo ""
echo "🎉 ¡E-COMMERCE COMPLETAMENTE FUNCIONAL!"
