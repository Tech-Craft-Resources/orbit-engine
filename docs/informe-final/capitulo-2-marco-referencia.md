# Capítulo 2 — Marco de Referencia

---

## 2.1 Marco Conceptual

Esta sección define los conceptos fundamentales sobre los que se sustenta el proyecto OrbitEngine, estableciendo el vocabulario técnico y académico compartido a lo largo del documento.

### 2.1.1 Pequeña y Mediana Empresa (Pyme)

La definición de pyme varía según el país y el organismo de referencia. En América Latina, los criterios más comunes consideran el número de empleados y el volumen de ventas anuales. La CEPAL (2022) y el Banco Mundial utilizan como referencia general la siguiente clasificación:

| Categoría | Empleados | Ventas anuales (USD) |
|-----------|-----------|----------------------|
| Microempresa | 1–9 | < 100.000 |
| Pequeña empresa | 10–49 | 100.000 – 1.000.000 |
| Mediana empresa | 50–249 | 1.000.000 – 10.000.000 |

Para el contexto de este proyecto, el término "pyme" se utiliza con énfasis en el segmento de pequeñas empresas de comercio minorista y mayorista, con equipos de entre 2 y 30 personas, operaciones presenciales o híbridas, y necesidades de gestión de inventario físico, registro de ventas y seguimiento de clientes.

### 2.1.2 Sistema de Planificación de Recursos Empresariales (ERP)

Un Enterprise Resource Planning (ERP) es un sistema de información integrado que unifica los procesos de negocio de una organización —finanzas, producción, inventario, ventas, recursos humanos— en una única plataforma con una base de datos compartida (Klaus et al., 2000). La integración elimina la duplicación de datos y proporciona una visión unificada del estado del negocio en tiempo real.

Los ERP surgen en los años noventa como evolución de los sistemas MRP (Material Requirements Planning). Empresas como SAP, Oracle y Microsoft Dynamics dominaron el mercado inicial con soluciones de altísimo costo y complejidad, orientadas a grandes corporaciones. La segunda generación de ERP, surgida en la década de 2000, introdujo soluciones para el mercado de pymes (SAP Business One, Microsoft Dynamics 365 Business Central), si bien con costos de implementación y operación aún inaccesibles para la mayoría de las pequeñas empresas latinoamericanas.

OrbitEngine no se clasifica como un ERP en el sentido amplio del término —no incluye módulos de contabilidad, nómina ni producción—, sino como una plataforma de gestión operativa orientada a los procesos comerciales centrales de una pyme: inventario, ventas y clientes.

### 2.1.3 Software como Servicio (SaaS)

Software as a Service (SaaS) es un modelo de distribución de software en el que el proveedor aloja la aplicación en infraestructura propia (nube) y la pone a disposición de los usuarios finales a través de internet, típicamente mediante una suscripción periódica (Benlian & Hess, 2011).

El modelo SaaS elimina para el cliente la necesidad de:
- Adquirir y mantener infraestructura de servidores.
- Gestionar instalaciones, actualizaciones y parches del software.
- Invertir en licencias únicas de alto costo.

En cambio, el cliente paga una tarifa recurrente (mensual o anual) que cubre el uso del software, la infraestructura, el mantenimiento y el soporte. Este modelo democratiza el acceso a herramientas empresariales sofisticadas para organizaciones sin departamento de TI.

Desde la perspectiva del proveedor, el modelo SaaS permite economías de escala: una misma infraestructura sirve a múltiples clientes (multi-tenancy), reduciendo el costo marginal por cliente adicional.

### 2.1.4 Arquitectura Multi-Tenant

El concepto de multi-tenancy (multi-arrendamiento) describe una arquitectura de software en la que una única instancia de la aplicación y su infraestructura subyacente sirven a múltiples clientes (tenants), manteniendo el aislamiento lógico de los datos de cada uno (Bezemer & Zaidman, 2010).

Existen tres enfoques principales de implementación:

| Enfoque | Descripción | Aislamiento | Costo |
|---------|-------------|-------------|-------|
| Base de datos por tenant | Cada cliente tiene su propia BD | Alto | Alto |
| Esquema por tenant | Una BD, esquemas separados | Medio | Medio |
| Tabla compartida + discriminador | Una BD, filas diferenciadas por `tenant_id` | Bajo-Medio | Bajo |

OrbitEngine implementa el tercer enfoque: todas las organizaciones comparten las mismas tablas, y cada registro lleva asociado un campo `organization_id` que actúa como discriminador. El acceso a los datos se filtra automáticamente en cada operación, garantizando el aislamiento sin multiplicar el costo de infraestructura.

