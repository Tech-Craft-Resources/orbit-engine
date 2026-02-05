# OrbitEngine 🚀

> Plataforma SaaS para la gestión integral de procesos internos en pequeñas y medianas empresas utilizando Inteligencia Artificial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.3+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-336791.svg)](https://www.postgresql.org/)

---

## 📋 Descripción

OrbitEngine es una plataforma SaaS diseñada para digitalizar y optimizar los procesos internos de pequeñas y medianas empresas (pymes). Proporciona herramientas para gestionar inventario, ventas, clientes y reportes, incorporando Inteligencia Artificial para predicción de demanda y análisis predictivo.

**Estado del Proyecto:** 🚧 En desarrollo (Proyecto de Grado)  
**Período:** Noviembre 2025 - Abril 2026

---

## ✨ Características Principales

- 🔐 **Autenticación y Roles:** Sistema seguro con JWT y control de acceso basado en roles
- 📦 **Gestión de Inventario:** CRUD de productos, categorías, alertas de stock bajo
- 💰 **Gestión de Ventas:** Registro de ventas, facturación, historial de transacciones
- 👥 **Gestión de Clientes:** Base de datos de clientes, historial de compras
- 📊 **Dashboard y Reportes:** KPIs en tiempo real, exportación a PDF/Excel
- 🤖 **IA - Predicción de Demanda:** Forecasting con Prophet para optimizar inventario
- 🏢 **Multi-tenancy:** Soporte para múltiples empresas con aislamiento de datos

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** React 18.3+ con TypeScript 5+
- **Build Tool:** Vite 5+
- **Styling:** Tailwind CSS 3+
- **Components:** shadcn/ui
- **State Management:** Zustand + TanStack Query (React Query)
- **Forms:** React Hook Form + Zod
- **Charts:** Recharts

### Backend
- **Framework:** FastAPI 0.110+ (Python 3.11+)
- **ORM:** SQLAlchemy 2.0+
- **Migrations:** Alembic
- **Validation:** Pydantic 2.0+
- **Auth:** JWT (python-jose + passlib)
- **Tasks:** Celery + Redis
- **Testing:** pytest

### Database & Storage
- **Primary:** PostgreSQL 15+
- **Cache:** Redis 7+ (to be implemented)
- **Storage:** MinIO (development) / AWS S3 (production)

### Machine Learning
- **Libraries:** scikit-learn, Prophet, pandas, numpy
- **Use Case:** Demand forecasting, trend analysis

### Infrastructure
- **Cloud:** AWS (EC2/ECS, RDS, S3, CloudFront, ALB)
- **Containerization:** Docker + Docker Compose
- **CI/CD:** GitHub Actions
- **Monitoring:** CloudWatch, Sentry

---

## 📁 Estructura del Proyecto

```
orbitengine/
├── backend/                 # FastAPI Backend
│   ├── alembic/            # Database migrations
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── ml/             # Machine Learning
│   │   ├── tasks/          # Celery tasks
│   │   └── main.py         # App entry point
│   ├── tests/              # Tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # Reusable components
│   │   ├── features/      # Feature modules
│   │   ├── hooks/         # Custom hooks
│   │   ├── pages/         # Page components
│   │   ├── stores/        # Zustand stores
│   │   └── types/         # TypeScript types
│   ├── public/
│   ├── Dockerfile
│   └── package.json
│
├── docs/                   # 📚 Academic documentation
│   ├── propuesta.md
│   ├── 01-alcance-mvp.md
│   ├── 02-requisitos.md
│   ├── 03-cronograma.md
│   ├── 04-stack-tecnologico.md
│   ├── 05-base-de-datos.md
│   ├── 06-arquitectura-tecnica.md
│   └── README.md
│
├── docker-compose.yml      # Local development setup
├── .github/                # GitHub Actions workflows
└── README.md              # This file
```

---

## 🚀 Getting Started

### Prerequisitos

- **Docker** y **Docker Compose** instalados
- **Git** para clonar el repositorio
- **Bun** instalado (para desarrollo de frontend)
- (Opcional) **Python 3.11+** y **uv** para desarrollo de backend sin Docker

### Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/orbitengine.git
cd orbitengine
```

2. **Configurar variables de entorno**

```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. **Iniciar con Docker Compose**

```bash
# Primera vez o después de cambiar Dockerfiles
docker compose build

# Iniciar los servicios
docker compose up -d
```

Esto iniciará:
- PostgreSQL en `localhost:5432`
- Adminer (DB admin) en `http://adminer.localhost`
- Backend (FastAPI) en `http://api.localhost`
- Frontend (React) en `http://localhost`
- MinIO (S3-compatible storage) en:
  - API: `http://minio.localhost`
  - Console: `http://minio-console.localhost`
- Mailcatcher (email testing) en `http://localhost:1080`
- Traefik dashboard en `http://localhost:8090`

**Nota:** El backend usa volúmenes configurados en `compose.override.yml` para hot-reload automático. Los cambios en el código Python se reflejan inmediatamente sin reiniciar. Solo necesitas reiniciar el contenedor si instalas/actualizas/eliminas dependencias.

4. **Acceder a la aplicación**

- Frontend: http://localhost
- Backend API Docs: http://api.localhost/docs
- Backend ReDoc: http://api.localhost/redoc
- Adminer (DB): http://adminer.localhost
- MinIO Console: http://minio-console.localhost (user: `minioadmin`, pass: `minioadmin`)
- Mailcatcher: http://localhost:1080

**Nota sobre MinIO:** MinIO es un servidor de almacenamiento de objetos compatible con S3 para desarrollo local. Para usar AWS S3 en producción, simplemente cambia las variables de entorno (ver [`docs/varios/s3-storage.md`](./docs/varios/s3-storage.md)).

---

## 💻 Desarrollo Local

### Backend

El backend corre dentro de Docker con **hot-reload automático** gracias a:
- Volúmenes configurados en `compose.override.yml` que sincronizan el código
- Comando `fastapi run --reload` que detecta cambios automáticamente

**¿Cuándo reiniciar el contenedor backend?**
- ✅ **NO reiniciar** cuando cambies código Python (hot-reload automático)
- ⚠️ **SÍ reiniciar** cuando instales/actualices/elimines dependencias con `uv`:
  ```bash
  docker compose restart backend
  ```

**Ver logs en tiempo real:**
```bash
docker compose logs -f backend
```

**Ejecutar migraciones:**
```bash
docker compose exec backend alembic revision --autogenerate -m "description"
docker compose exec backend alembic upgrade head
```

**Acceder al contenedor:**
```bash
docker compose exec backend bash
```

### Frontend

Para desarrollo de frontend, es recomendable **detener el contenedor de Docker** y ejecutar Bun localmente para mejor experiencia de desarrollo:

```bash
# Detener el contenedor de frontend
docker compose stop frontend

# Ir al directorio frontend
cd frontend

# Instalar dependencias (primera vez)
bun install

# Iniciar servidor de desarrollo
bun run dev
```

Esto te dará:
- ⚡ Hot-reload instantáneo
- 🔥 Mejor rendimiento
- 🐛 Mejor debugging

El frontend seguirá usando el backend que corre en Docker (`http://localhost:8000`).

### Ejecutar Tests

```bash
# Backend (desde la raíz del proyecto)
docker compose exec backend bash scripts/test.sh

# O con uv localmente
cd backend
uv run bash scripts/test.sh

# Frontend (con Playwright)
cd frontend
bun run test

# Frontend con UI
bun run test:ui
```

---

## 🗄️ Base de Datos

### Crear nueva migración

```bash
docker compose exec backend alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
docker compose exec backend alembic upgrade head
```

### Rollback

```bash
docker compose exec backend alembic downgrade -1
```

---

## 📝 Variables de Entorno

### Backend (`.env`)

```env
# Project
PROJECT_NAME=OrbitEngine
STACK_NAME=orbitengine-stack
DOMAIN=localhost

# Backend
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost"]
SECRET_KEY=your-secret-key-here-change-in-production

# Frontend
FRONTEND_HOST=http://localhost:5173

# Database
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

# First Superuser
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis

# Email (using mailcatcher in development)
SMTP_HOST=mailcatcher
SMTP_PORT=1025
SMTP_TLS=false
EMAILS_FROM_EMAIL=noreply@example.com

# Redis (to be implemented)
# REDIS_URL=redis://redis:6379/0

# Celery (to be implemented)
# CELERY_BROKER_URL=redis://redis:6379/1
# CELERY_RESULT_BACKEND=redis://redis:6379/2

# S3 / Object Storage (S3-compatible)
# For development with MinIO (default configuration)
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=app-storage
S3_REGION=us-east-1

# MinIO (only for local development)
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# Docker Images
DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_FRONTEND=frontend

# Environment
ENVIRONMENT=development
```

---

## 🤖 IA/ML - Predicción de Demanda

El sistema utilizará **Prophet** (Meta) para forecasting de demanda. Esta funcionalidad será implementada en fases posteriores del proyecto.

### Características planeadas:

- Predicción de demanda basada en histórico de ventas
- Alertas automáticas de reabastecimiento
- Análisis de tendencias y estacionalidad
- Optimización de inventario

Las predicciones se generarán automáticamente usando **Celery Beat** (scheduler) ejecutándose en background.

Para más detalles sobre los algoritmos de IA planeados, ver [`docs/planteamiento/IA.md`](./docs/planteamiento/IA.md)

---

## 🧪 Testing

### Estrategia de Testing

- **Backend:** Tests unitarios y de integración con pytest
- **Frontend:** Tests E2E con Playwright

### Ejecutar tests

```bash
# Backend - todos los tests con coverage
cd backend
uv run bash scripts/test.sh

# Backend - test específico
uv run pytest tests/api/routes/test_users.py -v

# Backend - dentro de Docker
docker compose exec backend bash scripts/test.sh

# Frontend - E2E con Playwright
cd frontend
bun run test

# Frontend - con UI interactiva
bun run test:ui
```

---

## 🚢 Deployment

El deployment a producción será configurado en fases posteriores usando AWS:

### Infraestructura planeada:

**Backend:**
- ECS/EC2 para servicios FastAPI
- Celery Workers para tareas asíncronas
- Celery Beat para tareas programadas

**Frontend:**
- S3 para hosting estático
- CloudFront como CDN global

**Database & Cache:**
- RDS PostgreSQL (instancia gestionada)
- ElastiCache Redis para cache y Celery

**CI/CD:**
- GitHub Actions para deployment automático
- Environments: staging y production

Ver documentación completa en [`docs/planteamiento/06-arquitectura-tecnica.md`](./docs/planteamiento/06-arquitectura-tecnica.md)

---

## 📚 Documentación

La documentación académica completa del proyecto se encuentra en la carpeta [`docs/planteamiento/`](./docs/planteamiento/):

- **[Alcance y MVP](./docs/planteamiento/01-alcance-mvp.md)** - Definición del alcance y métricas de éxito
- **[Requisitos (SRS)](./docs/planteamiento/SRS.md)** - Requisitos funcionales y no funcionales
- **[Cronograma](./docs/planteamiento/03-cronograma.md)** - Planificación temporal (6 meses)
- **[Stack Tecnológico](./docs/planteamiento/04-stack-tecnologico.md)** - Decisiones técnicas justificadas
- **[Base de Datos](./docs/planteamiento/05-base-de-datos.md)** - Modelo de datos completo
- **[Arquitectura Técnica](./docs/planteamiento/06-arquitectura-tecnica.md)** - Diseño arquitectónico del sistema
- **[IA/ML](./docs/planteamiento/IA.md)** - Algoritmos de predicción de demanda

---

## 🗺️ Roadmap

### ✅ Fase 1: Investigación y Planificación (Noviembre 2025)
- [x] Definición de requisitos
- [x] Diseño de arquitectura
- [x] Selección de stack tecnológico
- [x] Documentación inicial

### 🚧 Fase 2: Diseño y Setup (Noviembre-Diciembre 2025)
- [ ] Setup de repositorios
- [ ] Configuración de infraestructura AWS
- [ ] Diseño de UI/UX (Figma)
- [ ] Setup de CI/CD

### 📅 Fase 3: Desarrollo Core (Diciembre 2025 - Febrero 2026)
- [ ] Sprint 1: Autenticación y usuarios
- [ ] Sprint 2-3: Gestión de inventario
- [ ] Sprint 4: Gestión de ventas
- [ ] Sprint 5: Gestión de clientes

### 📅 Fase 4: Desarrollo Avanzado (Febrero - Marzo 2026)
- [ ] Sprint 6: Dashboard y reportes
- [ ] Sprint 7: Integración de IA/ML

### 📅 Fase 5: Testing y Validación (Marzo - Abril 2026)
- [ ] Pruebas con usuarios reales
- [ ] Recolección de métricas
- [ ] Ajustes y mejoras

### 📅 Fase 6: Documentación y Defensa (Abril 2026)
- [ ] Documentación final
- [ ] Presentación del proyecto
- [ ] Defensa de proyecto de grado

---

## 👥 Equipo

- **Backend Lead:** [Nombre] - Arquitectura, APIs, ML/IA
- **Frontend Lead:** [Nombre] - UI/UX, React, Integración
- **DevOps & Full Stack:** [Nombre] - Infraestructura, CI/CD, Soporte

**Asesor Académico:** [Nombre del asesor]  
**Universidad:** [Nombre de la universidad]

---

## 🤝 Contribución

Este es un proyecto de grado académico. Las contribuciones están limitadas al equipo de desarrollo.

### Workflow de Git

```bash
# Crear rama para feature
git checkout -b feature/nombre-feature

# Commits siguiendo Conventional Commits
git commit -m "feat: descripción del cambio"
git commit -m "fix: descripción del fix"

# Push y crear PR
git push origin feature/nombre-feature
```

### Conventional Commits

- `feat:` Nueva funcionalidad
- `fix:` Corrección de bug
- `docs:` Cambios en documentación
- `style:` Cambios de formato (no afectan lógica)
- `refactor:` Refactorización de código
- `test:` Añadir o modificar tests
- `chore:` Tareas de mantenimiento

---

## 📄 Licencia

Este proyecto es académico y forma parte de un Proyecto de Grado.

---

## 🙏 Agradecimientos

- A nuestro asesor académico por su guía
- A las pymes que participarán en las pruebas piloto
- A la comunidad open source por las herramientas utilizadas

---

## 📞 Contacto

Para consultas sobre el proyecto:

- **Email:** [email del equipo]
- **GitHub:** [link al repo]
- **Documentación:** [link a docs]

---

**Última actualización:** Noviembre 2025  
**Versión:** 0.1.0-alpha

---

<p align="center">
  <strong>Hecho con ❤️ por el equipo OrbitEngine</strong>
</p>

