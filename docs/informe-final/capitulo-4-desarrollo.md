# Capítulo 4 — Desarrollo e Implementación

---

## 4.1 Metodología de Desarrollo

### 4.1.1 Marco Ágil: Scrum Adaptado

El desarrollo de OrbitEngine siguió un proceso ágil basado en el framework Scrum, adaptado a las condiciones de un equipo académico de tres personas con dedicación parcial. Las adaptaciones principales respecto al Scrum estándar fueron:

- **Sprints de 2 semanas** (en lugar de 1 semana) para reducir la sobrecarga de ceremonias y dar margen a las obligaciones académicas paralelas.
- **Daily standups asincrónicos** mediante mensajes en un canal dedicado de Discord, dado que los horarios de los integrantes no siempre coincidían.
- **Roles simplificados**: no se designó un Scrum Master formal; los tres integrantes rotaron informalmente la facilitación de las ceremonias.

Las ceremonias mantenidas fueron:
- **Sprint Planning** (inicio del sprint, 2 horas): revisión del backlog priorizado, estimación con puntos de historia en escala Fibonacci y asignación de tareas.
- **Sprint Review** (fin del sprint, 1 hora): demostración de las funcionalidades completadas.
- **Sprint Retrospective** (fin del sprint, 30 minutos): identificación de mejoras al proceso.

### 4.1.2 Herramientas del Proceso

| Herramienta | Propósito |
|-------------|-----------|
| GitHub Projects | Gestión del backlog, kanban de sprints |
| GitHub (repositorio) | Control de versiones, pull requests, code review |
| GitHub Actions | CI/CD: pruebas automatizadas y despliegue |
| Discord | Comunicación del equipo, standups asincrónicos |
| Figma | Diseño de wireframes y mockups de UI |

### 4.1.3 Estructura del Equipo

El equipo se organizó en roles complementarios con zonas de especialización clara, aunque todos los integrantes contribuyeron en múltiples capas del sistema:

- **Backend Lead**: arquitectura del sistema, endpoints de la API, modelos de base de datos, lógica de negocio y reportes.
- **Frontend Lead**: componentes de UI, flujos de usuario, integración con la API, diseño responsivo.
- **DevOps / Full Stack**: infraestructura en Railway y Vercel, pipelines CI/CD, monitoreo, soporte en backend y frontend.

### 4.1.4 Gestión de la Calidad del Código

Se establecieron las siguientes prácticas de calidad desde el inicio del proyecto:

**Backend:**
- Tipado estático completo con mypy (modo strict).
- Linting y formateo con Ruff.
- Revisión de código mediante pull requests antes de hacer merge a `main`.
- Cobertura de pruebas mínima del 60% como condición para que el CI apruebe.

**Frontend:**
- Tipado estricto con TypeScript.
- Linting y formateo con Biome.
- Generación automática del cliente de API desde el schema OpenAPI (`bun run generate-client`) para garantizar la sincronización entre frontend y backend.

---

## 4.2 Fases y Sprints de Desarrollo

El proyecto se estructuró en seis fases que cubrieron el período comprendido entre octubre de 2025 y mediados de mayo de 2026.

### Fase 1 — Documentación e Investigación (octubre 2025, semanas 1–3)

Esta fase se dedicó a la comprensión del dominio del problema, el levantamiento de requisitos y la selección del stack tecnológico. Las actividades principales incluyeron:
- Revisión de literatura sobre digitalización de pymes y soluciones ERP/SaaS existentes.
- Levantamiento informal de información a partir de la experiencia previa de los integrantes del equipo con pymes del sector comercio, sin un proceso estructurado de entrevistas externas.
- Análisis comparativo de plataformas competidoras.
- Elaboración del backlog inicial con historias de usuario estimadas.

**Entregables**: propuesta de proyecto aprobada, backlog priorizado, documento de requisitos.

### Fase 2 — Diseño y Arquitectura (octubre–noviembre 2025, semanas 4–5)

Con el backlog definido, se realizó el diseño técnico del sistema:
- Diseño del modelo de datos (diagrama ER, diccionario de tablas).
- Especificación de la API RESTful en formato OpenAPI.
- Wireframes y mockups de alta fidelidad de las vistas principales.
- Configuración del repositorio, estructura de carpetas, entorno de desarrollo local con Docker Compose y pipeline base de CI en GitHub Actions (lint y type-check).

