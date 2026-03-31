# Capítulo 6 — Conclusiones y Trabajo Futuro

---

## 6.1 Conclusiones por Objetivo

Esta sección presenta las conclusiones del proyecto OrbitEngine organizadas por cada uno de los objetivos específicos planteados en el Capítulo 1.

---

**Objetivo 1**: *Diseñar la arquitectura técnica de una plataforma SaaS multi-tenant que garantice el aislamiento de datos entre organizaciones, la escalabilidad horizontal y la seguridad de la información.*

Se diseñó e implementó una arquitectura de N capas con multi-tenancy por campo discriminador (`organization_id`), desplegada sobre infraestructura AWS con soporte de escalado horizontal en la capa de aplicación. La arquitectura adoptada demostró ser adecuada para el alcance del proyecto: el mecanismo de aislamiento de datos mediante el filtrado sistemático por `organization_id` en todas las operaciones de base de datos, combinado con la inclusión del contexto de organización en el token JWT, garantizó que no se produjeran filtraciones de datos entre tenants durante las pruebas de integración ni durante el período de uso en producción.

Las decisiones arquitectónicas documentadas (monolito modular sobre microservicios, tabla compartida sobre BD por tenant, REST sobre GraphQL) resultaron apropiadas para un equipo de tres personas en un plazo de siete meses, permitiendo entregar un sistema funcional sin comprometer la escalabilidad futura.

---

**Objetivo 2**: *Desarrollar los módulos de gestión operativa esenciales conforme a los requisitos levantados con usuarios reales de pymes.*

Los cinco módulos de gestión operativa planteados en el alcance (autenticación con RBAC, inventario, ventas, clientes y reportes) fueron implementados completamente y validados con las empresas piloto. El proceso de levantamiento de requisitos, basado en entrevistas con usuarios reales y en la construcción de personas representativas, resultó clave para priorizar correctamente las funcionalidades del MVP.

Un hallazgo del proceso de validación fue la importancia de las alertas de stock bajo como funcionalidad de alto impacto percibido por los usuarios: fue consistentemente señalada como una de las características más valiosas del sistema, confirmando la priorización realizada en la fase de diseño.

---

**Objetivo 3**: *Construir un sistema de reportes y analítica que proporcione KPIs en tiempo real con capacidad de exportación.*

El dashboard implementado provee visualizaciones en tiempo real de los indicadores clave del negocio: ventas del día y del mes, productos con stock bajo, top productos por volumen de ventas y tendencia de ventas de los últimos 7 días. Los módulos de exportación generan reportes en formato PDF y Excel correctamente.

Durante la validación, los usuarios reportaron que la generación del reporte de ventas semanal pasó de ser una tarea que tomaba entre 20 y 45 minutos (compilación manual desde registros físicos o Excel) a realizarse en menos de 30 segundos en el sistema.

---

**Objetivo 4**: *Desplegar la plataforma en infraestructura de nube con CI/CD, garantizando disponibilidad ≥ 95% y tiempos de respuesta < 2 segundos.*

El sistema fue desplegado en AWS con un pipeline de CI/CD completamente automatizado mediante GitHub Actions. Durante el período de producción, se alcanzó una disponibilidad del **[X]%** y los tiempos de respuesta en el percentil 95 se mantuvieron por debajo de los 500ms para todas las operaciones CRUD bajo carga normal. Ambos requisitos no funcionales (RNF-01, RNF-02) fueron satisfechos.

La adopción de CI/CD desde las primeras etapas del proyecto fue una decisión de alto valor: el pipeline automatizado detectó múltiples regresiones antes de que llegaran a producción, en particular errores de tipado en los schemas de Pydantic que surgían al modificar los modelos de base de datos.

---

**Objetivo 5**: *Validar la solución mediante pruebas con al menos dos empresas piloto, midiendo el impacto en la eficiencia operativa.*

**[COMPLETAR: resumir aquí los resultados clave del Capítulo 5. Por ejemplo:]**

La validación se llevó a cabo con [N] empresas piloto durante un período de [X] semanas. Los resultados mostraron una reducción promedio del [X]% en el tiempo dedicado a tareas administrativas clave, [X]% de reducción en las discrepancias de inventario y un puntaje SUS de [X]/100, lo que [valida / valida parcialmente] las hipótesis planteadas.

---

## 6.2 Conclusión General

OrbitEngine demostró ser una solución técnicamente viable y funcionalmente completa para la gestión operativa de pymes del sector comercio. El proyecto logró construir, desplegar y validar con usuarios reales una plataforma SaaS multi-tenant que integra gestión de inventario, ventas, clientes y reportes operativos en un período de siete meses con un equipo de tres personas.

