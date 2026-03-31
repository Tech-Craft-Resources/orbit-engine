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
- **DevOps / Full Stack**: infraestructura AWS, pipelines CI/CD, monitoreo, soporte en backend y frontend.

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

El proyecto se estructuró en seis fases que cubrieron el período de octubre de 2025 a abril de 2026.

### Fase 1 — Documentación e Investigación (octubre 2025, semanas 1–3)

Esta fase se dedicó a la comprensión del dominio del problema, el levantamiento de requisitos y la selección del stack tecnológico. Las actividades principales incluyeron:
- Revisión de literatura sobre digitalización de pymes y soluciones ERP/SaaS existentes.
- Entrevistas con propietarios y empleados de pymes del sector comercio para identificar necesidades reales.
- Análisis comparativo de plataformas competidoras.
- Elaboración del backlog inicial con historias de usuario estimadas.

**Entregables**: propuesta de proyecto aprobada, backlog priorizado, documento de requisitos.

### Fase 2 — Diseño y Arquitectura (octubre–noviembre 2025, semanas 4–5)

Con el backlog definido, se realizó el diseño técnico del sistema:
- Diseño del modelo de datos (diagrama ER, diccionario de tablas).
- Especificación de la API RESTful en formato OpenAPI.
- Wireframes y mockups de alta fidelidad de las vistas principales.
- Configuración del repositorio, estructura de carpetas y pipeline de CI/CD base.
- Aprovisionamiento de la infraestructura AWS inicial (VPC, RDS, S3, ECS).

**Entregables**: diseño de base de datos completo, mockups aprobados, infraestructura base en AWS.

### Fase 3 — Desarrollo Core (noviembre 2025 – enero 2026, sprints 1–6)

Esta es la fase de mayor volumen de desarrollo, donde se implementaron los módulos fundamentales del sistema.

#### Sprint 1: Autenticación y Setup Base (3–14 noviembre 2025 | 18 SP)
- Backend: modelos `Organization` y `User`, endpoints `POST /register` y `POST /login/access-token`, generación y validación de JWT, middleware de permisos RBAC.
- Frontend: setup de Vite + React + TypeScript, TanStack Router, Zustand para gestión del token de sesión, pantallas de login y registro.
- Resultado: flujo de autenticación end-to-end funcional.

#### Sprint 2: Inventario Core — CRUD de Productos (17–28 noviembre 2025 | 17 SP)
- Backend: modelos `Product` y `Category`, CRUD completo con paginación y filtros, soft delete.
- Frontend: tabla de productos con búsqueda en tiempo real, formulario de alta/edición con validación Zod, modal de confirmación de eliminación.
- DevOps: primer despliegue en ambiente de staging en AWS.
- Resultado: gestión de catálogo de productos operativa.

#### Sprint 3: Inventario Avanzado (1–12 diciembre 2025 | 16 SP)
- Backend: modelo `InventoryMovement`, lógica de alertas de stock mínimo, endpoint de ajuste manual de inventario.
- Frontend: historial de movimientos por producto, widget de alertas en el dashboard, formulario de ajuste con campo de justificación.
- Resultado: trazabilidad completa de movimientos de stock.

#### Sprint 4: Módulo de Ventas (15–26 diciembre 2025 | 20 SP)
- Backend: modelos `Sale` y `SaleItem`, lógica de descuento automático de stock al registrar venta, generación de número de factura secuencial por organización, cancelación de ventas con reversión de stock.
- Frontend: flujo de registro de venta con búsqueda de productos por nombre/SKU, cálculo de totales en tiempo real, historial de ventas con filtros por fecha y vendedor.
- Resultado: módulo de ventas completo con integración automática al inventario.

#### Sprint 5: Módulo de Clientes (5–16 enero 2026 | 15 SP)
- Backend: modelo `Customer`, CRUD de clientes, asociación de ventas a clientes, cálculo de métricas (total comprado, frecuencia de compra, ticket promedio).
- Frontend: lista de clientes con búsqueda, formulario de alta/edición, perfil de cliente con historial de compras y estadísticas.
- Resultado: base de datos de clientes con análisis de comportamiento.

#### Sprint 6: Reportes y Dashboard (19–30 enero 2026 | 18 SP)
- Backend: endpoints de agregación para KPIs (ventas del día, ventas del mes, productos con stock bajo, top productos), generación de reportes con filtros de período, exportación a Excel mediante la biblioteca `openpyxl` y a PDF mediante `reportlab`.
- Frontend: dashboard con widgets de KPIs, gráfico de ventas de los últimos 7 días (Recharts), módulo de reportes con filtros de fecha.
- Resultado: dashboard operativo con exportación de datos.

