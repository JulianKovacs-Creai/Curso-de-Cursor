# Ecommerce Frontend

Una aplicación web moderna de ecommerce construida con React, TypeScript, Vite y Ant Design.

## Características

- ⚡️ **Vite** - Build tool rápido y moderno
- ⚛️ **React 18** - Biblioteca de UI
- 🔷 **TypeScript** - Tipado estático
- 🎨 **Ant Design** - Componentes de UI profesionales
- 🛣️ **React Router** - Enrutamiento del lado del cliente
- 📡 **Axios** - Cliente HTTP para APIs
- 📱 **Responsive** - Diseño adaptable a diferentes dispositivos

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── pages/           # Páginas de la aplicación
│   ├── shared/          # Componentes y utilidades compartidas
│   │   ├── components/  # Componentes reutilizables
│   │   ├── services/    # Servicios y APIs
│   │   └── types/       # Definiciones de tipos TypeScript
│   ├── App.tsx          # Componente principal
│   ├── main.tsx         # Punto de entrada
│   └── index.css        # Estilos globales
├── package.json         # Dependencias y scripts
├── vite.config.ts       # Configuración de Vite
├── tsconfig.json        # Configuración de TypeScript
└── index.html           # Template HTML
```

## Instalación

1. Instalar dependencias:
```bash
pnpm install
```

2. Ejecutar en modo desarrollo:
```bash
pnpm dev
```

3. Construir para producción:
```bash
pnpm build
```

## Scripts Disponibles

- `pnpm dev` - Inicia el servidor de desarrollo
- `pnpm build` - Construye la aplicación para producción
- `pnpm preview` - Previsualiza la build de producción
- `pnpm lint` - Ejecuta el linter

## Tecnologías Utilizadas

- **React 18** - Biblioteca de UI
- **TypeScript** - Tipado estático
- **Vite** - Build tool
- **Ant Design** - Componentes de UI
- **React Router** - Enrutamiento
- **Axios** - Cliente HTTP
- **ESLint** - Linting de código

## Configuración de Path Aliases

El proyecto incluye path aliases configurados para facilitar las importaciones:

- `@/*` → `./src/*`
- `@components/*` → `./src/shared/components/*`
- `@types/*` → `./src/shared/types/*`
- `@services/*` → `./src/shared/services/*`
- `@pages/*` → `./src/pages/*`

## Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
VITE_API_BASE_URL=http://localhost:3000/api
```

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT.
