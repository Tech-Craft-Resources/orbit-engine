# Cronograma de Desarrollo
## Pecesaurio - Plataforma SaaS para Gestión de Pymes

**Proyecto de Grado**  
**Equipo:** 3 Integrantes  
**Duración:** 6 meses (Noviembre 2024 - Abril 2025)  
**Versión:** 1.0

---

## 1. Resumen Ejecutivo

Este cronograma establece la planificación completa del proyecto Pecesaurio desde su concepción hasta la entrega final. El proyecto se estructura en **6 fases principales** y **12 sprints de desarrollo** de 2 semanas cada uno, con un enfoque ágil que permite iteración y adaptación.

### Fechas Clave
- **Inicio del Proyecto:** 1 de Noviembre de 2024
- **Finalización de Desarrollo:** 31 de Marzo de 2025
- **Entrega Final:** 30 de Abril de 2025
- **Defensa del Proyecto:** Primera quincena de Mayo de 2025

---

## 2. Estructura del Equipo

### Roles y Responsabilidades

#### Integrante 1 - Backend Lead
- Arquitectura del sistema
- Desarrollo de APIs
- Modelos de IA/ML
- Base de datos

#### Integrante 2 - Frontend Lead
- Interfaz de usuario
- Experiencia de usuario
- Integración con APIs
- Diseño responsive

#### Integrante 3 - DevOps & Full Stack
- Infraestructura AWS
- CI/CD
- Monitoreo y logging
- Soporte en backend y frontend

**Nota:** Todos los integrantes contribuyen en testing, documentación y validación.

---

## 3. Metodología

### Framework Ágil - Scrum Adaptado

- **Sprint Duration:** 2 semanas
- **Sprint Planning:** Lunes al inicio del sprint (2 horas)
- **Daily Standups:** Martes, Jueves (15 minutos) - Asíncronos vía Slack/Discord
- **Sprint Review:** Viernes al final del sprint (1 hora)
- **Sprint Retrospective:** Viernes al final del sprint (30 minutos)

### Estimación
- **Story Points:** Escala Fibonacci (1, 2, 3, 5, 8, 13, 21)
- **Velocidad Estimada:** 15-20 story points por sprint (equipo de 3)
- **Horas por Integrante:** 15-20 horas/semana

---

## 4. Cronograma General

### Fase 1: Investigación y Planificación
**Duración:** 3 semanas  
**Fechas:** 1 de Noviembre - 22 de Noviembre de 2024

### Fase 2: Diseño y Arquitectura
**Duración:** 2 semanas  
**Fechas:** 25 de Noviembre - 6 de Diciembre de 2024

### Fase 3: Desarrollo Core (MVP)
**Duración:** 10 semanas (5 sprints)  
**Fechas:** 9 de Diciembre de 2024 - 21 de Febrero de 2025

### Fase 4: Desarrollo Avanzado y AI
**Duración:** 4 semanas (2 sprints)  
**Fechas:** 24 de Febrero - 21 de Marzo de 2025

### Fase 5: Testing, Validación y Refinamiento
**Duración:** 4 semanas  
**Fechas:** 24 de Marzo - 18 de Abril de 2025

### Fase 6: Documentación Final y Preparación de Defensa
**Duración:** 2 semanas  
**Fechas:** 21 de Abril - 30 de Abril de 2025

---

## 5. Cronograma Detallado por Fase

## FASE 1: INVESTIGACIÓN Y PLANIFICACIÓN
### Semanas: 1-3 (1 Nov - 22 Nov 2024)

#### Semana 1 (1-8 Nov)
**Objetivo:** Alineación del equipo y definición de alcance

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Kick-off del proyecto | Todos | Acta de inicio |
| Revisión de literatura sobre SaaS para pymes | Integrante 1 | Documento de estado del arte |
| Investigación de arquitecturas SaaS | Integrante 3 | Comparativa de arquitecturas |
| Análisis de plataformas existentes | Integrante 2 | Análisis competitivo |
| Definición preliminar de requisitos | Todos | Borrador de requisitos |

