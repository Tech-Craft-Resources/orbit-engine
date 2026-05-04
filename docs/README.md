# Documentación del Proyecto OrbitEngine
## Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**
**Período:** Noviembre 2025 – Mayo 2026

---

## Índice de Documentos

### Planteamiento del Proyecto

| Documento | Descripción |
|---|---|
| [Alcance y MVP](./planteamiento/01-alcance-mvp.md) | Alcance del proyecto, definición del MVP, módulos y métricas de éxito |
| [Historias de Usuario y Requisitos](./planteamiento/02-requisitos.md) | Personas, 27 historias de usuario, requisitos funcionales y no funcionales |
| [Cronograma](./planteamiento/03-cronograma.md) | Planificación por sprints, hitos y distribución de tareas |
| [Arquitectura Técnica](./planteamiento/04-arquitectura-tecnica.md) | Arquitectura de alto nivel, backend, frontend, seguridad y deployment |
| [Base de Datos](./planteamiento/05-base-de-datos.md) | Diagrama ER, tablas, relaciones, estrategia de multi-tenancy |
| [SRS – Especificación de Requisitos](./planteamiento/SRS.md) | Documento formal de especificación de requisitos del sistema |
| [IA / Predicción de Demanda](./planteamiento/IA.md) | Diseño del módulo de forecasting con Prophet |

### Informe Final

| Documento | Descripción |
|---|---|
| [Preliminares](./informe-final/00-preliminares.md) | Portada, resumen, agradecimientos |
| [Capítulo 1 – Introducción](./informe-final/capitulo-1-introduccion.md) | Contexto, problema, objetivos, justificación |
| [Capítulo 2 – Marco de Referencia](./informe-final/capitulo-2-marco-referencia.md) | Estado del arte, marco teórico, tecnologías |
| [Capítulo 3 – Análisis y Diseño](./informe-final/capitulo-3-analisis-diseno.md) | Requisitos, arquitectura, diseño de BD y UI |
| [Capítulo 4 – Desarrollo](./informe-final/capitulo-4-desarrollo.md) | Implementación por módulos, decisiones técnicas |
| [Capítulo 5 – Resultados](./informe-final/capitulo-5-resultados.md) | Pruebas, métricas, validación con usuarios |
| [Capítulo 6 – Conclusiones](./informe-final/capitulo-6-conclusiones.md) | Conclusiones, trabajo futuro |
| [Anexo A – Manual de Usuario](./informe-final/anexo-a-manual-usuario.md) | Guía de uso de la plataforma |
| [Anexo B – Manual de Despliegue](./informe-final/anexo-b-manual-despliegue.md) | Instrucciones de instalación y configuración |
| [Anexo C – Documentación Técnica](./informe-final/anexo-c-documentacion-tecnica.md) | API, modelos, estructura de código |
| [Referencias](./informe-final/referencias.md) | Bibliografía y fuentes |

---

## Resumen del Proyecto

### ¿Qué es OrbitEngine?

Plataforma SaaS full-stack que permite a las pymes gestionar de forma centralizada sus procesos internos: **inventario, ventas, clientes y usuarios**, con soporte multi-tenancy y control de acceso por roles.

### Problema que Resuelve

Las pymes gestionan sus procesos con métodos manuales (hojas de cálculo, mensajería), lo que genera:
- Duplicidad y pérdida de información
- Errores frecuentes en inventarios
- Falta de trazabilidad y métricas
- Sobrecarga administrativa

### Stack Tecnológico

```
Frontend:   React 19 + TypeScript + TanStack Router/Query + Tailwind CSS + shadcn/ui
Backend:    Python 3.10 + FastAPI + SQLModel + PostgreSQL + Alembic
Auth:       JWT (PyJWT + pwdlib)
Email:      Resend + Mailcatcher (dev)
Storage:    MinIO (dev) / AWS S3 (prod)
Infra:      Docker + Docker Compose + Traefik
Testing:    pytest (backend) + Playwright (frontend)
```

---

## Estado del Proyecto (Mayo 2026)

### Módulos Completados

| Módulo | Estado |
|---|---|
| Autenticación (login, registro, recuperación de contraseña) | Completo |
| Multi-tenancy con organizaciones | Completo |
| Control de acceso basado en roles (admin, seller, viewer) | Completo |
| Gestión de inventario (productos, categorías, movimientos, ajuste de stock) | Completo |
| Gestión de ventas (registro, detalle, cancelación) | Completo |
| Gestión de clientes (CRUD, historial de compras) | Completo |
| Dashboard con KPIs y gráficos | Completo |
| Administración de usuarios | Completo |
| Configuración de cuenta y organización | Completo |
| Landing page pública | Completo |
| Tests backend (pytest) | Completo |
| Tests frontend E2E (Playwright) | Completo |

### Módulos Pendientes

| Módulo | Estado |
|---|---|
| Predicción de demanda con IA (Prophet) | Pendiente |
| Exportación a PDF/Excel | Pendiente |
| Deployment en producción | Pendiente |
| CI/CD con GitHub Actions | Pendiente |

---

## Métricas de Éxito

### Técnicas
- Tiempo de respuesta API < 500ms
- Cobertura de tests > 60%

### Producto
- 2+ pymes usando el sistema en piloto
- Satisfacción de usuario > 4/5

### Académicas
- Reducción de tiempo en tareas administrativas > 30%
- Reducción de errores en inventario > 40%

---

## Control de Versiones

| Versión | Fecha | Descripción |
|---|---|---|
| 1.0 | Nov 2025 | Documentación inicial de planteamiento |
| 2.0 | Ene 2026 | Inicio del informe final |
| 3.0 | May 2026 | Actualización al estado real del proyecto |

---

**Última actualización:** Mayo 2026
