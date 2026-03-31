# Anexo C — Documentación Técnica

**OrbitEngine** — Plataforma SaaS para la Gestión de Procesos Internos en Pymes  
Versión: 1.0 | Abril 2026  
Universidad Sergio Arboleda — Semillero de Software como Innovación

---

## C.1 Stack Tecnológico

### C.1.1 Backend

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| Lenguaje | Python | 3.10+ | Lenguaje principal del backend |
| Framework web | FastAPI | 0.115+ | API REST asíncrona con tipado estricto |
| ORM + Schemas | SQLModel | 0.0.21+ | Modelos compartidos entre SQLAlchemy y Pydantic |
| Motor de BD | SQLAlchemy | 2.x | Capa de abstracción de base de datos |
| Driver PostgreSQL | Psycopg3 | 3.x | Conector PostgreSQL para Python |
| Migraciones | Alembic | 1.x | Gestión de migraciones de esquema |
| Autenticación | PyJWT | 2.x | Generación y verificación de tokens JWT |
| Hash de contraseñas | Pwdlib | 0.2+ | Hashing seguro con bcrypt |
| Validación | Pydantic | 2.x | Schemas de entrada/salida de datos |
| Configuración | Pydantic-Settings | 2.x | Variables de entorno tipadas |
| Linter/Formatter | Ruff | 0.6+ | Análisis estático y formato de código |
| Verificación de tipos | Mypy | 1.x | Chequeo de tipos estático en modo estricto |
| Testing | Pytest + Coverage | 8.x | Pruebas unitarias e integración |
| Monitoring | Sentry (opcional) | — | Rastreo de errores en producción |

### C.1.2 Frontend

| Componente | Tecnología | Versión | Propósito |
|------------|-----------|---------|-----------|
| Lenguaje | TypeScript | 5.x | Tipado estático sobre JavaScript |
| Framework UI | React | 19.x | Librería de componentes reactivos |
| Build tool | Vite | 6.x | Empaquetado y servidor de desarrollo |
| Router | TanStack Router | 1.x | Enrutamiento con tipado por archivo |
| Server state | TanStack Query | 5.x | Cache y sincronización de datos del servidor |
| Tablas | TanStack Table | 8.x | Tablas con sorting/filtering/paginación |
| Formularios | React Hook Form | 7.x | Manejo de formularios con rendimiento optimizado |
| Validación | Zod | 3.x | Schemas de validación con inferencia de tipos |
| UI Components | Shadcn/ui | — | Componentes base sobre Radix UI |
| Estilos | Tailwind CSS | 4.x | Utilidades CSS de bajo nivel |
| Gráficos | Recharts | 2.x | Gráficas para el dashboard |
| HTTP Client | Axios (generado) | — | Cliente OpenAPI auto-generado |
| Notificaciones | Sonner | 1.x | Toasts y notificaciones |
| Íconos | Lucide React | 0.4+ | Librería de íconos SVG |
| Linter/Formatter | Biome | 1.x | Análisis estático y formato |
| E2E Testing | Playwright | 1.x | Pruebas end-to-end en navegador |

### C.1.3 Infraestructura

| Componente | Tecnología | Propósito |
|------------|-----------|-----------|
| Base de datos | PostgreSQL 18 | Almacenamiento relacional principal |
| Contenedores | Docker Compose v2 | Orquestación de servicios |
| Reverse proxy | Traefik 3.6 | Enrutamiento HTTP/HTTPS + TLS automático |
| Almacenamiento | MinIO (dev) / AWS S3 (prod) | Almacenamiento de objetos S3-compatible |
| CI/CD | GitHub Actions | Pipeline de integración y entrega continua |
| Panel de BD | Adminer | Administración web de PostgreSQL |
| Email (dev) | Mailcatcher | Interceptor SMTP para desarrollo |

---

## C.2 Estructura del Proyecto

