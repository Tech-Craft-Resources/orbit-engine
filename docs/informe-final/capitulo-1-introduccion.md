# Capítulo 1 — Introducción

---

## 1.1 Planteamiento del Problema

Las pequeñas y medianas empresas (pymes) constituyen el motor económico de América Latina. Según la Comisión Económica para América Latina y el Caribe (CEPAL, 2022), las pymes representan más del 99% del tejido empresarial en la región y generan entre el 60% y el 70% del empleo formal. Sin embargo, pese a su relevancia, enfrentan una brecha estructural frente a las grandes corporaciones en materia de gestión operativa y adopción tecnológica.

Un diagnóstico recurrente en la literatura especializada señala que la gran mayoría de las pymes latinoamericanas aún gestionan sus operaciones —inventario, ventas, clientes y contabilidad básica— mediante herramientas rudimentarias: cuadernos físicos, hojas de cálculo de Excel no estructuradas o sistemas ad hoc sin integración entre módulos. De acuerdo con el Banco Interamericano de Desarrollo (BID, 2021), solo el 16% de las pymes de la región ha adoptado algún tipo de software de gestión empresarial, frente a un 74% en países de la OCDE.

Esta brecha de digitalización se traduce en consecuencias concretas y medibles para el negocio:

- **Errores de inventario**: la gestión manual provoca discrepancias frecuentes entre el stock físico y el registrado, generando roturas de stock o sobrestock. Ambos escenarios tienen costos directos: ventas perdidas en el primer caso, capital inmovilizado en el segundo.
- **Ineficiencia operativa**: los empleados dedican tiempo significativo a tareas administrativas repetitivas —conciliación de registros, elaboración de reportes manuales, búsqueda de información— tiempo que podría orientarse a actividades de mayor valor.
- **Toma de decisiones reactiva**: sin acceso a datos consolidados y en tiempo real, los dueños de pymes toman decisiones basadas en intuición antes que en evidencia. El abastecimiento de productos, la identificación de clientes de alto valor y la detección de tendencias de ventas se realizan de manera subjetiva, sin soporte de indicadores ni reportes estructurados.

Las soluciones existentes en el mercado presentan limitaciones específicas para este segmento. Los sistemas ERP de nivel empresarial (SAP, Oracle) son prohibitivos en costo y complejidad para una pyme. Las alternativas de código abierto como Odoo, si bien potentes, requieren infraestructura propia y capacidad técnica para su instalación, configuración y mantenimiento. Las soluciones SaaS disponibles en el mercado latinoamericano (Alegra, Siigo, Defontana) se enfocan principalmente en facturación electrónica y contabilidad, sin integrar capacidades de gestión de inventario, análisis de clientes y reportes operativos en un único entorno accesible.

Se identifica así un problema de investigación y desarrollo bien definido: **la inexistencia de una plataforma SaaS integrada, accesible y orientada al contexto latinoamericano, que combine la gestión operativa esencial de una pyme —inventario, ventas, clientes y reportes— bajo un modelo de precios y complejidad adecuados para este segmento.**

---

## 1.2 Justificación

### 1.2.1 Justificación Económica y Social

La digitalización de las pymes no es un objetivo exclusivamente tecnológico; es un imperativo económico. El BID estima que cerrar la brecha digital de las pymes en América Latina podría incrementar el PIB regional en hasta un 5% adicional para 2030. En términos individuales, los estudios de adopción de ERP en pymes reportan reducciones de costos operativos del 15% al 30% y mejoras en la eficiencia de la gestión de inventario de hasta el 40% en el primer año de implementación (Kumar & Hillegersberg, 2000; Duan et al., 2012).

La relevancia del problema es, por tanto, tanto académica como práctica: una solución bien diseñada tiene potencial de impacto directo en la competitividad de cientos de pequeñas empresas.

### 1.2.2 Justificación Tecnológica

