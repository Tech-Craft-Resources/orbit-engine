# Anexo B — Manual de Instalación y Despliegue

**OrbitEngine** — Plataforma SaaS para la Gestión de Procesos Internos en Pymes  
Versión: 1.0 | Abril 2026  
Universidad Sergio Arboleda — Semillero de Software como Innovación

---

## B.1 Visión General

OrbitEngine utiliza **Docker Compose** como orquestador de contenedores en todos los entornos. La arquitectura de despliegue se compone de los siguientes servicios:

| Servicio | Imagen | Descripción |
|----------|--------|-------------|
| `db` | `postgres:18` | Base de datos relacional PostgreSQL |
| `backend` | Custom (FastAPI) | API REST del sistema |
| `frontend` | Custom (React/Nginx) | Interfaz de usuario compilada |
| `prestart` | Custom (FastAPI) | Ejecuta migraciones y datos iniciales al iniciar |
| `adminer` | `adminer` | Panel web de administración de BD |
| `proxy` | `traefik:3.6` | Reverse proxy y gestor de rutas HTTP/HTTPS |
| `minio` | `minio/minio` | Almacenamiento de objetos S3-compatible (dev) |
| `mailcatcher` | `schickling/mailcatcher` | Servidor SMTP de prueba (solo dev) |

El enrutamiento externo se gestiona con **Traefik**, que expone los servicios bajo subdominios configurados y maneja la terminación TLS automática mediante Let's Encrypt en producción.

---

## B.2 Prerrequisitos

### B.2.1 Herramientas requeridas

| Herramienta | Versión mínima | Propósito |
|-------------|---------------|-----------|
| Docker Engine | 24.x | Contenedores |
| Docker Compose | v2.x | Orquestación de servicios |
| Git | 2.x | Control de versiones |
| `uv` | 0.4+ | Gestor de dependencias Python (para desarrollo local sin Docker) |
| Bun | 1.x | Runtime JS / gestor de paquetes (para desarrollo local sin Docker) |

### B.2.2 Puertos utilizados

| Puerto | Servicio | Entorno |
|--------|----------|---------|
| 80 | Traefik HTTP | Dev y Producción |
| 443 | Traefik HTTPS | Producción |
| 8000 | Backend FastAPI | Dev (expuesto directamente) |
| 5173 | Frontend (Vite) | Dev |
| 5432 | PostgreSQL | Dev |
| 8080 | Adminer | Dev |
| 8090 | Traefik Dashboard | Dev |
| 9000 | MinIO API | Dev |
| 9001 | MinIO Console | Dev |
| 1025 | Mailcatcher SMTP | Dev |
| 1080 | Mailcatcher UI | Dev |

---

## B.3 Configuración de Variables de Entorno

Antes de ejecutar cualquier entorno, crear el archivo `.env` en la raíz del repositorio:

```bash
cp .env.example .env   # si existe el archivo de ejemplo, de lo contrario crearlo manualmente
```

Las variables requeridas son:

```ini
# ─── Proyecto ──────────────────────────────────────────────────────────────────
PROJECT_NAME=OrbitEngine
STACK_NAME=orbitengine-stack
DOMAIN=localhost                       # En producción: tu-dominio.com

# ─── Backend ───────────────────────────────────────────────────────────────────
SECRET_KEY=cambia-esto-en-produccion   # Clave aleatoria, mínimo 32 chars
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost"]
FRONTEND_HOST=http://localhost:5173    # En producción: https://tu-dominio.com

# ─── Base de datos ─────────────────────────────────────────────────────────────
POSTGRES_SERVER=db
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=cambia-esto
POSTGRES_DB=app

# ─── Superusuario inicial ──────────────────────────────────────────────────────
FIRST_SUPERUSER=admin@ejemplo.com
FIRST_SUPERUSER_PASSWORD=cambia-esto

# ─── Email ─────────────────────────────────────────────────────────────────────
SMTP_HOST=mailcatcher                  # En producción: smtp.tu-proveedor.com
SMTP_PORT=1025                         # En producción: 587
SMTP_TLS=false                         # En producción: true
EMAILS_FROM_EMAIL=noreply@tu-dominio.com

# ─── Almacenamiento S3 / MinIO ────────────────────────────────────────────────
S3_ENDPOINT_URL=http://minio:9000      # Omitir en producción con AWS S3 nativo
S3_ACCESS_KEY_ID=minioadmin
S3_SECRET_ACCESS_KEY=minioadmin
S3_BUCKET_NAME=app-storage
S3_REGION=us-east-1

# ─── MinIO (solo desarrollo) ──────────────────────────────────────────────────
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin

# ─── Imágenes Docker ──────────────────────────────────────────────────────────
DOCKER_IMAGE_BACKEND=backend
DOCKER_IMAGE_FRONTEND=frontend
ENVIRONMENT=local                      # local | staging | production
```

> **Producción:** Cambiar todas las claves y contraseñas por valores aleatorios seguros. Se recomienda usar un gestor de secretos (HashiCorp Vault, AWS Secrets Manager, etc.).