```
orbit-engine/
├── .env                        # Variables de entorno (no incluir en git)
├── compose.yml                 # Configuración Docker Compose base
├── compose.override.yml        # Sobreescrituras para desarrollo local
├── compose.traefik.yml         # Traefik para producción
├── pyproject.toml              # Configuración Ruff y Mypy (nivel raíz)
│
├── backend/
│   ├── Dockerfile
│   ├── pyproject.toml          # Dependencias Python (uv)
│   ├── scripts/
│   │   ├── prestart.sh         # Ejecutado por el servicio prestart
│   │   ├── test.sh             # Script de pruebas con cobertura
│   │   ├── lint.sh             # Mypy + Ruff check
│   │   └── format.sh           # Ruff format
│   └── app/
│       ├── main.py             # Punto de entrada FastAPI + registro de routers
│       ├── models.py           # Todos los modelos SQLModel + schemas Pydantic
│       ├── crud.py             # Operaciones de base de datos
│       ├── utils.py            # Helpers (email, generación de tokens)
│       ├── backend_pre_start.py # Script de inicialización
│       ├── initial_data.py     # Seed de datos iniciales (roles, superusuario)
│       ├── api/
│       │   ├── deps.py         # Dependencias FastAPI (auth, sesión, roles)
│       │   └── routes/
│       │       ├── login.py            # Autenticación y recuperación de contraseña
│       │       ├── users.py            # Gestión de usuarios
│       │       ├── organizations.py    # Registro y configuración de organización
│       │       ├── roles.py            # Listado de roles
│       │       ├── categories.py       # CRUD de categorías
│       │       ├── products.py         # CRUD de productos + stock
│       │       ├── customers.py        # CRUD de clientes
│       │       ├── sales.py            # Registro y gestión de ventas
│       │       ├── inventory_movements.py  # Historial de movimientos
│       │       ├── dashboard.py        # Estadísticas del dashboard
│       │       ├── utils.py            # Health check
│       │       └── private.py          # Endpoints de superusuario
│       ├── core/
│       │   ├── config.py       # Settings con Pydantic-Settings
│       │   ├── db.py           # Engine SQLAlchemy
│       │   └── security.py     # JWT, hashing de contraseñas
│       └── alembic/
│           ├── env.py
│           └── versions/
│               ├── 001_initial_schema.py   # organizations, roles, users
│               ├── 002_categories.py
│               ├── 003_products.py
│               ├── 004_customers.py
│               ├── 005_inventory_movements.py
│               └── 006_sales.py
│
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── vite.config.ts
│   ├── openapi-ts.config.ts    # Configuración del generador de cliente API
│   └── src/
│       ├── main.tsx            # Punto de entrada React
│       ├── routeTree.gen.ts    # Árbol de rutas auto-generado (no editar)
│       ├── utils.ts            # Helpers compartidos
│       ├── client/             # Cliente API auto-generado (no editar)
│       │   ├── index.ts
│       │   ├── sdk.gen.ts      # Funciones de llamada a la API
│       │   ├── types.gen.ts    # Tipos TypeScript desde OpenAPI
│       │   ├── schemas.gen.ts
│       │   └── core/           # Configuración Axios
│       ├── components/
│       │   ├── Admin/          # Componentes de gestión de usuarios
│       │   ├── Common/         # Componentes reutilizables (DataTable, layouts)
│       │   ├── Customers/      # Componentes del módulo de clientes
│       │   ├── Inventory/      # Componentes del módulo de inventario
│       │   ├── Landing/        # Componentes de la página pública
│       │   ├── Pending/        # Componentes de estados de carga
│       │   ├── Sales/          # Componentes del módulo de ventas
│       │   ├── Sidebar/        # Navegación principal
│       │   ├── UserSettings/   # Configuración de perfil y organización
│       │   ├── theme-provider.tsx
│       │   └── ui/             # Componentes Shadcn/ui (no editar)
│       ├── hooks/
│       │   ├── useAuth.ts
│       │   ├── useCopyToClipboard.ts
│       │   ├── useCustomToast.ts
│       │   ├── useDebounce.ts
│       │   ├── useMobile.ts
│       │   └── useScrollAnimation.ts
│       ├── lib/
│       │   └── utils.ts        # cn() helper para Tailwind
│       └── routes/
│           ├── __root.tsx      # Layout raíz con providers
│           ├── index.tsx       # Landing page (/)
│           ├── login.tsx       # Inicio de sesión (/login)
│           ├── signup.tsx      # Registro de usuario (/signup)
│           ├── signup-org.tsx  # Registro de organización (/signup-org)
│           ├── recover-password.tsx
│           ├── reset-password.tsx
│           └── dashboard/
│               ├── index.tsx   # Dashboard KPIs (/dashboard)
│               ├── inventory.tsx
│               ├── sales.tsx
│               ├── customers.tsx
│               ├── admin.tsx
│               └── settings.tsx
│
└── docs/
    └── informe-final/          # Documentación del proyecto de grado
```

---

## C.3 Autenticación y Autorización

### C.3.1 Flujo de autenticación

OrbitEngine usa **JWT Bearer Tokens** siguiendo el estándar OAuth2 Password Flow:

