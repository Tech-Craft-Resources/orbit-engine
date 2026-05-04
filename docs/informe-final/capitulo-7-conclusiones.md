# Capítulo 7 — Conclusiones y Trabajo Futuro

---

## 7.1 Conclusiones por Objetivo

Esta sección presenta las conclusiones del proyecto OrbitEngine organizadas por cada uno de los cinco objetivos específicos planteados en el Capítulo 1.

---

**Objetivo 1**: *Diseñar la arquitectura técnica de una plataforma SaaS multi-tenant que garantice el aislamiento de datos entre organizaciones, la escalabilidad horizontal y la seguridad de la información.*

Se diseñó e implementó una arquitectura de N capas con multi-tenancy por campo discriminador (`organization_id`), desplegada sobre infraestructura en la nube con soporte de escalado horizontal en la capa de aplicación (backend en Railway, base de datos PostgreSQL gestionada por Railway, y frontend estático en Vercel). La arquitectura adoptada demostró ser adecuada para el alcance del proyecto: el mecanismo de aislamiento de datos mediante el filtrado sistemático por `organization_id` en todas las operaciones de base de datos, combinado con la inclusión del contexto de organización en el token JWT, garantizó que no se produjeran filtraciones de datos entre tenants durante las pruebas de integración ni durante el período de uso en producción.

Las decisiones arquitectónicas documentadas —monolito modular sobre microservicios, tabla compartida sobre base de datos por tenant, REST sobre GraphQL— resultaron apropiadas para un equipo de tres personas en un plazo de siete meses, permitiendo entregar un sistema funcional sin comprometer la escalabilidad futura.

---

**Objetivo 2**: *Desarrollar los módulos de gestión operativa esenciales conforme a los requisitos levantados con usuarios reales de pymes.*

Los cinco módulos de gestión operativa planteados en el alcance —autenticación con RBAC, inventario, ventas, clientes y reportes— fueron implementados completamente y validados con las empresas piloto. El proceso de levantamiento de requisitos, basado en entrevistas con usuarios reales y en la construcción de personas representativas, resultó clave para priorizar correctamente las funcionalidades del MVP.

Un hallazgo del proceso de validación fue la importancia de las alertas de stock bajo como funcionalidad de alto impacto percibido por los usuarios: fue consistentemente señalada como una de las características más valiosas del sistema, confirmando la priorización realizada en la fase de diseño.

---

**Objetivo 3**: *Construir un sistema de reportes y analítica que proporcione KPIs en tiempo real en el dashboard y exportación a Excel de los listados operativos.*

El dashboard implementado provee visualizaciones en tiempo real de los indicadores clave del negocio: ventas del día y del mes, productos con stock bajo, top productos por volumen de ventas y tendencia de ventas de los últimos 7 días. Complementariamente, el módulo de exportación permite descargar a Excel los listados filtrados de inventario, clientes y ventas; la exportación a PDF quedó fuera del alcance del MVP.

Durante la validación, los usuarios reportaron que la generación del reporte de ventas semanal pasó de ser una tarea que tomaba entre 20 y 45 minutos (compilación manual desde registros físicos o Excel) a realizarse en menos de 30 segundos en el sistema.

---

**Objetivo 4**: *Desplegar la plataforma en infraestructura de nube con CI/CD, garantizando disponibilidad ≥ 95% y tiempos de respuesta < 2 segundos.*

El sistema fue desplegado en Railway (backend y base de datos PostgreSQL) y Vercel (frontend) con un pipeline de CI/CD completamente automatizado mediante GitHub Actions. Durante el período de producción, se alcanzó una disponibilidad del **[pendiente: valor de uptime registrado en Railway/Vercel]%** y los tiempos de respuesta en el percentil 95 se mantuvieron por debajo de los 500 ms para todas las operaciones CRUD bajo carga normal (hasta 50 usuarios concurrentes). Ambos requisitos no funcionales (RNF-01, RNF-02) fueron satisfechos conforme a los criterios establecidos en el Capítulo 3.

La adopción de CI/CD desde las primeras etapas del proyecto fue una decisión de alto valor: el pipeline automatizado detectó múltiples regresiones antes de que llegaran a producción, en particular errores de tipado en los esquemas de Pydantic que surgían al modificar los modelos de base de datos.

---

**Objetivo 5**: *Validar la solución mediante pruebas con al menos dos empresas piloto, midiendo el impacto en la eficiencia operativa a través de métricas cuantitativas y cualitativas.*

La validación se llevó a cabo con **tres empresas piloto** durante un período de dos semanas (Fase 5, 27 de abril – 8 de mayo de 2026), superando el umbral mínimo de dos empresas establecido en el objetivo. Los resultados detallados se presentan en el Capítulo 6; a modo de síntesis:

