#!/bin/bash

# Script para limpiar el proyecto e-commerce

echo "🧹 LIMPIEZA DEL PROYECTO E-COMMERCE"
echo "==================================="
echo ""

# Función para confirmar eliminación
confirm() {
    read -p "¿Estás seguro de que quieres eliminar $1? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

echo "📋 Archivos que se pueden eliminar:"
echo "1. Archivos Zone.Identifier (Windows)"
echo "2. Archivos temporales (prometheus.yml, ecommerce_clean.db)"
echo "3. node_modules y package-lock.json"
echo "4. Archivos de documentación de desarrollo"
echo ""

# Eliminar archivos Zone.Identifier
if confirm "archivos Zone.Identifier"; then
    echo "🗑️ Eliminando archivos Zone.Identifier..."
    find . -name "*.Zone.Identifier" -delete
    echo "✅ Archivos Zone.Identifier eliminados"
fi

# Eliminar archivos temporales
if confirm "archivos temporales"; then
    echo "🗑️ Eliminando archivos temporales..."
    rm -f prometheus.yml ecommerce_clean.db
    echo "✅ Archivos temporales eliminados"
fi

# Eliminar node_modules
if confirm "node_modules y package-lock.json"; then
    echo "🗑️ Eliminando node_modules y package-lock.json..."
    rm -rf node_modules package-lock.json
    echo "✅ node_modules y package-lock.json eliminados"
fi

# Eliminar documentación de desarrollo
if confirm "documentación de desarrollo"; then
    echo "🗑️ Eliminando documentación de desarrollo..."
    find . -name "*SUMMARY*.md" -delete
    find . -name "*IMPLEMENTATION*.md" -delete
    find . -name "*ANALYSIS*.md" -delete
    find . -name "*STATUS*.md" -delete
    find . -name "*FIXES*.md" -delete
    echo "✅ Documentación de desarrollo eliminada"
fi

echo ""
echo "🎉 Limpieza completada!"
echo "El proyecto está ahora optimizado."