1. El cliente envía credenciales a `POST /api/v1/login/access-token`.
2. El backend valida las credenciales, verifica que la cuenta no esté bloqueada.
3. Si son válidas, retorna un `access_token` JWT.
4. El cliente incluye el token en el header `Authorization: Bearer <token>` en cada request.
5. El backend decodifica el token, extrae el `sub` (UUID del usuario) y carga el usuario de la BD.
6. La organización del usuario se extrae de `user.organization_id` — no del token directamente.

**Parámetros del token:**

| Parámetro | Valor |
|-----------|-------|
| Algoritmo | HS256 |
| Payload `sub` | UUID del usuario (`str`) |
| Expiración | 8 días (11,520 minutos) |
| Clave de firma | `SECRET_KEY` del entorno |

### C.3.2 Control de acceso basado en roles (RBAC)

Los roles se almacenan en la tabla `roles` con permisos como array JSONB. La verificación en los endpoints usa la dependencia `require_role()`:

```python
# Solo administradores pueden crear usuarios
@router.post("/", dependencies=[Depends(require_role("admin"))])
def create_user(...) -> Any: ...

# Administradores y vendedores pueden registrar ventas
@router.post("/", dependencies=[Depends(require_role("admin", "seller"))])
def create_sale(...) -> Any: ...
```

**Dependencias de autenticación disponibles:**

| Tipo anotado | Descripción |
|-------------|-------------|
| `CurrentUser` | Usuario autenticado; error 403 si token inválido |
| `CurrentAdminUser` | Usuario autenticado con rol `admin`; error 403 si no |
| `CurrentOrganization` | UUID de organización extraído del `CurrentUser` |
| `SessionDep` | Sesión de base de datos SQLModel |

### C.3.3 Protección contra fuerza bruta

El modelo `User` incluye campos `failed_login_attempts` y `locked_until`. Tras N intentos fallidos consecutivos, la cuenta se bloquea temporalmente.

---

## C.4 API REST — Referencia de Endpoints

Todos los endpoints están prefijados con `/api/v1`. La documentación interactiva se sirve en `/docs` (Swagger UI) y `/redoc`.

### C.4.1 Autenticación (`/login`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/login/access-token` | No | Obtener token JWT (login) |
| POST | `/login/test-token` | Sí | Verificar validez del token |
| POST | `/password-recovery/{email}` | No | Solicitar enlace de recuperación |
| POST | `/reset-password` | No | Restablecer contraseña con token |

### C.4.2 Usuarios (`/users`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/users/` | Sí | admin | Listar usuarios de la organización |
| POST | `/users/` | Sí | admin | Crear usuario en la organización |
| GET | `/users/me` | Sí | Cualquiera | Obtener perfil propio |
| PATCH | `/users/me` | Sí | Cualquiera | Actualizar nombre/apellido/teléfono |
| DELETE | `/users/me` | Sí | Cualquiera | Eliminar cuenta propia (soft delete) |
| PATCH | `/users/me/password` | Sí | Cualquiera | Cambiar contraseña |
| GET | `/users/{user_id}` | Sí | admin | Obtener usuario por ID |
| PATCH | `/users/{user_id}` | Sí | admin | Actualizar usuario |
| DELETE | `/users/{user_id}` | Sí | admin | Eliminar usuario |

### C.4.3 Organizaciones (`/organizations`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/organizations/me` | Sí | Cualquiera | Ver datos de la organización actual |
| PATCH | `/organizations/me` | Sí | admin | Actualizar nombre/slug/descripción |
| POST | `/organizations/signup` | No | — | Registro de nueva organización + admin |

### C.4.4 Roles (`/roles`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/roles/` | Sí | Listar roles disponibles en la organización |

### C.4.5 Categorías (`/categories`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/categories/` | Sí | Cualquiera | Listar categorías (soporta `search`, `is_active`) |
| POST | `/categories/` | Sí | admin | Crear categoría |
| GET | `/categories/{id}` | Sí | Cualquiera | Obtener categoría por ID |
| PATCH | `/categories/{id}` | Sí | admin | Actualizar categoría |
| DELETE | `/categories/{id}` | Sí | admin | Eliminar / desactivar categoría |