**Entregables**: diseño de base de datos completo, mockups aprobados, repositorio inicializado con CI básico y entorno local reproducible vía Docker Compose.

### Fase 3 — Desarrollo Core (noviembre 2025 – segunda semana de abril 2026, sprints 1–8)

Esta es la fase de mayor volumen de desarrollo, donde se implementaron y consolidaron todos los módulos funcionales del sistema. Se extendió desde la primera semana de noviembre de 2025 hasta la segunda semana de abril de 2026 para permitir cerrar el alcance funcional completo antes de pasar a la fase de estabilización. Los ocho sprints se distribuyeron en duraciones de **dos o tres semanas** según el tamaño de cada bloque de funcionalidad y, entre los Sprints 3 y 4, se respetó un receso académico de dos semanas (22 de diciembre de 2025 – 4 de enero de 2026) en el que el equipo no ejecutó iteraciones formales.

#### Sprint 1: Autenticación y Setup Base (3–14 noviembre 2025 | 18 SP)
- Backend: modelos `Organization` y `User`, endpoints `POST /organizations/signup` (alta de organización con su usuario administrador) y `POST /login/access-token`, generación y validación de JWT con `sub`, `organization_id`, `role` y `exp`, dependencia `get_current_user` y `require_role` para control de acceso por rol.
- Frontend: setup de Vite + React + TypeScript, TanStack Router con rutas basadas en archivos, gestión del token de sesión vía un módulo propio (`lib/auth-session`) integrado con TanStack Query, pantallas de login y registro de organización.
- Resultado: flujo de autenticación end-to-end funcional con multi-tenancy desde el primer commit productivo.

#### Sprint 2: Inventario Core — CRUD de Productos (17 noviembre – 5 diciembre 2025 | 17 SP)
- Backend: modelos `Product` y `Category`, CRUD completo con paginación, búsqueda y filtros, soft delete (`deleted_at`).
- Frontend: tabla de productos con búsqueda en tiempo real, formulario de alta/edición con validación Zod + React Hook Form, modal de confirmación de eliminación.
- Resultado: gestión de catálogo de productos operativa en entorno de desarrollo local.

#### Sprint 3: Inventario Avanzado (8–19 diciembre 2025 | 16 SP)
- Backend: modelo `InventoryMovement` con tipos `sale`, `purchase`, `adjustment` y `return`; endpoint `GET /products/low-stock` para listar productos por debajo del mínimo; endpoint `POST /inventory-movements/` para movimientos manuales (ajuste, compra, devolución).
- Frontend: historial de movimientos por producto, widget de productos con stock bajo en el dashboard, formulario de ajuste manual con campo de justificación.
- Resultado: trazabilidad completa de movimientos de stock.

#### Sprint 4: Módulo de Ventas (5–23 enero 2026 | 20 SP)
- Backend: modelos `Sale` y `SaleItem`, lógica de descuento automático de stock al registrar venta, generación de número de factura secuencial por organización, endpoint `POST /sales/{sale_id}/cancel` para anular ventas con reversión de stock vía movimientos de tipo `return`.
- Frontend: flujo de registro de venta con búsqueda de productos por nombre/SKU, cálculo de totales en tiempo real, historial de ventas con filtros por fecha, estado y método de pago.
- Resultado: módulo de ventas completo con integración automática al inventario.

#### Sprint 5: Módulo de Clientes (26 enero – 13 febrero 2026 | 15 SP)
- Backend: modelo `Customer`, CRUD de clientes, asociación opcional de ventas a clientes y actualización automática de métricas (total comprado, número de compras, ticket promedio) al registrar o cancelar una venta.
- Frontend: lista de clientes con búsqueda, formulario de alta/edición, perfil de cliente con historial de compras y estadísticas.
- Resultado: base de datos de clientes con análisis de comportamiento.

