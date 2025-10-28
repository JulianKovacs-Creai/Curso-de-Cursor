# 🛒 E-Commerce Clean Architecture

Un proyecto de e-commerce completo implementado con Clean Architecture, FastAPI, React y TypeScript.

## 🚀 Inicio Rápido

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- Docker (opcional)

### Instalación

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd cursor-project-main
```

2. **Configurar Backend**
```bash
cd backend
pip install -r requirements.txt
export DATABASE_URL="./ecommerce_clean.db"
python main_clean.py
```

3. **Configurar Frontend**
```bash
cd frontend
npm install
npm run dev
```

### Acceso
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs

## 📁 Estructura del Proyecto

```
cursor-project-main/
├── backend/           # API FastAPI con Clean Architecture
├── frontend/          # Aplicación React con TypeScript
├── docs/             # Documentación del proyecto
├── scripts/          # Scripts de utilidad
├── monitoring/       # Configuración de monitoreo
├── nginx/            # Configuración de Nginx
├── terraform/        # Infraestructura como código
└── src/             # Código fuente compartido
```

## 🔧 Scripts Disponibles

Ver `scripts/` para scripts de utilidad:
- `start-backend.sh` - Iniciar solo el backend
- `start-frontend.sh` - Iniciar solo el frontend
- `start-ecommerce.sh` - Iniciar todo el e-commerce
- `test-endpoints.sh` - Probar todos los endpoints

## 📚 Documentación

Ver `docs/` para documentación detallada.

## 🏗️ Arquitectura

- **Backend**: FastAPI con Clean Architecture
- **Frontend**: React con TypeScript y Vite
- **Base de datos**: SQLite
- **Autenticación**: JWT
- **Compliance**: GDPR y SOX

## 🚀 Despliegue

Ver `docs/DEPLOYMENT.md` para instrucciones de despliegue.

## 📄 Licencia

MIT License