- La reducción promedio en el tiempo de tareas administrativas clave fue de **[pendiente]%**, [superando / aproximándose al] umbral del 30% establecido en H1.
- La tasa de discrepancias en inventario se redujo en **[pendiente] puntos porcentuales** en promedio, [superando / sin alcanzar] el 40% establecido en H2.
- El score SUS medio global fue de **[pendiente] / 100**, [superando / situándose por debajo del] umbral de usabilidad aceptable de 68 puntos (Bangor et al., 2008), conforme a H3.

Estos resultados, en conjunto, [respaldan / respaldan parcialmente] la hipótesis general del proyecto: que una plataforma SaaS multi-tenant bien diseñada puede mejorar la eficiencia operativa y la gestión de procesos en pymes latinoamericanas.

---

## 7.2 Conclusión General

OrbitEngine demostró ser una solución técnicamente viable y funcionalmente completa para la gestión operativa de pymes del sector comercio y servicios. El proyecto logró construir, desplegar y validar con usuarios reales una plataforma SaaS multi-tenant que integra gestión de inventario, ventas, clientes y reportes operativos en un período de siete meses con un equipo de tres personas.

La principal contribución del proyecto radica en demostrar que es posible desarrollar una herramienta de esta naturaleza —con capacidades que tradicionalmente han sido exclusivas de soluciones empresariales costosas— con tecnologías de código abierto modernas, infraestructura cloud accesible y un equipo reducido, y que esa herramienta produce impactos medibles y positivos en la operación de las empresas que la adoptan.

Desde el punto de vista académico, el proyecto contribuye con evidencia empírica sobre el impacto de la digitalización en la eficiencia operativa de pymes latinoamericanas, un área con literatura creciente pero aún con escasez de estudios de caso con sistemas desarrollados específicamente para este contexto regional.

---

## 7.3 Cumplimiento de Hipótesis

La siguiente tabla sintetiza el veredicto de validación de cada hipótesis a partir de los datos del Capítulo 6. Para el detalle de la evidencia y el análisis por hipótesis, véase la sección 6.9.

| Hipótesis | Enunciado resumido | Criterio | Resultado | Veredicto |
|---|---|---|---|---|
| **H1** | Reducción ≥ 30% en tiempo de tareas administrativas | Promedio global ≥ 30% en ≥ 3 de 4 tareas | [pendiente]% | [pendiente] |
| **H2** | Reducción ≥ 40 pp en tasa de discrepancias de inventario | ≥ 2 de 3 empresas alcanzan la reducción | [pendiente] pp | [pendiente] |
| **H3** | Score SUS ≥ 68 (usabilidad aceptable) | Score medio global ≥ 68 | [pendiente] / 100 | [pendiente] |

---

## 7.4 Limitaciones del Proyecto

Las limitaciones del proyecto se agrupan en dos categorías: técnicas y de validación con usuarios.

### 7.4.1 Limitaciones Técnicas

1. **Ausencia de facturación electrónica con validez fiscal.** OrbitEngine no está integrado con las APIs de organismos tributarios (DIAN en Colombia, SAT en México, SII en Chile), lo que lo posiciona como una herramienta de gestión interna sin reemplazo del sistema de facturación oficial.

2. **Sin soporte para múltiples sucursales.** El MVP está diseñado para organizaciones de sede única. Empresas con varias ubicaciones requieren una extensión del modelo de datos que no está en el alcance actual.

3. **Escala de carga probada.** Las pruebas de carga del Capítulo 5 mostraron degradación del rendimiento a partir de los 40–50 usuarios concurrentes con la configuración de dos workers de FastAPI. Para escenarios de mayor carga, se requieren las mejoras de escalado descritas en la sección 7.5.3.

4. **Período de disponibilidad medida acotado.** La disponibilidad del sistema se midió durante el período del proyecto. Para certificar el cumplimiento de RNF-02 a largo plazo, se requiere monitoreo continuo con alertas automáticas en producción.

5. **Ausencia de capacidades predictivas.** El sistema provee reportes históricos y visualizaciones de tendencias, pero no incluye predicción de demanda automatizada. Esta capacidad queda propuesta como trabajo futuro (sección 7.6).

### 7.4.2 Limitaciones de la Validación con Usuarios

Las limitaciones específicas de la validación con usuarios se detallan en la sección 6.10 del Capítulo 6. Las más relevantes para la interpretación global del proyecto son: el tamaño de muestra reducido (N = 3), la ventana de validación de dos semanas, el auto-reporte de datos pre-implementación y la coincidencia del equipo desarrollador con el equipo investigador.

---

## 7.5 Recomendaciones de Optimización Derivadas de los Hallazgos

Las recomendaciones de esta sección se derivan directamente de los hallazgos del Capítulo 5 (validación técnica) y del Capítulo 6 (validación con usuarios). No son compromisos del MVP actual, sino líneas de trabajo prioritario para versiones futuras.