#### Semana 2 (11-15 Nov)
**Objetivo:** Levantamiento de requisitos y casos de uso

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Entrevistas con potenciales usuarios (pymes) | Integrante 2 | Notas de entrevistas |
| Definición de personas y escenarios | Integrante 2 | Documento de personas |
| Elaboración de historias de usuario | Todos | Backlog inicial |
| Investigación de modelos de ML para predicción | Integrante 1 | Propuesta de modelos IA |
| Setup de herramientas de colaboración | Integrante 3 | GitHub, Jira/Trello, Slack |

#### Semana 3 (18-22 Nov)
**Objetivo:** Planificación técnica y aprobación de propuesta

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Selección de stack tecnológico | Todos | Documento de stack |
| Estimación de historias de usuario | Todos | Backlog estimado |
| Definición de arquitectura preliminar | Integrante 1, 3 | Diagrama de arquitectura |
| Documentación de propuesta completa | Todos | Propuesta final |
| Presentación a asesor académico | Todos | Aprobación de propuesta |

**Entregables de Fase 1:**
- ✅ Propuesta de proyecto aprobada
- ✅ Backlog priorizado y estimado
- ✅ Documento de requisitos
- ✅ Documento de stack tecnológico
- ✅ Arquitectura preliminar

---

## FASE 2: DISEÑO Y ARQUITECTURA
### Semanas: 4-5 (25 Nov - 6 Dic 2024)

#### Semana 4 (25-29 Nov)
**Objetivo:** Diseño de sistema y base de datos

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Diseño detallado de base de datos | Integrante 1 | Diagrama ER |
| Diseño de API RESTful | Integrante 1 | Especificación OpenAPI |
| Wireframes de interfaz principal | Integrante 2 | Wireframes Figma/Sketch |
| Diseño de sistema de autenticación | Integrante 3 | Diagrama de flujo auth |
| Setup de infraestructura AWS inicial | Integrante 3 | VPC, RDS, S3 configurados |

#### Semana 5 (2-6 Dic)
**Objetivo:** Prototipos y configuración de entorno

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Prototipo de UI (mockups alta fidelidad) | Integrante 2 | Mockups en Figma |
| Setup de repositorios y estructura de proyecto | Todos | Repos configurados |
| Configuración de CI/CD básico | Integrante 3 | Pipeline GitHub Actions |
| Definición de estándares de código | Todos | Guía de estilo |
| Sprint Planning - Sprint 1 | Todos | Sprint backlog |

**Entregables de Fase 2:**
- ✅ Diseño de base de datos completo
- ✅ Especificación de API
- ✅ Mockups de interfaz aprobados
- ✅ Infraestructura base configurada
- ✅ Repositorios y CI/CD listos

---

## FASE 3: DESARROLLO CORE (MVP)
### Semanas: 6-15 (9 Dic 2024 - 21 Feb 2025)

### Sprint 1: Autenticación y Setup Base
**Duración:** 9-20 Diciembre 2024  
**Story Points:** 18

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-001: Registro de usuario | Backend Lead | 5 | Modelo User, endpoint POST /register, validaciones |
| HU-002: Inicio de sesión | Backend Lead | 5 | Endpoint POST /login, generación JWT |
| HU-003: Gestión de roles | Backend Lead | 5 | Modelo Role, middleware de permisos |
| Setup frontend base | Frontend Lead | 3 | Vite + React + TypeScript, routing, auth context |

**Entregables Sprint 1:**
- Backend: API de autenticación funcional con JWT
- Frontend: Login y registro UI
- Base de datos: Tablas users, roles
- Documentación: API docs de auth

---

### Sprint 2: Inventario Core - CRUD Productos
**Duración:** 6-17 Enero 2025 (post-vacaciones)  
**Story Points:** 17

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-005: Agregar producto | Backend + Frontend | 5 | Modelo Product, CRUD endpoints, formulario UI |
| HU-006: Editar producto | Backend + Frontend | 3 | PUT endpoint, formulario edición |
| HU-007: Ver lista productos | Backend + Frontend | 5 | GET con paginación, tabla con filtros |
| HU-008: Eliminar producto | Backend + Frontend | 2 | Soft delete, confirmación UI |
| Deploy inicial AWS | DevOps | 2 | EC2/ECS, RDS production |