### C.4.6 Productos (`/products`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/products/` | Sí | Cualquiera | Listar productos (`search`, `is_active`, `category_id`, `sort_by`) |
| POST | `/products/` | Sí | admin | Crear producto |
| GET | `/products/{id}` | Sí | Cualquiera | Obtener producto por ID |
| PATCH | `/products/{id}` | Sí | admin | Actualizar producto |
| DELETE | `/products/{id}` | Sí | admin | Eliminar / desactivar producto |
| POST | `/products/{id}/stock-adjustment` | Sí | admin | Ajuste manual de stock |
| GET | `/products/{id}/movements` | Sí | Cualquiera | Historial de movimientos del producto |

### C.4.7 Clientes (`/customers`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/customers/` | Sí | Cualquiera | Listar clientes (`search`, `is_active`) |
| POST | `/customers/` | Sí | Cualquiera | Registrar cliente |
| GET | `/customers/{id}` | Sí | Cualquiera | Obtener cliente por ID |
| PATCH | `/customers/{id}` | Sí | Cualquiera | Actualizar cliente |
| DELETE | `/customers/{id}` | Sí | admin | Desactivar cliente |
| GET | `/customers/{id}/sales` | Sí | Cualquiera | Historial de compras del cliente |

### C.4.8 Ventas (`/sales`)

| Método | Ruta | Auth | Rol mínimo | Descripción |
|--------|------|------|-----------|-------------|
| GET | `/sales/` | Sí | Cualquiera | Listar ventas (`search`, `status`, `payment_method`, `sort_by`) |
| POST | `/sales/` | Sí | Cualquiera | Registrar venta (descuenta stock automáticamente) |
| GET | `/sales/{id}` | Sí | Cualquiera | Obtener venta por ID |
| POST | `/sales/{id}/cancel` | Sí | admin | Cancelar venta (revierte stock) |

### C.4.9 Movimientos de inventario (`/inventory-movements`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/inventory-movements/` | Sí | Listar movimientos (`product_id`, `movement_type`, `sort_by`) |

### C.4.10 Dashboard (`/dashboard`)

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/dashboard/stats` | Sí | Estadísticas consolidadas de la organización |

**Respuesta de `/dashboard/stats`:**

```json
{
  "sales_today": { "count": 5, "total": "250000.00" },
  "sales_month": { "count": 42, "total": "1850000.00" },
  "low_stock_count": 3,
  "average_ticket": "44047.62",
  "top_products": [
    { "product_id": "...", "product_name": "Producto A", "quantity_sold": 15, "revenue": "450000.00" }
  ],
  "sales_by_day": [
    { "date": "2026-04-01", "count": 3, "total": "120000.00" }
  ]
}
```

### C.4.11 Utilidades

| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/utils/health-check/` | No | Health check del servicio backend |

---

## C.5 Modelos de Datos

### C.5.1 Organization

```
organizations
├── id              UUID           PK
├── name            VARCHAR(255)   NOT NULL
├── slug            VARCHAR(100)   UNIQUE, INDEX
├── description     TEXT           NULLABLE
├── logo_url        VARCHAR(500)   NULLABLE
├── is_active       BOOLEAN        DEFAULT true
├── created_at      TIMESTAMPTZ    NOT NULL
└── updated_at      TIMESTAMPTZ    NOT NULL

Índices: idx_organizations_slug (unique), idx_organizations_is_active
```

**Validación del slug:** expresión regular `^[a-z0-9-]{3,50}$` (solo minúsculas, números y guiones).

### C.5.2 Role

```
roles
├── id              INTEGER        PK (autoincrement)
├── name            VARCHAR(50)    UNIQUE, INDEX
├── description     TEXT           NULLABLE
├── permissions     JSONB          DEFAULT []
└── created_at      TIMESTAMPTZ    NOT NULL

Índices: idx_roles_name (unique)
```

### C.5.3 User

```
users
├── id                     UUID           PK
├── organization_id        UUID           FK → organizations.id, INDEX
├── role_id                INTEGER        FK → roles.id, INDEX
├── email                  VARCHAR(255)   INDEX
├── first_name             VARCHAR(100)   NOT NULL
├── last_name              VARCHAR(100)   NOT NULL
├── phone                  VARCHAR(50)    NULLABLE
├── avatar_url             VARCHAR(500)   NULLABLE
├── hashed_password        VARCHAR(255)   NOT NULL
├── is_active              BOOLEAN        DEFAULT true
├── is_verified            BOOLEAN        DEFAULT false
├── last_login_at          TIMESTAMPTZ    NULLABLE
├── failed_login_attempts  INTEGER        DEFAULT 0
├── locked_until           TIMESTAMPTZ    NULLABLE
├── created_at             TIMESTAMPTZ    NOT NULL
├── updated_at             TIMESTAMPTZ    NOT NULL
└── deleted_at             TIMESTAMPTZ    NULLABLE (soft delete)

Restricciones: UNIQUE(organization_id, email)
Índices: idx_users_organization_id, idx_users_role_id, idx_users_is_active
```

