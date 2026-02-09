# Plan de Acción - Recuperación del Cronograma (Cerrado)

## OrbitEngine - Plataforma SaaS para Gestión de Pymes

**Fecha de Evaluación Inicial:** 4 de Febrero de 2026  
**Fecha de Cierre:** 9 de Febrero de 2026  
**Estado Actual:** Plan completado al 100% (cerrado)  
**Estado Esperado (inicial):** 60% completado (Sprint 4 - Ventas Core)  
**Resultado Final:** 100% de entregables del plan implementados y validados

---

## Resumen Ejecutivo

### Situación Final

| Aspecto | Esperado (plan) | Resultado final | Brecha |
|---------|------------------|-----------------|--------|
| **Sprints completados** | 3 de 7 (hito de recuperación) | 7 de 7 cerrados | 0 |
| **Módulos funcionales** | Auth + Inventario + Ventas | Auth + Inventario + Ventas + Clientes + Dashboard | Superado |
| **Progreso general** | 60% | 100% | 0 |

### Resultado del Plan

Se recuperó el retraso del proyecto y se completaron los módulos faltantes (Inventario, Ventas, Clientes), junto con dashboard, pruebas y estabilización. El alcance del plan quedó **cerrado y cumplido**.

---

## Estructura del Equipo

| Integrante | Rol | Responsabilidades Principales |
|------------|-----|------------------------------|
| **Integrante 1** | Backend - Inventario & Roles | Sistema de roles, módulo de inventario completo (backend + tests) |
| **Integrante 2** | Backend - Ventas & Clientes | Módulo de ventas y clientes (backend + tests), migraciones, CI/CD |
| **Integrante 3** | Frontend Lead | Todas las interfaces de usuario, integración con API, tests E2E |

---

## Definiciones Comunes

### Estructura de Datos (Contratos Backend-Frontend)

Para asegurar consistencia entre backend y frontend, definimos los modelos principales:

#### Organization & Multi-tenancy

```typescript
interface Organization {
  id: string
  name: string
  description?: string
  slug: string  // Identificador único: "tech-craft", "mi-empresa", etc.
  logo_url?: string
  is_active: boolean
  created_at: string
  updated_at: string
}
```

**Reglas del identificador (slug):**
- El campo `slug` debe ser único en todo el sistema
- Formato: lowercase, solo letras, números y guiones, 3-50 caracteres
- Validación: `^[a-z0-9-]{3,50}$`
- Ejemplos válidos: `tech-craft`, `mi-empresa`, `store123`
- Se usa como identificador interno, NO como subdominio
- Todas las organizaciones acceden desde: `orbitengine.com`

#### User & Authentication

```typescript
interface User {
  id: string
  organization_id: string
  organization?: Organization  // Include en respuestas de login
  role_id: number
  role?: Role  // Include en respuestas
  email: string
  first_name: string
  last_name: string
  phone?: string
  avatar_url?: string
  is_active: boolean
  is_verified: boolean
  last_login_at?: string
  created_at: string
  updated_at: string
}

interface Role {
  id: number
  name: "admin" | "seller" | "viewer"
  description: string
  permissions: string[]
  created_at: string
}

interface LoginResponse {
  access_token: string
  token_type: "bearer"
  user: User & { organization: Organization }  // Siempre incluye org en login
}
```

**Notas sobre User:**
- El campo `password_hash` existe en la base de datos pero NUNCA se incluye en las respuestas de la API
- Los campos `first_name` y `last_name` se combinan en el frontend para mostrar el nombre completo
- Los campos de seguridad (`failed_login_attempts`, `locked_until`) no se exponen en la API pública

**Multi-tenancy:**
- Todos los modelos principales (excepto Organization, Role, User) tendrán `organization_id`
- Aislamiento de datos: las queries siempre filtran por `organization_id` del usuario autenticado
- El `organization_id` se extrae del JWT token
- Un usuario solo puede pertenecer a una organización
- Los roles son globales, pero los permisos se aplican dentro de cada organización
- Todas las organizaciones usan la misma URL: `orbitengine.com`

#### Inventory Module

```typescript
interface Category {
  id: string
  organization_id: string
  name: string
  description?: string
  parent_id?: string  // Categoría padre (para jerarquías)
  parent?: Category  // Include opcional
  is_active: boolean
  created_at: string
  updated_at: string
}
```