**Entregables Sprint 2:**
- CRUD completo de productos
- Interfaz de gestión de inventario
- Deploy en AWS staging

---

### Sprint 3: Inventario Avanzado
**Duración:** 20-31 Enero 2025  
**Story Points:** 16

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-009: Alertas stock bajo | Backend + Frontend | 5 | Lógica de alertas, widget dashboard |
| HU-010: Ajuste manual inventario | Backend + Frontend | 5 | Endpoint ajuste, historial, formulario |
| HU-011: Historial movimientos | Backend + Frontend | 5 | Modelo MovementLog, tabla historial |
| Categorías de productos | Backend + Frontend | 1 | Modelo Category, CRUD básico |

**Entregables Sprint 3:**
- Sistema de alertas funcional
- Historial de movimientos
- Categorización implementada

---

### Sprint 4: Ventas Core
**Duración:** 3-14 Febrero 2025  
**Story Points:** 20

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-012: Registrar venta | Backend + Frontend | 8 | Modelo Sale, SaleItem, actualización stock, UI venta |
| HU-013: Ver historial ventas | Backend + Frontend | 5 | GET ventas con filtros, tabla |
| HU-014: Ver detalle venta | Backend + Frontend | 5 | GET venta/:id, vista detalle |
| Generación número factura | Backend | 2 | Secuencia automática |

**Entregables Sprint 4:**
- Módulo de ventas funcional
- Actualización automática de inventario
- Historial de ventas

---

### Sprint 5: Clientes
**Duración:** 17-28 Febrero 2025  
**Story Points:** 15

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-016: Agregar cliente | Backend + Frontend | 3 | Modelo Customer, CRUD endpoints, formulario |
| HU-017: Editar cliente | Backend + Frontend | 2 | PUT endpoint, UI edición |
| HU-018: Ver lista clientes | Backend + Frontend | 3 | GET con búsqueda, tabla |
| HU-019: Ver perfil cliente | Backend + Frontend | 5 | Vista perfil, stats, historial compras |
| Asociar ventas con clientes | Backend | 2 | Foreign key, modificar venta |

**Entregables Sprint 5:**
- Módulo de clientes completo
- Asociación ventas-clientes
- Estadísticas por cliente

---

## FASE 4: DESARROLLO AVANZADO Y AI
### Semanas: 16-19 (24 Feb - 21 Mar 2025)

### Sprint 6: Reportes y Dashboard
**Duración:** 3-14 Marzo 2025  
**Story Points:** 18

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-021: Dashboard principal | Backend + Frontend | 8 | Agregación de métricas, KPIs, widgets |
| HU-022: Reporte de ventas | Backend + Frontend | 5 | Endpoint reportes, filtros, gráficos |
| HU-023: Reporte de inventario | Backend + Frontend | 3 | Reporte stock, valor inventario |
| Exportación a Excel | Backend | 2 | Librería de exportación |

**Entregables Sprint 6:**
- Dashboard con KPIs principales
- Reportes de ventas e inventario
- Exportación de datos

---

### Sprint 7: Inteligencia Artificial - Predicción
**Duración:** 17-28 Marzo 2025  
**Story Points:** 21

| Historia de Usuario | Responsable | SP | Tareas Técnicas |
|--------------------|-------------|-----|-----------------|
| HU-025: Predicción de demanda | Backend Lead | 13 | Modelo ML (ARIMA/Prophet), entrenamiento, API |
| HU-026: Recomendaciones reabastecimiento | Backend Lead | 5 | Lógica de recomendación, cálculos |
| UI de predicciones | Frontend Lead | 3 | Visualizaciones, gráficos tendencias |

**Tareas de IA:**
1. Preparación de datos históricos
2. Selección de algoritmo (ARIMA, Prophet, o Regresión)
3. Entrenamiento de modelo
4. Validación de precisión
5. API endpoint para predicciones
6. Actualización automática (job diario)
7. Visualización de resultados