El desarrollo de OrbitEngine se justifica por la convergencia de condiciones tecnológicas que hacen viable hoy lo que no era posible hace una década:

1. **Democratización de la nube**: el modelo SaaS elimina la necesidad de servidores propios, reduciendo la barrera de entrada a un costo mensual por suscripción.
2. **Madurez del ecosistema de desarrollo moderno**: frameworks como FastAPI y React, combinados con herramientas de contenerización (Docker) e infraestructura en la nube (AWS), permiten a equipos pequeños construir plataformas escalables con calidad de producción.
3. **Generación automática de API clients**: herramientas como OpenAPI permiten mantener sincronizados el contrato de la API y el frontend sin esfuerzo manual, reduciendo errores y acelerando el desarrollo.

### 1.2.3 Justificación Académica

El presente proyecto representa una contribución en la intersección de dos áreas de investigación activa: la adopción de tecnologías de información en pymes y el diseño de plataformas SaaS multi-tenant para contextos de recursos limitados. El desarrollo de un sistema funcional, validado con usuarios reales, permite contrastar con evidencia empírica las hipótesis sobre el impacto de la digitalización en la eficiencia operativa de pequeñas empresas latinoamericanas.

---

## 1.3 Objetivos

### 1.3.1 Objetivo General

Desarrollar e implementar una plataforma SaaS multi-tenant para la gestión integral de procesos internos en pequeñas y medianas empresas, que integre módulos de gestión de inventario, ventas, clientes y reportes operativos, y validar su impacto en la eficiencia operativa mediante pruebas con empresas reales.

### 1.3.2 Objetivos Específicos

1. **Diseñar** la arquitectura técnica de una plataforma SaaS multi-tenant que garantice el aislamiento de datos entre organizaciones, la escalabilidad horizontal y la seguridad de la información, documentando las decisiones arquitectónicas con su justificación.

2. **Desarrollar** los módulos de gestión operativa esenciales —autenticación y control de acceso basado en roles, gestión de inventario con alertas automáticas, registro de ventas con generación de documentos, y gestión de clientes con análisis de historial— conforme a los requisitos levantados con usuarios reales de pymes.

3. **Construir** un sistema de reportes y analítica que proporcione indicadores clave de desempeño (KPIs) en tiempo real, con capacidad de exportación de datos en formatos estándar (PDF, Excel), facilitando la toma de decisiones basada en datos.

4. **Desplegar** la plataforma en infraestructura de nube (AWS) con un pipeline de integración y entrega continua (CI/CD), garantizando una disponibilidad mínima del 95% y tiempos de respuesta inferiores a 2 segundos para operaciones transaccionales.

5. **Validar** la solución mediante pruebas de usabilidad y rendimiento con al menos dos empresas piloto, midiendo el impacto en la eficiencia operativa a través de métricas cuantitativas (reducción de tiempo en tareas, tasa de error) y cualitativas (satisfacción de usuario).

---

## 1.4 Alcance y Limitaciones

### 1.4.1 Alcance del Sistema

OrbitEngine abarca el siguiente conjunto de funcionalidades dentro del producto mínimo viable (MVP):

**Módulos implementados:**
- Autenticación y gestión de usuarios con control de acceso basado en roles (RBAC): Administrador, Vendedor y Visualizador.
- Gestión de inventario: CRUD de productos por categorías, control de stock en tiempo real, alertas automáticas de nivel mínimo e historial de movimientos.
- Gestión de ventas: registro de transacciones multi-producto, historial de ventas con filtros, exportación de facturas en PDF.
- Gestión de clientes: base de datos de clientes, historial de compras y métricas de comportamiento.
- Dashboard y reportes: KPIs en tiempo real, reportes por período y exportación a PDF y Excel.
- Infraestructura multi-tenant: soporte para múltiples organizaciones con aislamiento total de datos.

