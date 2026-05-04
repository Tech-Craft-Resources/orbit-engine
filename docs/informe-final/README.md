# OrbitEngine — Informe de Proyecto de Grado

> Plataforma SaaS para la Gestión Integral de Procesos Internos en Pequeñas y Medianas Empresas

**Universidad:** Universidad Sergio Arboleda — Escuela de Ciencias Exactas e Ingeniería  
**Programa:** Pregrado en Ciencias de la Computación e Inteligencia Artificial  
**Período:** Octubre 2025 – Abril 2026  
**Autores:** Nicolás Rodríguez Forero, Daniel Velasco González, Fabián Rincón Suárez  
**Directores:** Juan Pablo Ospina López, Camilo Enrique Rodríguez Torres  
**Semillero:** Software como Innovación

---

## Estructura del Informe

Este directorio contiene el informe de grado completo de OrbitEngine, organizado en archivos Markdown por capítulo para facilitar la edición colaborativa. Para la versión final de entrega, los archivos deben consolidarse en un único documento Word/PDF siguiendo la plantilla de la universidad.


| Archivo                                                                          | Contenido                                                                                                             | Estado                                                      |
| -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [00-preliminares.md](00-preliminares.md) | Portada, página de aprobación, resumen (ES) y abstract (EN) | ✅ Borrador completo (pendiente: nombres de jurados y número de páginas) |
| [capitulo-1-introduccion.md](capitulo-1-introduccion.md) | Planteamiento del problema, justificación, objetivos, alcance, metodología | ✅ Borrador completo (placeholders pendientes) |
| [capitulo-2-marco-referencia.md](capitulo-2-marco-referencia.md) | Marco conceptual, estado del arte, marco tecnológico | ✅ Borrador completo (placeholders pendientes) |
| [capitulo-3-analisis-diseno.md](capitulo-3-analisis-diseno.md) | Requisitos, arquitectura, modelo de datos, diseño de UI | ✅ Borrador completo (placeholders pendientes) |
| [capitulo-4-desarrollo.md](capitulo-4-desarrollo.md) | Metodología ágil, sprints, implementación, pruebas, CI/CD | ✅ Borrador completo (placeholders pendientes) |
| [capitulo-5-resultados-tecnicos.md](capitulo-5-resultados-tecnicos.md) | Resultados Técnicos: pruebas de carga (Locust) y de rendimiento web (Lighthouse, PageSpeed Insights, WebPageTest) | ✅ Borrador completo (pendiente menor: registrar datos formales de uptime mensual RNF-02) |
| [capitulo-6-resultados-usuarios.md](capitulo-6-resultados-usuarios.md) | Resultados de Usuarios: eficiencia operativa pre/post, SUS, NPS, CSAT, telemetría, entrevistas, validación de hipótesis (N = 3 empresas reales) | ✅ Borrador completo (datos reales de las tres empresas piloto incluidos) |
| [capitulo-7-conclusiones.md](capitulo-7-conclusiones.md) | Conclusiones por objetivo, conclusión general, validación de hipótesis, limitaciones, recomendaciones de optimización, trabajo futuro | ✅ Borrador completo (sección 7.5.4 y 7.1 obj. 5 pendientes de datos del Cap. 6) |
| [referencias.md](referencias.md) | Referencias bibliográficas en formato APA 7.ª edición | ✅ Borrador completo |
| [anexo-a-manual-usuario.md](anexo-a-manual-usuario.md) | Manual de uso para usuarios finales (no técnico) | ✅ Borrador completo (pendiente: capturas de pantalla de la aplicación) |
| [anexo-b-manual-despliegue.md](anexo-b-manual-despliegue.md) | Guía técnica de instalación y despliegue | ✅ Borrador completo (placeholders pendientes) |
| [anexo-c-documentacion-tecnica.md](anexo-c-documentacion-tecnica.md) | Documentación técnica profesional: API, modelos, variables de entorno, convenciones | ✅ Borrador completo (placeholders pendientes) |
| [recomendaciones.md](recomendaciones.md) | Guía interna: cómo aplicar SUS, NPS, CSAT, pruebas de tareas, entrevistas y extraer telemetría para completar el Cap. 6 | ✅ Borrador completo |


---

## Tabla de Contenidos General