**Notas sobre Category:**
- El campo `parent_id` permite crear jerarquías de categorías (ej: Electrónica > Computadoras > Laptops)
- Si `parent_id` es NULL, es una categoría raíz
- El campo `deleted_at` existe en BD pero no se expone en la API (soft delete)

```typescript
interface Product {
  id: string
  organization_id: string
  category_id?: string
  category?: Category  // Include en algunas respuestas
  sku: string  // Único por organización
  name: string
  description?: string
  image_url?: string
  cost_price: number
  sale_price: number
  stock_quantity: number
  stock_min: number
  stock_max?: number
  unit: string
  barcode?: string
  is_active: boolean
  created_at: string
  updated_at: string
}
```

**Notas sobre Product:**
- El campo `deleted_at` existe en BD pero no se expone en la API (soft delete)
- Los checks de validación en BD garantizan: `cost_price >= 0`, `sale_price >= 0`, `stock_quantity >= 0`

```typescript
interface InventoryMovement {
  id: string
  organization_id: string
  product_id: string
  product?: Product  // Include opcional
  user_id: string
  user?: User  // Include opcional
  movement_type: "sale" | "purchase" | "adjustment" | "return"
  quantity: number  // positivo = entrada, negativo = salida
  previous_stock: number
  new_stock: number
  reference_id?: string
  reference_type?: string  // "sale", "purchase", "adjustment"
  reason?: string
  created_at: string
}
```

**Notas sobre InventoryMovement:**
- `movement_type` debe coincidir con los valores definidos en BD: "sale", "purchase", "adjustment", "return"
- `reference_id` y `reference_type` vinculan el movimiento con la transacción que lo originó

#### Sales Module

```typescript
interface Customer {
  id: string
  organization_id: string
  document_type: string
  document_number: string  // Único por organización
  first_name: string
  last_name: string
  email?: string
  phone?: string
  address?: string
  city?: string
  country?: string
  notes?: string
  total_purchases: number  // Campo desnormalizado
  purchases_count: number  // Campo desnormalizado
  last_purchase_at?: string
  is_active: boolean
  created_at: string
  updated_at: string
}
```

**Notas sobre Customer:**
- Los campos `first_name` y `last_name` se combinan en el frontend para mostrar el nombre completo
- Los campos `total_purchases`, `purchases_count`, y `last_purchase_at` son desnormalizados y se actualizan automáticamente mediante triggers
- El campo `deleted_at` existe en BD pero no se expone en la API (soft delete)

```typescript
interface Sale {
  id: string
  organization_id: string
  invoice_number: string  // Único por organización
  customer_id?: string
  customer?: Customer  // Include opcional
  user_id: string
  user?: User  // Include opcional
  sale_date: string
  subtotal: number
  discount: number
  tax: number
  total: number
  payment_method: "cash" | "card" | "transfer" | "other"
  status: "completed" | "cancelled" | "pending"
  notes?: string
  cancelled_at?: string
  cancelled_by?: string  // UUID del usuario
  cancellation_reason?: string
  items?: SaleItem[]  // Include en detalle
  created_at: string
  updated_at: string
}
```

**Notas sobre Sale:**
- Los checks de validación en BD garantizan: `subtotal >= 0`, `discount >= 0`, `tax >= 0`, `total >= 0`
- El campo `cancelled_by` es una FK a `users.id` en la BD

```typescript
interface SaleItem {
  id: string
  sale_id: string
  product_id: string
  product_name: string  // Snapshot del nombre en el momento de la venta
  product_sku: string   // Snapshot del SKU en el momento de la venta
  quantity: number
  unit_price: number    // Snapshot del precio en el momento de la venta
  subtotal: number
  created_at: string
}
```

**Notas sobre SaleItem:**
- Los campos snapshot (`product_name`, `product_sku`, `unit_price`) preservan el estado del producto al momento de la venta
- El check de validación en BD garantiza: `quantity > 0`, `unit_price >= 0`, `subtotal >= 0`

#### Dashboard

```typescript
interface DashboardStats {
  sales_today: {
    count: number
    total: number
  }
  sales_month: {
    count: number
    total: number
  }
  low_stock_count: number
  average_ticket: number
  top_products: Array<{
    product_id: string
    product_name: string
    quantity_sold: number
    revenue: number
  }>
  sales_by_day: Array<{
    date: string
    count: number
    total: number
  }>
}
```

### Endpoints API (Convenciones)