**Características técnicas:**
- API RESTful documentada con OpenAPI/Swagger.
- Interfaz web responsive, compatible con navegadores modernos (Chrome, Firefox, Safari, Edge).

***- Despliegue en AWS con Docker y GitHub Actions.***
- Suite de pruebas automatizadas con cobertura mínima del 60%.

### 1.4.2 Limitaciones y Exclusiones

Las siguientes características quedan fuera del alcance del MVP y podrán abordarse en versiones futuras:

- Facturación electrónica oficial con validez tributaria (DIAN, SAT, SII u organismos equivalentes).
- Gestión de nómina y recursos humanos.
- Aplicación móvil nativa (iOS/Android).
- Integración con pasarelas de pago o sistemas ERP externos.
- Soporte para gestión de múltiples sucursales o bodegas dentro de una misma organización.
- Gestión de servicios (el sistema está orientado a empresas de comercio de productos físicos).
- Múltiples monedas o idiomas en la interfaz.

### 1.4.3 Supuestos

1. Los usuarios de la plataforma disponen de conexión a internet estable para el acceso a la aplicación web.
2. Las empresas piloto están dispuestas a cargar sus datos de productos, clientes y stock inicial para comenzar a operar con el sistema.
3. El equipo de desarrollo cuenta con acceso a créditos de AWS para educación o presupuesto operativo para la infraestructura de nube.

---

## 1.5 Metodología

El proyecto se desarrolló bajo un enfoque de investigación aplicada con componente de desarrollo de software. Se adoptó la metodología ágil Scrum adaptada para equipos académicos, organizando el desarrollo en sprints de dos semanas durante un período de siete meses (octubre 2025 – abril 2026).

La investigación siguió las siguientes etapas:

1. **Documentación y planificación** (octubre 2025): revisión bibliográfica, levantamiento de requisitos con usuarios potenciales, diseño de arquitectura, modelo de datos y definición del backlog inicial.
2. **Desarrollo del núcleo** (noviembre 2025 – enero 2026): implementación de la infraestructura base y los módulos de autenticación, inventario, ventas, clientes y reportes.
3. **Estabilización y refinamiento** (febrero – marzo 2026): corrección de errores, mejoras de experiencia de usuario, pruebas de carga y consolidación del despliegue en producción.
4. **Validación con empresas piloto** (abril 2026, semanas 1–3): pruebas con usuarios reales, recolección de métricas de eficiencia operativa y encuestas de usabilidad.
5. **Documentación y entrega** (abril 2026, semana 4): consolidación del informe final, análisis de resultados y defensa del proyecto.

---

## 1.6 Estructura del Documento

El presente informe se organiza en los siguientes capítulos:

- **Capítulo 2 — Marco de Referencia**: define los conceptos fundamentales del dominio (pyme, ERP, SaaS, multi-tenancy, API REST, RBAC) y presenta el estado del arte mediante una revisión de soluciones existentes en el mercado y de la literatura académica relevante.
- **Capítulo 3 — Análisis y Diseño del Sistema**: describe el proceso de levantamiento de requisitos, la arquitectura técnica adoptada, el diseño del modelo de datos y el diseño de las interfaces de usuario.
- **Capítulo 4 — Desarrollo e Implementación**: detalla la metodología de desarrollo utilizada, los módulos implementados, las decisiones técnicas relevantes y la estrategia de pruebas.
- **Capítulo 5 — Resultados y Validación**: presenta los resultados de las pruebas de rendimiento, usabilidad y validación con empresas piloto, contrastándolos con los objetivos planteados.
- **Capítulo 6 — Conclusiones y Trabajo Futuro**: sintetiza los logros del proyecto por objetivo, enumera las limitaciones encontradas y propone líneas de trabajo para versiones futuras.
- **Referencias Bibliográficas**: lista completa de las fuentes citadas a lo largo del documento.
- **Anexos**: manual de usuario, manual de despliegue, especificación de la API y resultados detallados de pruebas.