#### Sprint 6: Reportes y Dashboard (16 febrero – 6 marzo 2026 | 18 SP)
- Backend: endpoint `GET /dashboard/stats` con KPIs agregados (ventas del día, ventas del mes, conteo de productos con stock bajo, ticket promedio, top productos, ventas por día) y endpoint `POST /dashboard/export-excel` que genera archivos `.xlsx` para los datasets de inventario, clientes y ventas construyendo el formato Office Open XML manualmente sin dependencias externas.
- Frontend: dashboard con widgets de KPIs, gráfico de ventas de los últimos días con Recharts, módulo de reportes con filtros de fecha y exportación a Excel.
- Resultado: dashboard de KPIs operativo y módulo de exportación a Excel de los tres listados principales.

#### Sprint 7: Roles, Permisos y Refinamiento Funcional (9–27 marzo 2026 | 16 SP)
- Backend: endpoints `GET /roles/` y consolidación del rol `contador` además de `admin`, `seller` y `viewer`; ajustes de permisos en endpoints sensibles (exportación, gestión de usuarios, cancelación de ventas) usando la dependencia `require_role`.
- Frontend: control de visibilidad de menús y acciones según el rol del usuario autenticado, pantallas de gestión de usuarios y de organización.
- Resultado: matriz de permisos consolidada y aplicada de extremo a extremo.

#### Sprint 8: Cierre Funcional y Pulido (30 marzo – 10 abril 2026 | 17 SP)
- Backend: cierre de los últimos endpoints pendientes del backlog, ajustes de filtros y validaciones, mejoras en mensajes de error.
- Frontend: pulido de UI (estados vacíos, loaders, toasts), responsive en vistas críticas, accesibilidad básica en formularios.
- Resultado: alcance funcional de OrbitEngine cerrado y listo para iniciar la fase de estabilización y despliegue.

### Fase 4 — Estabilización, Despliegue y Refinamiento (mediados de abril – última semana de abril 2026, sprints 9–10)

Con el alcance funcional cerrado al final de la Fase 3, esta fase se enfocó en llevar el sistema a producción y dejarlo listo para usuarios externos. Es en este punto cuando se aprovisionó por primera vez la infraestructura de despliegue: hasta ese momento OrbitEngine se ejecutaba únicamente en entornos de desarrollo local con Docker Compose. Por la duración total de la fase, los Sprints 9 y 10 se planificaron como iteraciones cortas de una semana cada una.

#### Sprint 9: Pruebas de Carga, Rendimiento y Refinamiento Interno (13–17 abril 2026 | 16 SP)
- Diseño y ejecución de pruebas de carga con Locust contra una instancia de pre-producción, alternando entre escenarios de 8 y 200 usuarios concurrentes con distintos perfiles de interacción.
- Pruebas de rendimiento del frontend con Lighthouse y herramientas web gratuitas similares (PageSpeed Insights, WebPageTest) sobre las vistas principales.
- Identificación y corrección de queries lentas, ajustes de índices en PostgreSQL y memoización selectiva de componentes pesados en el frontend.
- Sesiones internas de prueba por parte del equipo simulando flujos reales de una pyme; corrección de defectos de usabilidad detectados.
- Resultado: sistema estabilizado, métricas base de carga y rendimiento documentadas (los resultados se reportan en el Capítulo 5).

#### Sprint 10: Despliegue en Producción y Validación Interna (20–24 abril 2026 | 18 SP)
- Aprovisionamiento de la infraestructura productiva: backend y base de datos PostgreSQL en Railway, frontend en Vercel.
- Configuración del dominio definitivo (registrado en Namecheap), certificados TLS gestionados por las plataformas y registros DNS apuntando a Railway y Vercel.
- Configuración del pipeline de despliegue continuo (push a `main` → despliegue automático en Railway y Vercel) y de las variables de entorno de producción.
- Ampliación de la suite de pruebas Playwright (E2E) y de la cobertura de pruebas backend sobre los flujos críticos.
- Preparación del material de onboarding para las empresas piloto: guías de inicio rápido, plantillas de carga de datos y tutoriales.
- Resultado: OrbitEngine desplegado en producción bajo dominio definitivo, monitorizable y listo para la validación con empresas piloto.

### Fase 5 — Validación con Empresas Piloto (última semana de abril – primera semana de mayo 2026)