### C.5.4 Category

```
categories
├── id              UUID           PK
├── organization_id UUID           FK → organizations.id, INDEX
├── parent_id       UUID           FK → categories.id, NULLABLE (jerarquía)
├── name            VARCHAR(255)   NOT NULL
├── description     TEXT           NULLABLE
├── is_active       BOOLEAN        DEFAULT true
├── created_at      TIMESTAMPTZ    NOT NULL
├── updated_at      TIMESTAMPTZ    NOT NULL
└── deleted_at      TIMESTAMPTZ    NULLABLE (soft delete)

Restricciones: UNIQUE(organization_id, name, parent_id)
Índices: idx_categories_organization_id, idx_categories_parent_id, idx_categories_is_active
```

### C.5.5 Product

```
products
├── id              UUID               PK
├── organization_id UUID               FK → organizations.id, INDEX
├── category_id     UUID               FK → categories.id, NULLABLE
├── name            VARCHAR(255)       NOT NULL
├── sku             VARCHAR(100)       NOT NULL
├── description     TEXT               NULLABLE
├── image_url       VARCHAR(500)       NULLABLE
├── cost_price      NUMERIC(12,2)      DEFAULT 0
├── sale_price      NUMERIC(12,2)      DEFAULT 0
├── stock_quantity  INTEGER            DEFAULT 0
├── stock_min       INTEGER            DEFAULT 0
├── stock_max       INTEGER            NULLABLE
├── unit            VARCHAR(50)        DEFAULT 'unit'
├── barcode         VARCHAR(100)       NULLABLE
├── is_active       BOOLEAN            DEFAULT true
├── created_at      TIMESTAMPTZ        NOT NULL
├── updated_at      TIMESTAMPTZ        NOT NULL
└── deleted_at      TIMESTAMPTZ        NULLABLE (soft delete)

Restricciones: UNIQUE(organization_id, sku)
Índices: idx_products_organization_id, idx_products_category_id, idx_products_is_active, idx_products_sku
```

**Stock bajo:** un producto está en alerta cuando `stock_quantity ≤ stock_min`.

### C.5.6 Customer

```
customers
├── id                UUID           PK
├── organization_id   UUID           FK → organizations.id, INDEX
├── document_type     VARCHAR(50)    NOT NULL (CC, NIT, Pasaporte, Otro)
├── document_number   VARCHAR(50)    NOT NULL
├── first_name        VARCHAR(100)   NOT NULL
├── last_name         VARCHAR(100)   NOT NULL
├── email             VARCHAR(255)   NULLABLE, INDEX
├── phone             VARCHAR(50)    NULLABLE, INDEX
├── address           TEXT           NULLABLE
├── city              VARCHAR(100)   NULLABLE
├── country           VARCHAR(100)   NULLABLE
├── notes             TEXT           NULLABLE
├── is_active         BOOLEAN        DEFAULT true
├── total_purchases   NUMERIC(12,2)  DEFAULT 0 (actualizado automáticamente)
├── purchases_count   INTEGER        DEFAULT 0 (actualizado automáticamente)
├── last_purchase_at  TIMESTAMPTZ    NULLABLE (actualizado automáticamente)
├── created_at        TIMESTAMPTZ    NOT NULL
├── updated_at        TIMESTAMPTZ    NOT NULL
└── deleted_at        TIMESTAMPTZ    NULLABLE (soft delete)

Restricciones: UNIQUE(organization_id, document_number)
Índices: idx_customers_organization_id, idx_customers_email, idx_customers_phone, idx_customers_is_active
```

### C.5.7 Sale

```
sales
├── id                   UUID           PK
├── organization_id      UUID           FK → organizations.id, INDEX
├── customer_id          UUID           FK → customers.id, NULLABLE
├── user_id              UUID           FK → users.id, INDEX
├── invoice_number       VARCHAR(100)   NOT NULL
├── sale_date            TIMESTAMPTZ    NOT NULL
├── subtotal             NUMERIC(12,2)  DEFAULT 0
├── discount             NUMERIC(12,2)  DEFAULT 0
├── tax                  NUMERIC(12,2)  DEFAULT 0
├── total                NUMERIC(12,2)  DEFAULT 0
├── payment_method       VARCHAR(50)    DEFAULT 'cash' (cash/card/transfer/other)
├── status               VARCHAR(50)    DEFAULT 'completed' (completed/cancelled/pending)
├── notes                TEXT           NULLABLE
├── cancelled_at         TIMESTAMPTZ    NULLABLE
├── cancelled_by         UUID           FK → users.id, NULLABLE
├── cancellation_reason  TEXT           NULLABLE
├── created_at           TIMESTAMPTZ    NOT NULL
└── updated_at           TIMESTAMPTZ    NOT NULL

Restricciones: UNIQUE(organization_id, invoice_number)
Índices: idx_sales_organization_id, idx_sales_customer_id, idx_sales_user_id,
         idx_sales_status, idx_sales_sale_date, idx_sales_invoice_number
```

