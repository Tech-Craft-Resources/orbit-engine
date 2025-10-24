# Pecesaurio 🦕

> Plataforma SaaS para la gestión integral de procesos internos en pequeñas y medianas empresas utilizando Inteligencia Artificial

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.3+-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-15+-336791.svg)](https://www.postgresql.org/)

---

## 📋 Descripción

Pecesaurio es una plataforma SaaS diseñada para digitalizar y optimizar los procesos internos de pequeñas y medianas empresas (pymes). Proporciona herramientas para gestionar inventario, ventas, clientes y reportes, incorporando Inteligencia Artificial para predicción de demanda y análisis predictivo.

**Estado del Proyecto:** 🚧 En desarrollo (Proyecto de Grado)  
**Período:** Noviembre 2024 - Abril 2025

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

### Database
- **Primary:** PostgreSQL 15+
- **Cache:** Redis 7+
- **Storage:** AWS S3

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
pecesaurio/
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
- (Opcional) **Python 3.11+** y **Node.js 18+** para desarrollo sin Docker

### Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/pecesaurio.git
cd pecesaurio
```

2. **Configurar variables de entorno**

```bash
# Backend
cp backend/.env.example backend/.env
# Editar backend/.env con tus configuraciones

# Frontend
cp frontend/.env.example frontend/.env
# Editar frontend/.env con tus configuraciones
```

3. **Iniciar con Docker Compose**

```bash
docker-compose up -d
```

Esto iniciará:
- PostgreSQL en `localhost:5432`
- Redis en `localhost:6379`
- Backend (FastAPI) en `http://localhost:8000`
- Frontend (React) en `http://localhost:5173`
- Celery Worker
- Celery Beat (scheduler)

4. **Ejecutar migraciones**

```bash
docker-compose exec backend alembic upgrade head
```

5. **Crear usuario admin inicial (opcional)**

```bash
docker-compose exec backend python -m app.scripts.create_admin
```

6. **Acceder a la aplicación**

- Frontend: http://localhost:5173
- Backend API Docs: http://localhost:8000/docs
- Backend ReDoc: http://localhost:8000/redoc

---

## 💻 Desarrollo Local

### Backend (sin Docker)

```bash
cd backend

# Crear virtual environment
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend (sin Docker)

```bash
cd frontend

# Instalar dependencias
npm install
# o con pnpm
pnpm install

# Iniciar servidor de desarrollo
npm run dev
# o
pnpm dev
```

### Ejecutar Tests

```bash
# Backend
cd backend
pytest

# Con coverage
pytest --cov=app tests/

# Frontend
cd frontend
npm run test
```

---

## 🗄️ Base de Datos

### Crear nueva migración

```bash
docker-compose exec backend alembic revision --autogenerate -m "Descripción del cambio"
```

### Aplicar migraciones

```bash
docker-compose exec backend alembic upgrade head
```

### Rollback

```bash
docker-compose exec backend alembic downgrade -1
```

---

## 📝 Variables de Entorno

### Backend (`backend/.env`)

```env
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/pecesaurio

# Redis
REDIS_URL=redis://redis:6379/0

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AWS (opcional para desarrollo local)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=

# Celery
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

# Environment
ENVIRONMENT=development
```

### Frontend (`frontend/.env`)

```env
VITE_API_URL=http://localhost:8000
VITE_APP_NAME=Pecesaurio
```

---

## 🤖 IA/ML - Predicción de Demanda

El sistema utiliza **Prophet** (Meta) para forecasting de demanda. Las predicciones se generan automáticamente cada 24 horas mediante Celery Beat.

### Entrenar modelo manualmente

```bash
docker-compose exec backend python -m app.ml.trainer --tenant-id=<uuid> --product-id=<uuid>
```

### Generar predicciones

```bash
docker-compose exec backend python -m app.ml.predictor --tenant-id=<uuid> --product-id=<uuid> --days=30
```

---

## 🧪 Testing

### Estrategia de Testing

- **Backend:** Tests unitarios y de integración con pytest
- **Frontend:** Tests de componentes con Vitest + Testing Library
- **E2E:** (Futuro) Playwright o Cypress

### Ejecutar todos los tests

```bash
# Backend
docker-compose exec backend pytest --cov=app

# Frontend
docker-compose exec frontend npm run test
```

---

## 🚢 Deployment

### Producción en AWS

El deployment a AWS se realiza automáticamente mediante GitHub Actions cuando se hace push a `main`.

1. Backend se despliega en **ECS/EC2**
2. Frontend se construye y sube a **S3 + CloudFront**
3. Base de datos en **RDS PostgreSQL**
4. Cache en **ElastiCache Redis**

Ver documentación completa en [`docs/06-arquitectura-tecnica.md`](./docs/06-arquitectura-tecnica.md)

---

## 📚 Documentación

La documentación académica completa del proyecto se encuentra en la carpeta [`docs/`](./docs/):

- **[Propuesta del Proyecto](./docs/propuesta.md)** - Planteamiento del problema y objetivos
- **[Alcance y MVP](./docs/01-alcance-mvp.md)** - Definición del alcance y métricas de éxito
- **[Requisitos](./docs/02-requisitos.md)** - Historias de usuario y requisitos funcionales
- **[Cronograma](./docs/03-cronograma.md)** - Planificación temporal (6 meses)
- **[Stack Tecnológico](./docs/04-stack-tecnologico.md)** - Decisiones técnicas justificadas
- **[Base de Datos](./docs/05-base-de-datos.md)** - Modelo de datos completo
- **[Arquitectura Técnica](./docs/06-arquitectura-tecnica.md)** - Diseño arquitectónico del sistema

---

## 🗺️ Roadmap

### ✅ Fase 1: Investigación y Planificación (Noviembre 2024)
- [x] Definición de requisitos
- [x] Diseño de arquitectura
- [x] Selección de stack tecnológico
- [x] Documentación inicial

### 🚧 Fase 2: Diseño y Setup (Noviembre-Diciembre 2024)
- [ ] Setup de repositorios
- [ ] Configuración de infraestructura AWS
- [ ] Diseño de UI/UX (Figma)
- [ ] Setup de CI/CD

### 📅 Fase 3: Desarrollo Core (Diciembre 2024 - Febrero 2025)
- [ ] Sprint 1: Autenticación y usuarios
- [ ] Sprint 2-3: Gestión de inventario
- [ ] Sprint 4: Gestión de ventas
- [ ] Sprint 5: Gestión de clientes

### 📅 Fase 4: Desarrollo Avanzado (Febrero - Marzo 2025)
- [ ] Sprint 6: Dashboard y reportes
- [ ] Sprint 7: Integración de IA/ML

### 📅 Fase 5: Testing y Validación (Marzo - Abril 2025)
- [ ] Pruebas con usuarios reales
- [ ] Recolección de métricas
- [ ] Ajustes y mejoras

### 📅 Fase 6: Documentación y Defensa (Abril 2025)
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

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

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

**Última actualización:** Octubre 2024  
**Versión:** 0.1.0-alpha

---

<p align="center">
  <strong>Hecho con ❤️ por el equipo Pecesaurio</strong>
</p>

