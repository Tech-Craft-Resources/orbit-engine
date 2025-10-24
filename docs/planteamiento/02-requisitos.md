# Historias de Usuario y Requisitos del Sistema
## Pecesaurio - Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Versión:** 1.0  
**Fecha:** Octubre 2024

---

## Tabla de Contenidos

1. [Personas y Roles](#1-personas-y-roles)
2. [Historias de Usuario](#2-historias-de-usuario)
3. [Requisitos Funcionales](#3-requisitos-funcionales)
4. [Requisitos No Funcionales](#4-requisitos-no-funcionales)

---

## 1. Personas y Roles

### 1.1 Administrador de Pyme (María)
- **Perfil:** Dueña de una tienda de abarrotes, 45 años
- **Conocimientos técnicos:** Básicos (usa WhatsApp, Excel básico)
- **Necesidades:** Control total del negocio, reportes claros, predicciones para compras
- **Frustraciones:** Errores en inventario manual, tiempo perdido en hojas de cálculo
- **Objetivos:** Digitalizar el negocio, tomar mejores decisiones, ahorrar tiempo

### 1.2 Vendedor (Carlos)
- **Perfil:** Empleado de tienda, 28 años
- **Conocimientos técnicos:** Intermedios (smartphone, apps básicas)
- **Necesidades:** Registrar ventas rápido, consultar stock, ver historial de clientes
- **Frustraciones:** Sistemas complicados, procesos lentos
- **Objetivos:** Ser eficiente en ventas, brindar buen servicio

### 1.3 Contador/Visualizador (Ana)
- **Perfil:** Contadora externa que asesora la pyme, 35 años
- **Conocimientos técnicos:** Avanzados (Excel, software contable)
- **Necesidades:** Acceso a reportes, exportar datos, análisis de métricas
- **Frustraciones:** Datos incompletos o desorganizados
- **Objetivos:** Generar informes precisos rápidamente

---

## 2. Historias de Usuario

### 2.1 Módulo de Autenticación y Usuarios

#### HU-001: Registro de Usuario
**Como** administrador de pyme  
**Quiero** registrarme en la plataforma con mis datos empresariales  
**Para** poder empezar a usar el sistema

**Criterios de Aceptación:**
- El usuario proporciona: nombre, email, contraseña, nombre de empresa, teléfono
- La contraseña debe tener mínimo 8 caracteres
- El email debe ser único en el sistema
- Se envía email de verificación (opcional en MVP)
- Al registrarse, se crea automáticamente el tenant para la empresa

**Prioridad:** Crítica

---

#### HU-002: Inicio de Sesión
**Como** usuario del sistema  
**Quiero** iniciar sesión con mi email y contraseña  
**Para** acceder a las funcionalidades de la plataforma

**Criterios de Aceptación:**
- Validación de credenciales correcta
- Generación de token JWT
- Redirección al dashboard principal
- Mensaje de error claro si las credenciales son incorrectas
- Límite de 5 intentos fallidos antes de bloqueo temporal

**Prioridad:** Crítica

---

#### HU-003: Gestión de Roles
**Como** administrador  
**Quiero** asignar roles a mis empleados (Admin, Vendedor, Visualizador)  
**Para** controlar qué acciones puede realizar cada uno

**Criterios de Aceptación:**
- Admin: acceso total
- Vendedor: crear ventas, ver inventario, ver clientes
- Visualizador: solo lectura de reportes y datos
- Los permisos se verifican en backend
- UI adapta opciones según rol

**Prioridad:** Alta

---

#### HU-004: Recuperación de Contraseña
**Como** usuario  
**Quiero** recuperar mi contraseña si la olvido  
**Para** poder acceder nuevamente al sistema

**Criterios de Aceptación:**
- Link de "Olvidé mi contraseña"
- Envío de email con token temporal
- Formulario para establecer nueva contraseña
- Token expira en 1 hora

**Prioridad:** Media

---

### 2.2 Módulo de Gestión de Inventario

#### HU-005: Agregar Producto
**Como** administrador  
**Quiero** agregar productos a mi inventario con toda su información  
**Para** mantener un catálogo actualizado

**Criterios de Aceptación:**
- Campos: nombre, descripción, SKU, categoría, precio compra, precio venta, stock inicial, stock mínimo, stock máximo
- SKU debe ser único por empresa
- Validación de campos obligatorios
- Posibilidad de agregar imagen del producto
- Confirmación de éxito al guardar

**Prioridad:** Crítica

---

#### HU-006: Editar Producto
**Como** administrador  
**Quiero** modificar la información de un producto existente  
**Para** mantener los datos actualizados

**Criterios de Aceptación:**
- Acceso a formulario prellenado con datos actuales
- Validación de campos
- Historial de cambios (quién y cuándo modificó)
- Confirmación antes de guardar

**Prioridad:** Crítica

---

#### HU-007: Ver Lista de Productos
**Como** usuario  
**Quiero** ver todos mis productos en una tabla organizada  
**Para** tener visión general de mi inventario

**Criterios de Aceptación:**
- Tabla con paginación
- Columnas: nombre, SKU, categoría, stock actual, precio venta
- Indicadores visuales para stock bajo (amarillo/rojo)
- Buscador por nombre o SKU
- Filtros por categoría y estado de stock

**Prioridad:** Crítica

---

#### HU-008: Eliminar Producto
**Como** administrador  
**Quiero** eliminar productos que ya no vendo  
**Para** mantener el catálogo limpio

**Criterios de Aceptación:**
- Solo administradores pueden eliminar
- Confirmación con advertencia
- Validar que no tenga ventas pendientes
- Soft delete (mantener en BD pero oculto)

**Prioridad:** Media

---

#### HU-009: Alertas de Stock Bajo
**Como** administrador  
**Quiero** recibir alertas cuando un producto esté bajo stock mínimo  
**Para** realizar pedidos a tiempo y evitar desabastecimiento

**Criterios de Aceptación:**
- Indicador visual en dashboard principal
- Lista de productos con stock bajo
- Badge con número de productos en alerta
- Posibilidad de marcar como "pedido realizado"

**Prioridad:** Alta

---

#### HU-010: Ajuste Manual de Inventario
**Como** administrador  
**Quiero** ajustar manualmente la cantidad de un producto  
**Para** corregir discrepancias o registrar mermas

**Criterios de Aceptación:**
- Formulario con cantidad actual y nueva cantidad
- Campo de motivo (merma, corrección, donación, etc.)
- Registro en historial de movimientos
- Cálculo automático de diferencia

**Prioridad:** Alta

---

#### HU-011: Historial de Movimientos
**Como** administrador  
**Quiero** ver el historial de movimientos de inventario  
**Para** auditar y entender cambios en el stock

**Criterios de Aceptación:**
- Tabla con: fecha, producto, tipo movimiento, cantidad, usuario responsable
- Filtros por fecha, producto, tipo
- Exportación a Excel
- Paginación

**Prioridad:** Media

---

### 2.3 Módulo de Gestión de Ventas

#### HU-012: Registrar Venta
**Como** vendedor  
**Quiero** registrar una venta seleccionando productos y cantidades  
**Para** generar una transacción y actualizar el inventario

**Criterios de Aceptación:**
- Buscador de productos
- Agregar múltiples productos a la venta
- Mostrar precio unitario y subtotal por producto
- Cálculo automático de total
- Selección de cliente (opcional)
- Método de pago (efectivo, tarjeta, transferencia)
- Descuento opcional
- Actualización automática de inventario
- Generación de número de factura único

**Prioridad:** Crítica

---

#### HU-013: Ver Historial de Ventas
**Como** usuario  
**Quiero** ver todas las ventas realizadas  
**Para** hacer seguimiento de transacciones

**Criterios de Aceptación:**
- Tabla con: fecha, número factura, cliente, total, usuario que vendió
- Filtros por fecha, cliente, rango de monto
- Búsqueda por número de factura
- Paginación
- Ver detalle de venta al hacer clic

**Prioridad:** Crítica

---

#### HU-014: Ver Detalle de Venta
**Como** usuario  
**Quiero** ver el detalle completo de una venta específica  
**Para** conocer qué productos se vendieron y sus cantidades

**Criterios de Aceptación:**
- Mostrar: número factura, fecha, hora, cliente, vendedor
- Lista de productos con: nombre, cantidad, precio unitario, subtotal
- Subtotal, descuento, total
- Método de pago
- Opción de imprimir o descargar PDF

**Prioridad:** Alta

---

#### HU-015: Cancelar Venta
**Como** administrador  
**Quiero** cancelar una venta registrada por error  
**Para** corregir equivocaciones y revertir inventario

**Criterios de Aceptación:**
- Solo administradores pueden cancelar
- Solo ventas del día actual (configuración)
- Confirmación con contraseña
- Revertir inventario automáticamente
- Registro en log de auditoría
- Venta marcada como cancelada (no eliminada)

**Prioridad:** Media

---

### 2.4 Módulo de Gestión de Clientes

#### HU-016: Agregar Cliente
**Como** vendedor  
**Quiero** agregar un cliente con su información de contacto  
**Para** mantener un registro de mis compradores

**Criterios de Aceptación:**
- Campos: nombre, apellido, email, teléfono, dirección, documento identidad
- Email y teléfono opcionales
- Validación de formato de email
- Documento debe ser único
- Confirmación de guardado

**Prioridad:** Alta

---

#### HU-017: Editar Cliente
**Como** vendedor  
**Quiero** actualizar los datos de un cliente  
**Para** mantener la información correcta

**Criterios de Aceptación:**
- Formulario prellenado
- Validaciones correspondientes
- Historial de cambios

**Prioridad:** Alta

---

#### HU-018: Ver Lista de Clientes
**Como** usuario  
**Quiero** ver todos mis clientes registrados  
**Para** tener acceso rápido a su información

**Criterios de Aceptación:**
- Tabla con: nombre, teléfono, email, total de compras
- Buscador por nombre o documento
- Ordenamiento por diferentes campos
- Paginación
- Ver perfil completo al hacer clic

**Prioridad:** Alta

---

#### HU-019: Ver Perfil de Cliente
**Como** usuario  
**Quiero** ver el perfil detallado de un cliente  
**Para** conocer su historial de compras y comportamiento

**Criterios de Aceptación:**
- Información de contacto completa
- Estadísticas: total comprado, número de compras, promedio de compra
- Historial de ventas con fechas y montos
- Productos más comprados
- Última compra

**Prioridad:** Media

---

#### HU-020: Eliminar Cliente
**Como** administrador  
**Quiero** eliminar clientes que ya no son relevantes  
**Para** mantener la base de datos limpia

**Criterios de Aceptación:**
- Solo admin puede eliminar
- Confirmación requerida
- Soft delete (mantener histórico de ventas)
- No se pueden eliminar clientes con ventas del último mes

**Prioridad:** Baja

---

### 2.5 Módulo de Reportes y Dashboard

#### HU-021: Dashboard Principal
**Como** administrador  
**Quiero** ver un dashboard con las métricas más importantes de mi negocio  
**Para** tener visión general del estado actual

**Criterios de Aceptación:**
- KPIs: ventas del día, ventas del mes, productos con stock bajo, top productos vendidos
- Gráficos: ventas por día (últimos 7 días), ventas por categoría
- Widgets informativos y visuales
- Actualización en tiempo real
- Filtros por rango de fechas

**Prioridad:** Crítica

---

#### HU-022: Reporte de Ventas
**Como** administrador  
**Quiero** generar reportes de ventas por período  
**Para** analizar el rendimiento del negocio

**Criterios de Aceptación:**
- Selección de rango de fechas
- Métricas: total vendido, número de transacciones, ticket promedio
- Gráfico de ventas por día
- Tabla con desglose por producto
- Tabla con desglose por vendedor
- Exportación a PDF y Excel

**Prioridad:** Alta

---

#### HU-023: Reporte de Inventario
**Como** administrador  
**Quiero** generar un reporte del estado actual del inventario  
**Para** conocer mi stock y su valor

**Criterios de Aceptación:**
- Listado completo de productos con stock actual
- Valor total de inventario (al costo y al precio venta)
- Productos con stock bajo
- Productos sin movimiento (últimos 30 días)
- Exportación a Excel

**Prioridad:** Alta

---

#### HU-024: Reporte de Clientes
**Como** administrador  
**Quiero** ver estadísticas de mis clientes  
**Para** entender mejor mi base de compradores

**Criterios de Aceptación:**
- Total de clientes registrados
- Top 10 clientes por monto comprado
- Clientes nuevos en el período
- Clientes inactivos (sin compras últimos 60 días)
- Exportación de lista de clientes

**Prioridad:** Media

---

### 2.6 Módulo de Predicción con IA

#### HU-025: Predicción de Demanda
**Como** administrador  
**Quiero** ver predicciones de demanda para mis productos  
**Para** planificar mejor mis compras a proveedores

**Criterios de Aceptación:**
- Listado de productos con predicción de demanda (próximos 7, 15, 30 días)
- Visualización gráfica de tendencia histórica vs predicción
- Indicador de confianza de la predicción
- Solo productos con histórico suficiente (mínimo 30 días de datos)
- Mensaje explicativo si no hay datos suficientes

**Prioridad:** Alta

---

#### HU-026: Recomendaciones de Reabastecimiento
**Como** administrador  
**Quiero** recibir recomendaciones automáticas de cuándo y cuánto comprar  
**Para** optimizar mi inventario y evitar quiebres de stock

**Criterios de Aceptación:**
- Lista de productos que necesitan reabastecimiento
- Cantidad sugerida basada en predicción y stock actual
- Fecha sugerida de pedido
- Justificación de la recomendación
- Opción de marcar como "pedido realizado"

**Prioridad:** Alta

---

#### HU-027: Análisis de Tendencias
**Como** administrador  
**Quiero** ver análisis de tendencias de ventas  
**Para** identificar patrones y oportunidades

**Criterios de Aceptación:**
- Identificación de productos con tendencia creciente
- Identificación de productos con tendencia decreciente
- Productos estacionales
- Visualización gráfica de tendencias
- Período configurable (últimos 3, 6, 12 meses)

**Prioridad:** Media

---

## 3. Requisitos Funcionales

### 3.1 Autenticación y Autorización (RF-AUTH)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-AUTH-01 | El sistema debe permitir registro de usuarios con validación de email único | Crítica |
| RF-AUTH-02 | El sistema debe autenticar usuarios mediante email y contraseña con JWT | Crítica |
| RF-AUTH-03 | El sistema debe implementar 3 roles: Administrador, Vendedor, Visualizador | Alta |
| RF-AUTH-04 | El sistema debe permitir recuperación de contraseña mediante email | Media |
| RF-AUTH-05 | El sistema debe bloquear cuenta tras 5 intentos fallidos por 15 minutos | Alta |
| RF-AUTH-06 | El sistema debe cerrar sesión automáticamente tras 24 horas de inactividad | Media |
| RF-AUTH-07 | El sistema debe permitir a admin gestionar usuarios de su empresa | Alta |

### 3.2 Gestión de Inventario (RF-INV)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-INV-01 | El sistema debe permitir CRUD completo de productos | Crítica |
| RF-INV-02 | El sistema debe validar unicidad de SKU por tenant | Crítica |
| RF-INV-03 | El sistema debe permitir categorización de productos | Alta |
| RF-INV-04 | El sistema debe actualizar stock automáticamente en cada venta | Crítica |
| RF-INV-05 | El sistema debe generar alertas cuando stock < stock mínimo | Alta |
| RF-INV-06 | El sistema debe permitir ajustes manuales de inventario con justificación | Alta |
| RF-INV-07 | El sistema debe mantener historial de movimientos de inventario | Alta |
| RF-INV-08 | El sistema debe permitir búsqueda de productos por nombre, SKU o categoría | Crítica |
| RF-INV-09 | El sistema debe permitir carga de imagen por producto | Media |
| RF-INV-10 | El sistema debe soportar soft delete de productos | Media |

### 3.3 Gestión de Ventas (RF-VEN)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-VEN-01 | El sistema debe permitir registro de ventas con múltiples productos | Crítica |
| RF-VEN-02 | El sistema debe generar número de factura único y secuencial | Crítica |
| RF-VEN-03 | El sistema debe calcular totales automáticamente (subtotal, descuento, total) | Crítica |
| RF-VEN-04 | El sistema debe validar stock disponible antes de completar venta | Crítica |
| RF-VEN-05 | El sistema debe asociar venta con cliente (opcional) | Alta |
| RF-VEN-06 | El sistema debe registrar método de pago | Alta |
| RF-VEN-07 | El sistema debe permitir aplicar descuentos a la venta | Alta |
| RF-VEN-08 | El sistema debe permitir cancelación de ventas solo por admin | Media |
| RF-VEN-09 | El sistema debe generar PDF de factura | Alta |
| RF-VEN-10 | El sistema debe mantener log de usuario que realizó cada venta | Alta |

### 3.4 Gestión de Clientes (RF-CLI)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-CLI-01 | El sistema debe permitir CRUD de clientes | Alta |
| RF-CLI-02 | El sistema debe validar unicidad de documento por tenant | Alta |
| RF-CLI-03 | El sistema debe asociar ventas con clientes | Alta |
| RF-CLI-04 | El sistema debe calcular estadísticas por cliente (total comprado, # compras) | Alta |
| RF-CLI-05 | El sistema debe mostrar historial de compras por cliente | Alta |
| RF-CLI-06 | El sistema debe permitir búsqueda de clientes por nombre o documento | Alta |
| RF-CLI-07 | El sistema debe identificar clientes frecuentes | Media |

### 3.5 Reportes y Análisis (RF-REP)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-REP-01 | El sistema debe mostrar dashboard con KPIs principales | Crítica |
| RF-REP-02 | El sistema debe generar reporte de ventas por período | Alta |
| RF-REP-03 | El sistema debe generar reporte de inventario actual | Alta |
| RF-REP-04 | El sistema debe permitir exportación de reportes a PDF y Excel | Alta |
| RF-REP-05 | El sistema debe mostrar gráficos de ventas por período | Alta |
| RF-REP-06 | El sistema debe identificar productos más vendidos | Alta |
| RF-REP-07 | El sistema debe identificar productos sin movimiento | Media |
| RF-REP-08 | El sistema debe calcular ticket promedio | Media |
| RF-REP-09 | El sistema debe mostrar tendencias de ventas | Media |

### 3.6 Predicción con IA (RF-IA)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-IA-01 | El sistema debe predecir demanda de productos con histórico suficiente | Alta |
| RF-IA-02 | El sistema debe generar recomendaciones de reabastecimiento | Alta |
| RF-IA-03 | El sistema debe mostrar nivel de confianza de predicciones | Alta |
| RF-IA-04 | El sistema debe identificar tendencias (creciente/decreciente) | Media |
| RF-IA-05 | El sistema debe actualizar predicciones automáticamente cada 24 horas | Media |
| RF-IA-06 | El sistema debe requerir mínimo 30 días de datos históricos para predicción | Alta |
| RF-IA-07 | El sistema debe visualizar predicciones vs datos reales | Media |

### 3.7 Sistema General (RF-SYS)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RF-SYS-01 | El sistema debe ser multi-tenant (aislamiento por empresa) | Crítica |
| RF-SYS-02 | El sistema debe mantener logs de auditoría | Alta |
| RF-SYS-03 | El sistema debe permitir configuración de parámetros de negocio | Media |
| RF-SYS-04 | El sistema debe manejar zona horaria del tenant | Media |
| RF-SYS-05 | El sistema debe tener API RESTful documentada | Alta |

---

## 4. Requisitos No Funcionales

### 4.1 Rendimiento (RNF-PER)

| ID | Requisito | Métrica |
|----|-----------|---------|
| RNF-PER-01 | Tiempo de respuesta para operaciones CRUD | < 500ms (p95) |
| RNF-PER-02 | Tiempo de respuesta para predicciones de IA | < 3 segundos |
| RNF-PER-03 | Tiempo de carga del dashboard | < 2 segundos |
| RNF-PER-04 | Soporte de usuarios concurrentes por tenant | Mínimo 10 |
| RNF-PER-05 | Tiempo de generación de reportes PDF | < 5 segundos |
| RNF-PER-06 | Capacidad de productos por tenant | Mínimo 10,000 |
| RNF-PER-07 | Capacidad de ventas por tenant | Mínimo 100,000 registros |

### 4.2 Disponibilidad (RNF-DIS)

| ID | Requisito | Métrica |
|----|-----------|---------|
| RNF-DIS-01 | Disponibilidad del sistema | > 95% uptime |
| RNF-DIS-02 | Tiempo máximo de inactividad planificado | < 4 horas/mes |
| RNF-DIS-03 | Ventana de mantenimiento | Madrugadas (2-6 AM) |
| RNF-DIS-04 | Recovery Time Objective (RTO) | < 4 horas |
| RNF-DIS-05 | Recovery Point Objective (RPO) | < 24 horas |

### 4.3 Seguridad (RNF-SEG)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-SEG-01 | Contraseñas deben estar hasheadas | Usar bcrypt o Argon2 |
| RNF-SEG-02 | Comunicación mediante HTTPS | Certificado SSL válido |
| RNF-SEG-03 | Implementación de CORS | Configuración restrictiva |
| RNF-SEG-04 | Protección contra SQL Injection | Uso de ORM y queries parametrizadas |
| RNF-SEG-05 | Protección contra XSS | Sanitización de inputs |
| RNF-SEG-06 | Validación de entrada | En frontend y backend |
| RNF-SEG-07 | Rate limiting en API | 100 requests/minuto por usuario |
| RNF-SEG-08 | Tokens JWT con expiración | Máximo 24 horas |
| RNF-SEG-09 | Aislamiento de datos por tenant | Validación estricta en queries |
| RNF-SEG-10 | Backups automáticos | Diarios, retención 30 días |
| RNF-SEG-11 | Logging de acciones críticas | Auditoría de cambios |

### 4.4 Usabilidad (RNF-USA)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-USA-01 | Interfaz responsive | Soporte desktop, tablet, móvil |
| RNF-USA-02 | Soporte de navegadores | Chrome, Firefox, Safari, Edge (últimas 2 versiones) |
| RNF-USA-03 | Accesibilidad | Cumplimiento WCAG 2.0 nivel AA (básico) |
| RNF-USA-04 | Idioma | Español (MVP) |
| RNF-USA-05 | Mensajes de error claros | En lenguaje no técnico |
| RNF-USA-06 | Confirmaciones para acciones destructivas | Diálogos de confirmación |
| RNF-USA-07 | Feedback visual de acciones | Loaders, toasts, mensajes |
| RNF-USA-08 | Navegación intuitiva | Máximo 3 clics para cualquier acción |
| RNF-USA-09 | Tooltips y ayuda contextual | Para usuarios no técnicos |

### 4.5 Escalabilidad (RNF-ESC)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-ESC-01 | Arquitectura modular | Separación frontend/backend |
| RNF-ESC-02 | Base de datos escalable | Soporte de crecimiento vertical y horizontal |
| RNF-ESC-03 | Stateless backend | Para facilitar escalamiento horizontal |
| RNF-ESC-04 | Cacheo de datos frecuentes | Redis para sesiones y datos temporales |
| RNF-ESC-05 | CDN para assets estáticos | CloudFront o similar |
| RNF-ESC-06 | Optimización de queries | Índices apropiados en BD |

### 4.6 Mantenibilidad (RNF-MAN)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-MAN-01 | Código versionado | Git con GitHub |
| RNF-MAN-02 | Cobertura de pruebas | Mínimo 60% |
| RNF-MAN-03 | Documentación de código | Docstrings y comentarios |
| RNF-MAN-04 | Documentación de API | OpenAPI/Swagger |
| RNF-MAN-05 | Logging estructurado | Niveles: DEBUG, INFO, WARNING, ERROR |
| RNF-MAN-06 | Monitoreo de errores | Sentry o similar |
| RNF-MAN-07 | Estándares de código | Linters (ESLint, Black, etc.) |
| RNF-MAN-08 | CI/CD básico | Tests automáticos en PRs |

### 4.7 Portabilidad (RNF-POR)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-POR-01 | Contenedorización | Docker para todos los servicios |
| RNF-POR-02 | Variables de entorno | Configuración externalizada |
| RNF-POR-03 | Independencia de cloud provider | Uso de servicios estándar cuando sea posible |

### 4.8 Cumplimiento y Legal (RNF-LEG)

| ID | Requisito | Descripción |
|----|-----------|-------------|
| RNF-LEG-01 | Aviso de privacidad | Términos y condiciones |
| RNF-LEG-02 | Manejo de datos personales | Cumplimiento básico GDPR/LOPD |
| RNF-LEG-03 | Exportación de datos | Usuario puede exportar sus datos |
| RNF-LEG-04 | Eliminación de cuenta | Opción de eliminar cuenta y datos |

---

## 5. Matriz de Trazabilidad

### Priorización de Historias de Usuario para MVP

| Sprint | HU | Módulo | Esfuerzo (Story Points) |
|--------|----|----|-------------------------|
| Sprint 1 | HU-001, HU-002, HU-003 | Autenticación | 13 |
| Sprint 2 | HU-005, HU-006, HU-007 | Inventario Core | 13 |
| Sprint 3 | HU-009, HU-010, HU-011 | Inventario Avanzado | 13 |
| Sprint 4 | HU-012, HU-013, HU-014 | Ventas Core | 21 |
| Sprint 5 | HU-016, HU-017, HU-018, HU-019 | Clientes | 13 |
| Sprint 6 | HU-021, HU-022, HU-023 | Reportes | 13 |
| Sprint 7 | HU-025, HU-026 | IA - Predicción | 21 |
| Sprint 8 | HU-004, HU-015, HU-024, HU-027 | Complementos | 13 |

**Total Story Points:** 120  
**Sprints:** 8 (2 semanas cada uno) = 16 semanas ≈ 4 meses de desarrollo  

---

## 6. Validaciones y Reglas de Negocio

### 6.1 Reglas de Inventario
- RN-INV-01: No se puede vender más cantidad de la disponible en stock
- RN-INV-02: Stock no puede ser negativo
- RN-INV-03: Precio de venta debe ser mayor a precio de compra (advertencia, no bloqueo)
- RN-INV-04: SKU debe ser alfanumérico de máximo 50 caracteres
- RN-INV-05: Stock mínimo debe ser menor que stock máximo

### 6.2 Reglas de Ventas
- RN-VEN-01: Una venta debe tener al menos un producto
- RN-VEN-02: Descuento no puede ser mayor al 100%
- RN-VEN-03: Solo se pueden cancelar ventas del mismo día (configurable)
- RN-VEN-04: Al cancelar venta, se debe revertir inventario
- RN-VEN-05: Número de factura es autogenerado e inmutable

### 6.3 Reglas de Clientes
- RN-CLI-01: Email debe ser válido si se proporciona
- RN-CLI-02: Documento de identidad debe ser único por tenant
- RN-CLI-03: No se puede eliminar cliente con ventas en los últimos 30 días

### 6.4 Reglas de IA
- RN-IA-01: Se requieren mínimo 30 días de datos para predicción
- RN-IA-02: Predicciones se actualizan diariamente a medianoche
- RN-IA-03: Confianza de predicción < 60% debe mostrar advertencia
- RN-IA-04: No predecir productos con menos de 10 ventas totales

---

## Conclusión

Este documento establece las bases funcionales del sistema Pecesaurio mediante historias de usuario concretas, requisitos funcionales y no funcionales detallados. La priorización presentada permite un desarrollo incremental enfocado en el MVP, con claridad sobre qué construir primero y qué métricas cumplir.

**Próximos pasos:**
1. Revisión y aprobación del equipo
2. Refinamiento de story points según velocidad del equipo
3. Inicio de implementación según cronograma

---

**Fecha de elaboración:** Octubre 2024  
**Versión:** 1.0  
**Elaborado por:** Equipo Pecesaurio