Durante dos semanas (aproximadamente del 27 de abril al 8 de mayo de 2026), el sistema en producción se puso a disposición de las empresas piloto seleccionadas para su uso real, con sesiones de capacitación, acompañamiento y recolección de retroalimentación. Esta fase se detalla en el Capítulo 5.

### Fase 6 — Documentación Final y Entrega (segunda semana de mayo 2026)

Consolidación del informe de grado, preparación de la presentación y defensa del proyecto durante la segunda semana de mayo de 2026 (aproximadamente del 11 al 15 de mayo).

---

## 4.3 Implementación de Módulos Clave

### 4.3.1 Sistema de Autenticación y Multi-Tenancy

La implementación del sistema de autenticación se diseñó para resolver simultáneamente los requisitos de seguridad y la necesidad de multi-tenancy. El token JWT generado al hacer login contiene:

```json
{
  "sub": "<user_id>",
  "organization_id": "<organization_id>",
  "role": "admin|seller|viewer|contador",
  "exp": <timestamp>
}
```

Este diseño permite que el backend derive el contexto de organización directamente del token. La dependencia `get_current_user` de FastAPI valida la firma del token, lo decodifica en un modelo `TokenPayload` y carga el `User` correspondiente; sobre ella se construye `CurrentOrganization`, que expone el `organization_id` del usuario autenticado a los handlers:

```python
CurrentUser = Annotated[User, Depends(get_current_user)]
CurrentOrganization = Annotated[uuid.UUID, Depends(get_current_organization)]

@router.get("/products/", response_model=ProductsPublic)
def list_products(
    session: SessionDep,
    _current_user: CurrentUser,
    current_organization: CurrentOrganization,
) -> Any:
    products = crud.get_products(session=session, organization_id=current_organization)
    return ProductsPublic(data=products, count=len(products))
```

El filtrado por `organization_id` en todas las queries de base de datos es el mecanismo fundamental que garantiza el aislamiento de datos entre tenants. Para el control de acceso por rol se usa la dependencia `require_role("admin", "seller", ...)`, que se inyecta en los endpoints sensibles (creación y cancelación de ventas, exportaciones, gestión de usuarios).

### 4.3.2 Módulo de Inventario y Gestión de Stock

La lógica central del módulo de inventario es el mantenimiento de la consistencia del stock a través de todas las operaciones que lo modifican. Se optó por registrar cada cambio de stock como un `InventoryMovement` con un `movement_type` (`sale`, `purchase`, `adjustment` o `return`), la cantidad ajustada, los valores de stock previo y nuevo, y una referencia opcional al documento que lo originó (por ejemplo, el `sale_id` de la venta).

Esta decisión de diseño proporciona:
1. **Auditoría completa**: es posible reconstruir el stock en cualquier punto del tiempo reproduciendo los movimientos.
2. **Trazabilidad**: cada reducción de stock puede rastrearse hasta la venta específica o el ajuste manual que la causó.
3. **Confiabilidad**: las actualizaciones de stock y el registro del movimiento se realizan dentro de la misma sesión SQLAlchemy del request, garantizando consistencia ante fallos.

Adicionalmente, el endpoint `GET /products/low-stock` y el contador `low_stock_count` del dashboard exponen los productos cuyo `stock_quantity` cae por debajo de su mínimo configurado, lo que permite que la interfaz visualice alertas de reposición sin requerir una tabla de alertas adicional.

### 4.3.3 Módulo de Ventas y Consistencia Transaccional

El registro de una venta involucra múltiples operaciones que deben ejecutarse de forma consistente dentro de la misma sesión de base de datos:
1. Validación de existencia, estado activo y stock disponible para cada producto del carrito.
2. Cálculo del subtotal a partir de los precios actuales y aplicación de descuento e impuestos para obtener el total.
3. Generación del número de factura secuencial por organización.
4. Inserción del registro `Sale` con los totales calculados y los datos del usuario y cliente asociados.
5. Por cada ítem: inserción del `SaleItem` con un *snapshot* de nombre, SKU y precio del producto; descuento del stock; e inserción del `InventoryMovement` de tipo `sale` con `previous_stock` y `new_stock`.
6. Actualización de las métricas de compra del cliente (total comprado, número de compras, ticket promedio) si la venta está asociada a uno.

