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

| Archivo | Contenido | Estado |
|---------|-----------|--------|
| [00-preliminares.md](00-preliminares.md) | Portada, página de aprobación, resumen (ES) y abstract (EN) | ✅ Borrador completo |
| [capitulo-1-introduccion.md](capitulo-1-introduccion.md) | Planteamiento del problema, justificación, objetivos, alcance, metodología | ✅ Borrador completo |
| [capitulo-2-marco-referencia.md](capitulo-2-marco-referencia.md) | Marco conceptual, estado del arte, marco tecnológico | ✅ Borrador completo |
| [capitulo-3-analisis-diseno.md](capitulo-3-analisis-diseno.md) | Requisitos, arquitectura, modelo de datos, diseño de UI | ✅ Borrador completo |
| [capitulo-4-desarrollo.md](capitulo-4-desarrollo.md) | Metodología ágil, sprints, implementación, pruebas, CI/CD | ✅ Borrador completo |
| [capitulo-5-resultados.md](capitulo-5-resultados.md) | Resultados de rendimiento, usabilidad, validación de hipótesis | ⚠️ Requiere datos reales |
| [capitulo-6-conclusiones.md](capitulo-6-conclusiones.md) | Conclusiones por objetivo, limitaciones, trabajo futuro | ⚠️ Requiere datos del Cap. 5 |
| [referencias.md](referencias.md) | Referencias bibliográficas en formato APA 7.ª edición | ✅ Borrador completo |
| [anexo-a-manual-usuario.md](anexo-a-manual-usuario.md) | Manual de uso para usuarios finales (no técnico) | ✅ Borrador completo |
| [anexo-b-manual-despliegue.md](anexo-b-manual-despliegue.md) | Guía técnica de instalación y despliegue | ✅ Borrador completo |
| [anexo-c-documentacion-tecnica.md](anexo-c-documentacion-tecnica.md) | Documentación técnica profesional: API, modelos, variables de entorno, convenciones | ✅ Borrador completo |

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

Capítulo 5 — Resultados y Validación
  5.1 Descripción del Experimento de Validación
  5.2 Resultados de Rendimiento del Sistema
  5.3 Resultados de Eficiencia Operativa
  5.4 Resultados de Usabilidad
  5.5 Validación de Hipótesis
  5.6 Discusión

Capítulo 6 — Conclusiones y Trabajo Futuro
  6.1 Conclusiones por Objetivo
  6.2 Conclusión General
  6.3 Limitaciones del Proyecto
  6.4 Trabajo Futuro

Referencias Bibliográficas

Anexo A — Manual de Usuario
Anexo B — Manual de Instalación y Despliegue
Anexo C — Documentación Técnica
```

---

## Pendientes para Completar el Informe

Los siguientes elementos requieren información real que no puede generarse automáticamente:

### Capítulo 5 (Resultados) — Prioridad Alta
- [ ] Datos de las empresas piloto (nombre, sector, número de empleados)
- [ ] Tiempos medidos de tareas administrativas antes/después de la implementación
- [ ] Puntajes de la encuesta SUS (System Usability Scale) por usuario
- [ ] Feedback cualitativo de las entrevistas de cierre
- [ ] Datos de disponibilidad y tiempos de respuesta reales en producción
- [ ] Reporte de cobertura de pruebas (reemplazar valores de ejemplo con `pytest --cov`)

### Capítulo 6 (Conclusiones) — Requiere Cap. 5 completo
- [ ] Completar la sección 6.1 para el Objetivo 6 con los resultados reales
- [ ] Ajustar las conclusiones generales según los resultados obtenidos

### Portada y páginas iniciales
- [x] Nombres completos de los autores — incluidos en `00-preliminares.md`
- [x] Nombre de los directores — incluidos en `00-preliminares.md`
- [x] Nombre de la universidad y programa — incluidos en `00-preliminares.md`
- [x] Fecha de entrega — Abril 2026
- [ ] Nombres de los jurados evaluadores (asignados por la universidad)
- [ ] Número de páginas (tras consolidar en Word/PDF)

### Figuras y capturas de pantalla
- [ ] Insertar capturas de pantalla de la aplicación en el Manual de Usuario (Anexo A)
- [ ] Incluir gráficos y diagramas reales en el Capítulo 3 (diagrama ER con esquema actual de la BD)
- [ ] Incluir gráficos de resultados de validación en el Capítulo 5

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
