#!/bin/bash

# Script para iniciar el frontend del e-commerce

echo "🎨 Iniciando Frontend E-commerce..."

# Navegar al directorio del frontend
cd ../frontend

# Verificar si node_modules existe
if [ ! -d "node_modules" ]; then
    echo "📦 Instalando dependencias..."
    npm install
fi

# Ejecutar el frontend
echo "🌐 Iniciando servidor de desarrollo en http://localhost:3000"
npm run dev
