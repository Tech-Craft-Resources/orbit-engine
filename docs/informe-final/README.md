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


| Archivo                                                              | Contenido                                                                                                             | Estado                                                      |
| -------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| [00-preliminares.md](00-preliminares.md)                             | Portada, página de aprobación, resumen (ES) y abstract (EN)                                                           | ✅ Borrador completo                                         |
| [capitulo-1-introduccion.md](capitulo-1-introduccion.md)             | Planteamiento del problema, justificación, objetivos, alcance, metodología                                            | ✅ Borrador completo                                         |
| [capitulo-2-marco-referencia.md](capitulo-2-marco-referencia.md)     | Marco conceptual, estado del arte, marco tecnológico                                                                  | ✅ Borrador completo                                         |
| [capitulo-3-analisis-diseno.md](capitulo-3-analisis-diseno.md)       | Requisitos, arquitectura, modelo de datos, diseño de UI                                                               | ✅ Borrador completo                                         |
| [capitulo-4-desarrollo.md](capitulo-4-desarrollo.md)                 | Metodología ágil, sprints, implementación, pruebas, CI/CD                                                             | ✅ Borrador completo                                         |
| [capitulo-5-resultados-tecnicos.md](capitulo-5-resultados-tecnicos.md) | **Resultados Técnicos**: pruebas de carga (Locust) y de rendimiento web (Lighthouse, PageSpeed Insights, WebPageTest) | ✅ Borrador completo                                         |
| *(pendiente)* Capítulo 6 — Resultados de Usuarios                    | Eficiencia operativa, completitud de tareas, encuesta SUS, validación de hipótesis con empresas piloto                | 🟡 Por redactar (capítulo nuevo)                            |
| [capitulo-6-conclusiones.md](capitulo-6-conclusiones.md)             | Conclusiones por objetivo, limitaciones, trabajo futuro                                                               | ⚠️ Requiere datos del nuevo Cap. 6 (Resultados de Usuarios) |
| [referencias.md](referencias.md)                                     | Referencias bibliográficas en formato APA 7.ª edición                                                                 | ✅ Borrador completo                                         |
| [anexo-a-manual-usuario.md](anexo-a-manual-usuario.md)               | Manual de uso para usuarios finales (no técnico)                                                                      | ✅ Borrador completo                                         |
| [anexo-b-manual-despliegue.md](anexo-b-manual-despliegue.md)         | Guía técnica de instalación y despliegue                                                                              | ✅ Borrador completo                                         |
| [anexo-c-documentacion-tecnica.md](anexo-c-documentacion-tecnica.md) | Documentación técnica profesional: API, modelos, variables de entorno, convenciones                                   | ✅ Borrador completo                                         |


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

Capítulo 6 — Resultados de Usuarios  [pendiente — se redactará más adelante]
  Eficiencia operativa, completitud de tareas, encuesta SUS y
  validación de hipótesis con empresas piloto.

Capítulo (final) — Conclusiones y Trabajo Futuro
  Conclusiones por Objetivo
  Conclusión General
  Limitaciones del Proyecto
  Trabajo Futuro

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

### Capítulo 6 (Resultados de Usuarios) — Por redactar

Capítulo nuevo, separado del Cap. 5 técnico. Requiere los siguientes insumos:

- Datos de las empresas piloto (nombre, sector, número de empleados)
- Tiempos medidos de tareas administrativas antes/después de la implementación
- Puntajes de la encuesta SUS (System Usability Scale) por usuario
- Feedback cualitativo de las entrevistas de cierre
- Validación de las hipótesis del proyecto con base en los datos anteriores

### Capítulo de Conclusiones — Requiere Cap. 6 (Resultados de Usuarios) completo

- Completar las conclusiones por objetivo con los resultados de usuarios
- Trasladar a este capítulo las recomendaciones de optimización derivadas del Cap. 5 (paginación de `/sales/`, caché de `/dashboard/stats`, optimización de activos del frontend, plan de escalado horizontal)
- Ajustar la conclusión general en función de los resultados obtenidos

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

