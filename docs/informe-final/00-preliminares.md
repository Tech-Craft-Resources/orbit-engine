# OrbitEngine

## Desarrollo e Implementación de una Plataforma SaaS Multi-Tenant para la Gestión Integral de Procesos Internos en Pequeñas y Medianas Empresas

---

\vspace{2cm}

**Autores**

Nicolás Rodríguez Forero  
Daniel Velasco González  
Fabián Rincón Suárez  

\vspace{1.5cm}

**Semillero de Software como Innovación**

Directores:  
Juan Pablo Ospina López  
Camilo Enrique Rodríguez Torres  

\vspace{1.5cm}

**Universidad Sergio Arboleda**  
Escuela de Ciencias Exactas e Ingeniería  
Pregrado en Ciencias de la Computación e Inteligencia Artificial  

Bogotá, Colombia  
Abril de 2026

\newpage

---

## Página de Aprobación

El trabajo de grado titulado **"OrbitEngine: Desarrollo e Implementación de una Plataforma SaaS Multi-Tenant para la Gestión Integral de Procesos Internos en Pequeñas y Medianas Empresas"**, presentado por **Nicolás Rodríguez Forero**, **Daniel Velasco González** y **Fabián Rincón Suárez**, como requisito parcial para optar al título de **Profesional en Ciencias de la Computación e Inteligencia Artificial**, fue revisado y aprobado por:

\vspace{2cm}

**Director del Semillero**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Juan Pablo Ospina López  
Semillero de Software como Innovación  
Universidad Sergio Arboleda

\vspace{1.5cm}

**Co-director del Semillero**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
Camilo Enrique Rodríguez Torres  
Semillero de Software como Innovación  
Universidad Sergio Arboleda

\vspace{1.5cm}

**Jurado Evaluador**

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
[Nombre del jurado]  
[Cargo e institución]

\vspace{1.5cm}

\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_  
[Nombre del jurado]  
[Cargo e institución]

\vspace{2cm}

Bogotá, Colombia — Abril de 2026

\newpage

---

## Resumen

Las pequeñas y medianas empresas (pymes) de América Latina enfrentan una brecha estructural de digitalización en la gestión de sus operaciones internas. La mayoría administra inventario, ventas y clientes mediante hojas de cálculo o registros manuales, sin acceso a herramientas integradas y accesibles que proporcionen visibilidad en tiempo real del estado del negocio. Las soluciones ERP existentes en el mercado son, o bien demasiado costosas y complejas para este segmento, o bien insuficientes en sus capacidades operativas para cubrir el ciclo comercial completo.

El presente trabajo describe el diseño, desarrollo y validación de OrbitEngine, una plataforma SaaS multi-tenant orientada a pymes del sector comercio minorista y mayorista. La plataforma integra módulos de gestión de inventario con alertas automáticas de stock mínimo e historial de movimientos, registro de ventas con generación de facturas y control transaccional de stock, administración de clientes con análisis de comportamiento de compra, y un dashboard de indicadores clave de desempeño (KPIs) con exportación a PDF y Excel.

El proyecto se desarrolló en siete meses por un equipo de tres personas bajo una metodología Scrum adaptada al contexto académico. El backend fue construido con FastAPI y SQLModel sobre PostgreSQL; el frontend con React 19 y TypeScript; y el sistema fue desplegado en infraestructura AWS con un pipeline de integración y entrega continua (CI/CD) automatizado mediante GitHub Actions. La arquitectura multi-tenant adoptada garantiza el aislamiento total de datos entre organizaciones mediante un discriminador `organization_id` aplicado sistemáticamente en todas las tablas de negocio y en el token JWT de autenticación.

La plataforma fue validada con empresas piloto del sector comercio, midiendo el impacto en la eficiencia operativa a través de la reducción de tiempos en tareas administrativas, la disminución de errores de inventario y encuestas de usabilidad basadas en la escala SUS (*System Usability Scale*). Los resultados obtenidos evidencian mejoras significativas en la gestión operativa de las empresas participantes y confirman la viabilidad técnica y funcional de la solución propuesta.

**Palabras clave:** SaaS, pymes, gestión operativa, inventario, ventas, multi-tenancy, FastAPI, React, AWS, arquitectura en capas.

\newpage

---

## Abstract

Small and medium-sized enterprises (SMEs) in Latin America face a structural digitalization gap in the management of their internal operations. Most businesses rely on spreadsheets or manual records to manage inventory, sales, and customers, lacking access to integrated, affordable tools that provide real-time visibility into business performance. Existing ERP solutions in the market are either too costly and complex for this segment, or too limited in operational scope to support the full commercial cycle.

This work presents the design, development, and validation of OrbitEngine, a multi-tenant SaaS platform targeting retail and wholesale commerce SMEs. The platform integrates modules for inventory management with automatic low-stock alerts and movement history, sales recording with invoice generation and transactional stock control, customer administration with purchase behavior analytics, and a key performance indicator (KPI) dashboard with PDF and Excel export capabilities.

The project was developed over seven months by a three-person team following an Scrum methodology adapted to an academic context. The backend was built with FastAPI and SQLModel on PostgreSQL; the frontend with React 19 and TypeScript; and the system was deployed on AWS infrastructure with an automated CI/CD pipeline using GitHub Actions. The multi-tenant architecture ensures complete data isolation between organizations through an `organization_id` discriminator applied consistently across all business tables and embedded in the JWT authentication token.

The platform was validated with pilot companies from the commerce sector, measuring operational efficiency improvements through reductions in administrative task completion time, decreases in inventory discrepancy rates, and usability assessments based on the System Usability Scale (SUS). Results demonstrate significant improvements in the operational management of participating companies and confirm the technical and functional viability of the proposed solution.

**Keywords:** SaaS, SMEs, operational management, inventory, sales, multi-tenancy, FastAPI, React, AWS, layered architecture.