**Fórmula:** `total = subtotal - discount + tax`

### C.5.8 SaleItem

```
sale_items
├── id            UUID           PK
├── sale_id       UUID           FK → sales.id, INDEX
├── product_id    UUID           FK → products.id, INDEX
├── product_name  VARCHAR(255)   NOT NULL (snapshot al momento de la venta)
├── product_sku   VARCHAR(100)   NOT NULL (snapshot)
├── quantity      INTEGER        NOT NULL
├── unit_price    NUMERIC(12,2)  NOT NULL
├── subtotal      NUMERIC(12,2)  NOT NULL
└── created_at    TIMESTAMPTZ    NOT NULL

Índices: idx_sale_items_sale_id, idx_sale_items_product_id
```

> Los campos `product_name` y `product_sku` son snapshots del producto en el momento de la venta. Si el producto se edita posteriormente, el historial de ventas conserva los datos originales.

### C.5.9 InventoryMovement

```
inventory_movements
├── id              UUID           PK
├── organization_id UUID           FK → organizations.id, INDEX
├── product_id      UUID           FK → products.id, INDEX
├── user_id         UUID           FK → users.id, INDEX
├── movement_type   VARCHAR(50)    NOT NULL (sale/adjustment/return/purchase)
├── quantity        INTEGER        NOT NULL (positivo = entrada, negativo = salida)
├── previous_stock  INTEGER        NOT NULL
├── new_stock       INTEGER        NOT NULL
├── reference_id    UUID           NULLABLE (FK al objeto de origen)
├── reference_type  VARCHAR(50)    NULLABLE (sale/adjustment/return)
├── reason          TEXT           NULLABLE
└── created_at      TIMESTAMPTZ    NOT NULL

Índices: idx_inventory_movements_organization_id, idx_inventory_movements_product_id,
         idx_inventory_movements_user_id, idx_inventory_movements_movement_type,
         idx_inventory_movements_created_at,
         idx_inventory_movements_reference (reference_type, reference_id)
```

---

## C.6 Variables de Entorno

La configuración se carga desde el archivo `.env` usando Pydantic-Settings. Todas las variables se validan al iniciar el servicio.

### C.6.1 Variables requeridas

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `PROJECT_NAME` | `str` | Nombre del proyecto |
| `SECRET_KEY` | `str` | Clave para firmar los JWT |
| `POSTGRES_SERVER` | `str` | Host del servidor PostgreSQL |
| `POSTGRES_USER` | `str` | Usuario de PostgreSQL |
| `POSTGRES_DB` | `str` | Nombre de la base de datos |
| `FIRST_SUPERUSER` | `EmailStr` | Email del superusuario inicial |
| `FIRST_SUPERUSER_PASSWORD` | `str` | Contraseña del superusuario inicial |

### C.6.2 Variables opcionales con valores por defecto