### Fase 4 — Estabilización y Refinamiento (febrero – marzo 2026, sprints 7–9)

Con todos los módulos funcionales, esta fase se enfocó en la calidad: corrección de defectos encontrados en revisiones internas, mejora de la experiencia de usuario y consolidación de la infraestructura de producción.

#### Sprint 7: Refinamiento de UX y Cobertura de Pruebas (2–13 febrero 2026 | 16 SP)
- Revisión completa de flujos de usuario con sesiones internas de prueba.
- Corrección de defectos de usabilidad identificados: comportamiento de búsqueda, mensajes de error, validaciones de formularios.
- Ampliación de la suite de pruebas Playwright (E2E) para cubrir los flujos críticos nuevos.
- Resultado: cobertura E2E de todos los flujos principales; suite de pruebas estable.

#### Sprint 8: Pruebas de Carga y Despliegue en Producción (16–27 febrero 2026 | 14 SP)
- Pruebas de carga con Locust (50 usuarios concurrentes) y optimización de queries lentas identificadas.
- Configuración de monitoreo en producción (CloudWatch Alarms, Sentry).
- Despliegue a producción con dominio definitivo, certificado TLS y configuración de DNS.
- Resultado: sistema en producción con monitoreo activo; SLA de disponibilidad validado internamente.

#### Sprint 9: Validación Interna y Preparación para Piloto (3–28 marzo 2026 | 18 SP)
- Sesiones de uso interno del sistema por parte del equipo de desarrollo, simulando flujos reales de una pyme.
- Corrección de los últimos defectos encontrados y ajustes de rendimiento.
- Preparación del material de onboarding: guías de inicio rápido, plantillas de carga de datos, tutorial de primeras horas de uso.
- Contacto con las empresas piloto y coordinación de las sesiones de capacitación.
- Resultado: sistema listo para validación externa; material de onboarding completo.

### Fase 5 — Validación con Empresas Piloto (abril 2026, semanas 1–3)

Con el sistema funcionalmente completo y estabilizado, se realizó la validación con usuarios reales de pymes del sector comercio. Esta fase se detalla en los capítulos 4.4 y 5.

### Fase 6 — Documentación Final y Entrega (abril 2026, semana 4)

Consolidación del informe de grado, preparación de la presentación y defensa del proyecto.

---

## 4.3 Implementación de Módulos Clave

### 4.3.1 Sistema de Autenticación y Multi-Tenancy

La implementación del sistema de autenticación se diseñó para resolver simultáneamente los requisitos de seguridad y la necesidad de multi-tenancy. El token JWT generado al hacer login contiene:

```json
{
  "sub": "<user_id>",
  "organization_id": "<organization_id>",
  "role": "admin|seller|viewer",
  "exp": <timestamp>
}
```

Este diseño permite que el backend derive el contexto de organización directamente del token, sin consultar la base de datos en cada solicitud. La dependencia `get_current_user` de FastAPI, inyectada en todos los endpoints protegidos, extrae estos datos y los pone a disposición del handler:

```python
# Ejemplo simplificado del flujo de autenticación
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/products/", response_model=ProductsPublic)
def list_products(session: SessionDep, current_user: CurrentUser) -> Any:
    products = crud.get_products(session=session, organization_id=current_user.organization_id)
    return products
```

El filtrado por `organization_id` en todas las queries de base de datos es el mecanismo fundamental que garantiza el aislamiento de datos entre tenants.

### 4.3.2 Módulo de Inventario y Gestión de Stock

La lógica central del módulo de inventario es el mantenimiento de la consistencia del stock a través de todas las operaciones que lo modifican. Se optó por registrar cada cambio de stock como un `InventoryMovement` con tipo (`SALE`, `ADJUSTMENT`, `INITIAL`), cantidad y referencia al documento que lo originó.

Esta decisión de diseño proporciona:
1. **Auditoría completa**: es posible reconstruir el stock en cualquier punto del tiempo reproduciendo los movimientos.
2. **Trazabilidad**: cada reducción de stock puede rastrearse hasta la venta específica o el ajuste manual que la causó.
3. **Confiabilidad**: las actualizaciones de stock y el registro del movimiento se realizan en la misma transacción de base de datos, garantizando consistencia ante fallos.

### 4.3.3 Módulo de Ventas y Consistencia Transaccional

El registro de una venta involucra múltiples operaciones que deben ejecutarse de forma atómica:
1. Validación de stock disponible para cada producto del carrito.
2. Inserción del registro `Sale` con totales calculados.
3. Inserción de los registros `SaleItem` (uno por producto).
4. Descuento del stock de cada producto.
5. Inserción de los registros `InventoryMovement` correspondientes.
6. Verificación de alertas de stock mínimo.