### 2.1.5 API REST y OpenAPI

Una API REST (Representational State Transfer) es una interfaz de programación que permite la comunicación entre sistemas a través del protocolo HTTP, utilizando los verbos estándar (GET, POST, PUT, PATCH, DELETE) y representaciones de recursos en formato JSON o XML (Fielding, 2000).

OpenAPI (anteriormente Swagger) es una especificación estándar para describir APIs REST de forma legible tanto por humanos como por máquinas. Su adopción en OrbitEngine permite la generación automática de documentación interactiva y de clientes de API tipados para el frontend.

### 2.1.6 Control de Acceso Basado en Roles (RBAC)

Role-Based Access Control (RBAC) es un modelo de seguridad en el que los permisos de acceso a recursos del sistema se asignan a roles, y los usuarios adquieren permisos a través de su asignación a uno o más roles (Ferraiolo et al., 2001). Este modelo simplifica la administración de permisos en organizaciones donde múltiples usuarios realizan funciones diferenciadas.

En OrbitEngine se definen tres roles:
- **Administrador**: acceso total a todos los módulos y configuración de la organización.
- **Vendedor**: acceso a ventas, consulta de inventario y clientes. Sin acceso a reportes avanzados ni configuración.
- **Visualizador**: acceso de solo lectura a reportes y dashboards.

### 2.1.7 Integración y Entrega Continua (CI/CD)

Continuous Integration/Continuous Delivery (CI/CD) es un conjunto de prácticas de ingeniería de software que automatiza el proceso de verificación, construcción y despliegue del código. Un pipeline de CI/CD ejecuta, ante cada cambio en el repositorio, una secuencia de pasos: pruebas automatizadas, análisis estático, construcción de artefactos y despliegue en los ambientes correspondientes (Fowler & Foemmel, 2006).

La adopción de CI/CD en OrbitEngine, implementada mediante GitHub Actions, garantiza que cada versión desplegada en producción ha pasado exitosamente por la suite de pruebas, reduciendo la probabilidad de introducir regresiones.

---

## 2.2 Estado del Arte

### 2.2.1 Contexto de la Digitalización de Pymes en Latinoamérica

La transformación digital de las pymes en América Latina ha sido objeto de creciente atención académica y política en la última década. La pandemia de COVID-19 (2020–2021) actuó como catalizador de la adopción tecnológica, al forzar a empresas que operaban exclusivamente de manera presencial a explorar canales digitales y herramientas de gestión remota.

Rodríguez-Abitia et al. (2020), en su estudio sobre digitalización de pymes mexicanas, identificaron que los principales obstáculos para la adopción de sistemas de gestión son: el costo percibido como elevado, la falta de capacitación del personal, la desconfianza en la seguridad de datos en la nube y la baja oferta de soluciones adaptadas al contexto local. Un hallazgo relevante es que las pymes que sí adoptaron herramientas digitales de gestión reportaron mejoras significativas en eficiencia (entre el 20% y el 35%) en los 12 meses posteriores a la implementación.

Cardona et al. (2022) analizaron la adopción de ERP en pymes colombianas y encontraron que el 68% de las empresas que fallaron en su implementación lo hicieron por seleccionar soluciones demasiado complejas para su tamaño, o por falta de acompañamiento en la fase de puesta en marcha. Los autores concluyen que la simplicidad de la interfaz y la pertinencia funcional son más determinantes del éxito que las capacidades técnicas del sistema.

### 2.2.2 Soluciones Existentes en el Mercado

A continuación se analiza el panorama de soluciones que compiten, directa o indirectamente, con OrbitEngine en el segmento de pymes latinoamericanas.

#### Odoo Community / Enterprise

Odoo es un ERP de código abierto con más de 7 millones de usuarios en todo el mundo. Su versión Community es gratuita y cubre un amplio espectro de módulos: inventario, ventas, compras, contabilidad, CRM y recursos humanos. La versión Enterprise agrega módulos avanzados bajo un modelo de suscripción.

**Fortalezas**: altamente modular, comunidad amplia, documentación extensa.  
**Debilidades para el contexto de este proyecto**: requiere instalación en servidor propio o contratación de hosting especializado, lo que implica conocimiento técnico o un costo adicional de servicio. La curva de aprendizaje para usuarios no técnicos es elevada. La personalización para contextos latinoamericanos (localización fiscal, moneda local) requiere módulos adicionales o desarrollo a medida. No ofrece análisis de clientes integrado ni dashboard operativo simplificado.

#### Zoho One

Zoho One es una suite de aplicaciones SaaS que incluye más de 45 herramientas de negocio: CRM, inventario, contabilidad, proyectos y análisis. Es una solución madura con presencia global.