---

## B.4 Entorno de Desarrollo Local

El entorno de desarrollo combina `compose.yml` con `compose.override.yml`, que añade los servicios de desarrollo (Traefik local, Mailcatcher, MinIO) y sobrescribe las configuraciones para recarga en caliente.

### B.4.1 Iniciar el entorno

```bash
# Desde la raíz del repositorio
docker compose watch
```

Este comando:
1. Construye las imágenes de backend y frontend si no existen.
2. Levanta todos los servicios en orden de dependencias.
3. Activa la recarga automática del backend al detectar cambios en `./backend`.
4. El servicio `prestart` ejecuta las migraciones de Alembic y los datos iniciales antes de que el backend acepte peticiones.

### B.4.2 URLs del entorno local

| Servicio | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Documentación interactiva (Swagger) | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |
| Adminer | http://localhost:8080 |
| Traefik Dashboard | http://localhost:8090 |
| MinIO Console | http://localhost:9001 |
| Mailcatcher UI | http://localhost:1080 |

### B.4.3 Detener el entorno

```bash
# Detener y eliminar contenedores (datos persisten en volumen)
docker compose down

# Detener y eliminar contenedores + volúmenes (elimina datos de BD)
docker compose down -v
```

### B.4.4 Ver logs

```bash
docker compose logs -f backend    # Logs del backend en tiempo real
docker compose logs -f frontend   # Logs del frontend
docker compose logs -f db         # Logs de PostgreSQL
```

---

## B.5 Migraciones de Base de Datos

Las migraciones se gestionan con **Alembic** y se ejecutan automáticamente al iniciar el entorno (servicio `prestart`). Para operaciones manuales:

### B.5.1 Aplicar migraciones pendientes

```bash
docker compose exec backend alembic upgrade head
```

### B.5.2 Crear una nueva migración

Después de modificar los modelos en `backend/app/models.py`:

```bash
docker compose exec backend alembic revision --autogenerate -m "descripcion_del_cambio"
```

Revisar el archivo generado en `backend/app/alembic/versions/` antes de aplicarlo.

### B.5.3 Ver historial de migraciones

```bash
docker compose exec backend alembic history --verbose
```

### B.5.4 Revertir la última migración

```bash
docker compose exec backend alembic downgrade -1
```

### B.5.5 Migraciones del proyecto

Las migraciones actuales del esquema son:

| Archivo | Descripción |
|---------|-------------|
| `001_initial_schema.py` | Tablas base: `organizations`, `roles`, `users` |
| `002_categories.py` | Tabla `categories` con jerarquía padre-hijo |
| `003_products.py` | Tabla `products` |
| `004_customers.py` | Tabla `customers` |
| `005_inventory_movements.py` | Tabla `inventory_movements` |
| `006_sales.py` | Tablas `sales` y `sale_items` |

---

## B.6 Pruebas

### B.6.1 Pruebas del backend (pytest)

```bash
# Ejecutar todas las pruebas con cobertura
cd backend
uv run bash scripts/test.sh

# Prueba de un archivo específico
uv run pytest tests/api/routes/test_sales.py -v

# Prueba de una función específica
uv run pytest tests/api/routes/test_users.py::test_get_users_superuser_me -v

# Pruebas por patrón
uv run pytest -k "test_create" -v

# Reporte de cobertura
uv run coverage run -m pytest && coverage report
```

La cobertura de pruebas incluye:

| Módulo | Pruebas API | Pruebas CRUD |
|--------|-------------|--------------|
| Usuarios | ✅ | ✅ |
| Autenticación | ✅ | — |
| Categorías | ✅ | ✅ |
| Productos | ✅ | ✅ |
| Clientes | ✅ | ✅ |
| Ventas | ✅ | ✅ |
| Movimientos de inventario | ✅ | ✅ |
| Dashboard | ✅ | ✅ |

### B.6.2 Pruebas del frontend (Playwright E2E)

```bash
cd frontend

# Ejecutar todas las pruebas E2E
bun run test

# Prueba de un archivo específico
bunx playwright test tests/login.spec.ts

# Prueba por descripción
bunx playwright test --grep "crear venta"

# Modo con interfaz visual
bun run test:ui
```

Las pruebas E2E cubren los flujos: login, registro de organización, registro de usuario, restablecimiento de contraseña, inventario, ventas, clientes, administración de usuarios y configuración.

---

## B.7 Generación del Cliente API

Cuando se modifican los endpoints del backend, el cliente TypeScript del frontend debe regenerarse:

```bash
# El backend debe estar corriendo en http://localhost:8000
cd frontend
bun run generate-client
```

Esto actualiza los archivos en `src/client/` a partir del esquema OpenAPI del backend. **No editar manualmente** estos archivos.

---

## B.8 Despliegue en Producción

El despliegue en producción usa el mismo `compose.yml` sin el `compose.override.yml`.

### B.8.1 Prerrequisitos del servidor

- Servidor Linux con Docker Engine y Docker Compose instalados.
- Dominio apuntando a la IP del servidor (registros A/CNAME en el DNS).
- Puertos 80 y 443 abiertos en el firewall.