| Variable | Tipo | Default | Descripción |
|----------|------|---------|-------------|
| `POSTGRES_PORT` | `int` | `5432` | Puerto de PostgreSQL |
| `POSTGRES_PASSWORD` | `str` | `""` | Contraseña de PostgreSQL |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `int` | `11520` | Expiración del JWT (8 días) |
| `FRONTEND_HOST` | `str` | `http://localhost:5173` | URL del frontend para CORS |
| `BACKEND_CORS_ORIGINS` | `list[str]` | `[]` | Orígenes adicionales CORS |
| `ENVIRONMENT` | `Literal` | `"local"` | `local` \| `staging` \| `production` |
| `SMTP_HOST` | `str\|None` | `None` | Host SMTP para envío de emails |
| `SMTP_PORT` | `int` | `587` | Puerto SMTP |
| `SMTP_TLS` | `bool` | `True` | Usar TLS en SMTP |
| `SMTP_SSL` | `bool` | `False` | Usar SSL en SMTP |
| `SMTP_USER` | `str\|None` | `None` | Usuario SMTP |
| `SMTP_PASSWORD` | `str\|None` | `None` | Contraseña SMTP |
| `EMAILS_FROM_EMAIL` | `EmailStr\|None` | `None` | Email remitente |
| `EMAIL_RESET_TOKEN_EXPIRE_HOURS` | `int` | `48` | Expiración del token de reset |
| `SENTRY_DSN` | `HttpUrl\|None` | `None` | DSN de Sentry para error tracking |
| `S3_ENDPOINT_URL` | `str\|None` | `None` | Endpoint S3 (MinIO en dev) |
| `S3_ACCESS_KEY_ID` | `str\|None` | `None` | Access key para S3/MinIO |
| `S3_SECRET_ACCESS_KEY` | `str\|None` | `None` | Secret key para S3/MinIO |
| `S3_BUCKET_NAME` | `str\|None` | `None` | Nombre del bucket S3 |
| `S3_REGION` | `str` | `"us-east-1"` | Región S3 |

### C.6.3 Propiedades calculadas (no en `.env`)

| Propiedad | Descripción |
|-----------|-------------|
| `SQLALCHEMY_DATABASE_URI` | URI completa de conexión a PostgreSQL |
| `all_cors_origins` | `BACKEND_CORS_ORIGINS` + `FRONTEND_HOST` |
| `emails_enabled` | `True` si `SMTP_HOST` y `EMAILS_FROM_EMAIL` están configurados |
| `s3_enabled` | `True` si las tres variables S3 clave están configuradas |

---

## C.7 Convenciones de Código

### C.7.1 Backend (Python)

**Orden de imports:**
```python
# 1. Biblioteca estándar
import uuid
from typing import Any
from decimal import Decimal

# 2. Terceros
from fastapi import APIRouter, HTTPException
from sqlmodel import SQLModel, Field

# 3. Locales
from app.api.deps import CurrentUser, SessionDep
from app.models import ProductCreate, ProductPublic
```

**Nomenclatura:**
- Funciones y variables: `snake_case`
- Clases y modelos: `PascalCase`
- Modelos de BD: singular (`Product`, `Sale`)
- Schemas: `{Modelo}Create`, `{Modelo}Update`, `{Modelo}Public`, `{Modelo}sPublic`
- Aliases de tipo: `PascalCase` con `Annotated` (`CurrentUser`, `SessionDep`)

**Anotaciones de tipo:** obligatorias en todas las funciones. Usar `str | None` (no `Optional[str]`).

**Patrón de rutas:**
```python
@router.post("/", response_model=ProductPublic)
def create_product(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    current_organization: CurrentOrganization,
    product_in: ProductCreate,
) -> Any:
    product = Product.model_validate(product_in, update={"organization_id": current_organization})
    session.add(product)
    session.commit()
    session.refresh(product)
    return product
```

**Códigos HTTP usados:**
- `400` — Solicitud inválida (datos incorrectos)
- `403` — Sin permisos / credenciales inválidas
- `404` — Recurso no encontrado
- `409` — Conflicto (recurso duplicado)

**Multi-tenancy:** **todas** las consultas de negocio incluyen filtro `organization_id = current_organization`. El valor se extrae del usuario autenticado, nunca del cuerpo del request.

### C.7.2 Frontend (TypeScript/React)

**Orden de imports:**
```typescript
// 1. Externos
import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { z } from "zod"

// 2. Internos (alias @/)
import { ProductsService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import { useCustomToast } from "@/hooks/useCustomToast"
```

**Componentes:** solo funcionales, un componente por archivo, nombre de archivo en `PascalCase`.

**Patrón de mutación:**
```typescript
const mutation = useMutation({
  mutationFn: (data: ProductCreate) =>
    ProductsService.createProduct({ requestBody: data }),
  onSuccess: () => showSuccessToast("Producto creado"),
  onError: (err) => handleError(err),
  onSettled: () => queryClient.invalidateQueries({ queryKey: ["products"] }),
})
```

**Validación de formularios:** React Hook Form + Zod schemas con `zodResolver`.

**No editar:**
- `src/client/**` — auto-generado desde OpenAPI
- `src/components/ui/**` — componentes Shadcn/ui
- `src/routeTree.gen.ts` — auto-generado por TanStack Router

---

## C.8 Pipeline de CI/CD

El repositorio incluye workflows de GitHub Actions:

### C.8.1 Workflow de pruebas (en cada PR y push a `main`)