Todos los endpoints seguirán el patrón REST bajo `/api/v1/`:

```
# Authentication
POST   /api/v1/login/access-token
POST   /api/v1/login/test-token
POST   /api/v1/password-recovery/{email}
POST   /api/v1/reset-password/

# Organizations (solo para registro inicial)
POST   /api/v1/organizations/signup     # Crear organización + usuario admin
GET    /api/v1/organizations/me          # Ver mi organización
PATCH  /api/v1/organizations/me          # Actualizar mi organización

# Users & Roles
GET    /api/v1/users/
POST   /api/v1/users/
GET    /api/v1/users/me
PATCH  /api/v1/users/me
GET    /api/v1/users/{id}
PATCH  /api/v1/users/{id}
DELETE /api/v1/users/{id}
GET    /api/v1/roles/

# Categories
GET    /api/v1/categories/
POST   /api/v1/categories/
GET    /api/v1/categories/{id}
PATCH  /api/v1/categories/{id}
DELETE /api/v1/categories/{id}

# Products
GET    /api/v1/products/
POST   /api/v1/products/
GET    /api/v1/products/low-stock
GET    /api/v1/products/{id}
PATCH  /api/v1/products/{id}
DELETE /api/v1/products/{id}
POST   /api/v1/products/{id}/adjust-stock
GET    /api/v1/products/{id}/movements

# Customers
GET    /api/v1/customers/
POST   /api/v1/customers/
GET    /api/v1/customers/{id}
PATCH  /api/v1/customers/{id}
DELETE /api/v1/customers/{id}
GET    /api/v1/customers/{id}/sales

# Sales
GET    /api/v1/sales/
POST   /api/v1/sales/
GET    /api/v1/sales/today
GET    /api/v1/sales/stats
GET    /api/v1/sales/{id}
POST   /api/v1/sales/{id}/cancel

# Dashboard
GET    /api/v1/dashboard/stats
```

**Nota sobre multi-tenancy:** 
- Todos los endpoints (excepto login y signup) automáticamente filtran por la organización del usuario autenticado
- No es necesario pasar `organization_id` en las requests, se obtiene del token JWT
- Backend debe validar que el usuario solo acceda a datos de su organización

### Convenciones de Respuestas

#### Listados paginados
```json
{
  "data": [...],
  "count": 100
}
```

#### Errores
```json
{
  "detail": "Mensaje de error descriptivo"
}
```

Status codes:
- 200: Success
- 201: Created
- 400: Bad Request (validación)
- 401: Unauthorized
- 403: Forbidden (permisos)
- 404: Not Found
- 409: Conflict (duplicados)
- 500: Internal Server Error

### Sistema de Permisos

**Roles:**
- **admin**: Acceso total a todo el sistema
- **seller**: Puede crear ventas, ver inventario, gestionar clientes (sin eliminar)
- **viewer**: Solo lectura de reportes y dashboard

**Implementación:**
- Backend: Dependencias de FastAPI `require_role("admin", "seller")`
- Frontend: Componente `<RoleGuard roles={["admin", "seller"]}>`

---

## Plan de Trabajo por Integrante (Estado Final)

### INTEGRANTE 1: Backend - Inventario & Roles

#### Objetivo
Implementar el sistema de roles y todo el backend del módulo de inventario.

#### Entregables (Completados)

**Semana 1: Sistema de Roles y Organizations**
- [x] Modelo `Organization` en base de datos
- [x] Modelo `Role` en base de datos
- [x] Actualización del modelo `User` con relaciones a `Organization` y `Role`
- [x] Endpoint de signup de organización (crea org + usuario admin)
- [x] Dependencias de autenticación por rol y organización
- [x] Migración y datos seed (3 roles)
- [x] Tests de permisos y aislamiento de datos

**Semana 2-3: Módulo de Inventario**
- [x] Modelos: `Category`, `Product`, `InventoryMovement` (todos con `organization_id`)
- [x] CRUD completo con filtrado automático por organización
- [x] Endpoints REST para categorías y productos
- [x] Validaciones: SKU único por organización, stock no negativo
- [x] Tests de integración (>60% cobertura)
- [x] Tests de aislamiento multi-tenant

**Semana 4-6: Soporte y Refinamiento**
- [x] Code reviews
- [x] Optimización de queries
- [x] Documentación de API
- [x] Bug fixes

#### Tiempo Estimado
~56 horas (con buffer)

---