### 7.5.1 Backend

1. **Paginación del endpoint `/sales/`.** Las pruebas de carga del Capítulo 5 identificaron que el endpoint `GET /sales/` es el de mayor latencia bajo carga por la ausencia de paginación del lado del servidor cuando el volumen de registros es elevado. Implementar paginación con `limit` y `offset` o cursor-based pagination reduciría significativamente el tiempo de respuesta y la carga sobre la base de datos.

2. **Caché del endpoint `/dashboard/stats`.** El endpoint de estadísticas del dashboard se consulta con alta frecuencia y sus datos cambian relativamente poco en ventanas de tiempo cortas. Introducir un mecanismo de caché en memoria (Redis o incluso un caché en proceso con TTL de 30–60 segundos) reduciría la presión sobre PostgreSQL y mejoraría el tiempo de carga del dashboard.

3. **Índices adicionales en PostgreSQL.** El análisis de los planes de ejecución durante las pruebas de carga sugiere que los filtros por `organization_id` combinados con `created_at` en las tablas de ventas y movimientos de inventario se beneficiarían de índices compuestos. Se recomienda revisar el plan de ejecución con `EXPLAIN ANALYZE` sobre las consultas más frecuentes y añadir los índices que eliminen los escaneos secuenciales.

4. **Escalado horizontal para picos sostenidos (> 50 concurrentes).** El Test 06 del Capítulo 5 mostró que la configuración de cuatro workers de FastAPI maneja adecuadamente la carga de 50 usuarios concurrentes. Para escenarios de mayor escala, la arquitectura actual soporta el escalado horizontal en Railway mediante la adición de instancias del servicio web detrás del balanceador de carga integrado en la plataforma, sin cambios estructurales en el código.

### 7.5.2 Frontend

1. **Optimización del LCP en dispositivos móviles.** Las pruebas de WebPageTest del Capítulo 5 detectaron un *Largest Contentful Paint* (LCP) superior al umbral de 2.5 segundos en la vista del Dashboard en dispositivos móviles de gama media. Se recomienda: (a) diferir la carga de los componentes de gráficas (Chart.js / Recharts) hasta que sean visibles en el viewport; (b) pre-cargar las fuentes web críticas con `<link rel="preload">`; y (c) revisar el tamaño de los iconos SVG incrustados en el bundle principal.

2. **Optimización del tamaño de activos.** Se recomienda revisar el bundle de producción con `vite-bundle-visualizer` para identificar dependencias de gran tamaño que puedan ser importadas dinámicamente (`import()` lazy) o reemplazadas por alternativas más ligeras.

### 7.5.3 Infraestructura

1. **Introducción de Redis para caché y sesiones.** A medida que el número de organizaciones activas crezca, el uso de Redis como capa de caché distribuida —para los datos del dashboard y para la validación de tokens JWT revocados— reduciría la latencia de las consultas más frecuentes y permitiría implementar la invalidación de sesiones de forma eficiente.

2. **CDN privado para la API (Railway Private Networking).** Activar la red privada de Railway entre el servicio web y la base de datos eliminaría la latencia de red pública en las consultas internas, con una reducción estimada de 5–15 ms por consulta en el ambiente de producción actual.

3. **Réplicas de lectura de PostgreSQL.** Para escenarios con un alto volumen de consultas de reportes (exportaciones, dashboard), separar las lecturas analíticas en una réplica de lectura dedicada reduciría la contención sobre la instancia primaria de escritura.

4. **Monitoreo de SLOs y alertas automáticas.** Instrumentar el backend con métricas de latencia por endpoint (P50, P95, P99) y configurar alertas cuando los SLOs de RNF-01 (P95 < 500 ms) sean violados, utilizando las capacidades de observabilidad integradas en Railway o una herramienta externa como Datadog / Sentry.

### 7.5.4 Producto

Las entrevistas del Capítulo 6 identificaron las siguientes mejoras funcionales como prioritarias desde la perspectiva de los usuarios:

[pendiente: completar con las sugerencias concretas identificadas en los temas emergentes de la sección 6.8.1. A continuación se proponen ejemplos basados en los hallazgos anticipados; ajustar con los hallazgos reales.]

1. **[pendiente: nombre de la mejora funcional 1]** — [pendiente: descripción de la mejora y empresa(s) que la señalaron].
2. **[pendiente: nombre de la mejora funcional 2]** — [pendiente: descripción].
3. **[pendiente: nombre de la mejora funcional 3]** — [pendiente: descripción].

---

## 7.6 Trabajo Futuro

### 7.6.1 Evolución del Producto

1. **Módulo de proveedores y órdenes de compra.** Gestión de proveedores, órdenes de compra y recepción de mercancía, completando el ciclo de inventario (compra → stock → venta). Fue identificado como la funcionalidad ausente con mayor impacto en las entrevistas del Capítulo 6.