**Fortalezas**: modelo SaaS puro, integración entre módulos, amplia cobertura funcional.  
**Debilidades**: el costo por usuario ($37–$105 USD/mes) resulta elevado para pymes con equipos numerosos. La interfaz, aunque completa, puede resultar abrumadora para usuarios con bajo nivel de alfabetización digital.

#### QuickBooks

QuickBooks, de Intuit, es el software de contabilidad y gestión financiera más utilizado por pequeñas empresas en el mercado anglosajón. Su foco principal es la contabilidad, facturación y control de gastos.

**Fortalezas**: interfaz intuitiva, amplia base de usuarios, integración bancaria.  
**Debilidades**: diseñado para el mercado norteamericano y europeo, con limitada adaptación a las realidades tributarias latinoamericanas. No ofrece gestión de inventario avanzada ni análisis de clientes. Precios en dólares que pueden ser inaccesibles para pymes de ingresos bajos.

#### Alegra

Alegra es una solución SaaS desarrollada en Colombia con presencia en 10 países de América Latina. Se especializa en facturación electrónica, contabilidad y gestión de inventarios básica.

**Fortalezas**: fuerte localización tributaria latinoamericana, precio accesible (desde $25 USD/mes), interfaz en español, soporte en la región.  
**Debilidades**: las capacidades de gestión de inventario son básicas (sin alertas de stock mínimo ni historial de movimientos detallado). No incluye CRM ni análisis de clientes. El dashboard de indicadores operativos es limitado.

#### Siigo / Defontana

Siigo (Colombia) y Defontana (Chile) son soluciones SaaS con foco contable-tributario, similares a Alegra en su posicionamiento. Están bien adaptadas a la normativa local de sus países de origen pero tienen alcance funcional limitado en gestión operativa.

#### Análisis Comparativo

La siguiente tabla sintetiza la comparación entre las soluciones analizadas y OrbitEngine en las dimensiones relevantes para el segmento objetivo:

| Criterio | Odoo | Zoho | QuickBooks | Alegra | OrbitEngine |
|----------|------|------|------------|--------|-------------|
| Modelo de entrega | On-premise / SaaS | SaaS | SaaS | SaaS | SaaS |
| Precio accesible para pymes pequeñas | Medio | No | No | Sí | Sí (objetivo) |
| Gestión de inventario avanzada | Sí | Parcial | No | Básica | Sí |
| Gestión de clientes (CRM) | Sí | Sí | Básica | No | Sí |
| Dashboard y KPIs integrados | Sí | Sí | Parcial | Básico | Sí |
| Localización latinoamericana | Parcial | Parcial | Baja | Alta | Media |
| Curva de aprendizaje para no técnicos | Alta | Alta | Media | Baja | Baja (objetivo) |
| Multi-tenant nativo | Sí | Sí | No | No | Sí |

El análisis evidencia que ninguna de las soluciones disponibles combina en un único producto, accesible para el segmento de pymes latinoamericanas, la gestión operativa completa (inventario, ventas, clientes) con un dashboard de KPIs integrado, bajo una curva de aprendizaje adecuada para usuarios no técnicos. Esta brecha constituye el espacio que OrbitEngine busca ocupar.

### 2.2.3 Revisión de Literatura Académica

#### ERP en Pymes: Factores de Éxito y Fracaso

La adopción de ERP en pequeñas y medianas empresas ha sido estudiada extensamente. Soh et al. (2000) identificaron la brecha entre las funcionalidades genéricas de los sistemas ERP y las necesidades específicas de cada organización como la principal causa de fracaso en las implementaciones. Esta observación motivó el diseño de OrbitEngine como una solución vertical, enfocada en el nicho de comercio minorista y mayorista, en lugar de un ERP de propósito general.

Amid et al. (2012) propusieron un marco de factores críticos de éxito para implementaciones de ERP en pymes, destacando: (1) compromiso de la alta dirección, (2) simplicidad del proceso de implementación, (3) adaptación al contexto local y (4) capacitación de usuarios. Estos factores influyeron en las decisiones de diseño de OrbitEngine, especialmente en la priorización de la usabilidad y el proceso de onboarding.

#### Arquitecturas SaaS Multi-Tenant

Bezemer & Zaidman (2010) analizaron los desafíos de migrar aplicaciones monolíticas a arquitecturas multi-tenant, identificando como principales retos: (1) el aislamiento de datos, (2) la personalización por tenant y (3) el rendimiento bajo carga compartida. Su trabajo sienta las bases para las decisiones de diseño del modelo de datos de OrbitEngine.

