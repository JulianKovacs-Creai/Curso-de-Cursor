// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: '',
			logo: {
				light: './src/assets/logo-creai-dark.svg',
				dark: './src/assets/logo-creai-light.svg',
				replacesTitle: true,
			},
			titleDelimiter: '',
			favicon: '/favicon-creai.png',
			pagefind: false,
			sidebar: [
				{
					label: 'Introducción',
					items: [
						{ label: 'Bienvenido al Curso', link: '/' },
					],
				},
				{
					label: 'Fundamentos de Cursor AI',
					items: [
						{ label: 'Módulo 1: Introducción a Cursor AI', link: '/modulo-1/' },
						{ label: 'Módulo 2: Configuración y Workspace', link: '/modulo-2/' },
						{ label: 'Módulo 3: Workflows y Prompting Avanzado', link: '/modulo-3/' },
					],
				},
				{
					label: 'Desarrollo Full-Stack',
					items: [
						{ label: 'Módulo 4: Frontend con React', link: '/modulo-4/' },
						{ label: 'Módulo 5: Backend con FastAPI', link: '/modulo-5/' },
						{ label: 'Módulo 6: DevOps y Deployment', link: '/modulo-6/' },
					],
				},
				{
					label: 'Automatización Avanzada',
					items: [
						{ label: 'Módulo 7: Documentación y Reglas', link: '/modulo-7/' },
						{ label: 'Módulo 8: Agentes y Background Tasks', link: '/modulo-8/' },
						{ label: 'Módulo 9: UI desde Mockups', link: '/modulo-9/' },
					],
				},
				{
					label: 'Testing y Calidad',
					items: [
						{ label: 'Módulo 10: Testing Automatizado', link: '/modulo-10/' },
					],
				},
				{
					label: 'Integración y Seguridad',
					items: [
						{ label: 'Módulo 11: MCP y Integraciones', link: '/modulo-11/' },
						{ label: 'Módulo 12: Seguridad y Privacidad', link: '/modulo-12/' },
					],
				},
				{
					label: 'Recursos Adicionales',
					items: [
						{ label: 'El Proyecto E-commerce', link: '/proyecto/' },
						{ label: 'Frontend: React + TypeScript', link: '/proyecto/frontend/' },
						{ label: 'Backend: Python + FastAPI', link: '/proyecto/backend/' },
					],
				},
			],
		}),
	],
});