# Documento de Alcance del Proyecto
## Pecesaurio - Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Equipo:** 3 Integrantes  
**Fecha de inicio:** Noviembre 2024  
**Fecha de entrega:** Abril 2025  

---

## 1. Resumen Ejecutivo

Pecesaurio es una plataforma SaaS diseñada para digitalizar y optimizar los procesos internos de pequeñas y medianas empresas (pymes). El proyecto busca ofrecer una solución accesible, modular y potenciada con Inteligencia Artificial que permita a las pymes gestionar sus operaciones de manera centralizada, mejorando su eficiencia operativa y competitividad.

---

## 2. Alcance del Proyecto

### 2.1 En Alcance (In Scope)

#### Módulos Principales
1. **Módulo de Autenticación y Usuarios**
   - Registro e inicio de sesión de usuarios
   - Gestión de roles (Administrador, Vendedor, Visualizador)
   - Autenticación segura con JWT
   - Recuperación de contraseñas

2. **Módulo de Gestión de Inventario**
   - CRUD completo de productos
   - Categorización de productos
   - Control de stock (cantidad actual, mínimos, máximos)
   - Alertas de stock bajo
   - Historial de movimientos de inventario

3. **Módulo de Gestión de Ventas**
   - Registro de ventas
   - Generación de facturas básicas
   - Historial de transacciones
   - Dashboard de ventas con métricas básicas
   - Búsqueda y filtrado de ventas

4. **Módulo de Gestión de Clientes**
   - CRUD de clientes
   - Historial de compras por cliente
   - Información de contacto
   - Segmentación básica de clientes

5. **Módulo de Reportes y Análisis**
   - Dashboard principal con KPIs
   - Reportes de ventas (diario, semanal, mensual)
   - Reportes de inventario
   - Exportación de reportes (PDF, Excel)

6. **Funcionalidad de IA - Predicción de Demanda** (MVP Simplificado)
   - Análisis de tendencias históricas de ventas
   - Predicción simple de demanda basada en datos históricos
   - Recomendaciones de reabastecimiento
   - Visualización de predicciones

#### Características Técnicas
- Arquitectura SaaS multi-tenant (un tenant por empresa)
- API RESTful documentada
- Interfaz web responsive
- Despliegue en AWS
- Base de datos relacional
- Sistema de logging y monitoreo básico
- Pruebas unitarias y de integración (cobertura mínima 60%)

### 2.2 Fuera de Alcance (Out of Scope)

Las siguientes características NO serán implementadas en el MVP pero pueden considerarse para versiones futuras:

1. **Características Avanzadas**
   - Aplicación móvil nativa
   - Integración con pasarelas de pago
   - Sistema de punto de venta (POS) físico
   - Gestión de múltiples bodegas/sucursales
   - Contabilidad completa
   - Gestión de nómina
   - Sistema de facturación electrónica oficial

2. **IA Avanzada**
   - Chatbot con IA conversacional
   - Análisis de sentimientos de clientes
   - Optimización dinámica de precios
   - Detección de fraudes

3. **Integraciones Externas**
   - Integración con ERP existentes
   - Sincronización con marketplaces (Amazon, MercadoLibre)
   - Integración con redes sociales
   - APIs de terceros para logística

4. **Características Empresariales**
   - Marketplace de aplicaciones/plugins
   - Personalización white-label
   - Multi-idioma
   - Multi-moneda

---

## 3. Definición del MVP (Minimum Viable Product)

### 3.1 Objetivo del MVP

Desarrollar una plataforma funcional que permita a una pyme realizar las operaciones básicas de gestión de inventario, ventas y clientes, con un componente de IA que demuestre valor agregado mediante predicción de demanda.

### 3.2 Funcionalidades Críticas del MVP

#### Prioridad 1 (Crítica - Debe estar en MVP)
- ✅ Autenticación y autorización de usuarios
- ✅ CRUD de productos con control de stock
- ✅ Registro y consulta de ventas
- ✅ CRUD de clientes básico
- ✅ Dashboard con métricas principales
- ✅ Alertas de stock bajo
- ✅ API RESTful funcional

#### Prioridad 2 (Alta - Deseable en MVP)
- ⭐ Predicción de demanda con IA (simplificado)
- ⭐ Generación de reportes básicos
- ⭐ Exportación de datos
- ⭐ Historial de movimientos
- ⭐ Búsqueda y filtros avanzados

#### Prioridad 3 (Media - Post-MVP)
- 🔄 Gestión de categorías personalizadas
- 🔄 Notificaciones por email
- 🔄 Mejoras en visualizaciones
- 🔄 Optimización de rendimiento avanzada
- 🔄 Auditoría completa de cambios

### 3.3 Criterios de Aceptación del MVP

El MVP se considerará completo cuando:

