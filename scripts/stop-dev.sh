#!/bin/bash

echo "🛑 Deteniendo E-commerce Development Environment"
echo "=============================================="

# Detener procesos
echo "🔄 Deteniendo procesos..."
pkill -f "python3 main_clean.py"
pkill -f "npm run dev"

# Detener Docker (solo postgres y redis)
echo "🐳 Deteniendo contenedores Docker..."
docker-compose -f docker-compose.dev.yml down

echo "✅ Todo detenido correctamente"