### B.8.2 Preparar la red de Traefik

Traefik requiere una red Docker externa compartida entre todos los servicios:

```bash
docker network create traefik-public
```

### B.8.3 Configurar Traefik con TLS

Crear el archivo de configuración de Traefik (`compose.traefik.yml` ya incluido en el repositorio) y levantarlo:

```bash
docker compose -f compose.traefik.yml up -d
```

Esto levanta Traefik en modo producción con:
- Redirección automática HTTP → HTTPS.
- Certificados TLS gestionados por Let's Encrypt.
- Panel de Traefik accesible solo internamente.

### B.8.4 Configurar variables de entorno para producción

Editar el `.env` con los valores de producción:

```ini
DOMAIN=tu-dominio.com
ENVIRONMENT=production
SECRET_KEY=<clave-aleatoria-larga>
POSTGRES_PASSWORD=<contraseña-segura>
FIRST_SUPERUSER_PASSWORD=<contraseña-segura>
FRONTEND_HOST=https://tu-dominio.com
BACKEND_CORS_ORIGINS=["https://tu-dominio.com"]
SMTP_HOST=smtp.tu-proveedor.com
SMTP_PORT=587
SMTP_TLS=true
EMAILS_FROM_EMAIL=noreply@tu-dominio.com

# S3 real (AWS) — omitir S3_ENDPOINT_URL para usar AWS S3 nativo
S3_ACCESS_KEY_ID=<tu-access-key>
S3_SECRET_ACCESS_KEY=<tu-secret-key>
S3_BUCKET_NAME=<tu-bucket>
S3_REGION=us-east-1
```

### B.8.5 Construir y desplegar

```bash
# Construir imágenes con la etiqueta de versión
TAG=v1.0.0 docker compose build

# Iniciar todos los servicios
TAG=v1.0.0 docker compose up -d

# Verificar estado
docker compose ps
docker compose logs -f
```

Los servicios se levantan en este orden:
1. `db` — espera estar healthy (hasta 30s).
2. `prestart` — ejecuta migraciones y datos iniciales.
3. `backend` y `frontend` — arrancan tras `prestart`.
4. `adminer` — panel de administración de BD.

### B.8.6 Actualización de la aplicación

```bash
# Obtener la nueva versión
git pull origin main

# Reconstruir imágenes
TAG=v1.1.0 docker compose build

# Reiniciar servicios (downtime mínimo: solo el backend se reinicia)
TAG=v1.1.0 docker compose up -d --no-deps backend frontend

# Las migraciones se aplican automáticamente al iniciar prestart
```

---

## B.9 Monitoreo y Mantenimiento

### B.9.1 Estado de los servicios

```bash
docker compose ps                    # Estado de todos los contenedores
docker stats                         # Uso de CPU/RAM en tiempo real
docker compose exec db psql -U postgres -c "\l"   # Listar BDs en PostgreSQL
```

### B.9.2 Backup de la base de datos

```bash
# Crear un backup
docker compose exec db pg_dump -U postgres app > backup_$(date +%Y%m%d).sql

# Restaurar un backup
docker compose exec -T db psql -U postgres app < backup_20260401.sql
```

### B.9.3 Limpiar recursos no usados

```bash
docker system prune -f              # Elimina imágenes, contenedores y redes sin usar
docker volume prune -f              # Elimina volúmenes sin usar (¡precaución en producción!)
```

---

## B.10 Solución de Problemas

| Problema | Causa probable | Solución |
|----------|---------------|----------|
| El backend no inicia | BD no está disponible | Verificar que `db` esté `healthy` con `docker compose ps`. Revisar `POSTGRES_*` en `.env`. |
| Error de migraciones al iniciar | Migración incompatible | Ejecutar `docker compose exec backend alembic history` y `alembic current`. Corregir el script de migración. |
| `502 Bad Gateway` en el frontend | Backend no responde | Verificar logs del backend: `docker compose logs backend`. Comprobar el healthcheck. |
| Emails no se envían (producción) | SMTP mal configurado | Verificar `SMTP_HOST`, `SMTP_PORT` y credenciales. Probar con `telnet $SMTP_HOST $SMTP_PORT`. |
| MinIO no accesible | Variables de entorno incorrectas | Verificar `S3_ENDPOINT_URL`, `S3_ACCESS_KEY_ID` y `S3_BUCKET_NAME` en `.env`. |
| `Secret key too short` al iniciar | `SECRET_KEY` es demasiado corta | Generar una clave con `openssl rand -hex 32` y actualizar `.env`. |
| Traefik no renueva el certificado TLS | Puerto 80 bloqueado o DNS incorrecto | Verificar que el dominio resuelva a la IP correcta y el puerto 80 esté abierto. |
| Error `UNIQUE constraint` al insertar | Dato duplicado en BD | Verificar que el SKU, slug u otro campo único no esté repetido. |

---

*Documento generado como parte del proyecto de grado — Universidad Sergio Arboleda, Semillero de Software como Innovación, Abril 2026.*
