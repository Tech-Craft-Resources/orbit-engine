# OrbitEngine

> Plataforma SaaS para la gestión integral de procesos internos en pequeñas y medianas empresas

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-19+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.114+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-336791.svg)](https://www.postgresql.org/)

---

## Descripción

OrbitEngine es una plataforma SaaS full-stack diseñada para digitalizar y centralizar los procesos internos de pequeñas y medianas empresas. Permite gestionar inventario, ventas, clientes y usuarios desde un único panel, con soporte multi-tenancy mediante organizaciones y control de acceso basado en roles.

**Estado del Proyecto:** En desarrollo activo (Proyecto de Grado)
**Período:** Noviembre 2025 – Mayo 2026

---

## Funcionalidades Implementadas

- **Autenticación y Roles:** JWT con control de acceso por roles (admin, seller, viewer). Registro, login, recuperación de contraseña.
- **Multi-tenancy:** Soporte para múltiples organizaciones con aislamiento completo de datos.
- **Gestión de Inventario:** CRUD de productos y categorías, ajustes de stock, historial de movimientos.
- **Gestión de Ventas:** Registro de ventas con líneas de detalle, vista de detalle, cancelación.
- **Gestión de Clientes:** CRUD de clientes, historial de compras por cliente.
- **Administración de Usuarios:** Creación, edición y eliminación de usuarios por parte de admins.
- **Dashboard:** KPIs en tiempo real con gráficos (Recharts).
- **Configuración:** Perfil de usuario, cambio de contraseña, configuración de organización, eliminación de cuenta.
- **Landing Page:** Página pública con hero, características, beneficios y estadísticas.
- **Modo oscuro/claro:** Tema persistente por usuario.

---

## Tech Stack

### Frontend
- **Framework:** React 19 con TypeScript 5
- **Build Tool:** Vite 7
- **Routing:** TanStack Router v1 (file-based)
- **Server State:** TanStack Query v5
- **Tablas:** TanStack Table v8
- **Formularios:** React Hook Form 7 + Zod 4
- **Styling:** Tailwind CSS 4
- **Componentes:** shadcn/ui (Radix UI)
- **Gráficos:** Recharts
- **Linting:** Biome
- **Testing E2E:** Playwright

### Backend
- **Framework:** FastAPI 0.114+ (Python 3.10+)
- **ORM:** SQLModel (SQLAlchemy 2 + Pydantic 2)
- **Migraciones:** Alembic
- **Auth:** PyJWT + pwdlib (argon2/bcrypt)
- **Email:** Resend + Jinja2 (templates)
- **Monitoreo:** Sentry
- **Linting:** ruff + mypy (strict)
- **Testing:** pytest + coverage

### Base de Datos y Almacenamiento
- **Base de datos:** PostgreSQL 15+
- **Almacenamiento de archivos:** MinIO (desarrollo) / AWS S3 (producción)

### Infraestructura
- **Contenedores:** Docker + Docker Compose
- **Email (desarrollo):** Mailcatcher
- **Proxy:** Traefik

---

## Estructura del Proyecto

```
orbit-engine/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/         # Un archivo por dominio
│   │   │   │   ├── login.py
│   │   │   │   ├── users.py
│   │   │   │   ├── organizations.py
│   │   │   │   ├── roles.py
│   │   │   │   ├── products.py
│   │   │   │   ├── categories.py
│   │   │   │   ├── customers.py
│   │   │   │   ├── sales.py
│   │   │   │   ├── inventory_movements.py
│   │   │   │   ├── dashboard.py
│   │   │   │   └── utils.py
│   │   │   └── deps.py         # Dependencias inyectadas (CurrentUser, SessionDep…)
│   │   ├── core/               # Config, seguridad, base de datos
│   │   ├── alembic/            # Migraciones
│   │   ├── models.py           # Modelos SQLModel + schemas Pydantic
│   │   └── crud.py             # Operaciones CRUD
│   ├── tests/                  # Pruebas pytest
│   └── scripts/                # test.sh, lint.sh, format.sh
│
├── frontend/                   # React frontend
│   ├── src/
│   │   ├── client/             # Cliente API auto-generado (NO EDITAR)
│   │   ├── components/
│   │   │   ├── Admin/          # Gestión de usuarios (admin)
│   │   │   ├── Common/         # Componentes compartidos
│   │   │   ├── Customers/      # Módulo clientes
│   │   │   ├── Dashboard/      # KPIs y exportaciones
│   │   │   ├── Inventory/      # Módulo inventario
│   │   │   ├── Landing/        # Página pública
│   │   │   ├── Sales/          # Módulo ventas
│   │   │   ├── Sidebar/        # Navegación lateral
│   │   │   ├── UserSettings/   # Ajustes de cuenta y organización
│   │   │   └── ui/             # shadcn/ui (NO EDITAR)
│   │   ├── hooks/              # useAuth, useCustomToast, useCopyToClipboard, useMobile
│   │   ├── routes/             # Rutas file-based (TanStack Router)
│   │   └── routeTree.gen.ts    # Auto-generado (NO EDITAR)
│   └── tests/                  # Pruebas Playwright E2E
│
├── docs/                       # Documentación académica
├── docker-compose.yml
├── docker-compose.override.yml
└── .env.example
```

---

## Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose
- Git
- Bun (para desarrollo de frontend)
- (Opcional) Python 3.10+ y uv para desarrollo de backend sin Docker

### Instalación

1. Clonar el repositorio

```bash
git clone https://github.com/Tech-Craft-Resources/orbit-engine.git
cd orbit-engine
```

2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. Iniciar con Docker Compose

```bash
docker compose watch
```

Esto levanta:
- PostgreSQL en `localhost:5432`
- Backend (FastAPI) en `http://api.localhost`
- Frontend (React) en `http://localhost`
- Adminer en `http://adminer.localhost`
- MinIO API en `http://minio.localhost` / Consola en `http://minio-console.localhost`
- Mailcatcher en `http://localhost:1080`
- Traefik dashboard en `http://localhost:8090`

4. Acceder

| Servicio | URL |
|---|---|
| Frontend | http://localhost |
| API Docs (Swagger) | http://api.localhost/docs |
| API Docs (ReDoc) | http://api.localhost/redoc |
| Adminer | http://adminer.localhost |
| MinIO Console | http://minio-console.localhost |
| Mailcatcher | http://localhost:1080 |

---

## Desarrollo Local

### Backend

El backend tiene **hot-reload automático** dentro de Docker mediante `compose.override.yml`. No hace falta reiniciar el contenedor al cambiar código Python; solo al instalar/actualizar dependencias:

```bash
docker compose restart backend
```

```bash
# Logs en tiempo real
docker compose logs -f backend

# Acceder al contenedor
docker compose exec backend bash

# Servidor local sin Docker (requiere DB corriendo)
cd backend
uv run fastapi dev app/main.py
```

### Frontend

Para mejor experiencia de desarrollo, corre Bun localmente y detén el contenedor de frontend:

```bash
docker compose stop frontend
cd frontend
bun install       # solo la primera vez
bun run dev       # http://localhost:5173
```

### Migraciones

```bash
docker compose exec backend alembic revision --autogenerate -m "descripcion"
docker compose exec backend alembic upgrade head
docker compose exec backend alembic downgrade -1
```

### Regenerar cliente API

Después de cambiar endpoints o schemas del backend:

```bash
# Con el backend corriendo
cd frontend && bun run generate-client
```

---

## Tests

```bash
# Backend – todos los tests con coverage
cd backend && uv run bash scripts/test.sh

# Backend – test específico
uv run pytest tests/api/routes/test_users.py -v

# Backend – patrón
uv run pytest -k "test_create" -v

# Frontend – E2E con Playwright
cd frontend && bun run test

# Frontend – modo UI interactivo
bun run test:ui
```

---

## Variables de Entorno

Copia `.env.example` a `.env`. Variables clave:

```env
DOMAIN=localhost
SECRET_KEY=cambia-esto-en-produccion

POSTGRES_SERVER=db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis

# Email – Resend (producción) o Mailcatcher (desarrollo)
SMTP_HOST=mailcatcher
SMTP_PORT=1025
RESEND_API_KEY=

# Almacenamiento S3 / MinIO
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=app-storage
```

---

## Documentación Académica

La documentación completa del proyecto está en [`docs/`](./docs/):

- [Propuesta](./docs/planteamiento/propuesta.md)
- [Alcance y MVP](./docs/planteamiento/01-alcance-mvp.md)
- [Requisitos (SRS)](./docs/planteamiento/SRS.md)
- [Stack Tecnológico](./docs/planteamiento/04-stack-tecnologico.md)
- [Base de Datos](./docs/planteamiento/05-base-de-datos.md)
- [Arquitectura Técnica](./docs/planteamiento/06-arquitectura-tecnica.md)

---

## Roadmap

### Completado
- [x] Setup de infraestructura y repositorio
- [x] Autenticación JWT + registro + recuperación de contraseña
- [x] Multi-tenancy con organizaciones
- [x] Control de acceso basado en roles (admin, seller, viewer)
- [x] Gestión de inventario (productos, categorías, movimientos, ajustes de stock)
- [x] Gestión de ventas (registro, detalle, cancelación)
- [x] Gestión de clientes (CRUD, historial de compras)
- [x] Dashboard con KPIs y gráficos
- [x] Administración de usuarios
- [x] Configuración de cuenta y organización
- [x] Landing page pública
- [x] Modo oscuro/claro
- [x] Tests E2E con Playwright
- [x] Tests backend con pytest

### Pendiente
- [ ] Predicción de demanda con IA (Prophet)
- [ ] Exportación a PDF/Excel desde el dashboard
- [ ] Deployment en producción (AWS / VPS)
- [ ] CI/CD con GitHub Actions

---

## Contribución

Proyecto académico — contribuciones limitadas al equipo de desarrollo.

```bash
git checkout -b feature/nombre-feature
git commit -m "feat: descripción del cambio"
git push origin feature/nombre-feature
```

Convenciones de commits: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.

---

**Última actualización:** Mayo 2026
**Versión:** 0.4.0
