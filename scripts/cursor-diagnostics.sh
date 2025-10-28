#!/bin/bash

# Cursor Diagnostics Main Script
# Script principal para comandos de diagnóstico del proyecto e-commerce

echo "🔧 CURSOR DIAGNOSTICS"
echo "====================="
echo ""

# Verificar si estamos en el directorio correcto
if [ ! -f "package.json" ] && [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: No se detectó un proyecto válido en el directorio actual"
    echo "   Asegúrate de estar en el directorio raíz del proyecto e-commerce"
    exit 1
fi

echo "✅ Proyecto e-commerce detectado"
echo ""

# Función para mostrar ayuda
show_help() {
    echo "Uso: cursor [comando] [opciones]"
    echo ""
    echo "Comandos disponibles:"
    echo "  security status                    - Verificar configuración de seguridad"
    echo "  compliance check [--regulations]   - Validar cumplimiento normativo"
    echo "  audit report [--period]            - Generar reporte de auditoría"
    echo "  security scan [--full]             - Test de vulnerabilidades"
    echo "  help                               - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  cursor security status"
    echo "  cursor compliance check --regulations gdpr,sox,hipaa"
    echo "  cursor audit report --period 30days"
    echo "  cursor security scan --full"
    echo ""
}

# Función para ejecutar security status
run_security_status() {
    echo "🔒 Verificando configuración de seguridad..."
    echo ""
    
    # Verificar archivos de configuración de seguridad
    security_files=(
        "nginx/nginx.conf"
        "backend/src/shared/config.py"
        "frontend/src/shared/types/index.ts"
        "src/compliance/gdpr.ts"
        "src/compliance/sox.ts"
    )
    
    security_score=0
    total_files=${#security_files[@]}
    
    for file in "${security_files[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file - Encontrado"
            ((security_score++))
        else
            echo "❌ $file - No encontrado"
        fi
    done
    
    echo ""
    echo "📊 Puntuación de configuración: $security_score/$total_files"
    
    # Verificar dependencias de seguridad
    echo ""
    echo "🔍 DEPENDENCIAS DE SEGURIDAD"
    echo "----------------------------"
    
    if [ -f "frontend/package.json" ]; then
        echo "Frontend Dependencies:"
        if grep -q "eslint" frontend/package.json; then
            echo "✅ ESLint - Configurado"
        else
            echo "❌ ESLint - No configurado"
        fi
        
        if grep -q "typescript" frontend/package.json; then
            echo "✅ TypeScript - Configurado"
        else
            echo "❌ TypeScript - No configurado"
        fi
    fi
    
    if [ -f "backend/requirements.txt" ]; then
        echo ""
        echo "Backend Dependencies:"
        if grep -q "bcrypt" backend/requirements.txt; then
            echo "✅ BCrypt - Configurado"
        else
            echo "❌ BCrypt - No configurado"
        fi
        
        if grep -q "pyjwt" backend/requirements.txt; then
            echo "✅ PyJWT - Configurado"
        else
            echo "❌ PyJWT - No configurado"
        fi
    fi
    
    # Verificar configuración de Docker
    echo ""
    echo "🐳 CONFIGURACIÓN DOCKER"
    echo "----------------------"
    
    if [ -f "docker-compose.yml" ]; then
        echo "✅ Docker Compose - Configurado"
        
        if grep -q "user:" docker-compose.yml; then
            echo "✅ Usuarios no-root - Configurado"
        else
            echo "⚠️  Usuarios no-root - No detectado"
        fi
        
        if grep -q "healthcheck:" docker-compose.yml; then
            echo "✅ Health Checks - Configurado"
        else
            echo "⚠️  Health Checks - No detectado"
        fi
    else
        echo "❌ Docker Compose - No encontrado"
    fi
    
    # Resumen final
    echo ""
    echo "📊 RESUMEN DE SEGURIDAD"
    echo "======================"
    
    if [ $security_score -eq $total_files ]; then
        echo "🟢 Estado: EXCELENTE - Todas las configuraciones de seguridad están implementadas"
    elif [ $security_score -ge $((total_files * 80 / 100)) ]; then
        echo "🟡 Estado: BUENO - La mayoría de configuraciones están implementadas"
    elif [ $security_score -ge $((total_files * 60 / 100)) ]; then
        echo "🟠 Estado: REGULAR - Algunas configuraciones faltan"
    else
        echo "🔴 Estado: CRÍTICO - Muchas configuraciones de seguridad faltan"
    fi
}

# Función para ejecutar compliance check
run_compliance_check() {
    local regulations=("gdpr" "sox" "hipaa")
    
    # Parsear argumentos
    if [ $# -gt 0 ]; then
        if [[ "$*" == *"--regulations"* ]]; then
            regs=$(echo "$*" | sed 's/.*--regulations[[:space:]]*//' | tr ',' ' ')
            regulations=($regs)
        fi
    fi
    
    echo "📋 Verificando cumplimiento normativo: ${regulations[*]}"
    echo ""
    
    for reg in "${regulations[@]}"; do
        echo "🔍 Verificando cumplimiento: $reg"
        echo "----------------------------------------"
        
        case $reg in
            "gdpr")
                gdpr_files=(
                    "src/compliance/gdpr.ts"
                    "src/api/gdpr-endpoints.ts"
                    "src/validation/gdpr-validation.ts"
                    "src/audit/audit-logger.ts"
                )
                
                gdpr_score=0
                total_gdpr=${#gdpr_files[@]}
                
                for file in "${gdpr_files[@]}"; do
                    if [ -f "$file" ]; then
                        echo "✅ $file - Implementado"
                        ((gdpr_score++))
                    else
                        echo "❌ $file - No implementado"
                    fi
                done
                
                echo "📊 Puntuación GDPR: $gdpr_score/$total_gdpr"
                ;;
                
            "sox")
                sox_files=(
                    "src/compliance/sox.ts"
                )
                
                sox_score=0
                total_sox=${#sox_files[@]}
                
                for file in "${sox_files[@]}"; do
                    if [ -f "$file" ]; then
                        echo "✅ $file - Implementado"
                        ((sox_score++))
                    else
                        echo "❌ $file - No implementado"
                    fi
                done
                
                echo "📊 Puntuación SOX: $sox_score/$total_sox"
                ;;
                
            "hipaa")
                echo "⚠️  HIPAA - No implementado (no requerido para e-commerce)"
                ;;
        esac
        echo ""
    done
}

# Función para ejecutar audit report
run_audit_report() {
    local period="30days"
    
    # Parsear argumentos
    if [ $# -gt 0 ]; then
        if [[ "$*" == *"--period"* ]]; then
            period=$(echo "$*" | sed 's/.*--period[[:space:]]*//')
        fi
    fi
    
    echo "📊 Generando reporte de auditoría (período: $period)..."
    echo ""
    
    # Generar información del reporte
    local report_id="AUDIT-$(date +%Y%m%d-%H%M%S)"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "🆔 ID del Reporte: $report_id"
    echo "🕐 Generado: $timestamp"
    echo "📅 Período: $period"
    echo ""
    
    # Auditoría de archivos de compliance
    echo "📋 AUDITORÍA DE COMPLIANCE"
    echo "-------------------------"
    
    compliance_files=(
        "src/compliance/gdpr.ts"
        "src/compliance/sox.ts"
        "src/api/gdpr-endpoints.ts"
        "src/validation/gdpr-validation.ts"
        "src/audit/audit-logger.ts"
        "src/compliance/compliance-roi-calculator.ts"
    )
    
    compliance_count=0
    total_compliance=${#compliance_files[@]}
    
    for file in "${compliance_files[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file - Presente"
            ((compliance_count++))
        else
            echo "❌ $file - Ausente"
        fi
    done
    
    echo ""
    echo "📊 Archivos de compliance: $compliance_count/$total_compliance"
    
    # Auditoría de documentación
    echo ""
    echo "📚 AUDITORÍA DE DOCUMENTACIÓN"
    echo "----------------------------"
    
    doc_files=(
        "README.md"
        "COMPLIANCE_ANALYSIS.md"
        "COMPLIANCE_STATUS_UPDATE.md"
        "GDPR_ENDPOINTS_FIXES_SUMMARY.md"
        "COMPLIANCE_ROI_CALCULATOR_SUMMARY.md"
        "DOCKER_SETUP.md"
        "DOCKER_CONTAINERIZATION_SUMMARY.md"
    )
    
    doc_count=0
    total_docs=${#doc_files[@]}
    
    for file in "${doc_files[@]}"; do
        if [ -f "$file" ]; then
            echo "✅ $file - Presente"
            ((doc_count++))
        else
            echo "❌ $file - Ausente"
        fi
    done
    
    echo ""
    echo "📊 Documentación: $doc_count/$total_docs"
    
    # Resumen del reporte
    echo ""
    echo "📊 RESUMEN DEL REPORTE"
    echo "====================="
    
    total_files=$((compliance_count + doc_count))
    max_files=$((total_compliance + total_docs))
    
    if [ $max_files -gt 0 ]; then
        percentage=$((total_files * 100 / max_files))
        echo "📈 Puntuación general: $percentage%"
        
        if [ $percentage -ge 90 ]; then
            echo "🟢 Estado: EXCELENTE - Proyecto bien documentado y configurado"
        elif [ $percentage -ge 70 ]; then
            echo "🟡 Estado: BUENO - Proyecto bien estructurado con algunas mejoras pendientes"
        elif [ $percentage -ge 50 ]; then
            echo "🟠 Estado: REGULAR - Proyecto funcional pero necesita más documentación"
        else
            echo "🔴 Estado: CRÍTICO - Proyecto necesita mejoras significativas"
        fi
    fi
    
    echo ""
    echo "📄 Reporte guardado como: audit-report-$report_id.txt"
    
    # Guardar reporte en archivo
    {
        echo "CURSOR AUDIT REPORT"
        echo "=================="
        echo "ID: $report_id"
        echo "Generado: $timestamp"
        echo "Período: $period"
        echo ""
        echo "RESUMEN:"
        echo "- Archivos de compliance: $compliance_count/$total_compliance"
        echo "- Documentación: $doc_count/$total_docs"
        echo "- Puntuación general: $percentage%"
    } > "audit-report-$report_id.txt"
}

# Función para ejecutar security scan
run_security_scan() {
    local full_scan=false
    
    # Parsear argumentos
    if [ $# -gt 0 ]; then
        if [[ "$*" == *"--full"* ]]; then
            full_scan=true
        fi
    fi
    
    echo "🔍 Ejecutando scan de seguridad (modo: $([ "$full_scan" = true ] && echo "COMPLETO" || echo "RÁPIDO"))..."
    echo ""
    
    local scan_id="SECURITY-SCAN-$(date +%Y%m%d-%H%M%S)"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "🆔 ID del Scan: $scan_id"
    echo "🕐 Iniciado: $timestamp"
    echo ""
    
    # Escaneo de dependencias
    echo "📦 ESCANEO DE DEPENDENCIAS"
    echo "-------------------------"
    
    if [ -f "frontend/package.json" ]; then
        echo "Frontend Dependencies:"
        cd frontend
        
        if command -v npm &> /dev/null; then
            echo "🔍 Ejecutando npm audit..."
            if npm audit --audit-level=moderate 2>/dev/null; then
                echo "✅ Sin vulnerabilidades críticas en dependencias frontend"
            else
                echo "⚠️  Vulnerabilidades detectadas en dependencias frontend"
            fi
        else
            echo "❌ npm no disponible"
        fi
        
        cd ..
    fi
    
    if [ -f "backend/requirements.txt" ]; then
        echo ""
        echo "Backend Dependencies:"
        cd backend
        
        if command -v pip &> /dev/null; then
            echo "🔍 Verificando dependencias Python..."
            if command -v safety &> /dev/null; then
                if safety check 2>/dev/null; then
                    echo "✅ Sin vulnerabilidades conocidas en dependencias Python"
                else
                    echo "⚠️  Vulnerabilidades detectadas en dependencias Python"
                fi
            else
                echo "⚠️  safety no instalado"
            fi
        else
            echo "❌ pip no disponible"
        fi
        
        cd ..
    fi
    
    # Escaneo de configuración
    echo ""
    echo "🛡️  ESCANEO DE CONFIGURACIÓN"
    echo "---------------------------"
    
    if [ -f "nginx/nginx.conf" ]; then
        echo "Nginx Configuration:"
        
        security_headers=(
            "X-Frame-Options"
            "X-Content-Type-Options"
            "X-XSS-Protection"
            "Content-Security-Policy"
        )
        
        for header in "${security_headers[@]}"; do
            if grep -q "$header" nginx/nginx.conf; then
                echo "✅ $header - Configurado"
            else
                echo "❌ $header - No configurado"
            fi
        done
    else
        echo "❌ nginx/nginx.conf - No encontrado"
    fi
    
    # Resumen del scan
    echo ""
    echo "📊 RESUMEN DEL SCAN"
    echo "=================="
    
    echo "🆔 ID del Scan: $scan_id"
    echo "🕐 Completado: $(date '+%Y-%m-%d %H:%M:%S')"
    
    echo ""
    echo "📄 Scan guardado como: security-scan-$scan_id.txt"
    
    # Guardar scan en archivo
    {
        echo "CURSOR SECURITY SCAN"
        echo "==================="
        echo "ID: $scan_id"
        echo "Completado: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Modo: $([ "$full_scan" = true ] && echo "COMPLETO" || echo "RÁPIDO")"
    } > "security-scan-$scan_id.txt"
}

# Procesar argumentos
case "$1" in
    "security")
        case "$2" in
            "status")
                run_security_status
                ;;
            "scan")
                shift 2
                run_security_scan "$@"
                ;;
            *)
                echo "❌ Comando de seguridad no reconocido: $2"
                echo "Comandos disponibles: status, scan"
                exit 1
                ;;
        esac
        ;;
    "compliance")
        case "$2" in
            "check")
                shift 2
                run_compliance_check "$@"
                ;;
            *)
                echo "❌ Comando de compliance no reconocido: $2"
                echo "Comandos disponibles: check"
                exit 1
                ;;
        esac
        ;;
    "audit")
        case "$2" in
            "report")
                shift 2
                run_audit_report "$@"
                ;;
            *)
                echo "❌ Comando de audit no reconocido: $2"
                echo "Comandos disponibles: report"
                exit 1
                ;;
        esac
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    "")
        echo "❌ No se especificó ningún comando"
        echo ""
        show_help
        exit 1
        ;;
    *)
        echo "❌ Comando no reconocido: $1"
        echo ""
        show_help
        exit 1
        ;;
esac

echo ""
echo "✅ Comando completado"

exit 0