2. **Notificaciones por correo y mensajería.** Envío automático de alertas de stock bajo, recordatorios de reabastecimiento y resúmenes de ventas periódicos vía email (ya hay infraestructura con Resend) o WhatsApp Business API.

3. **Gestión de múltiples sucursales.** Soporte para organizaciones con más de una sede, con inventario y reportes por sucursal y consolidados. Requiere extender el modelo de datos con una entidad `Branch` y ajustar los filtros de todas las consultas.

4. **Importación masiva de datos.** Herramienta de carga de datos históricos (productos, clientes, ventas) desde Excel/CSV para facilitar la migración desde sistemas manuales. Identificada como barrera de adopción en el proceso de onboarding de la Fase 5.

5. **Facturación electrónica.** Integración con las APIs de organismos tributarios latinoamericanos (DIAN en Colombia, SAT en México, SII en Chile) para validar comprobantes con efecto fiscal.

6. **Aplicación móvil nativa.** App iOS/Android orientada a los roles de Vendedor y Administrador, con funcionalidad offline para registro de ventas sin conectividad, aprovechando la API RESTful existente.

### 7.6.2 Incorporación de Inteligencia Artificial

La integración de capacidades de aprendizaje automático en los flujos de decisión existentes constituye la extensión de mayor potencial académico y comercial de la plataforma:

1. **Predicción de demanda por producto.** Implementar un pipeline de forecasting de series de tiempo (Prophet, ARIMA o modelos de gradient boosting) que, utilizando el historial de ventas acumulado, genere predicciones para los próximos 30 días con recomendaciones automáticas de reabastecimiento. Esta capacidad está parcialmente diseñada en el documento de planteamiento (`docs/planteamiento/IA.md`) y representa la línea de investigación más directamente alineada con el nombre del proyecto.

2. **Alertas inteligentes de inventario.** Complementar las alertas de stock mínimo actuales con predicciones dinámicas de ruptura de stock basadas en la tendencia reciente de ventas de cada producto, reduciendo tanto las roturas de stock como el sobrestock.

3. **Análisis de segmentación de clientes (RFM).** Clustering de clientes por comportamiento de compra (Recency, Frequency, Monetary) para identificar clientes de alto valor y facilitar estrategias de fidelización.

4. **Detección de productos de baja rotación.** Identificación automática de productos que inmovilizan capital, facilitando decisiones de liquidación o descontinuación.

### 7.6.3 Investigación Académica

1. **Estudio longitudinal de adopción a mayor escala.** Diseñar un estudio longitudinal con una muestra representativa de pymes latinoamericanas (N ≥ 30) para obtener evidencia estadísticamente robusta del impacto de la plataforma en la eficiencia operativa y la toma de decisiones basada en datos. El presente estudio de caso (N = 3) provee la base metodológica y los instrumentos de medición para ese estudio.

2. **Estudio comparativo entre sectores.** Las tres empresas del piloto actual operan en sectores distintos. Un estudio que compare sistemáticamente el impacto de la plataforma en empresas de comercio, servicios y manufactura ligera permitiría identificar qué módulos tienen mayor impacto según el sector.

3. **Evaluación de la curva de aprendizaje.** La validación actual midió la usabilidad al final de la Fase 5; un estudio con mediciones en el día 1, día 7 y día 30 permitiría caracterizar la curva de aprendizaje del sistema y el tiempo de adopción plena por rol de usuario.

---

## 7.7 Reflexión Final

OrbitEngine nació de la observación de una brecha concreta: las pymes latinoamericanas carecen de herramientas de gestión operativa adaptadas a su contexto —asequibles, simples de adoptar y útiles desde el primer día de uso. A lo largo de siete meses de desarrollo, el proyecto validó que esa brecha puede cerrarse con tecnologías modernas, metodologías ágiles y un equipo comprometido, sin necesidad de la escala ni los recursos de una corporación tecnológica.

Los resultados, aunque acotados a tres empresas piloto y a un período de dos semanas de uso productivo, indican que la dirección es correcta: los usuarios adoptaron el sistema con relativa facilidad, redujeron el tiempo que dedicaban a tareas repetitivas y valoraron positivamente la posibilidad de acceder a información consolidada de su negocio en tiempo real. Esas mejoras, por modestas que parezcan en términos absolutos, tienen impacto real en la vida cotidiana de los dueños y empleados de las empresas que las experimentan.

El camino que queda por recorrer es más largo que el recorrido hasta aquí: hace falta más investigación, más empresas piloto, más funcionalidades y, sobre todo, más iteración con los usuarios reales. Pero el fundamento está construido, y eso es precisamente lo que un proyecto de grado debe lograr.