```
Portada                                → 00-preliminares.md
Página de aprobación / firmas          → 00-preliminares.md
Resumen (ES) / Abstract (EN)           → 00-preliminares.md
Tabla de contenidos                    → generada automáticamente por Pandoc
Lista de figuras                       → generada automáticamente por Pandoc
Lista de tablas                        → generada automáticamente por Pandoc

Capítulo 1 — Introducción
  1.1 Planteamiento del Problema
  1.2 Justificación
  1.3 Objetivos
      1.3.1 Objetivo General
      1.3.2 Objetivos Específicos
  1.4 Alcance y Limitaciones
  1.5 Metodología
  1.6 Estructura del Documento

Capítulo 2 — Marco de Referencia
  2.1 Marco Conceptual
  2.2 Estado del Arte
  2.3 Marco Tecnológico

Capítulo 3 — Análisis y Diseño del Sistema
  3.1 Proceso de Levantamiento de Requisitos
  3.2 Requisitos del Sistema
  3.3 Arquitectura del Sistema
  3.4 Diseño del Modelo de Datos
  3.5 Diseño de la Interfaz de Usuario

Capítulo 4 — Desarrollo e Implementación
  4.1 Metodología de Desarrollo
  4.2 Fases y Sprints de Desarrollo
  4.3 Implementación de Módulos Clave
  4.4 Estrategia y Resultados de Pruebas
  4.5 Infraestructura de Despliegue

Capítulo 5 — Resultados Técnicos
  5.1 Marco de la Validación Técnica
  5.2 Pruebas de Carga (Backend / API) — Locust
  5.3 Pruebas de Rendimiento (Frontend / Web Vitals)
  5.4 Síntesis de Cumplimiento de Requisitos No Funcionales
  5.5 Interpretación y Limitaciones

Capítulo 6 — Resultados de Usuarios
  6.1  Marco Metodológico de la Validación con Usuarios
  6.2  Caracterización de las Empresas Piloto
  6.3  Eficiencia Operativa (pre/post)
  6.4  Pruebas de Tareas Guiadas
  6.5  Encuesta de Usabilidad — SUS
  6.6  Satisfacción Específica (NPS y CSAT por módulo)
  6.7  Telemetría de Uso en Producción
  6.8  Hallazgos Cualitativos de las Entrevistas
  6.9  Validación de Hipótesis
  6.10 Limitaciones de la Validación con Usuarios

Capítulo 7 — Conclusiones y Trabajo Futuro
  7.1 Conclusiones por Objetivo
  7.2 Conclusión General
  7.3 Cumplimiento de Hipótesis
  7.4 Limitaciones del Proyecto
  7.5 Recomendaciones de Optimización
  7.6 Trabajo Futuro
  7.7 Reflexión Final

Referencias Bibliográficas

Anexo A — Manual de Usuario
Anexo B — Manual de Instalación y Despliegue
Anexo C — Documentación Técnica
```

---

## Pendientes para Completar el Informe

Los siguientes elementos requieren información real que no puede generarse automáticamente:

### Capítulo 5 (Resultados Técnicos) — Completo

- Resultados de carga con Locust (Test 01 a Test 06) y comportamiento por endpoint
- Resultados de rendimiento del frontend (Lighthouse, PageSpeed Insights, WebPageTest) por vista y por organización
- Síntesis de cumplimiento de RNF-01, RNF-02, RNF-07 y RNF-09
- **Pendiente menor**: registrar los datos formales de uptime mensual (RNF-02) desde el panel de Railway / Vercel cuando se cierre el período de medición

### Capítulo 6 (Resultados de Usuarios) — Borrador completo, datos pendientes

El borrador estructural está redactado con placeholders. Para completarlo se requieren los siguientes datos reales (ver `recomendaciones.md` para el protocolo de recolección):

- Caracterización de las tres empresas piloto: Frost Bitez, Miss Peggy y Empresa Placeholder (sector, empleados, herramientas previas)
- Tiempos pre/post para las cuatro tareas administrativas (por empresa y usuario)
- Auditoría de inventario pre/post (por empresa)
- Resultados de las pruebas de tareas guiadas (por usuario y tarea)
- Respuestas SUS crudas (10 ítems Likert 1–5 por usuario)
- Respuestas NPS (0–10) y CSAT por módulo (1–5) por usuario
- Datos de telemetría extraídos de la BD de producción (rango: 27 abr – 8 may 2026)
- Resúmenes o transcripciones de las entrevistas semiestructuradas de cierre
- Nombre definitivo de Empresa Placeholder

### Capítulo 7 (Conclusiones y Trabajo Futuro) — Borrador completo, dos puntos pendientes

- Sección 7.1 Objetivo 5: completar con los valores reales del Cap. 6 (reducción de tiempos, tasa de error, score SUS)
- Sección 7.5.4: completar con las sugerencias funcionales identificadas en las entrevistas del Cap. 6

### Portada y páginas iniciales

- Nombres completos de los autores — incluidos en `00-preliminares.md`
- Nombre de los directores — incluidos en `00-preliminares.md`
- Nombre de la universidad y programa — incluidos en `00-preliminares.md`
- Fecha de entrega — Abril 2026
- Nombres de los jurados evaluadores (asignados por la universidad)
- Número de páginas (tras consolidar en Word/PDF)

### Figuras y capturas de pantalla

- Insertar capturas de pantalla de la aplicación en el Manual de Usuario (Anexo A)
- Incluir gráficos y diagramas reales en el Capítulo 3 (diagrama ER con esquema actual de la BD)
- (Opcional) Añadir al Capítulo 5 una gráfica de la curva de degradación (tasa de fallos y P95 vs. escenario Test 01..06) construida a partir de los CSV de Locust
- Incluir gráficos de resultados con usuarios en el futuro Capítulo 6

---

## Notas de Estilo para la Versión Final

Al consolidar en Word/PDF, aplicar:

- Fuente: Times New Roman 12pt o Arial 11pt (según guía de la universidad).
- Interlineado: 1.5.
- Márgenes: superior e izquierdo 3cm, inferior y derecho 2.5cm (formato estándar colombiano; ajustar según institución).
- Numeración de páginas: en pie de página, centrado o derecha.
- Numeración de figuras y tablas: "Figura 3.1", "Tabla 4.2" (capítulo.número).
- Citas en el texto: formato APA 7.ª edición con autor-año entre paréntesis, ej. `(Bezemer & Zaidman, 2010)`.
- Todas las figuras y tablas deben tener título descriptivo y fuente.