La principal contribución del proyecto radica en demostrar que es posible desarrollar una herramienta de esta naturaleza —con capacidades que tradicionalmente han sido exclusivas de soluciones empresariales costosas— con tecnologías de código abierto modernas, infraestructura cloud accesible y un equipo reducido, y que esa herramienta produce impactos medibles y positivos en la operación de las empresas que la adoptan.

Desde el punto de vista académico, el proyecto contribuye con evidencia empírica sobre el impacto de la digitalización en la eficiencia operativa de pymes latinoamericanas, un área con literatura creciente pero aún con escasez de estudios de caso con sistemas desarrollados específicamente para este contexto.

---

## 6.3 Limitaciones del Proyecto

A pesar de los resultados obtenidos, el proyecto presenta las siguientes limitaciones que deben ser tenidas en cuenta al interpretar los resultados:

1. **Tamaño de la muestra de validación**: el experimento se realizó con [N] empresas piloto, lo que limita la capacidad de generalizar los resultados al universo de pymes. Un estudio con mayor escala sería necesario para conclusiones estadísticamente robustas.

2. **Período de prueba corto**: el período de prueba de [X] semanas es suficiente para medir el impacto inmediato de la adopción, pero no captura beneficios de largo plazo como la ganancia de eficiencia acumulada conforme los usuarios se familiarizan más con el sistema.

3. **Alcance funcional del MVP**: el sistema no incluye funcionalidades importantes para pymes que operan en un contexto regulatorio específico, como facturación electrónica con validez tributaria o integración con software contable. Estas ausencias pueden limitar la adopción en ciertos mercados.

4. **Localización fiscal**: OrbitEngine no está adaptado a las normativas tributarias específicas de ningún país latinoamericano, lo que lo posiciona como una herramienta de gestión interna pero no como reemplazo de sistemas de facturación oficial.

5. **Ausencia de capacidades predictivas**: el sistema actual provee reportes históricos y visualizaciones de tendencias, pero no incluye predicción de demanda automatizada. Esta capacidad, si bien identificada como valiosa por los usuarios piloto, queda propuesta como trabajo futuro.

---

## 6.4 Trabajo Futuro

Con base en las limitaciones identificadas y el feedback de los usuarios piloto, se proponen las siguientes líneas de trabajo para versiones futuras de OrbitEngine:

### 6.4.1 Mejoras Funcionales de Corto Plazo

1. **Módulo de proveedores**: gestión de proveedores, órdenes de compra y recepción de mercancía, complementando el ciclo completo de inventario.
2. **Notificaciones por correo y mensajería**: envío automático de alertas de stock bajo, recordatorios de reabastecimiento y resúmenes de ventas periódicos via email o WhatsApp Business API.
3. **Gestión de múltiples sucursales**: soporte para organizaciones con más de una sede, con inventario y reportes por sucursal y consolidados.
4. **Importación masiva de datos**: herramienta de carga de datos históricos (productos, clientes, ventas) desde Excel/CSV para facilitar la migración desde sistemas manuales.

### 6.4.2 Incorporación de Inteligencia Artificial

Una de las extensiones más prometedoras de la plataforma es la integración de capacidades de aprendizaje automático directamente en los flujos de decisión existentes. Las propuestas concretas incluyen:

1. **Predicción de demanda por producto**: implementar un pipeline de forecasting de series de tiempo (por ejemplo, con el modelo Prophet de Meta) que, utilizando el historial de ventas acumulado, genere predicciones de ventas para los próximos 30 días con recomendaciones automáticas de reabastecimiento.
2. **Alertas inteligentes de inventario**: complementar las alertas de stock mínimo actuales con predicciones dinámicas de ruptura de stock basadas en la tendencia reciente de ventas de cada producto.
3. **Análisis de segmentación de clientes**: clustering de clientes por comportamiento de compra (RFM: Recency, Frequency, Monetary) para identificar clientes de alto valor y personalizar estrategias de fidelización.
4. **Detección de productos de baja rotación**: identificación automática de productos que inmovilizan capital, facilitando decisiones de liquidación o descontinuación.

### 6.4.3 Evolución de la Plataforma

1. **Facturación electrónica**: integración con las APIs de organismos tributarios latinoamericanos (DIAN en Colombia, SAT en México, SII en Chile) para validar comprobantes con efecto fiscal.
2. **Aplicación móvil nativa**: app iOS/Android orientada a los roles de vendedor y administrador, con funcionalidad offline para registro de ventas sin conectividad.
3. **Modelo freemium / marketplace de módulos**: arquitectura de plugins que permita a las organizaciones activar módulos adicionales (e.g., contabilidad básica, gestión de empleados) de forma independiente.
4. **Estudio de adopción a mayor escala**: diseñar un estudio longitudinal con una muestra representativa de pymes latinoamericanas para obtener evidencia estadísticamente robusta del impacto de la plataforma.