### INTEGRANTE 2: Backend - Ventas & Clientes

#### Objetivo
Implementar los módulos de ventas y clientes, coordinar migraciones y configurar CI/CD.

#### Entregables (Completados)

**Semana 1: Infraestructura y Multi-tenancy**
- [x] Consolidar todas las migraciones de BD (incluyendo Organization)
- [x] Agregar `organization_id` a todos los modelos que lo necesiten
- [x] Middleware/dependencia para filtrado automático por organización
- [x] Script de datos seed completo (orgs de prueba, roles, productos demo)
- [x] Configurar GitHub Actions (CI/CD)
- [x] Documentar proceso de setup

**Semana 2: Módulo de Clientes**
- [x] Modelo `Customer` (con `organization_id`)
- [x] CRUD completo con filtrado por organización
- [x] Endpoints REST
- [x] Validación documento único por organización
- [x] Tests

**Semana 3-4: Módulo de Ventas**
- [x] Modelos: `Sale`, `SaleItem` (con `organization_id`)
- [x] Lógica de negocio (transacciones):
  - [x] Validar stock disponible
  - [x] Crear venta + items
  - [x] Actualizar stock automáticamente
  - [x] Actualizar estadísticas de cliente
  - [x] Cancelación con reversión de stock
- [x] Invoice number único por organización
- [x] Endpoint de estadísticas para dashboard
- [x] Tests complejos (escenarios de stock, cancelaciones, aislamiento)

**Semana 5-6: Features Adicionales**
- [x] Endpoint `/dashboard/stats` (filtrado por org)
- [x] Optimizaciones de rendimiento
- [x] Bug fixes y code reviews

#### Tiempo Estimado
~67 horas (con buffer)

---

### INTEGRANTE 3: Frontend Lead

#### Objetivo
Desarrollar todas las interfaces de usuario y asegurar la integración con el backend.

#### Entregables (Completados)

**Semana 1: Sistema de Roles UI y Signup de Organización**
- [x] Hook `useAuth` actualizado con roles y organización
- [x] Componente `<RoleGuard>`
- [x] Navegación dinámica según rol
- [x] Página de signup de organización (formulario: nombre empresa, slug, admin user)
- [x] Validación de slug único en tiempo real
- [x] Regeneración de cliente API

**Semana 2-3: Módulo de Inventario**
- [x] Página de listado de productos (tabla, filtros, búsqueda)
- [x] Formularios de producto (crear/editar/eliminar)
- [x] Ajuste de stock
- [x] Página de alertas de stock bajo
- [x] Gestión de categorías
- [x] Historial de movimientos

**Semana 4: Módulo de Ventas**
- [x] Interfaz POS (punto de venta) para registrar ventas
- [x] Historial de ventas con filtros
- [x] Detalle de venta
- [x] Cancelación de venta

**Semana 5: Módulo de Clientes**
- [x] Listado de clientes
- [x] Formularios (crear/editar)
- [x] Perfil de cliente con estadísticas
- [x] Historial de compras

**Semana 6: Dashboard y Testing**
- [x] Dashboard con KPIs y gráficos
- [x] Mostrar información de la organización en la UI
- [x] Tests E2E con Playwright (flujos críticos, incluyendo signup de org)
- [x] Refinamiento de UX
- [x] Bug fixes

#### Tiempo Estimado
~119 horas (con buffer)

---

## Cronograma Integrado (Ejecución Final)

| Semana | Backend 1 | Backend 2 | Frontend | Entregable | Estado |
|--------|-----------|-----------|----------|------------|--------|
| **1** | Sistema de Roles | Migraciones + CI/CD | Roles UI | Roles funcionales end-to-end | Completado |
| **2** | Modelos Inventario + CRUD | Módulo Clientes | UI Productos (base) | Backend inventario y clientes | Completado |
| **3** | Endpoints Inventario + Tests | Modelos Ventas + CRUD | UI Inventario completo | Módulo Inventario completo | Completado |
| **4** | Soporte + Code Review | Endpoints Ventas + Tests | POS + UI Ventas | Backend ventas completo, POS funcional | Completado |
| **5** | Bug fixes + Optimizaciones | Dashboard Stats + Tests | UI Clientes | Módulos de ventas y clientes completos | Completado |
| **6** | Documentación | Bug fixes | Dashboard + Tests E2E | Sistema completo y estable | Completado |

---

## Dependencias Críticas