**Entregables Sprint 7:**
- Modelo de IA funcional
- API de predicciones
- UI de visualización de predicciones
- Job automático de actualización

---

## FASE 5: TESTING, VALIDACIÓN Y REFINAMIENTO
### Semanas: 20-23 (24 Mar - 18 Abr 2025)

#### Semana 20 (24-28 Mar)
**Objetivo:** Testing exhaustivo y corrección de bugs

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Pruebas unitarias (backend) | Backend Lead | Cobertura > 60% |
| Pruebas integración (API) | Backend + DevOps | Suite de tests |
| Pruebas E2E (frontend) | Frontend Lead | Tests Cypress/Playwright |
| Pruebas de carga | DevOps | Reporte de rendimiento |
| Corrección de bugs críticos | Todos | Sistema estable |

#### Semana 21 (31 Mar - 4 Abr)
**Objetivo:** Despliegue en producción y validación inicial

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Deploy a producción | DevOps | Sistema en producción |
| Configuración de monitoreo | DevOps | Dashboards CloudWatch/Datadog |
| Pruebas en producción | Todos | Checklist validado |
| Preparación de datos demo | Backend Lead | Base de datos demo |
| Onboarding de pymes piloto | Todos | 2 pymes registradas |

#### Semana 22 (7-11 Abr)
**Objetivo:** Pruebas con usuarios reales

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Capacitación a usuarios piloto | Frontend Lead | Sesiones training |
| Soporte a usuarios durante pruebas | Todos | Tickets resueltos |
| Recolección de feedback | Frontend Lead | Encuestas y notas |
| Recolección de métricas | Backend Lead | Datos de uso |
| Ajustes rápidos según feedback | Todos | Hotfixes |

#### Semana 23 (14-18 Abr)
**Objetivo:** Análisis de resultados y mejoras finales

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Análisis de datos de uso | Backend Lead | Informe de métricas |
| Validación de hipótesis | Todos | Análisis estadístico |
| Mejoras de UX críticas | Frontend Lead | Refinamientos |
| Optimización de rendimiento | Backend + DevOps | Performance mejorado |
| Backup y seguridad final | DevOps | Sistema asegurado |

**Entregables de Fase 5:**
- ✅ Sistema probado exhaustivamente
- ✅ Producción estable y monitoreada
- ✅ Validación con usuarios reales
- ✅ Métricas de éxito recolectadas
- ✅ Feedback procesado

---

## FASE 6: DOCUMENTACIÓN FINAL Y PREPARACIÓN DE DEFENSA
### Semanas: 24-25 (21-30 Abril 2025)

#### Semana 24 (21-25 Abr)
**Objetivo:** Documentación técnica completa

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Documentación de API final | Backend Lead | API docs publicada |
| Manual de usuario | Frontend Lead | Manual PDF/web |
| Manual técnico de instalación | DevOps | Guía de deploy |
| Documentación de arquitectura | Backend + DevOps | Diagramas actualizados |
| README completo del proyecto | Todos | README.md |
| Video demo del sistema | Frontend Lead | Video 5-10 min |

#### Semana 25 (28-30 Abr)
**Objetivo:** Documento final y preparación de defensa

| Tarea | Responsable | Entregable |
|-------|-------------|------------|
| Redacción de documento final | Todos | Documento de grado |
| Análisis de resultados y conclusiones | Todos | Capítulo de resultados |
| Preparación de presentación | Todos | Slides defensa |
| Ensayo de defensa | Todos | Presentación pulida |
| Entrega de documentos | Todos | Documentos oficiales |

**Entregables de Fase 6:**
- ✅ Documento de proyecto de grado completo
- ✅ Presentación de defensa
- ✅ Video demo
- ✅ Documentación técnica completa
- ✅ Manual de usuario

---

## 6. Calendario Visual

### Noviembre 2024
```
Sem 1: [====Investigación====]
Sem 2: [====Requisitos====]
Sem 3: [====Planificación====]
Sem 4: [====Diseño====]
```

