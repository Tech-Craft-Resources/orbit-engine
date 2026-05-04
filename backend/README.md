# OrbitEngine – Backend

API REST construida con **FastAPI** y **Python 3.10+**. Usa SQLModel como ORM, Alembic para migraciones, PyJWT para autenticación y Resend para envío de correos.

---

## Requisitos

- [Docker](https://www.docker.com/) y Docker Compose (recomendado)
- [uv](https://docs.astral.sh/uv/) para gestión de entorno Python (desarrollo local)

---

## Desarrollo con Docker Compose (recomendado)

Desde la raíz del proyecto:

```bash
docker compose watch
```

El backend corre con **hot-reload automático**: los cambios en código Python se reflejan al instante sin reiniciar el contenedor. Solo reinicia cuando instales, actualices o elimines dependencias:

```bash
docker compose restart backend
```

```bash
# Logs en tiempo real
docker compose logs -f backend

# Acceder al contenedor
docker compose exec backend bash
```

**Endpoints disponibles:**
- Swagger UI: http://api.localhost/docs
- ReDoc: http://api.localhost/redoc
- Health check: http://api.localhost/api/v1/utils/health-check/

---

## Desarrollo Local (sin Docker)

Requiere PostgreSQL corriendo (puede ser solo el contenedor de la BD):

```bash
# Arrancar solo la base de datos
docker compose up db -d

cd backend

# Instalar dependencias
uv sync

# Activar entorno virtual
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Aplicar migraciones
alembic upgrade head

# Servidor de desarrollo con hot-reload
uv run fastapi dev app/main.py
```

---

## Estructura de Código

```
backend/app/
├── api/
│   ├── routes/             # Un archivo por dominio
│   │   ├── login.py        # Autenticación, tokens, recuperación de contraseña
│   │   ├── users.py        # Gestión de usuarios
│   │   ├── organizations.py # Configuración de organización
│   │   ├── roles.py        # Asignación de roles
│   │   ├── products.py     # Inventario – productos
│   │   ├── categories.py   # Inventario – categorías
│   │   ├── inventory_movements.py  # Movimientos de stock
│   │   ├── customers.py    # Clientes
│   │   ├── sales.py        # Ventas
│   │   ├── dashboard.py    # KPIs y métricas
│   │   └── utils.py        # Health check
│   └── deps.py             # CurrentUser, SessionDep, RoleChecker…
├── core/
│   ├── config.py           # Settings (pydantic-settings)
│   ├── security.py         # JWT, hashing de contraseñas
│   └── db.py               # Engine y sesión SQLModel
├── alembic/
│   └── versions/           # Migraciones
├── email-templates/
│   ├── src/                # Plantillas MJML (editables)
│   └── build/              # HTML compilado (usado por la app)
├── models.py               # Todos los modelos SQLModel y schemas Pydantic
├── crud.py                 # Operaciones CRUD reutilizables
└── main.py                 # Entry point, routers, CORS, Sentry
```

### Convenciones de modelos

Todos los modelos y schemas están en `models.py`. Nomenclatura:

| Clase | Propósito |
|---|---|
| `{Model}` | Tabla de base de datos (`table=True`) |
| `{Model}Create` | Schema de creación (input) |
| `{Model}Update` | Schema de actualización parcial (input) |
| `{Model}Public` | Schema de respuesta (output) |
| `{Model}sPublic` | Lista paginada de respuesta |

---

## Migraciones

Siempre ejecutar dentro del contenedor Docker para tener acceso a la base de datos:

```bash
# Crear migración automática a partir de cambios en models.py
docker compose exec backend alembic revision --autogenerate -m "descripcion del cambio"

# Aplicar migraciones pendientes
docker compose exec backend alembic upgrade head

# Revertir última migración
docker compose exec backend alembic downgrade -1
```

### Flujo de trabajo recomendado

1. Modificar modelos en `app/models.py`
2. Crear migración: `docker compose exec backend alembic revision --autogenerate -m "..."`
3. Revisar el archivo generado en `app/alembic/versions/`
4. Aplicar: `docker compose exec backend alembic upgrade head`
5. Commitear `models.py` y el archivo de migración juntos

---

## Tests

```bash
# Todos los tests con reporte de cobertura
uv run bash scripts/test.sh

# Archivo específico
uv run pytest tests/api/routes/test_users.py -v

# Función específica
uv run pytest tests/api/routes/test_users.py::test_get_users_superuser_me -v

# Tests que coincidan con un patrón
uv run pytest -k "test_create" -v

# Dentro de Docker
docker compose exec backend bash scripts/test.sh
```

Los reportes de cobertura en HTML se generan en `htmlcov/index.html`.

---

## Calidad de Código

```bash
# Lint (ruff + mypy strict)
uv run bash scripts/lint.sh

# Formateo automático
uv run bash scripts/format.sh
```

---

## Email

- **Desarrollo:** Mailcatcher (captura todos los correos en http://localhost:1080)
- **Producción:** [Resend](https://resend.com) — configurar `RESEND_API_KEY` en `.env`

Las plantillas están en `app/email-templates/src/` (formato MJML). Para compilarlas a HTML usa la extensión [MJML para VS Code](https://github.com/mjmlio/vscode-mjml) y guarda el resultado en `build/`.

---

## Almacenamiento de Archivos (S3 / MinIO)

- **Desarrollo:** MinIO (arranca automáticamente con Docker Compose). Consola en http://minio-console.localhost con `minioadmin/minioadmin`.
- **Producción:** AWS S3 — basta con cambiar las variables de entorno.

```env
# Desarrollo (MinIO)
S3_ENDPOINT_URL=http://minio:9000
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=app-storage

# Producción (AWS S3) – dejar S3_ENDPOINT_URL vacío
S3_ENDPOINT_URL=
S3_ACCESS_KEY_ID=tu-aws-key
S3_SECRET_ACCESS_KEY=tu-aws-secret
S3_BUCKET_NAME=tu-bucket
S3_REGION=us-east-1
```

---

## Variables de Entorno Clave

Se definen en el archivo `.env` de la raíz del proyecto:

```env
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=changethis
POSTGRES_DB=app

SECRET_KEY=cambia-esto-en-produccion
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost"]

SMTP_HOST=mailcatcher
SMTP_PORT=1025
SMTP_TLS=false
EMAILS_FROM_EMAIL=noreply@example.com
RESEND_API_KEY=

FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=changethis
```

Consulta `.env.example` en la raíz para la lista completa.