Todo el flujo se ejecuta dentro de la misma sesión SQLAlchemy gestionada por la dependencia `SessionDep`. Si cualquiera de las validaciones iniciales falla (stock insuficiente, producto inactivo, cliente inexistente), se levanta una `HTTPException` antes de cualquier escritura. La operación inversa (`POST /sales/{sale_id}/cancel`) sigue el mismo patrón: restituye el stock, registra movimientos de tipo `return` y revierte las métricas del cliente.

---

## 4.4 Estrategia y Resultados de Pruebas

### 4.4.1 Tipos de Pruebas Implementadas

El proyecto implementó cuatro niveles de pruebas automatizadas que en conjunto suman más de 300 casos de prueba ejecutables:

**Pruebas Unitarias / CRUD (backend):**
- Herramienta: pytest.
- Cobertura: lógica de negocio en `app/crud.py` para cada entidad (`category`, `customer`, `dashboard`, `inventory_movement`, `organization`, `product`, `role`, `sale`, `user`).
- Ejemplos: cálculo de totales de venta, generación secuencial del número de factura por organización, validación de stock disponible, actualización de métricas de cliente, agregaciones del dashboard.

**Pruebas de Integración (API):**
- Herramienta: pytest + TestClient de FastAPI (basado en httpx).
- Cobertura: flujos completos de cada router en `app/api/routes/` — login, organizaciones (signup), usuarios, productos, categorías, clientes, ventas (incluida cancelación), movimientos de inventario, dashboard (`/stats` y `/export-excel`) y roles.
- Se utilizaron fixtures (`conftest.py`) para crear datos de prueba aislados en una base de datos de test separada, garantizando la independencia entre pruebas.

**Pruebas de Seguridad y Multi-Tenancy (backend):**
- Herramienta: pytest sobre el TestClient de FastAPI.
- Cobertura: módulo `tests/security/test_multitenant.py` que verifica de forma sistemática que un usuario de una organización no pueda leer, modificar ni borrar recursos de otra (productos, categorías, clientes, ventas, movimientos), así como la correcta aplicación de los permisos por rol.

**Pruebas E2E (frontend):**
- Herramienta: Playwright.
- Cobertura: flujos críticos de usuario incluyendo login, registro de organización (`organization-signup`), alta y edición de productos (`inventory`), registro y consulta de ventas (`sales`), gestión de clientes (`customers`), gestión de roles (`roles`), reseteo de contraseña, configuración de cuenta y de organización, y panel de administración.

### 4.4.2 Pipeline de CI/CD

Cada push al repositorio de GitHub activa automáticamente el siguiente pipeline:

```
Trigger: push a cualquier rama / PR a main
    │
    ├─► Lint & Type Check
    │       Backend: ruff + mypy
    │       Frontend: biome check
    │
    ├─► Unit & Integration Tests
    │       pytest con base de datos de test en memoria (SQLite)
    │       Cobertura mínima: 60% (el pipeline falla si no se alcanza)
    │
    ├─► Build
    │       Backend: construcción de imagen Docker
    │       Frontend: bun run build
    │
    └─► Deploy (solo en merge a main)
            Backend: push a main → deploy automático en Railway
            Frontend: push a main → deploy automático en Vercel
```

Este pipeline garantiza que solo código probado y con tipos correctos llegue a producción.

### 4.4.3 Métricas de Cobertura

Con más de 300 pruebas automatizadas distribuidas entre las capas de CRUD, API, multi-tenancy y E2E, la cobertura del backend al cierre de la Fase 3 alcanzó:

| Módulo | Cobertura |
|--------|-----------|
| Autenticación y usuarios | 92% |
| Inventario (productos, categorías, movimientos) | 88% |
| Ventas | 91% |
| Clientes | 86% |
| Dashboard y reportes | 82% |
| Multi-tenancy y permisos | 95% |
| **Total** | **89%** |

La cobertura total del 89% supera holgadamente el umbral mínimo del 60% establecido como requisito no funcional. La buena cobertura del módulo de multi-tenancy es especialmente relevante porque protege la propiedad más crítica del sistema: el aislamiento de datos entre organizaciones.

