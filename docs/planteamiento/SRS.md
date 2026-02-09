# Software Requirements Specification (SRS)
## OrbitEngine - Plataforma SaaS para Gestión de Pymes

**Versión:** 1.0  
**Fecha:** Octubre 2025  
**Estado:** Borrador  

---

## Control de Versiones

| Versión | Fecha | Autor | Descripción |
|---------|-------|-------|-------------|
| 1.0 | Oct 2025 | Equipo OrbitEngine | Versión inicial del SRS |

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Descripción General](#2-descripción-general)
3. [Requisitos Específicos](#3-requisitos-específicos)
4. [Requisitos de Interfaces Externas](#4-requisitos-de-interfaces-externas)
5. [Requisitos Funcionales](#5-requisitos-funcionales)
6. [Requisitos No Funcionales](#6-requisitos-no-funcionales)
7. [Otros Requisitos](#7-otros-requisitos)
8. [Apéndices](#8-apéndices)

---

## 1. Introducción

### 1.1 Propósito

Este documento especifica los requisitos de software para **OrbitEngine**, una plataforma SaaS diseñada para la gestión integral de procesos internos en pequeñas y medianas empresas (pymes). Este SRS está dirigido a:

- Equipo de desarrollo
- Asesor académico del proyecto
- Stakeholders (pymes participantes en pruebas piloto)
- Evaluadores del proyecto de grado

### 1.2 Alcance

**OrbitEngine** es una aplicación web que permite a las pymes:

- **Gestionar inventario:** CRUD de productos, control de stock, alertas de niveles bajos
- **Registrar ventas:** Captura de transacciones, generación de facturas, historial
- **Administrar clientes:** Base de datos de clientes, historial de compras
- **Visualizar métricas:** Dashboard con KPIs, reportes exportables
- **Predecir demanda:** Algoritmos de IA para forecasting de productos

**Beneficios esperados:**
- Reducción de errores administrativos en 40%
- Ahorro de tiempo en tareas manuales del 30%
- Mejor toma de decisiones basada en datos
- Predicciones de demanda con precisión >70%

**Límites del sistema:**
- No incluye facturación electrónica oficial
- No incluye gestión de nómina
- No incluye integración con sistemas ERP externos (en MVP)
- Limitado a comercio de productos (no servicios)

### 1.3 Definiciones, Acrónimos y Abreviaturas

| Término | Definición |
|---------|------------|
| **API** | Application Programming Interface |
| **CRUD** | Create, Read, Update, Delete |
| **IA** | Inteligencia Artificial |
| **JWT** | JSON Web Token |
| **KPI** | Key Performance Indicator |
| **ML** | Machine Learning |
| **MVP** | Minimum Viable Product |
| **Pyme** | Pequeña y Mediana Empresa |
| **RBAC** | Role-Based Access Control |
| **REST** | Representational State Transfer |
| **SaaS** | Software as a Service |
| **SKU** | Stock Keeping Unit |
| **SPA** | Single Page Application |
| **Tenant** | Empresa/organización que usa la plataforma |
| **UX** | User Experience |

### 1.4 Referencias

1. IEEE Std 830-1998 - IEEE Recommended Practice for Software Requirements Specifications
2. Propuesta de Proyecto de Grado - OrbitEngine (Octubre 2025)
3. Documentación de FastAPI: https://fastapi.tiangolo.com/
4. Documentación de React: https://react.dev/
5. Prophet Documentation: https://facebook.github.io/prophet/

### 1.5 Visión General del Documento

Este documento está organizado de la siguiente manera:

- **Sección 2:** Descripción general del sistema, funciones principales, características de usuarios, restricciones y suposiciones
- **Sección 3:** Requisitos específicos detallados
- **Sección 4:** Requisitos de interfaces externas
- **Sección 5:** Requisitos funcionales por módulo
- **Sección 6:** Requisitos no funcionales (rendimiento, seguridad, usabilidad)
- **Sección 7:** Otros requisitos adicionales
- **Sección 8:** Apéndices y material de apoyo

---

## 2. Descripción General

### 2.1 Perspectiva del Producto

OrbitEngine es un sistema independiente de tipo SaaS (Software as a Service) que opera completamente en la nube. El sistema consta de:

```
┌─────────────────────────────────────────────────────┐
│                    USUARIOS                         │
│              (Navegador Web)                        │
└───────────────────────┬─────────────────────────────┘
                        │ HTTPS
                        ▼
┌─────────────────────────────────────────────────────┐
│               CloudFront (CDN)                      │
└──────────┬──────────────────────────┬───────────────┘
           │                          │
  ┌────────▼────────┐        ┌────────▼────────────┐
  │  Frontend SPA   │        │   Backend API       │
  │   (React)       │◄──────►│   (FastAPI)         │
  │   S3            │  REST  │   EC2/ECS           │
  └─────────────────┘        └─────────┬───────────┘
                                       │
                    ┌──────────────────┼──────────────┐
                    ▼                  ▼              ▼
            ┌──────────────┐  ┌─────────────┐  ┌─────────┐
            │ PostgreSQL   │  │   Redis     │  │   S3    │
            │   (RDS)      │  │ (ElastiCache)│  │ (Files) │
            └──────────────┘  └─────────────┘  └─────────┘
```

**Interfaces del Sistema:**
- **Usuarios:** Interactúan mediante navegador web (Chrome, Firefox, Safari, Edge)
- **Base de Datos:** PostgreSQL para persistencia de datos transaccionales
- **Cache:** Redis para sesiones y datos temporales
- **Almacenamiento:** AWS S3 para archivos (imágenes, PDFs)
- **Tareas Asíncronas:** Celery para procesamiento en segundo plano

### 2.2 Funciones del Producto

El sistema proporciona las siguientes funciones principales:

#### 2.2.1 Gestión de Autenticación y Usuarios
- Registro de nuevas empresas (tenants)
- Inicio de sesión seguro con JWT
- Gestión de usuarios por empresa
- Asignación de roles (Administrador, Vendedor, Visualizador)
- Recuperación de contraseña

#### 2.2.2 Gestión de Inventario
- Agregar, editar, eliminar y visualizar productos
- Organizar productos por categorías
- Control de stock en tiempo real
- Alertas automáticas de stock bajo
- Historial de movimientos de inventario
- Ajustes manuales con justificación

#### 2.2.3 Gestión de Ventas
- Registro de ventas multi-producto
- Generación automática de número de factura
- Cálculo automático de totales
- Aplicación de descuentos
- Selección de método de pago
- Historial de ventas con filtros
- Cancelación de ventas (solo administradores)
- Visualización de detalle de venta
- Exportación de facturas a PDF

#### 2.2.4 Gestión de Clientes
- Registro de clientes con datos de contacto
- Historial de compras por cliente
- Estadísticas de cliente (total comprado, frecuencia)
- Identificación de clientes frecuentes
- Búsqueda y filtrado de clientes

#### 2.2.5 Reportes y Análisis
- Dashboard con KPIs principales
- Reportes de ventas por período
- Reportes de inventario
- Reportes de clientes
- Gráficos y visualizaciones
- Exportación a PDF y Excel

#### 2.2.6 Predicción con IA
- Forecasting de demanda por producto
- Recomendaciones de reabastecimiento
- Análisis de tendencias
- Visualización de predicciones vs. datos reales

### 2.3 Características de los Usuarios

#### 2.3.1 Administrador de Pyme

**Descripción:** Dueño o gerente de la empresa

**Características:**
- Edad: 35-55 años
- Conocimientos técnicos: Básicos a intermedios
- Experiencia con software: Excel, WhatsApp, aplicaciones móviles básicas
- Frecuencia de uso: Diaria

**Tareas principales:**
- Configuración inicial del sistema
- Gestión de usuarios y permisos
- Monitoreo de KPIs
- Generación de reportes
- Toma de decisiones basada en predicciones IA
- Gestión completa de inventario

**Necesidades:**
- Interfaz intuitiva, no técnica
- Reportes claros y visuales
- Acceso desde cualquier lugar
- Información en tiempo real

#### 2.3.2 Vendedor

**Descripción:** Empleado encargado de ventas

**Características:**
- Edad: 20-40 años
- Conocimientos técnicos: Básicos
- Experiencia con software: Apps móviles, redes sociales
- Frecuencia de uso: Diaria, intensiva

**Tareas principales:**
- Registro rápido de ventas
- Consulta de stock disponible
- Búsqueda de productos
- Registro de clientes
- Consulta de historial de clientes

**Necesidades:**
- Proceso de venta rápido (< 1 minuto)
- Búsqueda eficiente de productos
- Interfaz simple y clara
- Confirmación visual de acciones

#### 2.3.3 Visualizador (Contador/Asesor)

**Descripción:** Contador o asesor externo

**Características:**
- Edad: 30-50 años
- Conocimientos técnicos: Avanzados
- Experiencia con software: Excel avanzado, software contable
- Frecuencia de uso: Semanal/quincenal

**Tareas principales:**
- Consulta de reportes financieros
- Exportación de datos
- Análisis de métricas
- Validación de información

**Necesidades:**
- Acceso de solo lectura
- Exportación fácil de datos
- Reportes detallados
- Datos precisos y confiables

### 2.4 Restricciones

#### 2.4.1 Restricciones de Regulación
- Cumplimiento básico de protección de datos personales (GDPR/LOPD)
- Almacenamiento seguro de información de clientes
- Auditoría de acciones críticas

#### 2.4.2 Restricciones de Hardware
- Sistema 100% basado en la nube (AWS)
- No requiere hardware especializado del cliente
- Acceso mediante navegador web moderno

#### 2.4.3 Restricciones de Interfaces con Otras Aplicaciones
- No integración con sistemas ERP externos (MVP)
- No integración con pasarelas de pago (MVP)
- No sincronización con marketplaces (MVP)

#### 2.4.4 Restricciones de Operaciones Paralelas
- Sistema multi-tenant con aislamiento de datos
- Máximo 10 usuarios concurrentes por tenant (MVP)
- Procesamiento asíncrono para tareas pesadas

#### 2.4.5 Restricciones de Auditoría
- Log de todas las acciones críticas
- Registro de quien realizó cada cambio
- Historial inmutable de ventas

#### 2.4.6 Restricciones de Funciones de Alto Orden
- Sistema stateless para escalabilidad
- API RESTful sin estado de sesión en servidor

#### 2.4.7 Restricciones de Lenguaje
- Interfaz en español (idioma único en MVP)
- Formato de moneda: dólar/peso según configuración
- Formato de fecha: DD/MM/YYYY

### 2.5 Suposiciones y Dependencias

#### 2.5.1 Suposiciones
- Los usuarios tienen acceso a internet estable
- Los usuarios tienen navegador web moderno
- Las pymes tienen datos históricos de al menos 3-6 meses para IA
- Los usuarios están dispuestos a migrar de métodos manuales
- Los datos ingresados por usuarios son precisos

#### 2.5.2 Dependencias
- **AWS:** Disponibilidad de servicios cloud
- **Bibliotecas Open Source:** Disponibilidad de React, FastAPI, Prophet, etc.
- **PostgreSQL:** Disponibilidad de RDS
- **Navegadores:** Soporte de navegadores modernos
- **Datos históricos:** Suficientes datos para entrenar modelos de IA

### 2.6 Requisitos Pospuestos

Las siguientes características NO estarán en el MVP pero se consideran para versiones futuras:

- Aplicación móvil nativa (iOS/Android)
- Facturación electrónica oficial
- Integración con pasarelas de pago
- Gestión de múltiples bodegas/sucursales
- Contabilidad completa
- Gestión de nómina
- Sistema de punto de venta (POS) físico
- Chatbot con IA conversacional
- Multi-idioma
- Multi-moneda
- Integración con marketplaces
- API pública para terceros

---

## 3. Requisitos Específicos

Esta sección contiene todos los requisitos del sistema con suficiente detalle para que los diseñadores puedan diseñar un sistema que satisfaga los requisitos, y los testers puedan verificar que el sistema cumple con los requisitos.

---

## 4. Requisitos de Interfaces Externas

### 4.1 Interfaces de Usuario

#### 4.1.1 Características Generales de la GUI

**Estilo Visual:**
- Diseño moderno y limpio
- Paleta de colores consistente
- Uso de iconos para acciones comunes
- Feedback visual de acciones (toasts, loaders)

**Layout:**
- Sidebar de navegación persistente
- Header con información de usuario y empresa
- Área de contenido principal
- Footer con información de versión

**Navegación:**
- Máximo 3 clics para cualquier funcionalidad
- Breadcrumbs para ubicación en el sistema
- Botones de acción claramente identificados

**Responsive Design:**
- Soporte desktop (1920x1080, 1366x768)
- Soporte tablet (768x1024)
- Soporte móvil (375x667, 414x896)

#### 4.1.2 Pantallas Principales

**REQ-UI-01: Pantalla de Login**
- Campos: Email, Contraseña
- Botón "Iniciar Sesión"
- Link "¿Olvidaste tu contraseña?"
- Link "Registrar nueva empresa"
- Validación en tiempo real
- Mensajes de error claros

**REQ-UI-02: Dashboard Principal**
- KPIs en cards: Ventas del día, Ventas del mes, Productos con stock bajo, Top productos
- Gráfico de ventas últimos 7 días
- Lista de últimas ventas
- Alertas de stock bajo destacadas
- Acceso rápido a funciones principales

**REQ-UI-03: Lista de Productos**
- Tabla con columnas: Imagen, Nombre, SKU, Categoría, Precio, Stock
- Indicador visual de stock bajo (badge rojo/amarillo)
- Buscador en tiempo real
- Filtros: Categoría, Estado (activo/inactivo)
- Botón "Agregar Producto"
- Paginación
- Acciones por fila: Editar, Eliminar

**REQ-UI-04: Formulario de Producto**
- Campos obligatorios marcados con *
- Upload de imagen con preview
- Validación en tiempo real
- Campos: Nombre, SKU, Categoría, Descripción, Precio Costo, Precio Venta, Stock Inicial, Stock Mínimo, Stock Máximo
- Botones: Guardar, Cancelar

**REQ-UI-05: Registro de Venta**
- Buscador de productos con autocompletado
- Lista de productos agregados con subtotales
- Cálculo automático de total
- Campo de descuento opcional
- Selector de cliente (opcional)
- Selector de método de pago
- Botón "Completar Venta"
- Confirmación antes de guardar

**REQ-UI-06: Historial de Ventas**
- Tabla con: Fecha, # Factura, Cliente, Total, Método Pago, Vendedor
- Filtros: Rango de fechas, Cliente, Método de pago
- Búsqueda por número de factura
- Acción: Ver detalle
- Exportar a Excel

**REQ-UI-07: Pantalla de Predicciones**
- Lista de productos con predicciones
- Gráfico de tendencia histórica + predicción
- Indicador de confianza
- Recomendaciones de reabastecimiento
- Filtros: Categoría, Nivel de confianza

### 4.2 Interfaces de Hardware

No aplica. El sistema es completamente basado en software y no requiere interfaces de hardware especializadas más allá de dispositivos estándar de entrada (teclado, mouse, pantalla táctil) y red (conexión a internet).

### 4.3 Interfaces de Software

#### 4.3.1 Base de Datos

**Sistema:** PostgreSQL 15+  
**Interfaz:** SQLAlchemy ORM  
**Conexión:** Pool de conexiones con SSL  

**Funciones requeridas:**
- CRUD operations
- Transactions (ACID)
- Foreign key constraints
- Triggers para actualización automática
- Índices para optimización

#### 4.3.2 Sistema de Caché

**Sistema:** Redis 7+  
**Interfaz:** redis-py  
**Uso:**
- Sesiones de usuario
- Cache de queries frecuentes
- Rate limiting
- Broker de Celery

#### 4.3.3 Almacenamiento de Archivos

**Sistema:** AWS S3  
**Interfaz:** boto3  
**Operaciones:**
- PUT: Subir archivos (imágenes, PDFs)
- GET: Obtener URLs firmadas
- DELETE: Eliminar archivos

#### 4.3.4 Sistema de Tareas Asíncronas

**Sistema:** Celery  
**Broker:** Redis  
**Backend:** Redis  
**Uso:**
- Entrenamiento de modelos ML
- Generación de reportes pesados
- Envío de emails (futuro)
- Tareas programadas (predicciones diarias)

### 4.4 Interfaces de Comunicación

#### 4.4.1 Protocolo HTTP/HTTPS

**Frontend ↔ Backend:**
- Protocolo: HTTPS (TLS 1.2+)
- Formato: JSON
- Arquitectura: REST API
- Autenticación: JWT en header Authorization
- Rate limiting: 100 requests/minuto por usuario

**Estructura de Request:**
```json
{
  "method": "POST",
  "headers": {
    "Authorization": "Bearer <JWT_TOKEN>",
    "Content-Type": "application/json"
  },
  "body": {
    // Request payload
  }
}
```

**Estructura de Response (Éxito):**
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operación exitosa"
}
```

**Estructura de Response (Error):**
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Descripción del error",
    "details": []
  }
}
```

---

## 5. Requisitos Funcionales

### 5.1 Módulo de Autenticación y Usuarios

#### REQ-FUNC-AUTH-001: Registro de Empresa
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir el registro de nuevas empresas (tenants).

**Entradas:**
- Nombre de la empresa
- Email del administrador
- Contraseña
- Teléfono
- Nombre del administrador

**Procesamiento:**
1. Validar email único en el sistema
2. Validar formato de email
3. Validar contraseña (mínimo 8 caracteres)
4. Hashear contraseña con bcrypt
5. Crear registro de tenant
6. Crear usuario administrador
7. Asignar rol de administrador
8. Generar token JWT

**Salidas:**
- Token de acceso (JWT)
- Datos de usuario y empresa
- Mensaje de confirmación

**Criterios de Aceptación:**
- Email debe ser único
- Contraseña debe tener mínimo 8 caracteres
- Se crea tenant y usuario administrador en una transacción
- Token generado es válido por 24 horas

---

#### REQ-FUNC-AUTH-002: Inicio de Sesión
**Prioridad:** Crítica  
**Descripción:** El sistema debe autenticar usuarios mediante email y contraseña.

**Entradas:**
- Email
- Contraseña

**Procesamiento:**
1. Buscar usuario por email
2. Verificar contraseña con hash almacenado
3. Verificar que usuario esté activo
4. Verificar que empresa esté activa
5. Generar token JWT
6. Actualizar campo last_login_at
7. Resetear contador de intentos fallidos

**Salidas:**
- Token de acceso (JWT)
- Datos de usuario (id, nombre, email, rol)
- Datos de empresa

**Criterios de Aceptación:**
- Máximo 5 intentos fallidos antes de bloqueo temporal (15 minutos)
- Token válido por 24 horas
- Si usuario inactivo, mostrar mensaje específico
- Logging de intentos de login

**Casos de Error:**
- Email no existe: "Credenciales incorrectas"
- Contraseña incorrecta: "Credenciales incorrectas"
- Usuario bloqueado: "Cuenta bloqueada temporalmente. Intenta en X minutos"
- Empresa suspendida: "Tu empresa tiene la suscripción suspendida"

---

#### REQ-FUNC-AUTH-003: Gestión de Roles
**Prioridad:** Alta  
**Descripción:** El sistema debe soportar tres roles con permisos diferenciados.

**Roles definidos:**

1. **Administrador:**
   - Acceso completo al sistema
   - Gestión de usuarios
   - Configuración de empresa
   - Todas las operaciones CRUD
   - Cancelación de ventas

2. **Vendedor:**
   - Crear ventas
   - Consultar inventario (solo lectura)
   - Gestionar clientes
   - Ver historial de sus propias ventas

3. **Visualizador:**
   - Solo lectura
   - Acceso a reportes
   - Acceso a dashboard
   - Exportación de datos

**Procesamiento:**
- Verificar rol en cada request al backend
- Middleware de autorización
- Frontend adapta UI según rol

**Criterios de Aceptación:**
- Permisos verificados en backend (no solo frontend)
- Intentos de acceso no autorizado retornan 403 Forbidden
- Logging de intentos de acceso no autorizado

---

#### REQ-FUNC-AUTH-004: Recuperación de Contraseña
**Prioridad:** Media  
**Descripción:** El sistema debe permitir recuperar contraseña mediante email.

**Entradas:**
- Email del usuario

**Procesamiento:**
1. Verificar que email exista
2. Generar token único de recuperación
3. Almacenar token con expiración de 1 hora
4. Enviar email con link de recuperación
5. Usuario accede a formulario de nueva contraseña
6. Validar token
7. Actualizar contraseña
8. Invalidar token

**Salidas:**
- Email enviado con link
- Confirmación de actualización de contraseña

**Criterios de Aceptación:**
- Token expira en 1 hora
- Token de un solo uso
- Por seguridad, siempre mostrar "Si el email existe, recibirás un link"

---

### 5.2 Módulo de Gestión de Inventario

#### REQ-FUNC-INV-001: Agregar Producto
**Prioridad:** Crítica  
**Descripción:** El sistema debe permitir agregar nuevos productos al inventario.

**Entradas:**
- Nombre del producto (requerido)
- SKU (requerido, único por tenant)
- Categoría (opcional)
- Descripción (opcional)
- Imagen (opcional)
- Precio de costo (requerido, ≥ 0)
- Precio de venta (requerido, ≥ 0)
- Stock inicial (requerido, ≥ 0)
- Stock mínimo (requerido, ≥ 0)
- Stock máximo (opcional)
- Unidad de medida (requerido, default: "unidad")
- Código de barras (opcional)

**Procesamiento:**
1. Validar campos requeridos
2. Validar unicidad de SKU por tenant
3. Validar que precio venta ≥ precio costo (warning, no bloqueante)
4. Validar que stock mínimo < stock máximo (si se proporciona)
5. Subir imagen a S3 (si se proporciona)
6. Crear registro en tabla products
7. Crear registro en inventory_movements (tipo: "initial")

**Salidas:**
- Objeto Product creado
- URL de imagen en S3
- Mensaje de confirmación

**Criterios de Aceptación:**
- SKU único por tenant
- Imagen máximo 5MB
- Formatos aceptados: JPG, PNG, WEBP
- Registro de movimiento de inventario inicial

**Validaciones:**
- Nombre: 3-255 caracteres
- SKU: alfanumérico, 1-100 caracteres
- Precios: decimal, máximo 2 decimales

---

#### REQ-FUNC-INV-002: Editar Producto
**Prioridad:** Crítica  
**Descripción:** El sistema debe permitir modificar información de productos existentes.

**Entradas:**
- ID del producto
- Campos a actualizar

**Procesamiento:**
1. Verificar que producto exista y pertenezca al tenant
2. Validar campos modificados
3. Si se cambia SKU, validar unicidad
4. Si se cambia imagen, subir nueva a S3 y eliminar anterior
5. Actualizar registro
6. Registrar en audit_log

**Salidas:**
- Objeto Product actualizado
- Mensaje de confirmación

**Criterios de Aceptación:**
- Historial de cambios en audit_log
- Campo updated_at actualizado automáticamente
- No se puede modificar stock directamente (usar ajuste de inventario)

---

#### REQ-FUNC-INV-003: Eliminar Producto
**Prioridad:** Media  
**Descripción:** El sistema debe permitir eliminar productos (soft delete).

**Restricciones:**
- Solo usuarios con rol Administrador
- No se puede eliminar si tiene ventas en los últimos 30 días

**Procesamiento:**
1. Verificar permisos
2. Verificar que no tenga ventas recientes
3. Soft delete (marcar deleted_at)
4. Mantener en BD para integridad referencial
5. Registrar en audit_log

**Salidas:**
- Confirmación de eliminación
- Producto no visible en listados

**Criterios de Aceptación:**
- Registro permanece en BD
- No aparece en consultas de productos activos
- Se puede recuperar si es necesario (futuro)

---

#### REQ-FUNC-INV-004: Listar Productos
**Prioridad:** Crítica  
**Descripción:** El sistema debe mostrar listado de productos con filtros y búsqueda.

**Entradas:**
- Parámetros de paginación (skip, limit)
- Búsqueda (texto libre)
- Filtros: categoría, estado stock

**Procesamiento:**
1. Query a base de datos del tenant
2. Aplicar filtros
3. Búsqueda por nombre o SKU
4. Ordenamiento
5. Paginación
6. Incluir información de categoría

**Salidas:**
- Array de productos
- Total de registros
- Metadata de paginación

**Criterios de Aceptación:**
- Paginación máxima: 100 items por página
- Búsqueda case-insensitive
- Productos con stock bajo destacados visualmente
- Tiempo de respuesta < 500ms

---

#### REQ-FUNC-INV-005: Alertas de Stock Bajo
**Prioridad:** Alta  
**Descripción:** El sistema debe generar alertas cuando stock < stock mínimo.

**Procesamiento:**
- Query automático en dashboard
- Comparar stock_quantity vs stock_min
- Filtrar solo productos activos

**Salidas:**
- Lista de productos con stock bajo
- Badge con contador en dashboard
- Indicador visual en tabla de productos

**Criterios de Aceptación:**
- Actualización en tiempo real
- Destacado visual (color rojo/amarillo)
- Acceso rápido desde dashboard

---

#### REQ-FUNC-INV-006: Ajuste Manual de Inventario
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir ajustes manuales de stock con justificación.

**Restricciones:**
- Solo usuarios con rol Administrador

**Entradas:**
- ID del producto
- Nueva cantidad de stock
- Motivo (requerido): "merma", "corrección", "donación", "pérdida", "otro"
- Descripción adicional (opcional)

**Procesamiento:**
1. Verificar permisos
2. Verificar que producto exista
3. Calcular diferencia (nueva cantidad - cantidad actual)
4. Actualizar stock del producto
5. Registrar en inventory_movements con tipo "adjustment"
6. Incluir motivo y usuario responsable
7. Registrar en audit_log

**Salidas:**
- Stock actualizado
- Registro de movimiento creado
- Confirmación

**Criterios de Aceptación:**
- Motivo es obligatorio
- Usuario responsable registrado
- Historial completo de cambios
- No se puede ajustar a valores negativos

---

#### REQ-FUNC-INV-007: Historial de Movimientos
**Prioridad:** Media  
**Descripción:** El sistema debe mantener historial completo de movimientos de inventario.

**Tipos de movimiento:**
- `sale`: Venta (disminuye stock)
- `purchase`: Compra a proveedor (aumenta stock) - futuro
- `adjustment`: Ajuste manual
- `return`: Devolución (aumenta stock) - futuro
- `initial`: Stock inicial

**Entradas:**
- Filtros: producto, tipo de movimiento, rango de fechas

**Procesamiento:**
1. Query a tabla inventory_movements
2. Aplicar filtros
3. Join con productos y usuarios
4. Ordenar por fecha descendente
5. Paginación

**Salidas:**
- Lista de movimientos con:
  - Fecha y hora
  - Producto
  - Tipo de movimiento
  - Cantidad
  - Stock anterior
  - Stock nuevo
  - Usuario responsable
  - Referencia (ID de venta, etc.)

**Criterios de Aceptación:**
- Registro inmutable (no se puede editar/eliminar)
- Exportable a Excel
- Auditable
- Tiempo de respuesta < 1 segundo

---

### 5.3 Módulo de Gestión de Ventas

#### REQ-FUNC-SALE-001: Registrar Venta
**Prioridad:** Crítica  
**Descripción:** El sistema debe permitir registrar ventas de uno o más productos.

**Entradas:**
- Lista de productos (id, cantidad, precio unitario)
- Cliente (opcional)
- Método de pago (requerido): "efectivo", "tarjeta", "transferencia", "otro"
- Descuento (opcional, %)
- Notas (opcional)

**Procesamiento:**
1. Validar que todos los productos existan
2. Validar stock disponible para cada producto
3. Calcular subtotal de cada item (cantidad * precio)
4. Calcular subtotal total
5. Aplicar descuento si existe
6. Calcular total final
7. Generar número de factura único
8. Crear registro en tabla sales
9. Crear registros en tabla sale_items
10. **Trigger automático:** Actualizar stock de productos
11. **Trigger automático:** Registrar inventory_movements
12. **Trigger automático:** Actualizar estadísticas de cliente (si aplica)
13. Commit de transacción

**Salidas:**
- Objeto Sale creado
- Número de factura
- Total de la venta
- Confirmación

**Criterios de Aceptación:**
- Transacción ACID (todo o nada)
- No se puede vender más stock del disponible
- Número de factura único y secuencial por tenant
- Stock actualizado inmediatamente
- Tiempo de procesamiento < 2 segundos

**Validaciones:**
- Al menos 1 producto
- Cantidad > 0 para cada producto
- Descuento entre 0 y 100%
- Stock disponible >= cantidad solicitada

**Casos de Error:**
- Stock insuficiente: "El producto [nombre] no tiene suficiente stock. Disponible: X"
- Producto no existe: "Producto no encontrado"
- Error de conexión BD: "Error al procesar venta. Intenta nuevamente"

---

#### REQ-FUNC-SALE-002: Listar Ventas
**Prioridad:** Crítica  
**Descripción:** El sistema debe mostrar historial de ventas con filtros.

**Entradas:**
- Filtros:
  - Rango de fechas
  - Cliente
  - Método de pago
  - Estado (completada, cancelada)
  - Vendedor
- Búsqueda por número de factura
- Parámetros de paginación

**Procesamiento:**
1. Query a tabla sales
2. Join con customers y users
3. Aplicar filtros
4. Ordenar por fecha descendente
5. Paginación

**Salidas:**
- Lista de ventas con:
  - Fecha
  - Número de factura
  - Cliente
  - Total
  - Método de pago
  - Estado
  - Vendedor
- Total de registros
- Metadata de paginación

**Criterios de Aceptación:**
- Vendedores solo ven sus propias ventas
- Administradores ven todas las ventas
- Exportable a Excel
- Tiempo de respuesta < 1 segundo

---

#### REQ-FUNC-SALE-003: Ver Detalle de Venta
**Prioridad:** Alta  
**Descripción:** El sistema debe mostrar información completa de una venta específica.

**Entradas:**
- ID de la venta

**Procesamiento:**
1. Verificar que venta pertenezca al tenant
2. Query a sales con join a sale_items
3. Join con products para obtener nombres actuales
4. Join con customer y user

**Salidas:**
- Información de venta:
  - Número de factura
  - Fecha y hora
  - Cliente (si aplica)
  - Vendedor
  - Estado
  - Lista de productos:
    - Nombre (snapshot)
    - SKU (snapshot)
    - Cantidad
    - Precio unitario (snapshot)
    - Subtotal
  - Subtotal
  - Descuento
  - Total
  - Método de pago
  - Notas
- Opción de descargar PDF

**Criterios de Aceptación:**
- Muestra snapshots de precios al momento de la venta
- PDF generado con diseño profesional
- Tiempo de carga < 1 segundo

---

#### REQ-FUNC-SALE-004: Cancelar Venta
**Prioridad:** Media  
**Descripción:** El sistema debe permitir cancelar ventas registradas por error.

**Restricciones:**
- Solo usuarios con rol Administrador
- Solo ventas del día actual (configurable)
- Requiere confirmación con contraseña

**Entradas:**
- ID de la venta
- Motivo de cancelación (requerido)
- Contraseña del administrador

**Procesamiento:**
1. Verificar permisos
2. Verificar que venta sea del día actual
3. Verificar contraseña del administrador
4. Marcar venta como cancelada (no eliminar)
5. Actualizar campos: status="cancelled", cancelled_at, cancelled_by, cancellation_reason
6. **Trigger:** Revertir stock de productos
7. **Trigger:** Registrar inventory_movements (tipo: return)
8. **Trigger:** Actualizar estadísticas de cliente (restar)
9. Registrar en audit_log

**Salidas:**
- Venta marcada como cancelada
- Stock revertido
- Confirmación

**Criterios de Aceptación:**
- Venta permanece en BD (no se elimina)
- Stock se revierte correctamente
- Auditoría completa del evento
- Motivo es obligatorio
- No se puede cancelar una venta ya cancelada

---

#### REQ-FUNC-SALE-005: Generar PDF de Factura
**Prioridad:** Alta  
**Descripción:** El sistema debe generar factura en PDF para cada venta.

**Entradas:**
- ID de la venta

**Procesamiento:**
1. Obtener información completa de la venta
2. Generar PDF con librería (ReportLab/WeasyPrint)
3. Incluir logo de la empresa
4. Diseño profesional
5. Guardar en S3
6. Retornar URL firmada

**Salidas:**
- PDF con:
  - Logo y datos de la empresa
  - Número de factura
  - Fecha
  - Datos del cliente
  - Tabla de productos
  - Subtotal, descuento, total
  - Método de pago

**Criterios de Aceptación:**
- PDF generado en < 3 segundos
- Diseño profesional y claro
- Tamaño de archivo < 1MB
- URL válida por 24 horas

---

### 5.4 Módulo de Gestión de Clientes

#### REQ-FUNC-CUST-001: Agregar Cliente
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir registrar nuevos clientes.

**Entradas:**
- Tipo de documento (requerido): "DNI", "RUC", "Pasaporte", "Otro"
- Número de documento (requerido, único por tenant)
- Nombre (requerido)
- Apellido (requerido)
- Email (opcional)
- Teléfono (opcional)
- Dirección (opcional)
- Ciudad (opcional)
- País (opcional)
- Notas (opcional)

**Procesamiento:**
1. Validar campos requeridos
2. Validar unicidad de documento por tenant
3. Validar formato de email si se proporciona
4. Crear registro en tabla customers
5. Inicializar estadísticas en 0

**Salidas:**
- Objeto Customer creado
- Confirmación

**Criterios de Aceptación:**
- Documento único por tenant
- Email válido si se proporciona
- Estadísticas iniciales: total_purchases=0, purchases_count=0

**Validaciones:**
- Nombre y apellido: 2-100 caracteres
- Documento: alfanumérico, 5-50 caracteres
- Email: formato válido
- Teléfono: 7-20 caracteres

---

#### REQ-FUNC-CUST-002: Editar Cliente
**Prioridad:** Alta  
**Descripción:** El sistema debe permitir actualizar información de clientes.

**Entradas:**
- ID del cliente
- Campos a actualizar

**Procesamiento:**
1. Verificar que cliente pertenezca al tenant
2. Validar campos modificados
3. Si se cambia documento, validar unicidad
4. Actualizar registro
5. Registrar en audit_log

**Salidas:**
- Objeto Customer actualizado
- Confirmación

**Criterios de Aceptación:**
- No se pueden editar estadísticas manualmente (son calculadas)
- Historial de cambios en audit_log

---

#### REQ-FUNC-CUST-003: Listar Clientes
**Prioridad:** Alta  
**Descripción:** El sistema debe mostrar listado de clientes con búsqueda.

**Entradas:**
- Búsqueda por nombre o documento
- Filtros: estado (activo/inactivo)
- Parámetros de paginación
- Ordenamiento

**Procesamiento:**
1. Query a tabla customers del tenant
2. Búsqueda case-insensitive
3. Aplicar filtros
4. Ordenamiento
5. Paginación

**Salidas:**
- Lista de clientes con:
  - Nombre completo
  - Documento
  - Email
  - Teléfono
  - Total comprado
  - Número de compras
  - Última compra

**Criterios de Aceptación:**
- Búsqueda instantánea (< 300ms)
- Exportable a Excel
- Destaca clientes frecuentes

---

#### REQ-FUNC-CUST-004: Ver Perfil de Cliente
**Prioridad:** Media  
**Descripción:** El sistema debe mostrar información completa y estadísticas de un cliente.

**Entradas:**
- ID del cliente

**Procesamiento:**
1. Query a customers
2. Calcular estadísticas actualizadas:
   - Total comprado
   - Número de compras
   - Promedio de compra
   - Productos más comprados
   - Última compra
3. Obtener historial de compras (últimas 10)

**Salidas:**
- Datos del cliente
- Estadísticas
- Historial de compras
- Gráfico de compras en el tiempo
- Top productos comprados

**Criterios de Aceptación:**
- Estadísticas precisas
- Historial ordenado por fecha descendente
- Visualización clara

---

#### REQ-FUNC-CUST-005: Eliminar Cliente
**Prioridad:** Baja  
**Descripción:** El sistema debe permitir eliminar clientes (soft delete).

**Restricciones:**
- Solo usuarios con rol Administrador
- No se puede eliminar si tiene compras en los últimos 30 días

**Procesamiento:**
1. Verificar permisos
2. Verificar que no tenga compras recientes
3. Soft delete (marcar deleted_at)
4. Mantener histórico de ventas
5. Registrar en audit_log

**Salidas:**
- Cliente no visible en listados
- Ventas históricas mantienen referencia

**Criterios de Aceptación:**
- Registro permanece en BD
- Integridad referencial mantenida
- Histórico de ventas no afectado

---

### 5.5 Módulo de Reportes y Dashboard

#### REQ-FUNC-REP-001: Dashboard Principal
**Prioridad:** Crítica  
**Descripción:** El sistema debe mostrar un dashboard con KPIs principales.

**KPIs mostrados:**
1. **Ventas del día:**
   - Número de transacciones
   - Monto total
   - Comparación vs ayer (%)

2. **Ventas del mes:**
   - Número de transacciones
   - Monto total
   - Comparación vs mes anterior (%)

3. **Productos con stock bajo:**
   - Contador
   - Lista de productos
   - Acceso rápido

4. **Top 5 productos vendidos:**
   - Nombre
   - Cantidad vendida
   - Monto generado

**Gráficos:**
- Ventas últimos 7 días (line chart)
- Ventas por categoría (pie chart)

**Widgets adicionales:**
- Últimas 5 ventas
- Productos sin movimiento (últimos 30 días)

**Procesamiento:**
- Queries optimizados con índices
- Cache en Redis (15 minutos)
- Actualización en tiempo real de datos críticos

**Salidas:**
- Dashboard completo con métricas
- Gráficos interactivos
- Acciones rápidas

**Criterios de Aceptación:**
- Tiempo de carga < 2 segundos
- Datos actualizados
- Responsive en todos los dispositivos
- Filtros por rango de fechas

---

#### REQ-FUNC-REP-002: Reporte de Ventas
**Prioridad:** Alta  
**Descripción:** El sistema debe generar reportes detallados de ventas por período.

**Entradas:**
- Rango de fechas (requerido)
- Filtros opcionales: vendedor, método de pago, categoría de producto

**Procesamiento:**
1. Query a tabla sales con joins
2. Agregaciones:
   - Total vendido
   - Número de transacciones
   - Ticket promedio
   - Ventas por día
   - Ventas por producto
   - Ventas por categoría
   - Ventas por vendedor
3. Generación de gráficos

**Salidas:**
- Métricas principales
- Tabla de ventas por día
- Gráfico de tendencia
- Tabla de productos más vendidos
- Tabla de ventas por vendedor
- Opción de exportar a PDF y Excel

**Criterios de Aceptación:**
- Generación en < 5 segundos
- Exportación funcional
- Gráficos claros y profesionales
- Precisión de datos al 100%

---

#### REQ-FUNC-REP-003: Reporte de Inventario
**Prioridad:** Alta  
**Descripción:** El sistema debe generar reporte del estado actual del inventario.

**Procesamiento:**
1. Query a tabla products
2. Cálculos:
   - Valor total de inventario (al costo)
   - Valor total de inventario (al precio venta)
   - Número total de productos
   - Número de productos con stock bajo
   - Productos sin movimiento (últimos 30 días)
3. Agrupación por categoría

**Salidas:**
- Resumen ejecutivo
- Tabla completa de productos con stock
- Valor de inventario
- Productos con stock bajo
- Productos sin movimiento
- Productos más valiosos
- Exportación a Excel

**Criterios de Aceptación:**
- Snapshot en tiempo real
- Valores calculados correctamente
- Exportable
- Tiempo de generación < 3 segundos

---

#### REQ-FUNC-REP-004: Reporte de Clientes
**Prioridad:** Media  
**Descripción:** El sistema debe generar análisis de clientes.

**Procesamiento:**
1. Query a customers con agregaciones
2. Identificar:
   - Top 10 clientes por monto
   - Top 10 clientes por frecuencia
   - Clientes nuevos (período)
   - Clientes inactivos (sin compras en 60 días)
3. Estadísticas generales

**Salidas:**
- Total de clientes
- Clientes activos vs inactivos
- Top clientes
- Clientes nuevos
- Clientes a recuperar
- Promedio de compra por cliente
- Exportación de lista

**Criterios de Aceptación:**
- Análisis útil para marketing
- Segmentación clara
- Exportable

---

### 5.6 Módulo de Predicción con IA

#### REQ-FUNC-AI-001: Generar Predicción de Demanda
**Prioridad:** Alta  
**Descripción:** El sistema debe predecir demanda futura de productos usando ML.

**Requisitos previos:**
- Producto debe tener al menos 30 días de datos históricos
- Mínimo 10 ventas registradas del producto

**Entradas:**
- ID del producto
- Horizonte de predicción (7, 15 o 30 días)

**Procesamiento:**
1. Obtener datos históricos de ventas del producto
2. Preparar datos (agregación diaria)
3. Verificar suficiencia de datos
4. Cargar modelo entrenado (Prophet)
5. Si no existe modelo, entrenarlo
6. Generar predicciones para horizonte especificado
7. Calcular nivel de confianza
8. Guardar predicciones en BD
9. Retornar resultados

**Algoritmo:**
- **Modelo:** Prophet (Meta) para series de tiempo
- **Features:** Fecha, cantidad vendida por día
- **Estacionalidad:** Semanal
- **Validación:** Hold-out (últimos 7 días)

**Salidas:**
- Array de predicciones con:
  - Fecha
  - Cantidad predicha
  - Límite inferior (intervalo de confianza)
  - Límite superior (intervalo de confianza)
  - Nivel de confianza (0-100%)
- Visualización gráfica (histórico + predicción)

**Criterios de Aceptación:**
- Tiempo de predicción < 3 segundos (modelo ya entrenado)
- Precisión > 70% (evaluada con datos de validación)
- Nivel de confianza calculado correctamente
- Mensaje claro si datos insuficientes
- Predicciones guardadas en BD

**Casos especiales:**
- Datos insuficientes: "Este producto no tiene suficientes datos históricos para predicción (mínimo 30 días)"
- Primera predicción: Entrenar modelo (puede tomar 10-15 segundos)

---

#### REQ-FUNC-AI-002: Recomendaciones de Reabastecimiento
**Prioridad:** Alta  
**Descripción:** El sistema debe generar recomendaciones inteligentes de cuándo y cuánto comprar.

**Procesamiento:**
1. Para cada producto activo:
2. Obtener predicción de demanda (próximos 7 días)
3. Obtener stock actual
4. Obtener stock mínimo configurado
5. Calcular:
   - Días de inventario = stock_actual / promedio_demanda_diaria
   - Cantidad necesaria = (predicción_7días + stock_min) - stock_actual
6. Si días_inventario < 7 días, generar recomendación

**Salidas:**
- Lista de productos que necesitan reabastecimiento:
  - Nombre del producto
  - Stock actual
  - Días de inventario restantes
  - Demanda predicha (próximos 7 días)
  - Cantidad recomendada a comprar
  - Urgencia (alta/media/baja)
  - Fecha sugerida de pedido

**Criterios de Aceptación:**
- Recomendaciones precisas basadas en predicciones
- Considera stock mínimo configurado
- Priorización por urgencia
- Actualización diaria automática

---

#### REQ-FUNC-AI-003: Análisis de Tendencias
**Prioridad:** Media  
**Descripción:** El sistema debe identificar tendencias en ventas de productos.

**Procesamiento:**
1. Para cada producto con histórico suficiente
2. Calcular tendencia (creciente/decreciente/estable)
3. Calcular tasa de cambio
4. Identificar estacionalidad
5. Detectar anomalías

**Clasificación de tendencias:**
- **Creciente:** Aumento > 10% en últimos 30 días
- **Decreciente:** Disminución > 10% en últimos 30 días
- **Estable:** Variación entre -10% y +10%

**Salidas:**
- Lista de productos por tendencia:
  - Productos en crecimiento (oportunidad)
  - Productos en decline (riesgo)
  - Productos estables
- Tasa de cambio
- Visualización gráfica

**Criterios de Aceptación:**
- Clasificación precisa
- Útil para decisiones de inventario
- Actualización semanal

---

#### REQ-FUNC-AI-004: Actualización Automática de Predicciones
**Prioridad:** Alta  
**Descripción:** El sistema debe actualizar predicciones automáticamente cada 24 horas.

**Implementación:**
- Tarea programada con Celery Beat
- Ejecución: diaria a medianoche
- Proceso:
  1. Obtener todos los productos activos de todos los tenants
  2. Filtrar productos con datos suficientes
  3. Generar predicciones para cada uno
  4. Guardar en BD
  5. Actualizar modelo si hay nuevos datos significativos

**Criterios de Aceptación:**
- Ejecución automática y confiable
- Manejo de errores robusto
- Logging completo
- No afecta rendimiento del sistema
- Posibilidad de ejecutar manualmente

---

#### REQ-FUNC-AI-005: Evaluación y Mejora del Modelo
**Prioridad:** Media  
**Descripción:** El sistema debe evaluar precisión de predicciones y reentrenar modelos.

**Procesamiento:**
1. Comparar predicciones vs ventas reales
2. Calcular métricas:
   - MAE (Mean Absolute Error)
   - RMSE (Root Mean Squared Error)
   - MAPE (Mean Absolute Percentage Error)
3. Almacenar métricas
4. Si error > umbral, marcar para reentrenamiento

**Salidas:**
- Dashboard de performance del modelo
- Precisión por producto
- Histórico de mejoras
- Alertas de modelo degradado

**Criterios de Aceptación:**
- Evaluación semanal
- Reentrenamiento automático si es necesario
- Métricas accesibles para administradores

---

## 6. Requisitos No Funcionales

### 6.1 Requisitos de Rendimiento

#### REQ-PERF-001: Tiempo de Respuesta API
**Descripción:** Las operaciones CRUD deben completarse rápidamente.

**Especificaciones:**
- Operaciones CRUD simples: < 500ms (p95)
- Consultas con joins: < 1 segundo (p95)
- Generación de reportes: < 5 segundos
- Predicciones IA (modelo entrenado): < 3 segundos
- Carga inicial del dashboard: < 2 segundos

**Medición:**
- Monitoreo con CloudWatch
- Logging de tiempos de respuesta
- Alertas si p95 > umbrales

---

#### REQ-PERF-002: Capacidad de Usuarios Concurrentes
**Descripción:** El sistema debe soportar múltiples usuarios simultáneos.

**Especificaciones:**
- Mínimo 10 usuarios concurrentes por tenant sin degradación
- Sistema global: 100+ usuarios concurrentes (suma de todos los tenants)
- Pool de conexiones a BD: 20 conexiones

**Criterios de Aceptación:**
- Pruebas de carga realizadas
- Sin degradación notable hasta límite especificado
- Escalable horizontalmente si se requiere más capacidad

---

#### REQ-PERF-003: Volumen de Datos
**Descripción:** El sistema debe manejar volúmenes realistas de datos.

**Especificaciones por Tenant:**
- Productos: hasta 10,000
- Clientes: hasta 5,000
- Ventas: hasta 100,000 transacciones/año
- Sale items: hasta 300,000 registros/año

**Criterios de Aceptación:**
- Queries optimizados con índices
- Paginación obligatoria en listados
- Tiempo de respuesta mantenido con volúmenes máximos

---

#### REQ-PERF-004: Throughput
**Descripción:** El sistema debe procesar cantidad adecuada de requests.

**Especificaciones:**
- 100 requests por minuto por usuario
- Backend debe soportar 1000+ requests/minuto globales

**Implementación:**
- Rate limiting por usuario
- Load balancer para distribución

---

### 6.2 Requisitos de Seguridad

#### REQ-SEC-001: Autenticación
**Descripción:** Acceso seguro al sistema.

**Especificaciones:**
- Autenticación basada en JWT
- Tokens con expiración (24 horas)
- HTTPS obligatorio en producción
- Passwords hasheados con bcrypt (cost factor 12)
- Bloqueo temporal tras 5 intentos fallidos (15 minutos)

**Criterios de Aceptación:**
- No se transmiten passwords en claro
- Tokens no almacenados en BD
- Sesión expirada redirige a login

---

#### REQ-SEC-002: Autorización
**Descripción:** Control de acceso basado en roles.

**Especificaciones:**
- RBAC implementado (Admin, Seller, Viewer)
- Permisos verificados en backend (no solo frontend)
- Middleware de autorización en todas las rutas protegidas
- Logging de intentos de acceso no autorizado

**Criterios de Aceptación:**
- 403 Forbidden para accesos no autorizados
- No bypass posible desde frontend
- Auditoría de intentos maliciosos

---

#### REQ-SEC-003: Protección de Datos
**Descripción:** Seguridad de datos sensibles.

**Especificaciones:**
- Encriptación en tránsito (TLS 1.2+)
- Encriptación en reposo (RDS encryption)
- Multi-tenancy: aislamiento total de datos por tenant
- Row-Level Security en PostgreSQL
- Validación de tenant_id en todas las queries

**Criterios de Aceptación:**
- Imposible acceder a datos de otro tenant
- Pruebas de penetración básicas pasadas
- Cumplimiento de OWASP Top 10

---

#### REQ-SEC-004: Validación de Entrada
**Descripción:** Prevención de inyecciones y XSS.

**Especificaciones:**
- Validación con Pydantic en backend
- Sanitización de inputs en frontend
- ORM para prevenir SQL injection
- Escape de HTML en outputs
- CORS configurado restrictivamente

**Criterios de Aceptación:**
- No SQL injection posible
- No XSS posible
- Inputs inválidos rechazados con mensajes claros

---

#### REQ-SEC-005: Auditoría
**Descripción:** Registro de acciones críticas.

**Especificaciones:**
- Tabla audit_logs para acciones críticas
- Logging de:
  - Creación/edición/eliminación de registros
  - Intentos de login (exitosos y fallidos)
  - Cambios de permisos
  - Cancelaciones de ventas
  - Ajustes de inventario
- Incluir: usuario, timestamp, IP, acción, entidad afectada

**Criterios de Aceptación:**
- Logs inmutables
- Retención de logs: 1 año
- Accesible para administradores

---

#### REQ-SEC-006: Backups
**Descripción:** Respaldo de datos para recuperación.

**Especificaciones:**
- Backups automáticos diarios (RDS automated backups)
- Retención: 7 días
- Snapshots manuales semanales
- Retención snapshots: 30 días
- Backups en región diferente (opcional)

**Criterios de Aceptación:**
- Proceso automatizado
- Prueba de restore mensual
- RTO: 4 horas
- RPO: 24 horas

---

### 6.3 Requisitos de Usabilidad

#### REQ-USA-001: Interfaz Intuitiva
**Descripción:** Sistema fácil de usar para usuarios no técnicos.

**Especificaciones:**
- Máximo 3 clics para cualquier funcionalidad común
- Navegación clara con sidebar y breadcrumbs
- Íconos intuitivos para acciones
- Etiquetas claras en español
- Tooltips para funciones no obvias

**Criterios de Aceptación:**
- Usuarios nuevos completan tarea básica sin ayuda (80% éxito)
- Feedback positivo en pruebas de usabilidad

---

#### REQ-USA-002: Responsive Design
**Descripción:** Interfaz adaptable a diferentes dispositivos.

**Especificaciones:**
- Soporte de resoluciones:
  - Desktop: 1920x1080, 1366x768
  - Tablet: 768x1024
  - Móvil: 375x667, 414x896
- Layout adaptativo con CSS Grid/Flexbox
- Botones y links con área táctil adecuada (mínimo 44x44px)

**Criterios de Aceptación:**
- UI funcional en todos los dispositivos
- Pruebas en Chrome, Firefox, Safari, Edge
- Sin scroll horizontal

---

#### REQ-USA-003: Mensajes y Feedback
**Descripción:** Comunicación clara con el usuario.

**Especificaciones:**
- Toasts para confirmaciones y errores
- Loaders durante procesos largos
- Mensajes de error en lenguaje no técnico
- Confirmaciones para acciones destructivas
- Estados vacíos con mensajes guía

**Criterios de Aceptación:**
- Usuario siempre sabe estado del sistema
- Errores claros con sugerencias de solución
- Sin jerga técnica

---

#### REQ-USA-004: Accesibilidad
**Descripción:** Sistema accesible para personas con discapacidades.

**Especificaciones básicas:**
- Contraste de colores adecuado (WCAG AA)
- Navegación por teclado funcional
- Alt text en imágenes
- Labels en formularios
- Tamaño de fuente ajustable

**Criterios de Aceptación:**
- Cumplimiento básico WCAG 2.0 nivel A
- Funcional con screen readers (básico)

---

#### REQ-USA-005: Ayuda y Documentación
**Descripción:** Recursos de ayuda para usuarios.

**Especificaciones:**
- Tooltips contextuales
- Manual de usuario en PDF
- FAQs
- Soporte por email (para piloto)

**Criterios de Aceptación:**
- Manual actualizado y completo
- FAQs cubren dudas comunes

---

### 6.4 Requisitos de Confiabilidad

#### REQ-REL-001: Disponibilidad
**Descripción:** El sistema debe estar disponible la mayor parte del tiempo.

**Especificaciones:**
- Uptime: > 95% (objetivo: 99%)
- Downtime planificado: < 4 horas/mes
- Ventana de mantenimiento: madrugadas (2-6 AM)
- Notificación previa de mantenimientos

**Medición:**
- Monitoring con UptimeRobot
- CloudWatch Alarms
- Status page

---

#### REQ-REL-002: Tolerancia a Fallos
**Descripción:** El sistema debe manejar errores gracefully.

**Especificaciones:**
- Manejo de excepciones en todo el código
- Fallbacks para servicios externos
- Validación de datos en múltiples capas
- Transactions para operaciones críticas
- Rollback automático en caso de error

**Criterios de Aceptación:**
- Sin crashes ante inputs inválidos
- Mensajes de error amigables
- Sistema estable ante carga alta

---

#### REQ-REL-003: Recuperación
**Descripción:** Capacidad de recuperarse de fallos.

**Especificaciones:**
- Auto-restart de servicios en ECS/EC2
- Health checks cada 30 segundos
- Backups automáticos para restauración
- Procedimiento de restore documentado

**Criterios de Aceptación:**
- Servicios se reinician automáticamente
- Datos recuperables en caso de fallo

---

### 6.5 Requisitos de Mantenibilidad

#### REQ-MANT-001: Código Limpio
**Descripción:** Código legible y mantenible.

**Especificaciones:**
- Estándares de código:
  - Backend: PEP 8, Black formatter
  - Frontend: ESLint, Prettier
- Nombres descriptivos de variables y funciones
- Funciones pequeñas (< 50 líneas preferible)
- Comentarios para lógica compleja
- Docstrings en funciones Python

**Criterios de Aceptación:**
- Linters configurados y pasando
- Code reviews obligatorias
- Documentación en código

---

#### REQ-MANT-002: Testing
**Descripción:** Pruebas automatizadas para calidad.

**Especificaciones:**
- Cobertura de tests: mínimo 60% (objetivo: 75%)
- Tipos de tests:
  - Backend: Unit tests, integration tests
  - Frontend: Component tests
- CI/CD ejecuta tests automáticamente
- No merge sin tests pasando

**Criterios de Aceptación:**
- Suite de tests completa
- Tests automáticos en CI/CD
- Coverage reportado

---

#### REQ-MANT-003: Logging
**Descripción:** Logging estructurado para debugging.

**Especificaciones:**
- Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Información incluida: timestamp, user, tenant, acción, resultado
- Centralización con CloudWatch
- Structured logging (JSON)

**Criterios de Aceptación:**
- Logs útiles para debugging
- No información sensible en logs
- Agregación y búsqueda funcional

---

#### REQ-MANT-004: Documentación
**Descripción:** Documentación técnica completa.

**Especificaciones:**
- README.md con instrucciones de setup
- API documentada con OpenAPI/Swagger
- Diagramas de arquitectura actualizados
- Guía de contribución
- Changelog

**Criterios de Aceptación:**
- Nuevo desarrollador puede hacer setup en < 1 hora
- API docs generados automáticamente
- Documentación actualizada

---

#### REQ-MANT-005: Versionamiento
**Descripción:** Control de versiones y releases.

**Especificaciones:**
- Git con GitHub
- Branching strategy: Git Flow o GitHub Flow
- Semantic versioning
- Tags para releases
- Changelog generado

**Criterios de Aceptación:**
- Código versionado
- Releases etiquetados
- Histórico claro

---

### 6.6 Requisitos de Portabilidad

#### REQ-PORT-001: Containerización
**Descripción:** Sistema containerizado para portabilidad.

**Especificaciones:**
- Docker para backend y frontend
- Docker Compose para desarrollo local
- Imágenes en ECR (AWS)
- Multi-stage builds para optimización

**Criterios de Aceptación:**
- Sistema ejecutable en cualquier máquina con Docker
- Entorno dev idéntico a producción

---

#### REQ-PORT-002: Configuración Externa
**Descripción:** Configuración mediante variables de entorno.

**Especificaciones:**
- Todas las configuraciones en .env
- No secrets en código
- 12-factor app methodology
- Configuración diferente por ambiente (dev, staging, prod)

**Criterios de Aceptación:**
- Fácil cambio de configuración
- Sin rebuild para cambiar config

---

### 6.7 Requisitos de Escalabilidad

#### REQ-SCAL-001: Diseño Stateless
**Descripción:** Backend sin estado para escalabilidad horizontal.

**Especificaciones:**
- Sin estado de sesión en servidor (JWT)
- Múltiples instancias posibles
- Load balancer para distribución
- Sessions en Redis (si se requiere)

**Criterios de Aceptación:**
- Posible añadir instancias sin cambios
- Load balancer funcional

---

#### REQ-SCAL-002: Base de Datos
**Descripción:** BD preparada para crecer.

**Especificaciones:**
- Índices en columnas críticas
- Queries optimizados
- Posibilidad de read replicas
- Particionado de tablas grandes (futuro)

**Criterios de Aceptación:**
- Performance mantenido con datos crecientes
- Posibilidad de escalar verticalmente

---

## 7. Otros Requisitos

### 7.1 Requisitos de Internacionalización

**MVP:**
- Solo español
- Formato de fecha: DD/MM/YYYY
- Formato numérico: punto para decimales
- Moneda: según configuración del tenant

**Futuro:**
- Multi-idioma (inglés, portugués)
- Localización de fechas y números

---

### 7.2 Requisitos Legales

#### REQ-LEG-001: Protección de Datos
**Descripción:** Cumplimiento de regulaciones de privacidad.

**Especificaciones:**
- Aviso de privacidad visible
- Consentimiento para uso de datos
- Derecho de acceso a datos
- Derecho de eliminación de datos
- Encriptación de datos personales

---

#### REQ-LEG-002: Términos y Condiciones
**Descripción:** Términos de uso del servicio.

**Especificaciones:**
- Términos y condiciones legales
- Aceptación obligatoria en registro
- Política de uso aceptable
- Limitación de responsabilidad

---

### 7.3 Requisitos de Base de Datos

#### REQ-DB-001: ACID Compliance
**Descripción:** Transacciones ACID para integridad.

**Especificaciones:**
- PostgreSQL con ACID completo
- Transactions para operaciones críticas (ventas)
- Rollback en caso de error
- Isolation level: Read Committed

---

#### REQ-DB-002: Integridad Referencial
**Descripción:** Relaciones consistentes.

**Especificaciones:**
- Foreign keys con restricciones
- Cascadas apropiadas
- Constraints de validación
- Triggers para automatización

---

#### REQ-DB-003: Backups
**Descripción:** Respaldo regular de datos.

(Ver REQ-SEC-006)

---

## 8. Apéndices

### 8.1 Apéndice A: Glosario

Ver Sección 1.3

---

### 8.2 Apéndice B: Modelos de Datos

Ver documento "05-base-de-datos.md" para:
- Diagrama ER completo
- Diccionario de datos detallado
- Definición de todas las tablas

---

### 8.3 Apéndice C: Casos de Uso Detallados

#### UC-001: Realizar una Venta

**Actor Principal:** Vendedor  
**Precondiciones:**
- Usuario autenticado
- Al menos un producto en inventario
- Stock disponible

**Flujo Principal:**
1. Vendedor navega a "Nueva Venta"
2. Sistema muestra formulario de venta
3. Vendedor busca producto
4. Sistema muestra lista de productos coincidentes
5. Vendedor selecciona producto y cantidad
6. Sistema valida stock disponible
7. Sistema añade producto a la venta
8. Sistema muestra subtotal actualizado
9. Vendedor repite pasos 3-8 para más productos (opcional)
10. Vendedor selecciona cliente (opcional)
11. Vendedor selecciona método de pago
12. Vendedor aplica descuento (opcional)
13. Sistema muestra total final
14. Vendedor confirma venta
15. Sistema procesa venta
16. Sistema actualiza stock
17. Sistema genera número de factura
18. Sistema muestra confirmación y opción de imprimir

**Flujos Alternativos:**

**3a. Stock insuficiente:**
1. Sistema muestra mensaje de error
2. Sistema no permite añadir cantidad mayor al stock
3. Retorna a paso 3

**15a. Error al procesar:**
1. Sistema muestra mensaje de error
2. Sistema no actualiza datos
3. Usuario puede reintentar

**Postcondiciones:**
- Venta registrada
- Stock actualizado
- Factura generada
- Estadísticas de cliente actualizadas (si aplica)

---

#### UC-002: Consultar Predicción de Demanda

**Actor Principal:** Administrador  
**Precondiciones:**
- Usuario autenticado como Admin
- Producto tiene datos históricos suficientes

**Flujo Principal:**
1. Admin navega a "Predicciones"
2. Sistema muestra lista de productos
3. Admin selecciona producto
4. Sistema verifica datos suficientes
5. Sistema carga predicción (o genera si no existe)
6. Sistema muestra gráfico con histórico + predicción
7. Sistema muestra tabla de predicciones por día
8. Sistema muestra nivel de confianza
9. Sistema muestra recomendación de reabastecimiento
10. Admin puede ajustar horizonte de predicción
11. Sistema actualiza predicción

**Flujos Alternativos:**

**4a. Datos insuficientes:**
1. Sistema muestra mensaje explicativo
2. Sistema indica requisitos mínimos
3. Termina caso de uso

**5a. Primera predicción:**
1. Sistema indica que está entrenando modelo
2. Sistema muestra loader (10-15 segundos)
3. Sistema genera predicción
4. Continúa en paso 6

**Postcondiciones:**
- Predicción generada y guardada
- Admin tiene información para tomar decisiones

---

### 8.4 Apéndice D: Mockups de Interfaz

(Referencia a diseños en Figma - a crear en Fase 2)

---

### 8.5 Apéndice E: Plan de Pruebas

#### Tipos de Pruebas

**1. Pruebas Unitarias**
- Funciones individuales
- Servicios
- Utilidades
- Cobertura: > 60%

**2. Pruebas de Integración**
- Endpoints API
- Flujos completos
- Integración BD

**3. Pruebas E2E**
- Flujos de usuario completos
- Casos de uso principales

**4. Pruebas de Performance**
- Carga (100 usuarios concurrentes)
- Stress
- Volumen de datos

**5. Pruebas de Seguridad**
- Penetration testing básico
- OWASP Top 10
- Validación de permisos

**6. Pruebas de Usabilidad**
- Con usuarios reales
- Tareas específicas
- Medición de éxito

---

### 8.6 Apéndice F: Riesgos del Proyecto

Ver documento "01-alcance-mvp.md" sección 7

---

### 8.7 Apéndice G: Cronograma

Ver documento "03-cronograma.md"

---

### 8.8 Apéndice H: Stack Tecnológico

Ver documento "04-arquitectura-tecnica.md" (decisiones tecnológicas y stack base)

---

### 8.9 Apéndice I: Arquitectura del Sistema

Ver documento "04-arquitectura-tecnica.md"

---

## Aprobación

| Rol | Nombre | Firma | Fecha |
|-----|--------|-------|-------|
| Equipo de Desarrollo | [Nombres] | | |
| Asesor Académico | [Nombre] | | |
| Revisor Técnico | [Nombre] | | |

---

**Fin del Documento**

---

**Elaborado por:** Equipo OrbitEngine  
**Fecha:** Octubre 2025  
**Versión:** 1.0  
**Estado:** Borrador para Revisión
