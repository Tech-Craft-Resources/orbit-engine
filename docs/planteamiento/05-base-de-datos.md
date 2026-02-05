# Propuesta de Base de Datos
## OrbitEngine - Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Versión:** 1.0  
**Fecha:** Octubre 2025

---

## Tabla de Contenidos

1. [Visión General](#1-visión-general)
2. [Modelo Entidad-Relación](#2-modelo-entidad-relación)
3. [Diccionario de Datos](#3-diccionario-de-datos)
4. [Índices y Optimización](#4-índices-y-optimización)
5. [Seguridad y Multi-tenancy](#5-seguridad-y-multi-tenancy)
6. [Estrategia de Backups](#6-estrategia-de-backups)
7. [Consideraciones de Escalabilidad](#7-consideraciones-de-escalabilidad)

---

## 1. Visión General

### 1.1 Sistema Gestor de Base de Datos

**PostgreSQL 15+**

### 1.2 Principios de Diseño

- **Multi-tenancy:** Aislamiento de datos por organización mediante `organization_id`
- **Integridad Referencial:** Foreign keys con cascadas apropiadas
- **Auditoría:** Campos `created_at`, `updated_at`, `deleted_at` (soft delete)
- **Normalización:** 3NF (Tercera Forma Normal) con desnormalizaciones estratégicas
- **Escalabilidad:** Diseño preparado para particionado futuro

### 1.3 Convenciones de Nombres

- **Tablas:** snake_case, plural (ej: `users`, `products`)
- **Columnas:** snake_case
- **PKs:** `id` (UUID o BIGSERIAL)
- **FKs:** `{tabla_singular}_id` (ej: `user_id`, `product_id`)
- **Timestamps:** `created_at`, `updated_at`, `deleted_at`
- **Índices:** `idx_{tabla}_{columna(s)}`
- **Foreign Keys:** `fk_{tabla_origen}_{tabla_destino}`

---

## 2. Modelo Entidad-Relación

### 2.1 Diagrama ER Simplificado

```
┌──────────────────┐
│  organizations   │
└──────┬───────────┘
       │
       │ 1:N
       │
┌──────▼───────┐         ┌──────────────┐
│    users     │────────►│    roles     │
└──────┬───────┘   N:1   └──────────────┘
       │
       │ 1:N
       │
┌──────▼───────┐         ┌──────────────┐
│  customers   │         │  categories  │
└──────────────┘         └──────┬───────┘
                                │ 1:N
       ┌────────────────────────┘
       │
┌──────▼───────┐         ┌──────────────┐
│   products   │◄────────│ inventory_   │
└──────┬───────┘  1:N    │  movements   │
       │                 └──────────────┘
       │ 1:N
       │
┌──────▼───────┐         ┌──────────────┐
│  sale_items  │────────►│    sales     │
└──────────────┘   N:1   └──────┬───────┘
                                │ N:1
                                │
                         ┌──────▼───────┐
                         │  customers   │
                         └──────────────┘

┌──────────────┐         ┌──────────────┐
│ predictions  │         │ audit_logs   │
└──────────────┘         └──────────────┘
```

---

## 3. Diccionario de Datos

### 3.1 Tabla: `organizations`
**Descripción:** Organizaciones que usan la plataforma (multi-tenancy)

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| name | VARCHAR(255) | NOT NULL | Nombre de la organización |
| domain | VARCHAR(100) | UNIQUE, NOT NULL | Dominio único (subdominio) |
| description | TEXT | NULL | Descripción de la organización |
| logo_url | VARCHAR(500) | NULL | URL del logo en S3 |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Organización activa |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |

**Índices:**
- `idx_organizations_domain` UNIQUE en `domain`
- `idx_organizations_is_active` en `is_active`

---

### 3.2 Tabla: `roles`
**Descripción:** Roles del sistema

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | SERIAL | PK, NOT NULL | Identificador único |
| name | VARCHAR(50) | UNIQUE, NOT NULL | admin, seller, viewer |
| description | TEXT | NULL | Descripción del rol |
| permissions | JSONB | DEFAULT '[]' | Array de permisos |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |

**Datos Iniciales:**
```sql
INSERT INTO roles (name, description, permissions) VALUES
  ('admin', 'Administrador con acceso completo', '["*"]'),
  ('seller', 'Vendedor con acceso a ventas e inventario', '["sales.*", "inventory.read", "customers.*"]'),
  ('viewer', 'Solo lectura de reportes', '["reports.read", "dashboard.read"]');
```

---

### 3.3 Tabla: `users`
**Descripción:** Usuarios del sistema

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| role_id | INTEGER | FK(roles.id), NOT NULL | Rol del usuario |
| email | VARCHAR(255) | NOT NULL | Email (único por organización) |
| password_hash | VARCHAR(255) | NOT NULL | Hash bcrypt de contraseña |
| first_name | VARCHAR(100) | NOT NULL | Nombre |
| last_name | VARCHAR(100) | NOT NULL | Apellido |
| phone | VARCHAR(50) | NULL | Teléfono |
| avatar_url | VARCHAR(500) | NULL | URL de avatar en S3 |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Usuario activo |
| is_verified | BOOLEAN | NOT NULL, DEFAULT FALSE | Email verificado |
| last_login_at | TIMESTAMP | NULL | Último inicio de sesión |
| failed_login_attempts | INTEGER | NOT NULL, DEFAULT 0 | Intentos fallidos |
| locked_until | TIMESTAMP | NULL | Bloqueo temporal |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |
| deleted_at | TIMESTAMP | NULL | Soft delete |

**Índices:**
- `idx_users_organization_email` UNIQUE en `(organization_id, email)` WHERE deleted_at IS NULL
- `idx_users_organization_id` en `organization_id`
- `idx_users_role_id` en `role_id`
- `idx_users_is_active` en `is_active`

**Constraints:**
- `fk_users_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_users_role` FOREIGN KEY (role_id) REFERENCES roles(id)

---

### 3.4 Tabla: `categories`
**Descripción:** Categorías de productos

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| name | VARCHAR(100) | NOT NULL | Nombre de categoría |
| description | TEXT | NULL | Descripción |
| parent_id | UUID | FK(categories.id), NULL | Categoría padre (jerarquía) |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Categoría activa |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |
| deleted_at | TIMESTAMP | NULL | Soft delete |

**Índices:**
- `idx_categories_organization_id` en `organization_id`
- `idx_categories_parent_id` en `parent_id`

**Constraints:**
- `fk_categories_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_categories_parent` FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL

---

### 3.5 Tabla: `products`
**Descripción:** Productos en inventario

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| category_id | UUID | FK(categories.id), NULL | Categoría del producto |
| sku | VARCHAR(100) | NOT NULL | Código SKU |
| name | VARCHAR(255) | NOT NULL | Nombre del producto |
| description | TEXT | NULL | Descripción detallada |
| image_url | VARCHAR(500) | NULL | URL de imagen en S3 |
| cost_price | DECIMAL(12,2) | NOT NULL, CHECK (cost_price >= 0) | Precio de costo |
| sale_price | DECIMAL(12,2) | NOT NULL, CHECK (sale_price >= 0) | Precio de venta |
| stock_quantity | INTEGER | NOT NULL, DEFAULT 0, CHECK (stock_quantity >= 0) | Cantidad en stock |
| stock_min | INTEGER | NOT NULL, DEFAULT 0 | Stock mínimo |
| stock_max | INTEGER | NULL | Stock máximo |
| unit | VARCHAR(50) | NOT NULL, DEFAULT 'unit' | Unidad de medida |
| barcode | VARCHAR(100) | NULL | Código de barras |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Producto activo |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |
| deleted_at | TIMESTAMP | NULL | Soft delete |

**Índices:**
- `idx_products_organization_sku` UNIQUE en `(organization_id, sku)` WHERE deleted_at IS NULL
- `idx_products_organization_id` en `organization_id`
- `idx_products_category_id` en `category_id`
- `idx_products_stock_quantity` en `stock_quantity` (para alertas)
- `idx_products_is_active` en `is_active`
- `idx_products_barcode` en `barcode`

**Constraints:**
- `fk_products_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_products_category` FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL

---

### 3.6 Tabla: `inventory_movements`
**Descripción:** Historial de movimientos de inventario

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| product_id | UUID | FK(products.id), NOT NULL | Producto afectado |
| user_id | UUID | FK(users.id), NOT NULL | Usuario responsable |
| movement_type | VARCHAR(50) | NOT NULL | sale, purchase, adjustment, return |
| quantity | INTEGER | NOT NULL | Cantidad (+ entrada, - salida) |
| previous_stock | INTEGER | NOT NULL | Stock antes del movimiento |
| new_stock | INTEGER | NOT NULL | Stock después del movimiento |
| reference_id | UUID | NULL | ID de venta/compra relacionada |
| reference_type | VARCHAR(50) | NULL | sale, purchase, adjustment |
| reason | TEXT | NULL | Motivo del movimiento |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha del movimiento |

**Índices:**
- `idx_inventory_movements_organization_id` en `organization_id`
- `idx_inventory_movements_product_id` en `product_id`
- `idx_inventory_movements_created_at` en `created_at`
- `idx_inventory_movements_reference` en `(reference_type, reference_id)`

**Constraints:**
- `fk_inventory_movements_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_inventory_movements_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
- `fk_inventory_movements_user` FOREIGN KEY (user_id) REFERENCES users(id)

---

### 3.7 Tabla: `customers`
**Descripción:** Clientes de la empresa

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| document_type | VARCHAR(50) | NOT NULL | DNI, RUC, Passport, etc. |
| document_number | VARCHAR(50) | NOT NULL | Número de documento |
| first_name | VARCHAR(100) | NOT NULL | Nombre |
| last_name | VARCHAR(100) | NOT NULL | Apellido |
| email | VARCHAR(255) | NULL | Email |
| phone | VARCHAR(50) | NULL | Teléfono |
| address | TEXT | NULL | Dirección |
| city | VARCHAR(100) | NULL | Ciudad |
| country | VARCHAR(100) | NULL | País |
| notes | TEXT | NULL | Notas adicionales |
| total_purchases | DECIMAL(12,2) | NOT NULL, DEFAULT 0 | Total comprado (desnormalizado) |
| purchases_count | INTEGER | NOT NULL, DEFAULT 0 | Número de compras (desnormalizado) |
| last_purchase_at | TIMESTAMP | NULL | Última compra |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Cliente activo |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |
| deleted_at | TIMESTAMP | NULL | Soft delete |

**Índices:**
- `idx_customers_organization_document` UNIQUE en `(organization_id, document_number)` WHERE deleted_at IS NULL
- `idx_customers_organization_id` en `organization_id`
- `idx_customers_email` en `email`
- `idx_customers_phone` en `phone`
- `idx_customers_last_purchase_at` en `last_purchase_at`

**Constraints:**
- `fk_customers_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE

**Nota:** `total_purchases` y `purchases_count` son campos desnormalizados por rendimiento, actualizados mediante triggers.

---

### 3.8 Tabla: `sales`
**Descripción:** Ventas realizadas

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| invoice_number | VARCHAR(50) | NOT NULL | Número de factura |
| customer_id | UUID | FK(customers.id), NULL | Cliente (opcional) |
| user_id | UUID | FK(users.id), NOT NULL | Vendedor |
| sale_date | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de venta |
| subtotal | DECIMAL(12,2) | NOT NULL, CHECK (subtotal >= 0) | Subtotal |
| discount | DECIMAL(12,2) | NOT NULL, DEFAULT 0, CHECK (discount >= 0) | Descuento aplicado |
| tax | DECIMAL(12,2) | NOT NULL, DEFAULT 0, CHECK (tax >= 0) | Impuestos |
| total | DECIMAL(12,2) | NOT NULL, CHECK (total >= 0) | Total final |
| payment_method | VARCHAR(50) | NOT NULL | cash, card, transfer, other |
| status | VARCHAR(50) | NOT NULL, DEFAULT 'completed' | completed, cancelled, pending |
| notes | TEXT | NULL | Notas adicionales |
| cancelled_at | TIMESTAMP | NULL | Fecha de cancelación |
| cancelled_by | UUID | FK(users.id), NULL | Usuario que canceló |
| cancellation_reason | TEXT | NULL | Motivo de cancelación |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de actualización |

**Índices:**
- `idx_sales_organization_invoice` UNIQUE en `(organization_id, invoice_number)`
- `idx_sales_organization_id` en `organization_id`
- `idx_sales_customer_id` en `customer_id`
- `idx_sales_user_id` en `user_id`
- `idx_sales_sale_date` en `sale_date`
- `idx_sales_status` en `status`
- `idx_sales_payment_method` en `payment_method`

**Constraints:**
- `fk_sales_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_sales_customer` FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE SET NULL
- `fk_sales_user` FOREIGN KEY (user_id) REFERENCES users(id)
- `fk_sales_cancelled_by` FOREIGN KEY (cancelled_by) REFERENCES users(id)

---

### 3.9 Tabla: `sale_items`
**Descripción:** Detalles de productos en cada venta

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| sale_id | UUID | FK(sales.id), NOT NULL | Venta a la que pertenece |
| product_id | UUID | FK(products.id), NOT NULL | Producto vendido |
| product_name | VARCHAR(255) | NOT NULL | Nombre del producto (snapshot) |
| product_sku | VARCHAR(100) | NOT NULL | SKU del producto (snapshot) |
| quantity | INTEGER | NOT NULL, CHECK (quantity > 0) | Cantidad vendida |
| unit_price | DECIMAL(12,2) | NOT NULL, CHECK (unit_price >= 0) | Precio unitario (snapshot) |
| subtotal | DECIMAL(12,2) | NOT NULL, CHECK (subtotal >= 0) | Subtotal (quantity * unit_price) |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |

**Índices:**
- `idx_sale_items_sale_id` en `sale_id`
- `idx_sale_items_product_id` en `product_id`

**Constraints:**
- `fk_sale_items_sale` FOREIGN KEY (sale_id) REFERENCES sales(id) ON DELETE CASCADE
- `fk_sale_items_product` FOREIGN KEY (product_id) REFERENCES products(id)

**Nota:** Se guardan snapshots (`product_name`, `product_sku`, `unit_price`) para mantener histórico aunque el producto cambie.

---

### 3.10 Tabla: `predictions`
**Descripción:** Predicciones de demanda generadas por IA

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| product_id | UUID | FK(products.id), NOT NULL | Producto predicho |
| prediction_date | DATE | NOT NULL | Fecha para la que se predice |
| predicted_quantity | DECIMAL(10,2) | NOT NULL | Cantidad predicha |
| confidence_score | DECIMAL(5,2) | NOT NULL, CHECK (confidence_score >= 0 AND confidence_score <= 100) | Nivel de confianza (0-100) |
| model_version | VARCHAR(50) | NOT NULL | Versión del modelo usado |
| actual_quantity | INTEGER | NULL | Cantidad real vendida (llenado después) |
| prediction_error | DECIMAL(10,2) | NULL | Error de predicción |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de creación |

**Índices:**
- `idx_predictions_organization_product_date` UNIQUE en `(organization_id, product_id, prediction_date)`
- `idx_predictions_organization_id` en `organization_id`
- `idx_predictions_product_id` en `product_id`
- `idx_predictions_prediction_date` en `prediction_date`

**Constraints:**
- `fk_predictions_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_predictions_product` FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE

---

### 3.11 Tabla: `audit_logs`
**Descripción:** Log de auditoría de acciones críticas

| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| id | UUID | PK, NOT NULL, DEFAULT uuid_generate_v4() | Identificador único |
| organization_id | UUID | FK(organizations.id), NOT NULL | Organización a la que pertenece |
| user_id | UUID | FK(users.id), NULL | Usuario que realizó la acción |
| action | VARCHAR(100) | NOT NULL | create, update, delete, login, etc. |
| entity_type | VARCHAR(100) | NOT NULL | product, sale, user, etc. |
| entity_id | UUID | NULL | ID de la entidad afectada |
| old_values | JSONB | NULL | Valores anteriores |
| new_values | JSONB | NULL | Valores nuevos |
| ip_address | VARCHAR(45) | NULL | IP del usuario |
| user_agent | TEXT | NULL | User agent del navegador |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Fecha de la acción |

**Índices:**
- `idx_audit_logs_organization_id` en `organization_id`
- `idx_audit_logs_user_id` en `user_id`
- `idx_audit_logs_action` en `action`
- `idx_audit_logs_entity` en `(entity_type, entity_id)`
- `idx_audit_logs_created_at` en `created_at`

**Constraints:**
- `fk_audit_logs_organization` FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
- `fk_audit_logs_user` FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL

**Particionado (Opcional para el futuro):**
- Particionar por rango de `created_at` (mensual o trimestral)

---

## 4. Índices y Optimización

### 4.1 Índices Estratégicos

#### Índices Compuestos Críticos

```sql
-- Usuarios únicos por organización
CREATE UNIQUE INDEX idx_users_organization_email 
ON users(organization_id, email) 
WHERE deleted_at IS NULL;

-- Productos únicos por organización
CREATE UNIQUE INDEX idx_products_organization_sku 
ON products(organization_id, sku) 
WHERE deleted_at IS NULL;

-- Clientes únicos por organización
CREATE UNIQUE INDEX idx_customers_organization_document 
ON customers(organization_id, document_number) 
WHERE deleted_at IS NULL;

-- Factura única por organización
CREATE UNIQUE INDEX idx_sales_organization_invoice 
ON sales(organization_id, invoice_number);
```

#### Índices de Rango para Reportes

```sql
-- Ventas por fecha (reportes)
CREATE INDEX idx_sales_organization_date 
ON sales(organization_id, sale_date DESC);

-- Movimientos de inventario por fecha
CREATE INDEX idx_inventory_movements_organization_date 
ON inventory_movements(organization_id, created_at DESC);
```

#### Índices para Queries Frecuentes

```sql
-- Productos con stock bajo
CREATE INDEX idx_products_low_stock 
ON products(organization_id, stock_quantity) 
WHERE is_active = TRUE AND stock_quantity < stock_min;

-- Clientes activos recientes
CREATE INDEX idx_customers_recent_active 
ON customers(organization_id, last_purchase_at DESC) 
WHERE is_active = TRUE AND deleted_at IS NULL;
```

### 4.2 Estimación de Tamaño de Datos

**Escenario: Pyme promedio con 500 productos, 1000 clientes, 100 ventas/día**

| Tabla | Registros/Año | Tamaño Estimado |
|-------|---------------|-----------------|
| organizations | 1 | < 1 KB |
| users | 5 | < 10 KB |
| categories | 20 | < 5 KB |
| products | 500 | ~200 KB |
| customers | 1,000 | ~500 KB |
| sales | 36,500 | ~15 MB |
| sale_items | 109,500 | ~30 MB |
| inventory_movements | 150,000 | ~50 MB |
| predictions | 18,250 | ~5 MB |
| audit_logs | 200,000 | ~100 MB |
| **TOTAL** | | **~200 MB/año** |

**Conclusión:** Base de datos muy manejable incluso para instancias pequeñas de RDS.

---

## 5. Seguridad y Multi-tenancy

### 5.1 Estrategia Multi-tenant

**Enfoque: Shared Database, Shared Schema con Row-Level Security**

#### Ventajas:
- ✅ Menor costo (una sola BD)
- ✅ Mantenimiento simplificado
- ✅ Backups centralizados
- ✅ Apropiado para el alcance del proyecto

#### Implementación:

**1. Organization ID en Todas las Tablas**
```sql
-- Todas las tablas de datos tienen organization_id
ALTER TABLE products ADD COLUMN organization_id UUID NOT NULL;
```

**2. Row-Level Security (RLS) en PostgreSQL**
```sql
-- Habilitar RLS en tabla
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

-- Policy para SELECT
CREATE POLICY organization_isolation_policy ON products
  FOR ALL
  USING (organization_id = current_setting('app.current_organization')::UUID);
```

**3. Set Organization en Sesión**
```python
# En el backend, después de autenticación
async def set_organization_context(organization_id: UUID):
    await db.execute(f"SET app.current_organization = '{organization_id}'")
```

**4. Validación en ORM**
```python
# SQLAlchemy filter automático
class OrganizationMixin:
    organization_id = Column(UUID, nullable=False)
    
    @declared_attr
    def __table_args__(cls):
        return (
            Index(f'idx_{cls.__tablename__}_organization_id', 'organization_id'),
        )

# Uso
query = db.query(Product).filter(Product.organization_id == current_organization_id)
```

### 5.2 Seguridad de Datos

#### Encriptación en Reposo
- AWS RDS con encriptación habilitada
- Backups encriptados

#### Encriptación en Tránsito
- SSL/TLS para conexiones a BD
- HTTPS para toda comunicación

#### Protección de PII (Personally Identifiable Information)
```sql
-- Considerar encriptación de columnas sensibles
-- Extensión pgcrypto
CREATE EXTENSION pgcrypto;

-- Ejemplo (si se requiere)
ALTER TABLE customers ADD COLUMN document_number_encrypted BYTEA;
```

---

## 6. Estrategia de Backups

### 6.1 Backups Automáticos (AWS RDS)

| Tipo | Frecuencia | Retención | Ubicación |
|------|-----------|-----------|-----------|
| Automated Backups | Diario | 7 días | Región AWS |
| Manual Snapshots | Semanal | 30 días | Región AWS |
| Export to S3 | Mensual | 1 año | S3 Glacier |

### 6.2 Estrategia de Recuperación

**RTO (Recovery Time Objective):** 4 horas  
**RPO (Recovery Point Objective):** 24 horas

#### Procedimiento de Restore
1. Identificar snapshot más reciente
2. Restore desde RDS snapshot
3. Actualizar endpoint en aplicación
4. Verificar integridad de datos
5. Reanudar operaciones

### 6.3 Testing de Backups

- **Mensual:** Restore de prueba en ambiente staging
- **Validación:** Verificar integridad referencial
- **Documentación:** Procedimiento paso a paso

---

## 7. Consideraciones de Escalabilidad

### 7.1 Estrategias de Escalamiento

#### Escalamiento Vertical (Corto Plazo)
- Aumentar CPU/RAM de instancia RDS
- De db.t3.micro → db.t3.small → db.t3.medium

#### Escalamiento Horizontal (Largo Plazo)

**1. Read Replicas**
```
Primary (Write) ──► Read Replica 1 (Read)
                 └─► Read Replica 2 (Read)
```
- Reportes y analytics en replicas
- Transacciones en primary

**2. Connection Pooling**
```python
# SQLAlchemy pool
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True
)
```

**3. Particionado de Tablas (Futuro)**
```sql
-- Particionar audit_logs por mes
CREATE TABLE audit_logs (
    ...
) PARTITION BY RANGE (created_at);

CREATE TABLE audit_logs_2025_01 PARTITION OF audit_logs
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

### 7.2 Optimizaciones de Queries

#### Uso de EXPLAIN ANALYZE
```sql
EXPLAIN ANALYZE
SELECT * FROM sales 
WHERE organization_id = '...' 
  AND sale_date BETWEEN '2026-01-01' AND '2026-01-31';
```

#### Materialized Views para Reportes
```sql
-- Vista materializada para dashboard
CREATE MATERIALIZED VIEW mv_sales_summary AS
SELECT 
    organization_id,
    DATE(sale_date) as date,
    COUNT(*) as total_sales,
    SUM(total) as total_amount
FROM sales
WHERE status = 'completed'
GROUP BY organization_id, DATE(sale_date);

-- Refresh diario
CREATE INDEX ON mv_sales_summary(organization_id, date);
```

#### Cacheo con Redis
```python
# Cache de productos frecuentes
@cache(expire=3600)  # 1 hora
async def get_products(organization_id: UUID):
    return await db.query(Product).filter_by(organization_id=organization_id).all()
```

### 7.3 Monitoreo de Performance

**Métricas Clave:**
- Query execution time
- Connection pool usage
- Table bloat
- Index usage
- Slow query log

**Herramientas:**
- AWS RDS Performance Insights
- pg_stat_statements
- CloudWatch Metrics

---

## 8. Triggers y Funciones Importantes

### 8.1 Trigger: Actualizar Stock en Venta

```sql
CREATE OR REPLACE FUNCTION update_stock_on_sale()
RETURNS TRIGGER AS $$
BEGIN
    -- Reducir stock del producto
    UPDATE products
    SET stock_quantity = stock_quantity - NEW.quantity,
        updated_at = NOW()
    WHERE id = NEW.product_id;
    
    -- Registrar movimiento de inventario
    INSERT INTO inventory_movements (
        organization_id, product_id, user_id, movement_type,
        quantity, previous_stock, new_stock, reference_id, reference_type
    ) VALUES (
        (SELECT organization_id FROM products WHERE id = NEW.product_id),
        NEW.product_id,
        (SELECT user_id FROM sales WHERE id = NEW.sale_id),
        'sale',
        -NEW.quantity,
        (SELECT stock_quantity + NEW.quantity FROM products WHERE id = NEW.product_id),
        (SELECT stock_quantity FROM products WHERE id = NEW.product_id),
        NEW.sale_id,
        'sale'
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_stock_on_sale
AFTER INSERT ON sale_items
FOR EACH ROW
EXECUTE FUNCTION update_stock_on_sale();
```

### 8.2 Trigger: Actualizar Estadísticas de Cliente

```sql
CREATE OR REPLACE FUNCTION update_customer_stats()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' THEN
        UPDATE customers
        SET total_purchases = total_purchases + NEW.total,
            purchases_count = purchases_count + 1,
            last_purchase_at = NEW.sale_date,
            updated_at = NOW()
        WHERE id = NEW.customer_id;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_customer_stats
AFTER INSERT ON sales
FOR EACH ROW
WHEN (NEW.customer_id IS NOT NULL)
EXECUTE FUNCTION update_customer_stats();
```

### 8.3 Trigger: Updated_at Automático

```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar a todas las tablas relevantes
CREATE TRIGGER update_products_updated_at BEFORE UPDATE ON products
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- etc.
```

---

## 9. Queries Comunes Optimizadas

### 9.1 Dashboard - Ventas del Día

```sql
SELECT 
    COUNT(*) as total_sales,
    SUM(total) as total_amount,
    AVG(total) as average_ticket
FROM sales
WHERE organization_id = :organization_id
  AND DATE(sale_date) = CURRENT_DATE
  AND status = 'completed';
```

### 9.2 Productos con Stock Bajo

```sql
SELECT 
    p.id,
    p.name,
    p.sku,
    p.stock_quantity,
    p.stock_min,
    c.name as category_name
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE p.organization_id = :organization_id
  AND p.is_active = TRUE
  AND p.stock_quantity <= p.stock_min
  AND p.deleted_at IS NULL
ORDER BY p.stock_quantity ASC;
```

### 9.3 Top 10 Productos Más Vendidos

```sql
SELECT 
    p.id,
    p.name,
    p.sku,
    SUM(si.quantity) as total_sold,
    SUM(si.subtotal) as total_revenue
FROM products p
INNER JOIN sale_items si ON p.id = si.product_id
INNER JOIN sales s ON si.sale_id = s.id
WHERE s.organization_id = :organization_id
  AND s.sale_date >= :start_date
  AND s.sale_date < :end_date
  AND s.status = 'completed'
GROUP BY p.id, p.name, p.sku
ORDER BY total_sold DESC
LIMIT 10;
```

### 9.4 Historial de Compras de Cliente

```sql
SELECT 
    s.id,
    s.invoice_number,
    s.sale_date,
    s.total,
    s.payment_method,
    u.first_name || ' ' || u.last_name as seller_name
FROM sales s
INNER JOIN users u ON s.user_id = u.id
WHERE s.customer_id = :customer_id
  AND s.status = 'completed'
ORDER BY s.sale_date DESC;
```

---

## 10. Script de Inicialización

### 10.1 Extensiones Requeridas

```sql
-- UUID support
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crypto functions (opcional)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Full text search (futuro)
CREATE EXTENSION IF NOT EXISTS pg_trgm;
```

### 10.2 Datos Iniciales

```sql
-- Roles
INSERT INTO roles (name, description, permissions) VALUES
  ('admin', 'Administrador con acceso completo', '["*"]'),
  ('seller', 'Vendedor', '["sales.*", "inventory.read", "customers.*"]'),
  ('viewer', 'Solo lectura', '["reports.read", "dashboard.read"]');

-- Organization de demostración (opcional)
INSERT INTO organizations (id, name, domain, is_active)
VALUES (
  'demo-organization-uuid',
  'Empresa Demo',
  'demo',
  true
);
```

---

## Conclusión

Este diseño de base de datos proporciona:

✅ **Escalabilidad:** Preparado para crecer con índices y estrategias de particionado  
✅ **Seguridad:** Multi-tenancy con aislamiento, backups y auditoría  
✅ **Performance:** Índices estratégicos y queries optimizadas  
✅ **Integridad:** Foreign keys, constraints y triggers  
✅ **Mantenibilidad:** Estructura clara y bien documentada  
✅ **Trazabilidad:** Audit logs y soft deletes  

El modelo es apropiado para el alcance del MVP y puede evolucionar según las necesidades futuras.

---

**Elaborado por:** Equipo OrbitEngine  
**Fecha:** Octubre 2025  
**Versión:** 1.0