### Diciembre 2024
```
Sem 1: [====Diseño====]
Sem 2: [Sprint 1: Auth]
Sem 3: [Sprint 1: Auth]
Sem 4: VACACIONES
```

### Enero 2025
```
Sem 1: VACACIONES
Sem 2: [Sprint 2: Inventario]
Sem 3: [Sprint 2: Inventario]
Sem 4: [Sprint 3: Inv Avanzado]
Sem 5: [Sprint 3: Inv Avanzado]
```

### Febrero 2025
```
Sem 1: [Sprint 4: Ventas]
Sem 2: [Sprint 4: Ventas]
Sem 3: [Sprint 5: Clientes]
Sem 4: [Sprint 5: Clientes]
```

### Marzo 2025
```
Sem 1: [Sprint 6: Reportes]
Sem 2: [Sprint 6: Reportes]
Sem 3: [Sprint 7: IA]
Sem 4: [Sprint 7: IA]
Sem 5: [====Testing====]
```

### Abril 2025
```
Sem 1: [====Validación====]
Sem 2: [====Pruebas Usuario====]
Sem 3: [====Refinamiento====]
Sem 4: [====Documentación====]
Sem 5: [====Entrega====]
```

---

## 7. Hitos Principales (Milestones)

| # | Hito | Fecha | Criterio de Éxito |
|---|------|-------|-------------------|
| M1 | Propuesta Aprobada | 22 Nov 2024 | Aprobación del asesor |
| M2 | Diseño Completado | 6 Dic 2024 | Mockups y arquitectura aprobados |
| M3 | Autenticación Funcional | 20 Dic 2024 | Login/registro operativo |
| M4 | MVP Core Completado | 21 Feb 2025 | Inventario + Ventas + Clientes |
| M5 | IA Integrada | 28 Mar 2025 | Predicciones funcionando |
| M6 | Validación Completada | 18 Abr 2025 | Pruebas con usuarios finalizadas |
| M7 | Entrega Final | 30 Abr 2025 | Documentos entregados |
| M8 | Defensa | Mayo 2025 | Presentación exitosa |

---

## 8. Gestión de Riesgos en el Cronograma

### Buffers Incluidos

1. **Buffer de Desarrollo:** 2 semanas adicionales distribuidas
   - Complejidad mayor a la estimada
   - Bugs críticos inesperados

2. **Buffer de Validación:** 4 semanas para pruebas
   - Tiempo para iterar según feedback
   - Margen para problemas con usuarios piloto

3. **Buffer Académico:** Vacaciones de diciembre-enero consideradas
   - Carga académica de otros cursos

### Plan de Contingencia

| Riesgo | Impacto en Cronograma | Plan de Mitigación |
|--------|----------------------|-------------------|
| Atraso en sprint | +2 semanas | Reducir alcance de features no críticas |
| Problemas con IA | +3 semanas | Modelo más simple (regresión lineal) |
| Pérdida de integrante | +4 semanas | Redistribución de tareas, extensión |
| AWS problemas/costos | +1 semana | Migrar a servicios alternativos |
| Pymes piloto no disponibles | 0 | Usar datos sintéticos para validación |

---

## 9. Ceremonias y Reuniones

### Reuniones Regulares

| Reunión | Frecuencia | Duración | Asistentes | Objetivo |
|---------|-----------|----------|------------|----------|
| Daily Standup | Martes, Jueves | 15 min | Todos | Sincronización |
| Sprint Planning | Inicio de sprint | 2 horas | Todos | Planificar sprint |
| Sprint Review | Fin de sprint | 1 hora | Todos | Demostrar trabajo |
| Sprint Retrospective | Fin de sprint | 30 min | Todos | Mejora continua |
| Reunión con Asesor | Quincenal | 1 hora | Todos + Asesor | Seguimiento académico |

### Comunicación Asíncrona

- **Slack/Discord:** Comunicación diaria
- **GitHub:** Code reviews, PRs, issues
- **Notion/Confluence:** Documentación compartida
- **Google Meet/Zoom:** Reuniones virtuales