Guo et al. (2017) propusieron un modelo de evaluación de arquitecturas multi-tenant en función de métricas de seguridad, rendimiento y mantenibilidad. Aplicando su framework, la arquitectura de OrbitEngine (tabla compartida con `organization_id`) se clasifica como de nivel de compartición alto, lo que maximiza la eficiencia de infraestructura al costo de una implementación más cuidadosa de los mecanismos de filtrado.

#### Usabilidad en Sistemas ERP para Usuarios No Técnicos

Zhang et al. (2021) realizaron un estudio de usabilidad con empleados de pymes latinoamericanas usando tres sistemas ERP distintos. Sus resultados mostraron que la tasa de abandono durante el onboarding aumenta un 45% cuando el sistema requiere más de 5 pasos para completar una tarea común (como registrar una venta). Este hallazgo motivó el énfasis en la experiencia de usuario (UX) de OrbitEngine, con flujos de trabajo optimizados para minimizar la fricción.

---

## 2.3 Marco Tecnológico

Esta sección justifica las decisiones tecnológicas adoptadas en el proyecto, situándolas en el contexto de las alternativas disponibles y los criterios de selección.

### 2.3.1 FastAPI (Backend)

FastAPI es un framework web moderno para Python, basado en Starlette y Pydantic, que permite construir APIs de alto rendimiento con tipado estático y generación automática de documentación OpenAPI (Ramírez, 2018). Su selección sobre alternativas como Django REST Framework o Flask se justifica por:

- **Rendimiento**: comparable a Node.js y Go en benchmarks de concurrencia, gracias a su implementación asíncrona (ASGI).
- **Tipado automático**: la integración con Pydantic valida automáticamente los datos de entrada y salida de cada endpoint, reduciendo el boilerplate de validación.
- **Documentación automática**: genera una interfaz Swagger UI y ReDoc sin configuración adicional, facilitando la comunicación con el frontend y la evaluación académica.
- **Ecosistema Python maduro**: la elección de Python como lenguaje de backend otorga acceso a un amplio ecosistema de bibliotecas para procesamiento de datos, generación de reportes (openpyxl, reportlab) y posibles extensiones futuras.

### 2.3.2 React (Frontend)

React es una biblioteca JavaScript para la construcción de interfaces de usuario basadas en componentes, desarrollada por Meta. Su adopción como tecnología de frontend es ampliamente respaldada por la industria y la academia (Gackenheimer, 2015).

La combinación con TypeScript añade tipado estático al frontend, mejorando la detección temprana de errores y la mantenibilidad del código. Las bibliotecas complementarias seleccionadas (TanStack Query para gestión de estado del servidor, TanStack Router para enrutamiento, React Hook Form + Zod para formularios con validación) representan el estándar actual de la industria para aplicaciones SaaS de escala media.

### 2.3.3 PostgreSQL

PostgreSQL es el sistema de gestión de bases de datos relacionales de código abierto más avanzado disponible. Su elección sobre alternativas como MySQL o bases de datos NoSQL se fundamenta en:

- **Integridad referencial**: las relaciones entre entidades de negocio (ventas → productos, ventas → clientes) se benefician de las garantías ACID de un motor relacional.
- **JSON nativo**: el soporte para columnas JSONB permite almacenar datos semi-estructurados (atributos variables de productos) sin sacrificar las ventajas relacionales.
- **Row-Level Security**: característica nativa de PostgreSQL que permite definir políticas de acceso a nivel de fila, complementando la estrategia de multi-tenancy a nivel de aplicación.
- **Ecosistema robusto**: integración nativa con SQLAlchemy/SQLModel (ORM Python) y soporte completo en AWS RDS.

### 2.3.4 Docker y AWS

La contenerización mediante Docker garantiza la paridad entre los ambientes de desarrollo, pruebas y producción, eliminando la clase de errores "funciona en mi máquina". El despliegue en AWS se apoya en los servicios:

- **ECS Fargate**: ejecución de los contenedores del backend de forma escalable y sin gestión de servidores.
- **RDS**: instancia gestionada de PostgreSQL, con backups automáticos y failover.
- **S3**: almacenamiento de archivos estáticos (frontend compilado) y archivos generados (PDFs de reportes).
- **CloudFront**: CDN para distribución global del frontend con baja latencia.

### 2.3.5 SQLModel

SQLModel es una biblioteca Python que combina SQLAlchemy (ORM) y Pydantic en un único modelo de clase, permitiendo que el mismo tipo Python sirva tanto como modelo de base de datos como schema de validación de la API (Ramírez, 2021). Esta unificación reduce la duplicación de código y asegura la consistencia entre la capa de datos y la capa de API.