### 4.4.4 Pruebas de Carga y Rendimiento Planeadas

Para validar el comportamiento del sistema bajo uso real se diseñó un plan de pruebas de carga y rendimiento que se ejecuta durante la Fase 4. Los resultados detallados se reportan en el Capítulo 5; en esta sección se describe únicamente el plan.

**Pruebas de carga con Locust** (`backend/tests/performance/locustfile.py`):
- Escenarios alternados entre **8 usuarios concurrentes** (carga representativa de pyme) y **200 usuarios concurrentes** (escenario de estrés muy por encima del uso esperado).
- Tres perfiles de usuario virtual mezclados según peso:
  - Lector realista (`OrbitEngineUser`): paginación, búsqueda, filtros y ordenamiento sobre productos, ventas, clientes, movimientos y dashboard.
  - Vendedor (`SellerUser`): crea ventas reales contra el catálogo y dispara los movimientos de inventario asociados.
  - "Spammer" (`SpammerUser`): martillea sin pausa los endpoints de agregación (`/dashboard/stats`).
- Cada usuario virtual rota cuentas reales de las distintas organizaciones piloto, lo que ejercita simultáneamente el aislamiento multi-tenant bajo carga.
- Se variará el ritmo de interacciones por segundo (entre `between(0.5, 1.5)` y `constant(0)` según la clase de usuario) para representar tanto el patrón humano como el peor caso.

**Pruebas de rendimiento del frontend**:
- **Lighthouse** (Chrome DevTools y CLI) sobre las vistas de login, dashboard, listado de productos, registro de venta y reportes, midiendo Performance, Accessibility, Best Practices y SEO.
- **PageSpeed Insights** y **WebPageTest** como herramientas web gratuitas complementarias para obtener mediciones desde redes y ubicaciones distintas a las del equipo de desarrollo.
- Las métricas objetivo (Core Web Vitals: LCP, INP, CLS) y los resultados obtenidos se documentan en el Capítulo 5.

---

## 4.5 Infraestructura de Despliegue

### 4.5.1 Arquitectura de Producción

El sistema fue desplegado en Railway y Vercel con la siguiente configuración:

| Plataforma | Componente | Configuración |
|-----------|-----------|---------------|
| Railway | Backend API | Servicio web desplegado desde imagen Docker; variables de entorno gestionadas en el panel de Railway |
| Railway | Base de datos PostgreSQL | Instancia gestionada, backups automáticos, URL de conexión inyectada como variable de entorno |
| Vercel | Frontend (React/Vite) | SPA compilada con Vite, CDN global integrado, HTTPS automático y previsualizaciones por pull request |
| Railway / Vercel | Certificados TLS | Certificados gestionados y renovados automáticamente por cada plataforma |
| Namecheap | Registro de dominio y DNS | Dominio adquirido en Namecheap; registros CNAME / A configurados desde el panel de Namecheap para apuntar al backend en Railway y al frontend en Vercel |

### 4.5.2 Estrategia de Secretos y Configuración

La configuración sensible (credenciales de base de datos, secreto JWT) se gestiona mediante las variables de entorno del panel de Railway para el backend, y mediante el panel de Vercel para el frontend. Las variables de configuración no sensibles se definen en el archivo `docker-compose.yml` para el entorno de desarrollo local.

Esta separación de configuración garantiza que nunca se cometan credenciales al repositorio de código.

### 4.5.3 Monitoreo y Observabilidad

Para esta fase del proyecto se previó apoyarse principalmente en las herramientas nativas de las plataformas de despliegue, dejando integraciones más sofisticadas para etapas posteriores:

- **Railway Logs**: los logs del backend se centralizan en el panel de Railway, con acceso en tiempo real y retención configurable desde la interfaz web.
- **Railway Metrics**: métricas de uso de CPU, memoria y tráfico de red disponibles en el panel de Railway, con alertas configurables por umbral.
- **Vercel Analytics y logs de despliegue**: información de tráfico básico del frontend y trazabilidad de cada despliegue por commit.
- **Healthcheck endpoint**: `GET /api/v1/utils/health-check/` expuesto por el backend, consultable por Railway o por monitores externos para detectar instancias no saludables.
