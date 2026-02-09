# Documentacion del Backend - OrbitEngine

## Indice

1. [Resumen General](#resumen-general)
2. [Arquitectura del Backend](#arquitectura-del-backend)
3. [Paso 1: Sistema Multi-Tenant con Roles y Autenticacion](#paso-1-sistema-multi-tenant-con-roles-y-autenticacion)
4. [Paso 2: Modulo de Categorias](#paso-2-modulo-de-categorias)
5. [Paso 3: Modulo de Productos](#paso-3-modulo-de-productos)
6. [Paso 4: Modulo de Clientes](#paso-4-modulo-de-clientes)
7. [Paso 5: Modulo de Movimientos de Inventario](#paso-5-modulo-de-movimientos-de-inventario)
8. [Paso 6: Modulo de Ventas](#paso-6-modulo-de-ventas)
9. [Paso 7: Dashboard (KPIs y Estadisticas)](#paso-7-dashboard-kpis-y-estadisticas)
10. [Errores Encontrados y Soluciones](#errores-encontrados-y-soluciones)
11. [Resultados de Testing](#resultados-de-testing)
12. [Comandos de Referencia](#comandos-de-referencia)

---

## Resumen General

OrbitEngine es una plataforma SaaS para la gestion de procesos internos en PYMEs. El backend esta construido con **FastAPI** + **SQLModel** + **PostgreSQL**, sigue una arquitectura multi-tenant donde cada organizacion tiene sus datos aislados a traves de `organization_id`.

### Stack Tecnologico

| Componente | Tecnologia |
|------------|-----------|
| Framework | FastAPI |
| ORM | SQLModel (SQLAlchemy) |
| Base de datos | PostgreSQL |
| Migraciones | Alembic |
| Autenticacion | JWT (HS256) via PyJWT |
| Hashing | Argon2 (con migracion automatica desde bcrypt) |
| Validacion | Pydantic v2 |
| Testing | pytest + coverage |
| Linting | Ruff + mypy |
| Contenedores | Docker Compose |

### Estructura del Backend

```
backend/
├── app/
│   ├── api/
│   │   ├── deps.py              # Dependencias de autenticacion y autorizacion
│   │   ├── main.py              # Registro de routers
│   │   └── routes/
│   │       ├── login.py         # Autenticacion
│   │       ├── organizations.py # Registro de organizaciones
│   │       ├── roles.py         # Consulta de roles
│   │       ├── users.py         # Gestion de usuarios
│   │       ├── categories.py    # Gestion de categorias
│   │       ├── products.py      # Gestion de productos
│   │       ├── customers.py     # Gestion de clientes
│   │       ├── inventory_movements.py # Movimientos de inventario
│   │       ├── sales.py         # Ventas / POS
│   │       ├── dashboard.py     # Estadisticas del dashboard
│   │       ├── utils.py         # Utilidades (health check, test email)
│   │       └── private.py       # Endpoints internos (solo entorno local)
│   ├── core/
│   │   ├── config.py            # Configuracion con Pydantic Settings
│   │   ├── security.py          # Hashing de contrasenas y generacion de JWT
│   │   └── db.py                # Motor de base de datos e inicializacion
│   ├── alembic/
│   │   └── versions/
│   │       ├── 001_initial_schema.py      # Organizations, Roles, Users
│   │       ├── 002_categories.py          # Categories
│   │       ├── 003_products.py            # Products
│   │       ├── 004_customers.py           # Customers
│   │       ├── 005_inventory_movements.py # Inventory Movements
│   │       └── 006_sales.py               # Sales + Sale Items
│   ├── models.py                # Todos los modelos SQLModel y schemas Pydantic
│   └── crud.py                  # Todas las operaciones CRUD
├── tests/
│   ├── conftest.py              # Fixtures de pytest
│   ├── api/routes/              # Tests de rutas API
│   ├── crud/                    # Tests de operaciones CRUD
│   ├── utils/                   # Utilidades de testing (factories)
│   └── scripts/                 # Tests de scripts de inicio
└── scripts/
    ├── test.sh                  # Script para ejecutar tests
    ├── lint.sh                  # Script para linting
    └── format.sh                # Script para formateo
```

---

## Arquitectura del Backend

### Multi-Tenancy

Toda la plataforma opera bajo un modelo multi-tenant donde:

- Cada entidad principal tiene un campo `organization_id` (UUID, FK a `organizations`)
- El `organization_id` se extrae del JWT token del usuario autenticado
- Todas las queries filtran automaticamente por `organization_id`
- Un usuario solo puede pertenecer a una organizacion
- Los datos de una organizacion son completamente invisibles para otra

### Sistema de Roles (RBAC)

Tres roles predefinidos, seeded en la migracion inicial:

| ID | Rol | Descripcion |
|----|-----|-------------|
| 1 | `admin` | Acceso total: CRUD completo de todos los modulos |
| 2 | `seller` | Puede crear/editar productos, categorias, clientes y ventas. No puede eliminar. |
| 3 | `viewer` | Solo lectura de reportes, dashboard y listados |

### Dependencias de Autenticacion (`deps.py`)

```python
SessionDep          # Sesion de base de datos inyectada
TokenDep            # Token JWT extraido del header Authorization
CurrentUser         # Usuario autenticado actual (valida token + usuario activo + no eliminado)
CurrentOrganization # UUID de la organizacion del usuario actual
CurrentAdminUser    # Usuario con rol admin obligatorio

require_role(*roles) # Dependencia parametrica para verificar rol
                     # Uso: dependencies=[Depends(require_role("admin", "seller"))]
```

### Seguridad (`security.py`)

- **Hashing**: Argon2 como hasher principal, con Bcrypt como fallback de lectura
- **Migracion automatica de hashes**: Si un usuario tiene hash Bcrypt, al autenticarse se actualiza a Argon2 transparentemente
- **JWT**: Tokens HS256 con claims `sub` (user_id), `organization_id`, `role`
- **Prevencion de timing attacks**: Si el email no existe, se ejecuta `verify_password` contra un hash dummy para mantener tiempo de respuesta constante

### Patron CRUD

Todas las funciones CRUD en `crud.py` siguen este patron:

```python
def create_entity(*, session: Session, entity_create: EntityCreate, organization_id: uuid.UUID) -> Entity:
    db_obj = Entity.model_validate(entity_create, update={"organization_id": organization_id})
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj
```

- Parametro `session` siempre keyword-only (`*`)
- `model_validate()` para crear objetos desde schemas Pydantic
- `model_dump(exclude_unset=True)` para updates parciales
- Soft deletes: `deleted_at` + `is_active = False`
- Todas las queries de lectura filtran `WHERE deleted_at IS NULL`

---

## Paso 1: Sistema Multi-Tenant con Roles y Autenticacion

### Objetivo

Transformar el sistema de autenticacion basico (usuario unico con `is_superuser`) a un sistema multi-tenant completo con organizaciones, roles y aislamiento de datos.

### Migracion: `001_initial_schema.py`

#### Tabla `organizations`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `name` | VARCHAR(255) | NOT NULL |
| `slug` | VARCHAR(100) | UNIQUE, INDEX |
| `description` | TEXT | NULL |
| `logo_url` | VARCHAR(500) | NULL |
| `is_active` | BOOLEAN | default TRUE |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |

**Validacion del slug**: `^[a-z0-9-]{3,50}$` (lowercase, alfanumerico + guiones, 3-50 caracteres)

#### Tabla `roles`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | INTEGER | PK, autoincrement |
| `name` | VARCHAR(50) | UNIQUE, INDEX |
| `description` | TEXT | NULL |
| `permissions` | JSONB | default [] |
| `created_at` | TIMESTAMPTZ | default now() |

**Seed data**: Inserta 3 roles: `admin`, `seller`, `viewer`.

#### Tabla `users`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `role_id` | INTEGER | FK -> roles(id), INDEX |
| `email` | VARCHAR(255) | INDEX |
| `hashed_password` | VARCHAR(255) | NOT NULL |
| `first_name` | VARCHAR(100) | NOT NULL |
| `last_name` | VARCHAR(100) | NOT NULL |
| `phone` | VARCHAR(50) | NULL |
| `avatar_url` | VARCHAR(500) | NULL |
| `is_active` | BOOLEAN | default TRUE |
| `is_verified` | BOOLEAN | default FALSE |
| `last_login_at` | TIMESTAMPTZ | NULL |
| `failed_login_attempts` | INTEGER | default 0 |
| `locked_until` | TIMESTAMPTZ | NULL |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |
| `deleted_at` | TIMESTAMPTZ | NULL (soft delete) |

**Constraint**: `UNIQUE(organization_id, email)` -- el mismo email puede existir en diferentes organizaciones.

### Modelos y Schemas

#### Modelos de Organization

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `OrganizationBase` | Base compartida | name, slug (validado), description, logo_url, is_active |
| `Organization` | Tabla DB (`table=True`) | + id, created_at, updated_at, relaciones |
| `OrganizationCreate` | Crear organizacion | Hereda OrganizationBase |
| `OrganizationUpdate` | Update parcial | Todos opcionales (name, description, logo_url, is_active) |
| `OrganizationPublic` | Respuesta API | + id, created_at, updated_at |
| `OrganizationSignup` | Registro completo | organization_name/slug/description + admin_email/password/first_name/last_name/phone |

#### Modelos de Role

| Schema | Uso |
|--------|-----|
| `RoleBase` | name, description, permissions (JSONB) |
| `Role` | Tabla DB + id, created_at |
| `RolePublic` | Respuesta API |
| `RolesPublic` | Lista paginada `{data: [...], count: int}` |

#### Modelos de User

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `UserBase` | Base compartida | email, first_name, last_name, phone, avatar_url, is_active, is_verified |
| `User` | Tabla DB | + id, organization_id, role_id, hashed_password, timestamps, deleted_at |
| `UserCreate` | Crear usuario | email, password (8-128 chars), first_name, last_name, phone, role_id |
| `UserUpdate` | Update por admin | Todos opcionales incluyendo password, role_id |
| `UserUpdateMe` | Self-update | first_name, last_name, email, phone (sin password ni role) |
| `UpdatePassword` | Cambiar contrasena | current_password, new_password |
| `UserPublic` | Respuesta API | Sin hashed_password |
| `UserPublicWithRelations` | Login response | + organization (OrganizationPublic) + role (RolePublic) |
| `UsersPublic` | Lista paginada | `{data: [...], count: int}` |

#### Modelos de Autenticacion

| Schema | Uso |
|--------|-----|
| `Token` | access_token + token_type |
| `TokenPayload` | sub (user_id), organization_id, role |
| `LoginResponse` | Token + user (UserPublicWithRelations) |
| `Message` | Respuestas genericas `{message: str}` |
| `NewPassword` | token + new_password |

### Funciones CRUD

```python
# Organization
create_organization(session, organization_create) -> Organization
get_organization_by_id(session, organization_id) -> Organization | None
get_organization_by_slug(session, slug) -> Organization | None
update_organization(session, db_organization, organization_in) -> Organization

# Role
get_role_by_id(session, role_id) -> Role | None
get_role_by_name(session, name) -> Role | None
get_roles(session) -> list[Role]

# User
create_user(session, user_create, organization_id) -> User
update_user(session, db_user, user_in) -> User
get_user_by_email(session, email, organization_id?) -> User | None
get_user_by_id(session, user_id, organization_id?) -> User | None
get_users_by_organization(session, organization_id, skip, limit) -> list[User]
count_users_by_organization(session, organization_id) -> int

# Authentication
authenticate(session, email, password, organization_id?) -> User | None
```

### Endpoints API

#### Login (`/api/v1/login`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| POST | `/login/access-token` | Login OAuth2, devuelve token + datos del usuario | Publico | `LoginResponse` |
| POST | `/login/test-token` | Validar token activo | Cualquier autenticado | `UserPublic` |
| POST | `/password-recovery/{email}` | Enviar email de recuperacion | Publico | `Message` |
| POST | `/reset-password/` | Resetear contrasena con token | Publico | `Message` |

**Nota sobre seguridad del login:**
- Actualiza `last_login_at` al iniciar sesion
- El endpoint `/password-recovery` siempre devuelve la misma respuesta para prevenir enumeracion de emails
- Si el email no existe en `/reset-password`, devuelve "Invalid token" (no revela que el usuario no existe)

#### Organizations (`/api/v1/organizations`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| POST | `/signup` | Crear organizacion + usuario admin | Publico | `LoginResponse` (201) |
| GET | `/me` | Ver mi organizacion | Cualquier autenticado | `OrganizationPublic` |
| PATCH | `/me` | Actualizar mi organizacion | Admin | `OrganizationPublic` |

**Flujo de signup:**
1. Valida que el slug no exista
2. Valida que el email no este en uso
3. Crea la organizacion
4. Busca el rol "admin"
5. Crea el usuario admin
6. Genera JWT y devuelve `LoginResponse`

#### Roles (`/api/v1/roles`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar todos los roles | Cualquier autenticado | `RolesPublic` |

#### Users (`/api/v1/users`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar usuarios de la organizacion | Admin | `UsersPublic` |
| POST | `/` | Crear usuario en la organizacion | Admin | `UserPublic` |
| GET | `/me` | Ver mi perfil | Cualquier autenticado | `UserPublic` |
| PATCH | `/me` | Actualizar mi perfil | Cualquier autenticado | `UserPublic` |
| PATCH | `/me/password` | Cambiar mi contrasena | Cualquier autenticado | `Message` |
| DELETE | `/me` | Eliminar mi cuenta (soft delete) | Cualquier autenticado | `Message` |
| GET | `/{user_id}` | Ver usuario por ID | Admin (o el mismo usuario) | `UserPublic` |
| PATCH | `/{user_id}` | Actualizar usuario | Admin | `UserPublic` |
| DELETE | `/{user_id}` | Eliminar usuario (soft delete) | Admin | `Message` |

**Reglas de negocio:**
- No se puede eliminar al unico admin de la organizacion
- No se puede eliminarse a si mismo via `DELETE /{id}` (debe usar `DELETE /me`)
- La contrasena nueva no puede ser igual a la actual
- Email unico dentro de la organizacion (puede repetirse entre organizaciones)

### Tests (Paso 1)

- **8 tests de login**: token de acceso, contrasena incorrecta, test-token, recuperacion de contrasena (usuario existente y no existente), reset de contrasena (token valido e invalido), migracion de hash bcrypt->argon2
- **20 tests de users**: GET /me (superuser y normal), POST crear usuario (nuevo, email existente, no-admin prohibido), GET listar, GET por ID, PATCH /me, PATCH /me/password (correcta, incorrecta, misma contrasena), DELETE /me, DELETE /{id}
- **10 tests CRUD de user**: crear, autenticar (exito/fallo), is_active, asignacion de rol, obtener, actualizar, migracion de hash
- **1 test private**: creacion de usuario por endpoint interno

---

## Paso 2: Modulo de Categorias

### Objetivo

Implementar un sistema de categorias jerarquico con soporte para categorias padre/hijo, unico por organizacion y nivel.

### Migracion: `002_categories.py`

#### Tabla `categories`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `name` | VARCHAR(255) | NOT NULL |
| `description` | TEXT | NULL |
| `parent_id` | UUID | FK -> categories(id) SET NULL, INDEX |
| `is_active` | BOOLEAN | default TRUE |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |
| `deleted_at` | TIMESTAMPTZ | NULL (soft delete) |

**Constraint**: `UNIQUE(organization_id, name, parent_id)` -- el mismo nombre puede existir en diferentes niveles de la jerarquia.

### Modelos y Schemas

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `CategoryBase` | Base compartida | name, description, parent_id (FK self-ref), is_active |
| `Category` | Tabla DB | + id, organization_id, timestamps, deleted_at, relaciones (parent, children, products) |
| `CategoryCreate` | Crear categoria | name, description, parent_id (opcional) |
| `CategoryUpdate` | Update parcial | name, description, parent_id, is_active (todos opcionales) |
| `CategoryPublic` | Respuesta API | + id, organization_id, created_at, updated_at |
| `CategoriesPublic` | Lista paginada | `{data: [...], count: int}` |

### Funciones CRUD

```python
create_category(session, category_create, organization_id) -> Category
get_category_by_id(session, category_id, organization_id) -> Category | None
get_categories_by_organization(session, organization_id, skip, limit) -> list[Category]
count_categories_by_organization(session, organization_id) -> int
get_category_by_name(session, name, organization_id, parent_id?) -> Category | None
update_category(session, db_category, category_in) -> Category
soft_delete_category(session, db_category) -> Category
```

**Nota sobre `get_category_by_name`**: Busca por nombre dentro del mismo nivel jerarquico. Si `parent_id` es `None`, busca entre categorias raiz (`WHERE parent_id IS NULL`).

### Endpoints API (`/api/v1/categories`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar categorias | Cualquier autenticado | `CategoriesPublic` |
| POST | `/` | Crear categoria | Admin, Seller | `CategoryPublic` |
| GET | `/{category_id}` | Ver categoria por ID | Cualquier autenticado | `CategoryPublic` |
| PATCH | `/{category_id}` | Actualizar categoria | Admin, Seller | `CategoryPublic` |
| DELETE | `/{category_id}` | Eliminar categoria (soft) | Admin | `Message` |

**Validaciones:**
- Si se proporciona `parent_id`, se verifica que la categoria padre exista en la misma organizacion
- No se puede crear una categoria con nombre duplicado en el mismo nivel (misma combinacion org + parent)
- No se puede asignar una categoria como su propia padre (`parent_id == category_id`)
- Al actualizar el nombre, se verifica unicidad en el nivel destino

### Tests (Paso 2)

- **14 tests de rutas**: listar, crear (con/sin padre, padre invalido, nombre duplicado, mismo nombre en diferente padre), obtener por ID, actualizar (padre propio rechazado), eliminar (soft), acceso por roles
- **8 tests CRUD**: crear (basico, con padre), obtener por ID (encontrado/no encontrado), listar por organizacion, contar, obtener por nombre, actualizar, soft delete

---

## Paso 3: Modulo de Productos

### Objetivo

Implementar un sistema de gestion de productos con control de inventario, precios, alertas de stock bajo y ajustes de stock manuales.

### Migracion: `003_products.py`

#### Tabla `products`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `category_id` | UUID | FK -> categories(id) SET NULL, INDEX |
| `name` | VARCHAR(255) | NOT NULL |
| `sku` | VARCHAR(100) | INDEX |
| `description` | TEXT | NULL |
| `image_url` | VARCHAR(500) | NULL |
| `cost_price` | NUMERIC(12,2) | NOT NULL, default 0 |
| `sale_price` | NUMERIC(12,2) | NOT NULL, default 0 |
| `stock_quantity` | INTEGER | default 0 |
| `stock_min` | INTEGER | default 0 |
| `stock_max` | INTEGER | NULL |
| `unit` | VARCHAR(50) | default "unit" |
| `barcode` | VARCHAR(100) | NULL |
| `is_active` | BOOLEAN | default TRUE |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |
| `deleted_at` | TIMESTAMPTZ | NULL (soft delete) |

**Constraint**: `UNIQUE(organization_id, sku)` -- SKU unico por organizacion.

### Modelos y Schemas

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `ProductBase` | Base compartida | name, sku, description, image_url, cost_price, sale_price, stock_quantity, stock_min, stock_max, unit, barcode, is_active |
| `Product` | Tabla DB | + id, organization_id, category_id, timestamps, deleted_at, relaciones |
| `ProductCreate` | Crear producto | Campos base + validadores de precio (>= 0) y stock (>= 0) |
| `ProductUpdate` | Update parcial | Todos opcionales + mismos validadores |
| `StockAdjustment` | Ajuste de stock | quantity (int, + o -), reason (str, max 500) |
| `ProductPublic` | Respuesta API | + id, organization_id, category_id, created_at, updated_at |
| `ProductsPublic` | Lista paginada | `{data: [...], count: int}` |

**Validadores Pydantic:**
- `cost_price`, `sale_price`: No pueden ser negativos
- `stock_quantity`, `stock_min`: No pueden ser negativos

### Funciones CRUD

```python
create_product(session, product_create, organization_id) -> Product
get_product_by_id(session, product_id, organization_id) -> Product | None
get_products_by_organization(session, organization_id, skip, limit) -> list[Product]
count_products_by_organization(session, organization_id) -> int
get_product_by_sku(session, sku, organization_id) -> Product | None
get_low_stock_products(session, organization_id, skip, limit) -> list[Product]
count_low_stock_products(session, organization_id) -> int
update_product(session, db_product, product_in) -> Product
adjust_product_stock(session, db_product, quantity) -> Product
soft_delete_product(session, db_product) -> Product
```

**Nota sobre `get_low_stock_products`**: Filtra productos donde `stock_quantity <= stock_min`.

### Endpoints API (`/api/v1/products`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar productos | Cualquier autenticado | `ProductsPublic` |
| POST | `/` | Crear producto | Admin, Seller | `ProductPublic` |
| GET | `/low-stock` | Productos con stock bajo | Cualquier autenticado | `ProductsPublic` |
| GET | `/{product_id}` | Ver producto por ID | Cualquier autenticado | `ProductPublic` |
| PATCH | `/{product_id}` | Actualizar producto | Admin, Seller | `ProductPublic` |
| DELETE | `/{product_id}` | Eliminar producto (soft) | Admin | `Message` |
| POST | `/{product_id}/adjust-stock` | Ajustar stock manualmente | Admin, Seller | `ProductPublic` |
| GET | `/{product_id}/movements` | Movimientos del producto | Cualquier autenticado | `InventoryMovementsPublic` |

**Validaciones y logica:**
- SKU unico dentro de la organizacion
- Si se proporciona `category_id`, se verifica que la categoria exista
- El stock no puede quedar negativo tras un ajuste
- El endpoint `adjust-stock` crea automaticamente un `InventoryMovement` de tipo "adjustment"
- El endpoint `movements` muestra el historial de movimientos de inventario del producto

### Tests (Paso 3)

- **22 tests de rutas**: listar, crear (con/sin categoria, categoria invalida, SKU duplicado, precio negativo), low-stock, obtener por ID, actualizar (nombre, SKU, SKU duplicado, categoria invalida), eliminar (soft), adjust-stock (agregar, restar, resultado negativo), acceso por roles
- **12 tests CRUD**: crear (basico, con categoria), obtener por ID (encontrado/no encontrado), listar, contar, obtener por SKU, low stock (obtener/contar), actualizar, ajustar stock, soft delete

---

## Paso 4: Modulo de Clientes

### Objetivo

Implementar un sistema de gestion de clientes con identificacion por documento y estadisticas de compra desnormalizadas.

### Migracion: `004_customers.py`

#### Tabla `customers`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `document_type` | VARCHAR(50) | NOT NULL (DNI, RUC, Pasaporte, Otro) |
| `document_number` | VARCHAR(50) | NOT NULL |
| `first_name` | VARCHAR(100) | NOT NULL |
| `last_name` | VARCHAR(100) | NOT NULL |
| `email` | VARCHAR(255) | NULL, INDEX |
| `phone` | VARCHAR(50) | NULL, INDEX |
| `address` | TEXT | NULL |
| `city` | VARCHAR(100) | NULL |
| `country` | VARCHAR(100) | NULL |
| `notes` | TEXT | NULL |
| `total_purchases` | NUMERIC(12,2) | NOT NULL, default 0 |
| `purchases_count` | INTEGER | default 0 |
| `last_purchase_at` | TIMESTAMPTZ | NULL |
| `is_active` | BOOLEAN | default TRUE |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |
| `deleted_at` | TIMESTAMPTZ | NULL (soft delete) |

**Constraint**: `UNIQUE(organization_id, document_number)` -- documento unico por organizacion.

**Campos desnormalizados**: `total_purchases`, `purchases_count` y `last_purchase_at` se actualizan automaticamente por el CRUD cada vez que se registra o cancela una venta.

### Modelos y Schemas

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `CustomerBase` | Base compartida | document_type, document_number, first_name, last_name, email, phone, address, city, country, notes, is_active |
| `Customer` | Tabla DB | + id, organization_id, total_purchases, purchases_count, last_purchase_at, timestamps, deleted_at |
| `CustomerCreate` | Crear cliente | Campos de contacto (sin campos desnormalizados ni is_active) |
| `CustomerUpdate` | Update parcial | Todos opcionales incluyendo is_active |
| `CustomerPublic` | Respuesta API | + id, organization_id, total_purchases, purchases_count, last_purchase_at, timestamps |
| `CustomersPublic` | Lista paginada | `{data: [...], count: int}` |

### Funciones CRUD

```python
create_customer(session, customer_create, organization_id) -> Customer
get_customer_by_id(session, customer_id, organization_id) -> Customer | None
get_customers_by_organization(session, organization_id, skip, limit) -> list[Customer]
count_customers_by_organization(session, organization_id) -> int
get_customer_by_document(session, document_number, organization_id) -> Customer | None
update_customer(session, db_customer, customer_in) -> Customer
soft_delete_customer(session, db_customer) -> Customer

# Funciones de estadisticas (usadas por el modulo de ventas)
update_customer_purchase_stats(session, db_customer, sale_total) -> Customer
revert_customer_purchase_stats(session, db_customer, sale_total) -> Customer
```

**Nota sobre `revert_customer_purchase_stats`**: Protege contra valores negativos -- si `total_purchases` queda < 0, se establece a 0. Lo mismo para `purchases_count` (usa `max(0, count - 1)`).

### Endpoints API (`/api/v1/customers`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar clientes | Cualquier autenticado | `CustomersPublic` |
| POST | `/` | Crear cliente | Admin, Seller | `CustomerPublic` |
| GET | `/{customer_id}` | Ver cliente por ID | Cualquier autenticado | `CustomerPublic` |
| PATCH | `/{customer_id}` | Actualizar cliente | Admin, Seller | `CustomerPublic` |
| DELETE | `/{customer_id}` | Eliminar cliente (soft) | Admin | `Message` |
| GET | `/{customer_id}/sales` | Ventas del cliente | Cualquier autenticado | `SalesPublic` |

**Validaciones:**
- `document_number` unico dentro de la organizacion
- Al actualizar `document_number`, se verifica que no exista otro cliente con ese numero

### Tests (Paso 4)

- **15 tests de rutas**: listar, crear, documento duplicado, obtener por ID, actualizar, documento duplicado en update, eliminar (soft), acceso por roles (seller puede crear pero no eliminar, viewer prohibido)
- **8 tests CRUD**: crear, obtener por ID (encontrado/no encontrado), listar, contar, obtener por documento, actualizar, soft delete

---

## Paso 5: Modulo de Movimientos de Inventario

### Objetivo

Implementar un sistema de trazabilidad para todos los cambios de stock, creando un registro de auditoria inmutable para cada movimiento de inventario.

### Migracion: `005_inventory_movements.py`

#### Tabla `inventory_movements`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `product_id` | UUID | FK -> products(id) CASCADE, INDEX |
| `user_id` | UUID | FK -> users(id) CASCADE, INDEX |
| `movement_type` | VARCHAR(50) | INDEX (sale, purchase, adjustment, return) |
| `quantity` | INTEGER | positivo = entrada, negativo = salida |
| `previous_stock` | INTEGER | Stock antes del movimiento |
| `new_stock` | INTEGER | Stock despues del movimiento |
| `reference_id` | UUID | NULL (vincula a la transaccion origen) |
| `reference_type` | VARCHAR(50) | NULL (tipo de transaccion: sale, purchase, etc.) |
| `reason` | TEXT | NULL |
| `created_at` | TIMESTAMPTZ | INDEX, default now() |

**Indices compuestos**: `(reference_type, reference_id)` para buscar movimientos por transaccion origen.

**Nota**: Esta tabla es immutable -- los registros nunca se actualizan ni eliminan. No tiene `updated_at` ni `deleted_at`.

### Modelos y Schemas

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `InventoryMovementBase` | Base compartida | movement_type, quantity, previous_stock, new_stock, reference_id, reference_type, reason |
| `InventoryMovement` | Tabla DB | + id, organization_id, product_id, user_id, created_at, relaciones |
| `InventoryMovementCreate` | Crear movimiento | product_id, movement_type, quantity, reference_id, reference_type, reason |
| `InventoryMovementPublic` | Respuesta API | Todos los campos |
| `InventoryMovementsPublic` | Lista paginada | `{data: [...], count: int}` |

### Funciones CRUD

```python
create_inventory_movement(session, movement_create, organization_id, user_id, previous_stock, new_stock) -> InventoryMovement
get_inventory_movement_by_id(session, movement_id, organization_id) -> InventoryMovement | None
get_movements_by_organization(session, organization_id, skip, limit) -> list[InventoryMovement]  # ordenado por created_at DESC
count_movements_by_organization(session, organization_id) -> int
get_movements_by_product(session, product_id, organization_id, skip, limit) -> list[InventoryMovement]  # ordenado por created_at DESC
count_movements_by_product(session, product_id, organization_id) -> int
```

### Endpoints API (`/api/v1/inventory-movements`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar movimientos | Cualquier autenticado | `InventoryMovementsPublic` |
| POST | `/` | Crear movimiento manual | Admin, Seller | `InventoryMovementPublic` |
| GET | `/{movement_id}` | Ver movimiento por ID | Cualquier autenticado | `InventoryMovementPublic` |

**Validaciones y logica:**
- Solo se permiten tipos manuales: `purchase`, `adjustment`, `return`
- El tipo `sale` esta prohibido en creacion manual -- se crea automaticamente al registrar una venta
- Se valida que el producto exista en la organizacion
- Se verifica que el stock no quede negativo despues del movimiento
- Se ajusta automaticamente el stock del producto

**Nota**: Los movimientos del producto tambien son accesibles via `GET /api/v1/products/{product_id}/movements`.

### Tests (Paso 5)

- **18 tests de rutas**: listar, crear (purchase, adjustment, return), tipos invalidos (sale y unknown rechazados), producto no encontrado, stock negativo, obtener por ID, movimientos de producto, adjust-stock crea movimiento, acceso por roles
- **8 tests CRUD**: crear, obtener por ID (encontrado/no encontrado), listar/contar por organizacion, listar/contar por producto, movimiento con referencia, ordenamiento

---

## Paso 6: Modulo de Ventas

### Objetivo

Implementar un sistema de punto de venta (POS) completo con generacion de facturas, deduccion automatica de stock, seguimiento de estadisticas de clientes y cancelacion con reversion.

### Migracion: `006_sales.py`

#### Tabla `sales`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `organization_id` | UUID | FK -> organizations(id) CASCADE, INDEX |
| `customer_id` | UUID | FK -> customers(id) SET NULL, INDEX |
| `user_id` | UUID | FK -> users(id) CASCADE, INDEX |
| `invoice_number` | VARCHAR(100) | INDEX |
| `sale_date` | TIMESTAMPTZ | INDEX, default now() |
| `subtotal` | NUMERIC(12,2) | NOT NULL, default 0 |
| `discount` | NUMERIC(12,2) | NOT NULL, default 0 |
| `tax` | NUMERIC(12,2) | NOT NULL, default 0 |
| `total` | NUMERIC(12,2) | NOT NULL, default 0 |
| `payment_method` | VARCHAR(50) | default "cash" |
| `status` | VARCHAR(50) | INDEX, default "completed" |
| `notes` | TEXT | NULL |
| `cancelled_at` | TIMESTAMPTZ | NULL |
| `cancelled_by` | UUID | FK -> users(id) SET NULL |
| `cancellation_reason` | TEXT | NULL |
| `created_at` | TIMESTAMPTZ | default now() |
| `updated_at` | TIMESTAMPTZ | default now() |

**Constraint**: `UNIQUE(organization_id, invoice_number)`

#### Tabla `sale_items`

| Columna | Tipo | Restricciones |
|---------|------|---------------|
| `id` | UUID | PK, default uuid4 |
| `sale_id` | UUID | FK -> sales(id) CASCADE, INDEX |
| `product_id` | UUID | FK -> products(id) CASCADE, INDEX |
| `product_name` | VARCHAR(255) | NOT NULL (snapshot) |
| `product_sku` | VARCHAR(100) | NOT NULL (snapshot) |
| `quantity` | INTEGER | CHECK quantity > 0 |
| `unit_price` | NUMERIC(12,2) | CHECK unit_price >= 0 (snapshot) |
| `subtotal` | NUMERIC(12,2) | CHECK subtotal >= 0 |
| `created_at` | TIMESTAMPTZ | default now() |

**Campos snapshot**: `product_name`, `product_sku` y `unit_price` preservan los valores del producto al momento de la venta, inmutables ante futuras modificaciones del producto.

### Modelos y Schemas

| Schema | Uso | Campos clave |
|--------|-----|-------------|
| `SaleBase` | Base compartida | invoice_number, sale_date, subtotal, discount, tax, total, payment_method, status, notes |
| `Sale` | Tabla DB | + id, organization_id, customer_id, user_id, cancelled_at/by/reason, timestamps, relaciones |
| `SaleItemBase` | Base item | product_name, product_sku, quantity, unit_price, subtotal |
| `SaleItem` | Tabla DB | + id, sale_id, product_id, created_at |
| `SaleItemCreate` | Input item | product_id, quantity (validador: > 0) |
| `SaleCreate` | Input venta | customer_id (opcional), payment_method, discount, tax, notes, items (lista no vacia de SaleItemCreate) |
| `SaleItemPublic` | Response item | Todos los campos |
| `SalePublic` | Response venta | Todos los campos + items (lista de SaleItemPublic) |
| `SalesPublic` | Lista paginada | `{data: [...], count: int}` |
| `SaleCancelRequest` | Cancelar venta | reason (str, max 500) |
| `SaleStatsPublic` | Estadisticas | sales_today_count/total, sales_month_count/total, average_ticket |

**Validadores Pydantic en `SaleCreate`:**
- `discount`, `tax`: No pueden ser negativos
- `items`: La lista no puede estar vacia (al menos 1 item)
- `quantity` en `SaleItemCreate`: Debe ser mayor que 0

### Funciones CRUD

```python
# Generacion de factura
generate_invoice_number(session, organization_id) -> str  # Formato: "INV-000001"

# CRUD
create_sale(session, organization_id, user_id, customer_id, invoice_number, subtotal, discount, tax, total, payment_method, notes) -> Sale
create_sale_item(session, sale_id, product_id, product_name, product_sku, quantity, unit_price, subtotal) -> SaleItem
get_sale_by_id(session, sale_id, organization_id) -> Sale | None
get_sales_by_organization(session, organization_id, skip, limit) -> list[Sale]  # ordenado por created_at DESC
count_sales_by_organization(session, organization_id) -> int
get_sale_items(session, sale_id) -> list[SaleItem]
cancel_sale(session, db_sale, cancelled_by, reason) -> Sale

# Ventas de hoy
get_sales_today(session, organization_id, skip, limit) -> list[Sale]
count_sales_today(session, organization_id) -> int

# Estadisticas
get_sales_stats(session, organization_id) -> dict  # today count/total, month count/total, average_ticket

# Estadisticas de cliente
update_customer_purchase_stats(session, db_customer, sale_total) -> Customer
revert_customer_purchase_stats(session, db_customer, sale_total) -> Customer

# Ventas por cliente
get_sales_by_customer(session, customer_id, organization_id, skip, limit) -> list[Sale]
count_sales_by_customer(session, customer_id, organization_id) -> int
```

**Formato de `invoice_number`**: `INV-{count+1:06d}` donde `count` es el total de ventas en la organizacion. Ejemplo: `INV-000001`, `INV-000002`, etc.

### Endpoints API (`/api/v1/sales`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/` | Listar ventas | Cualquier autenticado | `SalesPublic` |
| POST | `/` | Crear venta | Admin, Seller | `SalePublic` |
| GET | `/today` | Ventas de hoy | Cualquier autenticado | `SalesPublic` |
| GET | `/stats` | Estadisticas de ventas | Cualquier autenticado | `SaleStatsPublic` |
| GET | `/{sale_id}` | Ver venta por ID | Cualquier autenticado | `SalePublic` |
| POST | `/{sale_id}/cancel` | Cancelar venta | Admin, Seller | `SalePublic` |

### Flujo de Creacion de Venta (`POST /sales/`)

1. **Validar cliente** (si `customer_id` es proporcionado)
2. **Validar productos**: Para cada item, verificar que el producto exista, este activo y tenga stock suficiente
3. **Calcular subtotal**: `sum(product.sale_price * item.quantity)` para todos los items
4. **Calcular total**: `subtotal - discount + tax` (minimo 0)
5. **Generar numero de factura**: `INV-XXXXXX`
6. **Crear registro de venta**
7. **Para cada item:**
   - Crear `SaleItem` con datos snapshot del producto
   - Deducir stock del producto (`adjust_product_stock(-quantity)`)
   - Crear `InventoryMovement` de tipo "sale" con referencia a la venta
8. **Actualizar estadisticas del cliente** (si tiene cliente asignado)

### Flujo de Cancelacion de Venta (`POST /sales/{id}/cancel`)

1. **Validar** que la venta exista y no este ya cancelada
2. **Para cada item de la venta:**
   - Restaurar stock del producto (`adjust_product_stock(+quantity)`)
   - Crear `InventoryMovement` de tipo "return" con referencia a la venta
3. **Revertir estadisticas del cliente** (si la venta tenia cliente)
4. **Marcar la venta** como "cancelled" con timestamp, usuario y razon

### Tests (Paso 6)

- **~30 tests de rutas**: CRUD completo, crear con/sin cliente, multiples items, descuento/impuesto, stock insuficiente, producto inactivo, cliente no encontrado, verificacion de deduccion de stock, creacion de movimientos de inventario, actualizacion de estadisticas de cliente, ventas de hoy, estadisticas, obtener por ID, cancelar (restaurar stock, revertir stats cliente, movimientos return), ventas por cliente, acceso por roles (seller permitido, viewer prohibido)
- **16 tests CRUD**: generar invoice_number (formato, secuencial), crear venta (con/sin cliente), crear sale_item, obtener por ID (encontrado/no encontrado), listar/contar por organizacion, obtener items, cancelar, ventas hoy, contar hoy, estadisticas, actualizar/revertir stats cliente (incluyendo no-negativo), obtener/contar por cliente, ordenamiento

---

## Paso 7: Dashboard (KPIs y Estadisticas)

### Objetivo

Implementar un endpoint unico de dashboard que agrega estadisticas de ventas, inventario y productos mas vendidos.

### Migracion

**No se requirio migracion** -- el dashboard es un endpoint de solo lectura que consulta tablas existentes.

### Modelos y Schemas

| Schema | Uso | Campos |
|--------|-----|--------|
| `SalesTodayStats` | Stats del dia | count: int, total: Decimal |
| `SalesMonthStats` | Stats del mes | count: int, total: Decimal |
| `TopProductItem` | Producto top | product_id: UUID, product_name: str, quantity_sold: int, revenue: Decimal |
| `SalesByDayItem` | Ventas por dia | date: str, count: int, total: Decimal |
| `DashboardStatsPublic` | Respuesta unificada | sales_today, sales_month, low_stock_count, average_ticket, top_products, sales_by_day |

### Funciones CRUD

```python
get_top_products(session, organization_id, limit=5) -> list[dict]
# JOIN SaleItem + Sale, filtra completed, agrupa por producto, suma quantity + revenue, ordena DESC

get_sales_by_day(session, organization_id, days=30) -> list[dict]
# Ultimos 30 dias, solo completed, agrupado por cast(sale_date, Date), ordenado ASC

get_dashboard_stats(session, organization_id) -> dict
# Compone: get_sales_stats() + count_low_stock_products() + get_top_products() + get_sales_by_day()
```

### Endpoint API (`/api/v1/dashboard`)

| Metodo | Ruta | Descripcion | Roles | Response |
|--------|------|-------------|-------|----------|
| GET | `/stats` | Estadisticas del dashboard | Cualquier autenticado | `DashboardStatsPublic` |

**Respuesta ejemplo:**
```json
{
  "sales_today": { "count": 5, "total": 1250.00 },
  "sales_month": { "count": 42, "total": 15800.50 },
  "low_stock_count": 3,
  "average_ticket": 376.20,
  "top_products": [
    { "product_id": "uuid", "product_name": "Laptop HP", "quantity_sold": 15, "revenue": 12000.00 }
  ],
  "sales_by_day": [
    { "date": "2026-02-01", "count": 3, "total": 450.00 }
  ]
}
```

**Nota**: Este endpoint no usa `require_role` -- cualquier usuario autenticado (admin, seller, viewer) puede acceder al dashboard.

### Tests (Paso 7)

- **8 tests de rutas**: respuesta completa, estructura de sales_today, estructura de sales_month, top_products, sales_by_day, acceso normal user (viewer, 200 OK), acceso seller (200 OK), no autenticado (401)
- **8 tests CRUD**: get_top_products (basico, vacio, limit, ordenamiento), get_sales_by_day (basico, vacio, formato de fecha), get_dashboard_stats (estructura completa, low_stock_count, average_ticket)

---

## Errores Encontrados y Soluciones

### Error 1: Tests y Rutas Rotos Tras Migracion Multi-Tenant (Critico)

**Commit**: `0af3c8a` (8 Feb 2026)
**Severidad**: Critica -- 100% de los tests fallaban

**Problema**:
Cuando se implemento el multi-tenancy (commit `61fbaaf`), el modelo de User cambio fundamentalmente:
- `full_name` fue reemplazado por `first_name` y `last_name`
- `is_superuser` (boolean) fue reemplazado por `organization_id` (FK) y `role_id` (FK)
- El sistema de autenticacion fue refactorizado para incluir contexto de organizacion

Sin embargo, los tests existentes (`test_users.py`, `test_user.py`, `test_login.py`, `test_private.py`) y la ruta privada (`/api/v1/private/users/`) seguian referenciando los campos viejos. Esto significaba que **todos los tests estaban rotos**.

**Solucion** (22 archivos modificados, +4885/-300 lineas):

1. **`backend/app/api/routes/private.py`**: Se actualizo el schema `PrivateUserCreate`:
   - Se elimino `full_name: str`
   - Se agrego `first_name: str`, `last_name: str`, `organization_id: uuid.UUID`, `role_id: int = 3`
   - Se agrego validacion de que la organizacion y el rol existan
   - Se agrego `session.refresh(user)` que faltaba (devolvía datos stale)

2. **`backend/app/models.py`**: Se agrego campo `password` faltante al schema `UserUpdate`:
   ```python
   password: str | None = Field(default=None, min_length=8, max_length=128)
   ```
   Sin este campo, las actualizaciones de contrasena de usuarios por parte del admin fallaban silenciosamente.

3. **`backend/tests/conftest.py`**: Se actualizaron los fixtures para funcionar con el nuevo modelo multi-tenant.

4. **`backend/tests/utils/user.py`**: Se actualizaron las utilidades de creacion de usuarios para incluir `organization_id` y `role_id` en lugar de `is_superuser`.

5. **Tests reescritos**: `test_users.py`, `test_user.py`, `test_login.py`, `test_private.py` -- todas las aserciones cambiaron de `is_superuser === True` a `role_id === 1` (admin).

**Leccion**: Cuando se hace un cambio fundamental en los modelos, **todos los tests y rutas que dependen de esos modelos deben actualizarse en el mismo commit**.

---

### Error 2: Componente Logo Roto Tras Rebranding (Frontend)

**Commit**: `65d6cba` (7 Feb 2026)
**Severidad**: Media -- sidebar del frontend roto

**Problema**:
Durante el rebranding de FastAPI a OrbitEngine, se eliminaron los assets SVG de FastAPI, pero el componente `Logo` en `frontend/src/components/Common/Logo.tsx` aun los importaba:
```typescript
import icon from "/assets/images/fastapi-icon.svg"       // ELIMINADO
import iconLight from "/assets/images/fastapi-icon-light.svg"  // ELIMINADO
```

**Solucion**:
1. Se elimino el componente `Logo.tsx` completamente
2. Se actualizo `AppSidebar.tsx` para usar directamente el nuevo logo PNG de OrbitEngine
3. Se corrigio la ruta de navegacion de settings en `User.tsx` de `/settings` a `/dashboard/settings`

---

### Error 3: Documentacion Incorrecta de Docker Workflow

**Commit**: `e7d5ba1` (2 Feb 2026)
**Severidad**: Baja -- confundía a los desarrolladores

**Problema**:
La documentacion indicaba usar `docker compose watch`, que no es el comando correcto para iniciar el stack de desarrollo. Ademas no explicaba como funciona el hot-reload.

**Solucion**:
1. Se corrigio el comando a `docker compose build && docker compose up -d`
2. Se documento que el hot-reload funciona via volumenes en `compose.override.yml` + flag `--reload`
3. Se agrego `docker compose logs -f backend` para monitoreo
4. Se aclaro que solo es necesario reiniciar contenedores al cambiar dependencias de `uv`, no al cambiar codigo Python

---

## Resultados de Testing

### Resumen Final

| Metrica | Valor |
|---------|-------|
| **Total de tests** | 237 |
| **Tests exitosos** | 237 (0 fallos) |
| **Cobertura de codigo** | 91% |
| **Errores de linting** | 0 |

### Desglose por Modulo

| Modulo | Tests Rutas | Tests CRUD | Total |
|--------|-------------|------------|-------|
| Login/Auth | 8 | - | 8 |
| Users | 20 | 10 | 30 |
| Organizations | (incluido en login) | - | - |
| Roles | (incluido en otros) | - | - |
| Private | 1 | - | 1 |
| Categories | 14 | 8 | 22 |
| Products | 22 | 12 | 34 |
| Customers | 15 | 8 | 23 |
| Inventory Movements | 18 | 8 | 26 |
| Sales | ~30 | 16 | ~46 |
| Dashboard | 8 | 8 | 16 |
| Scripts | - | - | 2 |
| **Total** | | | **~237** |

### Fixtures de Test (`conftest.py`)

```python
# Session-scoped: una sola sesion de DB para todos los tests
db: Session           # Sesion con limpieza ordenada al finalizar
client: TestClient    # Cliente HTTP para pruebas de rutas
superuser_token_headers: dict  # Headers con JWT de usuario admin
normal_user_token_headers: dict # Headers con JWT de usuario viewer
```

**Limpieza de datos** (orden para respetar FKs):
`SaleItem -> Sale -> InventoryMovement -> Product -> Customer -> Category -> User (excepto superuser)`

### Utilidades de Test (`tests/utils/`)

| Archivo | Funciones |
|---------|-----------|
| `utils.py` | `random_lower_string()`, `random_email()`, `get_superuser_token_headers()` |
| `user.py` | `create_random_user()`, `authentication_token_from_email()`, `_get_default_org_id()`, `_get_role_id()` |
| `category.py` | `create_random_category()` |
| `product.py` | `create_random_product(stock_quantity, stock_min, category_id)` |
| `customer.py` | `create_random_customer()` |
| `inventory_movement.py` | `create_random_movement(product, movement_type, quantity)` |
| `sale.py` | `create_random_sale(customer, user, num_items, stock)` -- crea productos, items, ajusta stock, actualiza stats |

---

## Comandos de Referencia

### Migraciones (requiere Docker Compose activo)

```bash
# Aplicar todas las migraciones
docker compose exec backend alembic upgrade head

# Crear nueva migracion
docker compose exec backend alembic revision --autogenerate -m "descripcion"

# Revertir ultima migracion
docker compose exec backend alembic downgrade -1
```

### Testing

```bash
# Ejecutar todos los tests
docker compose exec backend bash -c "cd /app/backend && python -m pytest -v"

# Tests con cobertura
docker compose exec backend bash -c "cd /app/backend && python -m coverage run --source=app -m pytest && python -m coverage report -m"

# Test de un solo archivo
docker compose exec backend bash -c "cd /app/backend && python -m pytest tests/api/routes/test_sales.py -v"

# Tests que coincidan con un patron
docker compose exec backend bash -c "cd /app/backend && python -m pytest -k 'test_create' -v"
```

### Linting y Formateo

```bash
# Lint (ruff + mypy)
docker compose exec backend bash -c "cd /app/backend && uv run bash scripts/lint.sh"

# Formatear codigo
docker compose exec backend bash -c "cd /app/backend && uv run bash scripts/format.sh"

# Solo ruff check
docker compose exec backend bash -c "cd /app/backend && ruff check"
```

### Servidor de Desarrollo

```bash
# Iniciar todo el stack
docker compose build && docker compose up -d

# Ver logs del backend
docker compose logs -f backend

# Regenerar cliente API del frontend (backend debe estar corriendo)
cd frontend && bun run generate-client
```

### Reset de Contrasena del Superuser

Si el login falla con error 400 en tests:

```bash
docker compose exec backend bash -c "cd /app/backend && python -c \"
from sqlmodel import Session, select
from app.core.db import engine
from app.models import User
from app.core.config import settings
from app.core.security import get_password_hash
with Session(engine) as session:
    user = session.exec(select(User).where(User.email == settings.FIRST_SUPERUSER)).first()
    if user:
        user.hashed_password = get_password_hash(settings.FIRST_SUPERUSER_PASSWORD)
        session.add(user)
        session.commit()
        print('Password reset done')
\""
```

---

## Resumen de Endpoints Completo

| Modulo | Prefijo | Endpoints | Metodos |
|--------|---------|-----------|---------|
| Login | `/api/v1/login` | 4 | POST |
| Organizations | `/api/v1/organizations` | 3 | POST, GET, PATCH |
| Roles | `/api/v1/roles` | 1 | GET |
| Users | `/api/v1/users` | 9 | GET, POST, PATCH, DELETE |
| Categories | `/api/v1/categories` | 5 | GET, POST, PATCH, DELETE |
| Products | `/api/v1/products` | 8 | GET, POST, PATCH, DELETE |
| Customers | `/api/v1/customers` | 6 | GET, POST, PATCH, DELETE |
| Inventory | `/api/v1/inventory-movements` | 3 | GET, POST |
| Sales | `/api/v1/sales` | 6 | GET, POST |
| Dashboard | `/api/v1/dashboard` | 1 | GET |
| Utils | `/api/v1/utils` | 2 | GET, POST |
| **Total** | | **48** | |
