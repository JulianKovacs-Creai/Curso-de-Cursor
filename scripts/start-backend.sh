#!/bin/bash

# Script para iniciar el backend del e-commerce

echo "🚀 Iniciando Backend E-commerce..."

# Navegar al directorio del backend
cd /home/juliankovacs/curso-de-cursor/cursor-project-main/backend

# Configurar variables de entorno
export DATABASE_URL="sqlite:///./ecommerce_clean.db"
export SECRET_KEY="your-secret-key-here"
export JWT_SECRET_KEY="your-jwt-secret-key"
export ENVIRONMENT="development"
export DEBUG="true"

echo "✅ Variables de entorno configuradas"
echo "📊 Database URL: $DATABASE_URL"
echo "🔧 Environment: $ENVIRONMENT"

# Ejecutar el backend
echo "🌐 Iniciando servidor en http://localhost:8000"
python3 main_clean.py