```
Semana 1:
  Backend1 (Roles) ──────► Frontend (Roles UI)
  Backend2 (Migraciones) ► Base de datos lista para todos

Semana 2-3:
  Backend1 (Modelos) ──► Backend1 (Endpoints) ──► Backend2 (Generar cliente) ──► Frontend (UI)
  
Semana 3-4:
  Backend2 (Ventas CRUD) ──► Backend2 (Endpoints) ──► Frontend (POS)
  
Semana 5-6:
  Backend2 (Dashboard API) ──► Frontend (Dashboard UI)
```

**Regla de integración:** Frontend solo integra un endpoint después de que el backend lo confirme como estable y probado.

---

## Coordinación del Equipo

### Comunicación

**Daily Sync (15 min):**
- Qué hice ayer
- Qué haré hoy
- Bloqueantes

**Canales:**
- Chat diario: Discord/Slack
- Code reviews: GitHub PRs
- Documentación: README + comentarios en código

### Flujo de Trabajo

1. **Backend 1 y Backend 2** coordinan antes de crear migraciones
2. **Backend 2** es responsable de consolidar y ejecutar todas las migraciones
3. **Backend 2** ejecuta `bun run generate-client` después de agregar endpoints
4. **Backend** notifica a **Frontend** cuando un endpoint está listo para integrar
5. Todos los PRs requieren al menos 1 aprobación
6. Merge a `main` solo con CI en verde

### Estándares de Calidad

**Backend:**
- Cobertura de tests > 60%
- Ruff + Mypy sin errores
- Documentación de funciones complejas

**Frontend:**
- Biome lint sin errores
- Componentes reutilizables
- Loading states y error handling en todas las mutaciones

---

## Métricas de Éxito (Resultado)

Al cierre del plan:

**Funcionalidad:**
- [x] Sistema de 3 roles funcionando (Admin, Seller, Viewer)
- [x] CRUD completo de productos y categorías
- [x] Alertas de stock bajo visibles
- [x] Historial de movimientos de inventario
- [x] CRUD completo de clientes
- [x] Registro de ventas con actualización automática de stock
- [x] Historial de ventas con filtros
- [x] Cancelación de ventas con reversión de inventario
- [x] Dashboard con KPIs principales

**Calidad:**
- [x] Cobertura de tests backend > 60%
- [x] Tests E2E para flujos críticos
- [x] Pipeline de CI funcionando
- [x] Zero errores críticos en staging

**Documentación:**
- [x] README actualizado con setup completo
- [x] API documentada (OpenAPI/Swagger)

---

## Riesgos y Mitigación (Cierre)

| Riesgo | Probabilidad inicial | Impacto | Mitigación aplicada | Estado |
|--------|----------------------|---------|---------------------|--------|
| Complejidad en lógica de ventas | Alta | Alto | Simplificación de reglas + pruebas de escenarios críticos | Mitigado |
| Desincronización backend-frontend | Media | Alto | Cliente API regenerado frecuentemente + sync diario | Mitigado |
| Conflictos en migraciones | Media | Medio | Coordinación centralizada de migraciones | Mitigado |
| Falta de tiempo | Alta | Alto | Priorización semanal y gestión estricta de alcance | Resuelto |
| Bugs en integración | Media | Alto | Tests de integración + staging + fixes iterativos | Mitigado |

---

## Features Pospuestos

Con el plan de recuperación completado, estos puntos quedan fuera del alcance del cierre y pasan a roadmap posterior:

1. IA/Predicción de demanda
2. Exportación a PDF de facturas
3. Multi-tenancy completo
4. Verificación de email
5. Reportes avanzados con gráficos complejos
6. Importación masiva de productos
7. Sistema de notificaciones

---

## Conclusión

El plan redistribuyó el trabajo entre 3 personas con responsabilidades claras y puntos de sincronización efectivos. La ejecución se completó según lo definido y el cronograma quedó recuperado.

**Objetivo inicial:** Recuperar el proyecto del 15% al ~70% de completitud en 6 semanas.  
**Resultado:** Objetivo cumplido y superado, con cierre de entregables al 100%.

**Factor crítico de éxito validado:** Comunicación diaria, disciplina de integración y control de calidad continuo.

---

**Elaborado:** 4 de Febrero de 2026  
**Cierre del plan:** 9 de Febrero de 2026  
**Estado del documento:** Cerrado (ejecución completada)  
**Versión:** 4.0