1. **Funcionalidad:** Todos los módulos de Prioridad 1 estén implementados y funcionando
2. **Usabilidad:** La interfaz sea intuitiva y responsive
3. **Rendimiento:** Tiempo de respuesta < 2 segundos para operaciones CRUD
4. **Estabilidad:** Sin errores críticos que impidan el uso normal
5. **Seguridad:** Autenticación segura y validación de datos implementada
6. **IA Funcional:** Modelo de predicción de demanda operativo con visualizaciones
7. **Documentación:** API documentada y código con documentación técnica
8. **Pruebas:** Cobertura de pruebas mínima del 60%
9. **Despliegue:** Sistema desplegado en AWS y accesible vía web

---

## 4. Módulos Adicionales Interesantes (Post-MVP)

### 4.1 Módulo de Proveedores
- Gestión de proveedores
- Órdenes de compra
- Control de pagos a proveedores
- Evaluación de proveedores

### 4.2 Módulo de Empleados y Roles Avanzados
- Gestión de empleados
- Roles y permisos granulares
- Seguimiento de actividades por usuario
- Asignación de metas de ventas

### 4.3 Módulo de Marketing
- Campañas promocionales
- Segmentación de clientes
- Email marketing básico
- Análisis de efectividad de campañas

### 4.4 Módulo de Análisis Avanzado con IA
- Detección de productos de baja rotación
- Análisis de patrones de compra
- Recomendaciones personalizadas a clientes
- Predicción de churn de clientes

### 4.5 Módulo de Finanzas Básico
- Control de gastos
- Flujo de caja
- Cuentas por cobrar/pagar
- Reportes financieros básicos

### 4.6 Módulo de Integraciones
- Webhook system para integraciones
- API pública para terceros
- Exportación/importación masiva de datos
- Integración con servicios de mensajería (WhatsApp Business API)

---

## 5. Métricas de Éxito

### 5.1 Métricas Técnicas

#### Rendimiento
- **Tiempo de respuesta promedio:** < 500ms para consultas simples
- **Tiempo de respuesta de IA:** < 3 segundos para predicciones
- **Disponibilidad del sistema:** > 95% uptime
- **Capacidad:** Soportar al menos 10 tenants concurrentes sin degradación

#### Calidad de Código
- **Cobertura de pruebas:** Mínimo 60% (objetivo 75%)
- **Deuda técnica:** < 10% según análisis de SonarQube
- **Errores críticos en producción:** 0
- **Errores menores:** < 5 por sprint

#### Seguridad
- **Vulnerabilidades críticas:** 0
- **Implementación de OWASP Top 10:** 100%
- **Encriptación de datos sensibles:** Implementada
- **Backups automatizados:** Diarios

### 5.2 Métricas de Producto

#### Funcionalidad
- **Módulos completados:** 6/6 del alcance MVP
- **Historias de usuario completadas:** 100% de las críticas, 80% de las deseables
- **Funcionalidad de IA operativa:** Predicción con precisión > 70%

#### Usabilidad
- **Tasks completadas exitosamente en pruebas de usuario:** > 85%
- **Tiempo promedio para completar operación básica:** < 30 segundos
- **Calificación de satisfacción (escala 1-5):** > 4.0
- **Tasa de errores de usuario:** < 10%

### 5.3 Métricas de Validación Académica

#### Hipótesis Principal
**"Una plataforma SaaS modular con IA mejora significativamente la eficiencia operativa de las pymes"**

**Medición:**
- Reducción de tiempo en tareas administrativas: > 30%
- Reducción de errores en inventario: > 40%
- Mejora en precisión de predicción vs. estimación manual: > 25%

#### Métricas de Validación Empírica
- **Empresas piloto:** Mínimo 2 pymes participantes
- **Período de prueba:** 3-4 semanas por empresa
- **Datos recolectados:**
  - Tiempo en tareas antes/después
  - Número de errores antes/después
  - Satisfacción del usuario (encuestas pre/post)
  - Precisión de predicciones vs. realidad

### 5.4 Métricas del Proyecto

#### Gestión de Proyecto
- **Cumplimiento de sprints:** > 85% de tareas completadas
- **Desviación de cronograma:** < 10%
- **Presupuesto AWS:** < $50/mes durante desarrollo
- **Reuniones del equipo:** Semanales (100% asistencia)

#### Entregables Académicos
- ✅ Documento de propuesta completo
- ✅ Documento de requisitos y arquitectura
- ✅ Código fuente en repositorio con commits regulares
- ✅ Documentación técnica completa
- ✅ Informe de pruebas y validación
- ✅ Presentación final y defensa
- ✅ Paper/artículo académico (opcional)

---

## 6. Criterios de Éxito del Proyecto