1. **Backend:** Ejecuta `uv run bash scripts/test.sh` — incluye Mypy, Ruff y Pytest con cobertura.
2. **Frontend:** Ejecuta `bun run lint` — Biome linting y verificación de tipos TypeScript.

### C.8.2 Workflow de despliegue

Al hacer merge a `main`:
1. Construye las imágenes Docker de backend y frontend.
2. Las etiqueta con el hash del commit y con `latest`.
3. Las publica en el registro de imágenes.
4. Actualiza los contenedores en el servidor de producción via SSH.

---

## C.9 Estructura de Pruebas

### C.9.1 Backend (pytest)

```
backend/tests/
├── conftest.py                     # Fixtures globales: db, client, auth headers
├── api/routes/
│   ├── test_login.py               # Autenticación, recuperación de contraseña
│   ├── test_users.py               # CRUD de usuarios, cambio de contraseña
│   ├── test_categories.py          # CRUD de categorías
│   ├── test_products.py            # CRUD de productos, ajuste de stock
│   ├── test_customers.py           # CRUD de clientes, historial de compras
│   ├── test_sales.py               # Registro y cancelación de ventas
│   ├── test_inventory_movements.py # Listado de movimientos
│   ├── test_dashboard.py           # Estadísticas del dashboard
│   └── test_private.py             # Endpoints de superusuario
└── crud/
    ├── test_user.py
    ├── test_category.py
    ├── test_product.py
    ├── test_customer.py
    ├── test_sale.py
    ├── test_inventory_movement.py
    └── test_dashboard.py
```

**Fixtures disponibles en conftest.py:**

| Fixture | Descripción |
|---------|-------------|
| `db` | Sesión de BD para pruebas (con rollback automático) |
| `client` | `TestClient` de FastAPI |
| `superuser_token_headers` | Headers con token del superusuario |
| `normal_user_token_headers` | Headers con token de usuario normal |

**Ejecutar pruebas:**
```bash
cd backend
uv run bash scripts/test.sh           # Todos los tests con cobertura
uv run pytest tests/api/routes/ -v    # Solo tests de API
uv run pytest -k "test_create" -v     # Tests por patrón
```

### C.9.2 Frontend (Playwright E2E)

```
frontend/tests/
├── auth.setup.ts                   # Configuración de autenticación compartida
├── config.ts                       # Variables de configuración de tests
├── login.spec.ts                   # Flujo de inicio de sesión
├── sign-up.spec.ts                 # Registro de usuario
├── organization-signup.spec.ts     # Registro de organización
├── reset-password.spec.ts          # Recuperación de contraseña
├── inventory.spec.ts               # Módulo de inventario
├── sales.spec.ts                   # Módulo de ventas
├── customers.spec.ts               # Módulo de clientes
├── admin.spec.ts                   # Gestión de usuarios
├── user-settings.spec.ts           # Configuración de cuenta
└── utils/                          # Helpers de pruebas E2E
```

---

## C.10 Generación del Cliente API

El cliente TypeScript del frontend se genera automáticamente desde el esquema OpenAPI del backend:

```bash
# El backend debe estar corriendo en http://localhost:8000
cd frontend
bun run generate-client
```

La configuración del generador está en `frontend/openapi-ts.config.ts`. Los archivos generados en `src/client/` no deben editarse manualmente; cualquier cambio se sobreescribirá en la próxima generación.

---

## C.11 Multi-Tenancy

OrbitEngine implementa multi-tenancy mediante **aislamiento por discriminador en tablas compartidas** (Shared Database, Separate Rows):

- Todas las tablas de negocio (`categories`, `products`, `customers`, `sales`, `sale_items`, `inventory_movements`) incluyen la columna `organization_id`.
- La `organization_id` se indexa en cada tabla para garantizar rendimiento en consultas filtradas.
- Toda consulta de datos de negocio filtra por `organization_id = current_user.organization_id`.
- El valor de `organization_id` **nunca** se acepta como parámetro del request; siempre se extrae del token JWT del usuario autenticado.
- Las restricciones de unicidad incluyen `organization_id` como parte de la clave compuesta (ej. `UNIQUE(organization_id, sku)`), permitiendo que el mismo SKU exista en organizaciones distintas.

Esta estrategia garantiza aislamiento completo de datos entre tenants sin necesidad de esquemas o bases de datos separadas, facilitando el mantenimiento y la escalabilidad horizontal.

---

*Documento generado como parte del proyecto de grado — Universidad Sergio Arboleda, Semillero de Software como Innovación, Abril 2026.*