---

## 10. Métricas de Seguimiento

### Métricas de Desarrollo

| Métrica | Frecuencia | Objetivo |
|---------|-----------|----------|
| Story Points completados | Por sprint | 15-20 SP |
| Velocidad del equipo | Por sprint | Estable |
| Bugs abiertos | Semanal | < 10 |
| Cobertura de tests | Continua | > 60% |
| Deuda técnica | Por sprint | Controlada |

### Métricas de Proyecto

| Métrica | Frecuencia | Objetivo |
|---------|-----------|----------|
| % Completado del backlog | Semanal | Según plan |
| Desviación del cronograma | Semanal | < 1 semana |
| Asistencia a reuniones | Por reunión | 100% |
| Horas dedicadas por persona | Semanal | 15-20h |

---

## 11. Dependencias Críticas

### Externas
- Aprobación de propuesta por asesor (M1)
- Acceso a AWS (o créditos educativos)
- Disponibilidad de pymes para pruebas piloto
- Herramientas de desarrollo (cuentas, licencias)

### Internas
- Autenticación debe estar lista antes de cualquier módulo (Sprint 1)
- Inventario debe estar antes de ventas
- Ventas debe estar antes de reportes y IA
- IA requiere mínimo 3 meses de datos (o sintéticos)

---

## 12. Entregables por Mes

### Noviembre 2024
- ✅ Propuesta aprobada
- ✅ Requisitos definidos
- ✅ Stack tecnológico seleccionado

### Diciembre 2024
- ✅ Diseño completo
- ✅ Infraestructura configurada
- ✅ Autenticación funcional

### Enero 2025
- ✅ Módulo de inventario completo
- ✅ Deploy inicial en AWS

### Febrero 2025
- ✅ Módulo de ventas funcional
- ✅ Módulo de clientes funcional
- ✅ MVP Core completado

### Marzo 2025
- ✅ Reportes y dashboard
- ✅ IA de predicción integrada
- ✅ Testing completo

### Abril 2025
- ✅ Validación con usuarios
- ✅ Documentación final
- ✅ Entrega y defensa

---

## 13. Checklist de Finalización del Proyecto

### Técnico
- [ ] Código en repositorio con commits regulares
- [ ] Tests automatizados (> 60% cobertura)
- [ ] Sistema desplegado en AWS producción
- [ ] API documentada con OpenAPI
- [ ] Monitoreo y logging configurado
- [ ] Backups automatizados funcionando
- [ ] Seguridad validada (OWASP)

### Funcional
- [ ] Todos los módulos MVP operativos
- [ ] IA de predicción funcionando
- [ ] Dashboard con métricas
- [ ] Exportación de reportes
- [ ] Roles y permisos implementados

### Validación
- [ ] Pruebas con 2+ pymes completadas
- [ ] Métricas de éxito recolectadas
- [ ] Feedback de usuarios procesado
- [ ] Hipótesis validadas con datos

### Documentación
- [ ] Manual de usuario
- [ ] Manual técnico
- [ ] Documento de proyecto de grado
- [ ] Presentación de defensa
- [ ] Video demo

### Académico
- [ ] Aprobación del asesor
- [ ] Documentos entregados oficialmente
- [ ] Presentación preparada
- [ ] Ensayo de defensa realizado

---

## Conclusión

Este cronograma ha sido diseñado considerando:
- Equipo de 3 personas con dedicación parcial
- Timeline realista de 6 meses
- Metodología ágil con flexibilidad
- Buffers para contingencias
- Vacaciones y carga académica

El éxito del proyecto dependerá de:
✅ Disciplina en seguir las ceremonias ágiles  
✅ Comunicación constante del equipo  
✅ Priorización correcta del backlog  
✅ Gestión proactiva de riesgos  
✅ Enfoque en el MVP sin desviaciones  

**¡Manos a la obra! 🚀**

---

**Elaborado por:** Equipo Pecesaurio  
**Fecha:** Octubre 2024  
**Versión:** 1.0  
**Próxima Revisión:** Fin de cada sprint