### Éxito Técnico
- ✅ Sistema desplegado y funcional en AWS
- ✅ Todos los módulos MVP operativos
- ✅ Modelo de IA integrado y funcionando
- ✅ Documentación técnica completa
- ✅ Pruebas automatizadas implementadas

### Éxito Académico
- ✅ Defensa del proyecto aprobada
- ✅ Validación empírica con datos reales
- ✅ Hipótesis validadas con evidencia cuantitativa
- ✅ Contribución al conocimiento en el área

### Éxito de Producto
- ✅ Al menos 2 pymes pueden usar el sistema exitosamente
- ✅ Usuarios completan tareas sin requerir soporte extenso
- ✅ Predicciones de IA tienen precisión aceptable (>70%)
- ✅ Feedback positivo de usuarios (>4/5)

---

## 7. Riesgos y Mitigación

### Riesgos Técnicos
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Complejidad del modelo de IA | Media | Alto | Empezar con modelos simples (ARIMA, regresión), escalar si es necesario |
| Problemas de rendimiento | Baja | Medio | Pruebas de carga tempranas, optimización continua |
| Seguridad de datos | Media | Alto | Implementar mejores prácticas desde el inicio, auditorías |
| Costos de AWS excesivos | Media | Medio | Monitoreo de costos, uso de free tier, optimización |

### Riesgos de Proyecto
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Sobrecarga académica del equipo | Alta | Alto | Planificación realista, buffer en cronograma |
| Alcance demasiado ambicioso | Media | Alto | MVP bien definido, priorización estricta |
| Dificultad para conseguir pymes piloto | Media | Medio | Empezar búsqueda temprano, datos sintéticos como backup |
| Falta de sincronización del equipo | Baja | Alto | Daily standups, uso de herramientas colaborativas |

### Riesgos de Validación
| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Datos insuficientes para IA | Media | Alto | Generación de datos sintéticos realistas |
| Pymes no completan período de prueba | Media | Medio | Incentivos, seguimiento cercano, soporte activo |
| Resultados no validan hipótesis | Baja | Medio | Múltiples métricas, análisis cualitativo adicional |

---

## 8. Supuestos y Dependencias

### Supuestos
1. El equipo tiene acceso a infraestructura AWS (o créditos educativos)
2. Se conseguirán al menos 2 pymes para pruebas piloto
3. Las pymes tienen datos históricos de al menos 3-6 meses
4. El equipo tiene conocimientos básicos de desarrollo web y ML
5. Se dispone de 15-20 horas semanales por integrante

### Dependencias
1. Acceso a servicios cloud (AWS)
2. Herramientas de desarrollo (IDEs, repositorios)
3. Disponibilidad de bibliotecas de ML de código abierto
4. Aprobación de propuesta por parte de la universidad
5. Coordinación con asesor académico

---

## 9. Fases del Proyecto

### Fase 1: Investigación y Diseño (Noviembre 2024)
- Revisión de literatura y estado del arte
- Levantamiento de requisitos
- Diseño de arquitectura
- Diseño de base de datos
- Selección de stack tecnológico

### Fase 2: Desarrollo Core (Diciembre 2024 - Enero 2025)
- Setup de infraestructura
- Módulo de autenticación
- Módulo de inventario
- Módulo de ventas
- Módulo de clientes

### Fase 3: Desarrollo Avanzado (Febrero 2025)
- Módulo de reportes
- Integración de IA para predicción
- Dashboard y visualizaciones
- Testing y debugging

### Fase 4: Validación y Refinamiento (Marzo 2025)
- Despliegue en producción
- Pruebas con usuarios reales
- Recolección de métricas
- Ajustes y mejoras

### Fase 5: Documentación y Cierre (Abril 2025)
- Documentación final
- Análisis de resultados
- Preparación de presentación
- Defensa del proyecto

---

## 10. Entregables Finales

### Entregables Técnicos
1. Código fuente completo en repositorio (GitHub)
2. Aplicación desplegada en AWS
3. Documentación técnica completa (API, arquitectura, instalación)
4. Suite de pruebas automatizadas
5. Scripts de despliegue (IaC)

### Entregables Académicos
1. Documento de proyecto de grado completo
2. Presentación de defensa
3. Video demo de la plataforma
4. Informe de validación con datos y análisis
5. Manual de usuario

### Entregables de Validación
1. Resultados de pruebas con usuarios
2. Métricas de rendimiento y usabilidad
3. Análisis de precisión del modelo de IA
4. Comparativa antes/después en pymes piloto
5. Conclusiones y recomendaciones

---

## Conclusión

Este documento establece un alcance realista y alcanzable para el proyecto Pecesaurio, considerando un equipo de 3 personas y un timeline de 6 meses. El enfoque en el MVP asegura que se entregará un producto funcional que valide las hipótesis planteadas, con una base sólida para futuras expansiones.

**Fecha de elaboración:** Octubre 2024  
**Versión:** 1.0