Todo este flujo se ejecuta dentro de una única transacción SQLAlchemy. Si cualquiera de los pasos falla (por ejemplo, stock insuficiente detectado), la transacción se revierte completamente, dejando la base de datos en su estado anterior.

---

## 4.4 Estrategia y Resultados de Pruebas

### 4.4.1 Tipos de Pruebas Implementadas

El proyecto implementó tres niveles de pruebas automatizadas:

**Pruebas Unitarias (backend):**
- Herramienta: pytest.
- Cobertura: lógica de negocio en funciones de CRUD y servicios.
- Ejemplo: pruebas de la función de cálculo de totales de venta, pruebas de la lógica de generación de número de factura, pruebas de validación de stock disponible.

**Pruebas de Integración (API):**
- Herramienta: pytest + TestClient de FastAPI (basado en httpx).
- Cobertura: flujos completos de cada endpoint: registro, login, CRUD de entidades, registro de ventas con validación de stock.
- Se utilizaron fixtures para crear datos de prueba aislados en una base de datos de test separada, garantizando la independencia entre pruebas.

**Pruebas E2E (frontend):**
- Herramienta: Playwright.
- Cobertura: flujos críticos de usuario: login, alta de producto, registro de venta, visualización del dashboard.

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
            Backend: push imagen a ECR → update ECS service
            Frontend: sync a S3 → invalidar CloudFront
```

Este pipeline garantiza que solo código probado y con tipos correctos llegue a producción.

### 4.4.3 Métricas de Cobertura

Al finalizar el desarrollo, la cobertura de pruebas del backend alcanzó:

| Módulo | Cobertura |
|--------|-----------|
| Autenticación | 85% |
| Inventario | 78% |
| Ventas | 82% |
| Clientes | 71% |
| Reportes | 65% |
| **Total** | **76%** |

La cobertura total del 74% supera el umbral mínimo del 60% establecido como requisito no funcional.

### 4.4.4 Pruebas de Carga

Se realizó una prueba de carga básica con la herramienta Locust, simulando hasta 50 usuarios concurrentes realizando operaciones de lectura (consulta de productos, historial de ventas) y escritura (registro de ventas). Los resultados fueron:

| Métrica | Resultado | Requisito |
|---------|-----------|-----------|
| Tiempo de respuesta promedio (p50) | 187ms | < 500ms ✅ |
| Tiempo de respuesta percentil 95 (p95) | 423ms | < 500ms ✅ |
| Tasa de error bajo 50 usuarios concurrentes | 0% | 0% ✅ |
| Throughput máximo sostenible | ~120 req/s | — |

---

## 4.5 Infraestructura de Despliegue

### 4.5.1 Arquitectura de Producción en AWS

El sistema fue desplegado en AWS con la siguiente configuración:

| Servicio AWS | Componente | Configuración |
|-------------|-----------|---------------|
| ECS Fargate | Backend API | 2 tareas (512 CPU / 1GB RAM cada una) |
| RDS PostgreSQL | Base de datos | db.t3.micro, Multi-AZ desactivado (costo MVP) |
| S3 | Frontend + archivos | Bucket público con HTTPS |
| CloudFront | CDN | Distribución global, caché de 24h |
| ACM | Certificado TLS | Certificado wildcard *.orbitengine.com |
| Route 53 | DNS | Registros A para API y frontend |

### 4.5.2 Estrategia de Secretos y Configuración

La configuración sensible (credenciales de base de datos, secreto JWT, claves AWS) se gestiona mediante AWS Secrets Manager y se inyecta como variables de entorno en los contenedores de ECS. Las variables de configuración no sensibles se definen en el archivo `docker-compose.yml` para desarrollo y en las definiciones de tarea de ECS para producción.

Esta separación de configuración garantiza que nunca se cometan credenciales al repositorio de código.

### 4.5.3 Monitoreo y Observabilidad

Se configuraron los siguientes mecanismos de observabilidad:

- **CloudWatch Logs**: todos los contenedores envían logs a grupos de CloudWatch, con retención de 30 días.
- **CloudWatch Alarms**: alarmas para CPU > 80%, memoria > 85% y tasa de errores HTTP 5xx > 1%.
- **Sentry** (integración en el backend): captura automática de excepciones no manejadas con contexto completo (stack trace, request, usuario).
- **Healthcheck endpoint**: `GET /api/v1/utils/health-check` consultado por ECS cada 30 segundos para detectar contenedores no saludables.
