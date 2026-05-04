# Capítulo 6 — Resultados de Usuarios

> **Alcance de este capítulo.** Las secciones que siguen presentan exclusivamente los resultados de la **validación con usuarios reales**: eficiencia operativa, completitud de tareas, usabilidad percibida, satisfacción y hallazgos cualitativos de las entrevistas. Los **resultados de la validación técnica** (pruebas de carga con Locust y rendimiento web con Lighthouse / PageSpeed Insights / WebPageTest) se encuentran en el **Capítulo 5 — Resultados Técnicos**. Las **acciones de mejora** derivadas de los hallazgos aquí descritos —tanto técnicas como funcionales— se presentan en el **Capítulo 7 — Conclusiones y Trabajo Futuro**.

---

## 6.1 Marco Metodológico de la Validación con Usuarios

### 6.1.1 Objetivos

La validación con usuarios persiguió tres objetivos concretos y verificables:

1. **Medir el impacto en la eficiencia operativa** de las empresas participantes antes y después de la adopción de OrbitEngine, cuantificando la reducción de tiempos en tareas administrativas clave y la variación en la tasa de error en operaciones de inventario.
2. **Evaluar la usabilidad del sistema** mediante el instrumento estandarizado *System Usability Scale* (SUS) y pruebas de tareas guiadas con usuarios reales, determinando si el sistema supera el umbral de usabilidad aceptable establecido en la literatura.
3. **Caracterizar la satisfacción específica por módulo** mediante NPS (*Net Promoter Score*) y CSAT (*Customer Satisfaction Score*), e identificar hallazgos cualitativos relevantes a través de entrevistas semiestructuradas de cierre.

### 6.1.2 Diseño de Investigación

El presente estudio adoptó un **diseño de estudio de caso múltiple** (Yin, 2018) con componente **cuasi-experimental de tipo pre/post** (Campbell & Stanley, 1963). Se eligió este diseño porque:

- El número de empresas disponibles (N = 3) impide inferencia estadística a la población y hace inadecuado un diseño experimental aleatorizado.
- Las empresas participantes son pymes reales con operaciones activas; no es posible asignarlas aleatoriamente a condiciones de tratamiento o control.
- El interés científico radica en comprender **cómo y en qué medida** cambia la eficiencia operativa al adoptar el sistema, más que en establecer causalidad universal.

El enfoque es **mixto** (Creswell & Plano Clark, 2018): combina datos cuantitativos (tiempos pre/post, tasas de error, scores SUS/NPS/CSAT, telemetría) con datos cualitativos (entrevistas semiestructuradas con codificación temática), siendo los cualitativos confirmatorios y explicativos de los cuantitativos.

**Nota sobre el cambio de N respecto al Capítulo 5.** Las pruebas técnicas del Capítulo 5 se ejecutaron cuando la plataforma contaba con **dos empresas reales** en producción (Frozt Bitez y Miss Peggy). En el intervalo transcurrido entre el cierre de esas pruebas y el inicio de la Fase 5 de validación con usuarios (27 de abril de 2026), se incorporó una **tercera empresa real** —denominada Empresa Placeholder en este borrador, pendiente de confirmación del nombre definitivo— que también participó en el estudio de caso. El piloto de usuarios reales comprende, por tanto, **N = 3 empresas**.

### 6.1.3 Participantes

**Criterios de inclusión:**
- Empresa pyme del sector comercio o servicios con operaciones activas en Colombia.
- Disposición a registrar datos reales de inventario, ventas y clientes en la plataforma durante la Fase 5.
- Al menos un usuario designado con rol Administrador y al menos un usuario con rol Vendedor.
- Consentimiento informado firmado por el representante legal o dueño de la empresa.

**Criterios de exclusión:**
- Empresas sin acceso a internet estable (requisito técnico de la plataforma).
- Empresas en proceso de cierre o reestructuración durante el período de validación.

**Muestra resultante:** tres empresas (N = 3), con un total de [pendiente: número total de usuarios participantes] usuarios individuales distribuidos entre las tres organizaciones.

### 6.1.4 Instrumentos

| Instrumento | Tipo | Propósito | Momento de aplicación |
|---|---|---|---|
| **SUS** (*System Usability Scale*) | Cuantitativo | Evaluar la usabilidad percibida del sistema (score 0–100) | Post-uso, al cierre de la Fase 5 |
| **NPS** (*Net Promoter Score*) | Cuantitativo | Medir la probabilidad de recomendación del sistema (0–10) | Post-uso, al cierre de la Fase 5 |
| **CSAT por módulo** | Cuantitativo | Satisfacción específica con cada módulo del sistema (1–5) | Post-uso, al cierre de la Fase 5 |
| **Pruebas de tareas guiadas** | Cuantitativo / observacional | Medir completitud, tiempo y errores en tareas representativas | Durante la Fase 5 |
| **Entrevistas semiestructuradas** | Cualitativo | Explorar impacto percibido, dificultades y sugerencias | Al cierre de la Fase 5 |
| **Telemetría productiva** | Cuantitativo | Registrar uso real del sistema en producción | Continuo durante la Fase 5 |
| **Registro de tiempos pre/post** | Cuantitativo | Comparar duración de tareas administrativas antes y después | Pre-implementación (retrospectivo) y durante la Fase 5 |
| **Registro de errores de inventario** | Cuantitativo | Medir tasa de discrepancias antes y después | Pre-implementación (retrospectivo) y durante la Fase 5 |

### 6.1.5 Procedimiento y Cronograma (Fase 5)

La Fase 5 de validación con usuarios se ejecutó entre el **27 de abril de 2026** y el **8 de mayo de 2026** (dos semanas calendario). El procedimiento siguió las etapas que se describen a continuación:

**Semana 1 (27 abril – 1 mayo 2026):**
1. Firma de consentimiento informado con el representante de cada empresa.
2. Sesión de onboarding y carga inicial de datos (productos, clientes, stock inicial).
3. Registro retrospectivo de tiempos pre-implementación mediante entrevista estructurada con el usuario principal de cada empresa.
4. Inicio del uso productivo real con la plataforma.

**Semana 2 (4 mayo – 8 mayo 2026):**
1. Sesión de pruebas de tareas guiadas con cada usuario participante (duración estimada: 45–60 minutos por sesión).
2. Aplicación de la encuesta SUS (10 ítems, 5–10 minutos).
3. Aplicación del NPS y el CSAT por módulo (5 minutos).
4. Entrevista semiestructurada de cierre (20–30 minutos por empresa).
5. Extracción de datos de telemetría de la base de datos de producción.

### 6.1.6 Hipótesis a Contrastar

A partir del diseño cuasi-experimental descrito en la sección 1.2.3 del Capítulo 1, se formalizan las siguientes hipótesis de investigación:

> **H1 — Hipótesis de Eficiencia Operativa**
> La adopción de OrbitEngine reduce en al menos un 30% el tiempo dedicado a tareas administrativas clave (registro de ventas, actualización de inventario y generación de reportes) en las empresas piloto, medido como diferencia entre el tiempo promedio pre-implementación y el tiempo promedio post-implementación para el mismo conjunto de tareas.

> **H2 — Hipótesis de Precisión en Inventario**
> La adopción de OrbitEngine reduce en al menos un 40% la tasa de discrepancias entre el stock físico y el registrado en las empresas piloto, medida como proporción de ítems con discrepancia sobre el total de ítems auditados, antes y después de la implementación.

> **H3 — Hipótesis de Usabilidad**
> OrbitEngine obtiene un puntaje SUS promedio superior a 68 puntos (umbral de usabilidad "aceptable" según Bangor et al., 2008) en la evaluación con usuarios de las empresas piloto, indicando que el sistema es percibido como usable por el segmento objetivo.

### 6.1.7 Consideraciones Éticas

La validación con usuarios se desarrolló bajo los siguientes principios éticos:

- **Consentimiento informado**: todos los participantes firmaron un formulario de consentimiento antes de iniciar cualquier actividad de recolección de datos. El formulario explicitó el propósito del estudio, el uso que se daría a los datos y el derecho a retirarse sin consecuencias.
- **Anonimización**: los datos individuales de desempeño (tiempos de tarea, errores observados, respuestas a encuestas) se presentan de forma agregada. Las citas textuales se atribuyen únicamente a la empresa (no al individuo) salvo autorización explícita.
- **Protección de información comercial**: los datos operativos de las empresas (inventario, ventas, clientes) son propiedad de cada organización. Solo se reportan métricas derivadas y agregadas; no se incluyen datos nominales de clientes ni precios específicos de productos.
- **Conflicto de interés**: el equipo investigador es el mismo que desarrolló la plataforma. Esta limitación se reconoce explícitamente en la sección 6.10 y se mitiga mediante el uso de instrumentos estandarizados (SUS, NPS) y protocolos de entrevista predefinidos.
- **Posibilidad de retiro**: cualquier empresa pudo retirarse del estudio en cualquier momento sin que ello afectara su acceso continuado a la plataforma.

---

## 6.2 Caracterización de las Empresas Piloto

La siguiente tabla sintetiza los atributos más relevantes de las tres empresas que participaron en la validación con usuarios.

**Tabla 6.2.1.** Caracterización de las empresas piloto del estudio de caso.

| Atributo | Frozt Bitez | Miss Peggy | Empresa Placeholder |
|---|---|---|---|
| **Sector** | [pendiente: sector de Frozt Bitez] | [pendiente: sector de Miss Peggy] | [pendiente: sector de Empresa Placeholder] |
| **Antigüedad de la empresa** | [pendiente] | [pendiente] | [pendiente] |
| **Número de empleados** | [pendiente] | [pendiente] | [pendiente] |
| **Número de usuarios participantes en el estudio** | [pendiente] | [pendiente] | [pendiente] |
| **Roles representados** | [pendiente: Administrador / Vendedor / Visualizador] | [pendiente] | [pendiente] |
| **Rol del informante principal** | [pendiente: dueño / gerente / encargado] | [pendiente] | [pendiente] |
| **Herramientas de gestión previas** | [pendiente: Excel / cuaderno / ninguna / software previo] | [pendiente] | [pendiente] |
| **Incorporación al piloto** | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5 | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5 | Fase 5 (27 abr 2026) — incorporada entre el cierre del Cap. 5 y el inicio de la validación con usuarios |

> **Nota sobre Empresa Placeholder.** Esta empresa se incorporó a la plataforma OrbitEngine en el período comprendido entre el cierre de las pruebas técnicas del Capítulo 5 y el inicio de la Fase 5 de validación con usuarios. Su nombre definitivo se registrará en la versión final de este capítulo una vez confirmado por el representante de la organización.

---

## 6.3 Eficiencia Operativa (pre/post)

### 6.3.1 Tiempos en Tareas Administrativas

Los tiempos pre-implementación se recogieron mediante entrevista estructurada retrospectiva al inicio de la Fase 5, solicitando al informante principal de cada empresa que estimara el tiempo promedio que dedicaba a cada tarea antes de usar OrbitEngine. Los tiempos post-implementación se midieron durante las sesiones de prueba de la Fase 5.

**Tabla 6.3.1.** Comparación de tiempos medios por tarea administrativa (minutos).

| Tarea | Empresa | Tiempo pre (min) | Tiempo post (min) | Reducción (%) |
|---|---|---|---|---|
| Registro de una venta | Frozt Bitez | [pendiente] | [pendiente] | [pendiente] |
| Registro de una venta | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Registro de una venta | Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] |
| Actualización de stock (un producto) | Frozt Bitez | [pendiente] | [pendiente] | [pendiente] |
| Actualización de stock (un producto) | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Actualización de stock (un producto) | Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] |
| Generación de reporte de ventas semanal | Frozt Bitez | [pendiente] | [pendiente] | [pendiente] |
| Generación de reporte de ventas semanal | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Generación de reporte de ventas semanal | Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] |
| Consulta de historial de un cliente | Frozt Bitez | [pendiente] | [pendiente] | [pendiente] |
| Consulta de historial de un cliente | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Consulta de historial de un cliente | Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] |
| **Promedio global** | **Todas** | **[pendiente]** | **[pendiente]** | **[pendiente]** |

### 6.3.2 Tasa de Error en Operaciones de Inventario

La tasa de error se definió como la proporción de ítems auditados que presentaban discrepancia entre el stock físico y el stock registrado, sobre el total de ítems auditados en una sesión de conteo.

**Tabla 6.3.2.** Tasa de error en inventario antes y después de la implementación.

| Empresa | Ítems auditados (pre) | Discrepancias (pre) | Tasa de error pre (%) | Ítems auditados (post) | Discrepancias (post) | Tasa de error post (%) | Reducción (pp) |
|---|---|---|---|---|---|---|---|
| Frozt Bitez | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| **Promedio** | | | **[pendiente]** | | | **[pendiente]** | **[pendiente]** |

> **Nota metodológica.** Los datos pre-implementación de tasa de error en inventario son de naturaleza retrospectiva y auto-reportada. Las limitaciones de este tipo de medición se discuten en la sección 6.10.

### 6.3.3 Síntesis Cuantitativa de la Mejora

[pendiente: redactar párrafo de síntesis con los valores definitivos de la tabla 6.3.1 y 6.3.2. Indicar si se cumple o supera el umbral del 30% para H1 y del 40% para H2. Comparar con los benchmarks de la literatura citados en el Capítulo 1 (Kumar & van Hillegersberg, 2000; Duan et al., 2012).]

---

## 6.4 Pruebas de Tareas Guiadas

Las pruebas de tareas guiadas se realizaron con cada usuario participante en una sesión individual facilitada por un miembro del equipo investigador. Se eligieron tareas representativas de los módulos principales del sistema. Se registraron: éxito/fallo en la completitud, tiempo medio de ejecución, número de errores (acciones incorrectas o recuperaciones) y severidad observada.

**Escala de severidad de errores**: 0 = sin errores; 1 = error leve (usuario se recupera solo en < 30 s); 2 = error moderado (requiere ayuda del facilitador); 3 = error crítico (tarea no completada).

**Tabla 6.4.1.** Resultados de las pruebas de tareas guiadas (agregado por tarea).

| # | Tarea | Usuarios que completaron (n / total) | Tasa de éxito (%) | Tiempo medio (s) | Errores observados (media) | Severidad máxima |
|---|---|---|---|---|---|---|
| T1 | Iniciar sesión y navegar al Dashboard | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T2 | Crear un producto nuevo en inventario | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T3 | Registrar un movimiento de entrada de stock | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T4 | Registrar una venta nueva (múltiples productos) | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T5 | Consultar el historial de ventas con filtro de fechas | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T6 | Buscar un cliente y revisar su historial de compras | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T7 | Exportar el listado de inventario a Excel | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| T8 | Crear un usuario nuevo con rol Vendedor | [pendiente] / [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |

[pendiente: agregar párrafo narrativo destacando las tareas con mayor y menor tasa de éxito, y los patrones de error más frecuentes observados.]

---

## 6.5 Encuesta de Usabilidad — SUS

### 6.5.1 Score por Usuario y Agregado por Empresa

El instrumento SUS (*System Usability Scale*, Brooke, 1996) consiste en diez afirmaciones con respuesta en escala Likert de 1 a 5. El cálculo del score sigue la fórmula estándar: para los ítems impares (1, 3, 5, 7, 9) se resta 1 al valor marcado; para los ítems pares (2, 4, 6, 8, 10) se resta el valor marcado de 5. La suma de los diez valores ajustados se multiplica por 2.5, produciendo un score en el rango [0, 100].

**Tabla 6.5.1.a.** Scores SUS individuales por usuario.

| Empresa | Usuario | Ítem 1 | Ítem 2 | Ítem 3 | Ítem 4 | Ítem 5 | Ítem 6 | Ítem 7 | Ítem 8 | Ítem 9 | Ítem 10 | **Score SUS** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frozt Bitez | U1 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Frozt Bitez | U2 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Miss Peggy | U3 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Miss Peggy | U4 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Empresa Placeholder | U5 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Empresa Placeholder | U6 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |

> *[p] = pendiente de datos reales. Los números de usuarios por empresa (U1–U6) son indicativos; ajustar según la cantidad real de participantes.*

**Tabla 6.5.1.b.** Score SUS agregado por empresa.

| Empresa | N usuarios | Score SUS medio | Clasificación (Bangor et al., 2008) |
|---|---|---|---|
| Frozt Bitez | [pendiente] | [pendiente] | [pendiente: Excelente ≥ 85.5 / Bueno 72.5–85.4 / Aceptable 52–72.4 / Marginal < 52] |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] |

### 6.5.2 Score Global del Piloto vs. Benchmark 68

**Tabla 6.5.2.** Score SUS global del piloto comparado con el benchmark de referencia.

| Métrica | Valor |
|---|---|
| N total de usuarios | [pendiente] |
| Score SUS medio global | [pendiente] |
| Desviación estándar | [pendiente] |
| Score mínimo individual | [pendiente] |
| Score máximo individual | [pendiente] |
| Benchmark de usabilidad "aceptable" (Bangor et al., 2008) | 68 |
| ¿Supera el benchmark? | [pendiente: Sí / No] |

[pendiente: redactar párrafo de análisis interpretando el score global en relación al benchmark de 68 puntos y a las clasificaciones cualitativas de Bangor et al. (2008): Excelente, Bueno, Aceptable, Marginal, Inaceptable.]

### 6.5.3 Análisis por Ítem (Positivos vs. Negativos)

[pendiente: elaborar tabla con la media de respuesta a cada uno de los 10 ítems SUS, distinguiendo entre ítems positivos (1, 3, 5, 7, 9) e ítems negativos (2, 4, 6, 8, 10). Identificar los dos ítems con mayor satisfacción y los dos con menor satisfacción para orientar las recomendaciones del Cap. 7.]

**Tabla 6.5.3.** Media de respuesta por ítem SUS (escala 1–5, valor ajustado antes de calcular score).

| Ítem | Enunciado (resumido) | Tipo | Media (0–4) | Observaciones |
|---|---|---|---|---|
| 1 | Me gustaría usar este sistema frecuentemente | Positivo | [pendiente] | |
| 2 | El sistema es innecesariamente complejo | Negativo | [pendiente] | |
| 3 | El sistema es fácil de usar | Positivo | [pendiente] | |
| 4 | Necesité apoyo técnico para usar el sistema | Negativo | [pendiente] | |
| 5 | Las funciones del sistema están bien integradas | Positivo | [pendiente] | |
| 6 | Hay demasiada inconsistencia en el sistema | Negativo | [pendiente] | |
| 7 | La mayoría de personas aprendería rápido | Positivo | [pendiente] | |
| 8 | El sistema es engorroso de usar | Negativo | [pendiente] | |
| 9 | Me sentí muy confiado usando el sistema | Positivo | [pendiente] | |
| 10 | Tuve que aprender mucho antes de poder usarlo | Negativo | [pendiente] | |

---

## 6.6 Satisfacción Específica

### 6.6.1 NPS por Empresa y Agregado

El NPS se calculó a partir de la pregunta: *"En una escala de 0 a 10, ¿qué tan probable es que recomiendes OrbitEngine a otra empresa?"* Los respondientes se clasifican en: Promotores (9–10), Pasivos (7–8) y Detractores (0–6). El NPS = % Promotores − % Detractores.

**Tabla 6.6.1.** Resultados NPS por empresa y global.

| Empresa | N respondientes | Promotores (9–10) | Pasivos (7–8) | Detractores (0–6) | NPS |
|---|---|---|---|---|---|
| Frozt Bitez | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Empresa Placeholder | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| **Global** | **[pendiente]** | **[pendiente]** | **[pendiente]** | **[pendiente]** | **[pendiente]** |

> Referencia: un NPS positivo (> 0) se considera satisfactorio; un NPS ≥ 50 se considera excelente (Reichheld, 2003).

### 6.6.2 CSAT por Módulo

El CSAT se midió con la pregunta: *"¿Qué tan satisfecho estás con este módulo?"* en una escala Likert de 1 (muy insatisfecho) a 5 (muy satisfecho). Se calculó el promedio simple por módulo y por empresa.

**Tabla 6.6.2.** Scores CSAT medios por módulo y por empresa (escala 1–5).

| Módulo | Frozt Bitez | Miss Peggy | Empresa Placeholder | Media global |
|---|---|---|---|---|
| Inventario (productos y stock) | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Ventas | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Clientes | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Dashboard y KPIs | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Reportes y exportación | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Gestión de usuarios y roles | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| **CSAT global** | **[pendiente]** | **[pendiente]** | **[pendiente]** | **[pendiente]** |

### 6.6.3 Ranking de Módulos

[pendiente: ordenar los módulos de mayor a menor CSAT global e identificar el módulo mejor y el peor valorado. Añadir una oración de interpretación para cada extremo del ranking.]

---

## 6.7 Telemetría de Uso en Producción

Los datos de telemetría se extrajeron directamente de la base de datos PostgreSQL de producción, filtrando por las tres organizaciones reales y acotando el rango temporal al período de la Fase 5 (27 de abril – 8 de mayo de 2026).

**Tabla 6.7.1.** Actividad registrada en producción durante la Fase 5 (por empresa).

| Métrica | Frozt Bitez | Miss Peggy | Empresa Placeholder |
|---|---|---|---|
| Días activos (de 11 posibles) | [pendiente] | [pendiente] | [pendiente] |
| Sesiones totales iniciadas | [pendiente] | [pendiente] | [pendiente] |
| Usuarios únicos activos | [pendiente] | [pendiente] | [pendiente] |
| Productos creados o editados | [pendiente] | [pendiente] | [pendiente] |
| Ventas registradas | [pendiente] | [pendiente] | [pendiente] |
| Movimientos de inventario registrados | [pendiente] | [pendiente] | [pendiente] |
| Clientes creados o actualizados | [pendiente] | [pendiente] | [pendiente] |
| Exportaciones realizadas (Excel) | [pendiente] | [pendiente] | [pendiente] |
| Módulos utilizados (de 6 posibles) | [pendiente] | [pendiente] | [pendiente] |

[pendiente: agregar párrafo narrativo sobre los patrones de uso más destacados: módulos más frecuentados, patrones horarios si están disponibles, adopción de funcionalidades avanzadas (alertas de stock bajo, filtros de ventas, gestión de roles).]

---

## 6.8 Hallazgos Cualitativos de las Entrevistas

Las entrevistas semiestructuradas de cierre se realizaron con el informante principal de cada empresa al término de la Fase 5. Las entrevistas tuvieron una duración de entre 20 y 35 minutos, fueron grabadas con autorización de los participantes y transcritas parcialmente para la codificación. El análisis siguió el enfoque de **codificación temática** (Braun & Clarke, 2006): los investigadores identificaron patrones recurrentes en las transcripciones y los agruparon en temas emergentes.

### 6.8.1 Temas Emergentes

[pendiente: identificar 3–5 temas emergentes a partir de las transcripciones reales. A continuación se propone una estructura tentativa basada en los hallazgos anticipados; ajustar con los temas reales.]

| # | Tema emergente | Descripción | Frecuencia (empresas que lo mencionaron) |
|---|---|---|---|
| T1 | [pendiente: nombre del tema 1] | [pendiente: descripción breve] | [pendiente] / 3 |
| T2 | [pendiente: nombre del tema 2] | [pendiente: descripción breve] | [pendiente] / 3 |
| T3 | [pendiente: nombre del tema 3] | [pendiente: descripción breve] | [pendiente] / 3 |
| T4 | [pendiente: nombre del tema 4] | [pendiente: descripción breve] | [pendiente] / 3 |
| T5 | [pendiente: nombre del tema 5] | [pendiente: descripción breve] | [pendiente] / 3 |

### 6.8.2 Citas Representativas

[pendiente: incluir 1–2 citas textuales representativas de cada tema emergente, atribuidas a la empresa (no al individuo) a menos que el participante haya consentido la atribución nominal.]

> [pendiente: cita del tema T1] — *Frozt Bitez / Miss Peggy / Empresa Placeholder*

> [pendiente: cita del tema T2] — *[empresa]*

> [pendiente: cita del tema T3] — *[empresa]*

### 6.8.3 Estudios de Caso Narrativos

#### 6.8.3.1 Frozt Bitez

[pendiente: redactar un estudio de caso narrativo de 150–250 palabras para Frozt Bitez, describiendo: contexto previo de la empresa y sus herramientas de gestión, proceso de adopción de OrbitEngine, principales cambios observados en la operación durante la Fase 5, y valoración del informante principal sobre el impacto del sistema. Basarse en los datos de las secciones 6.3, 6.7 y las citas de la entrevista.]

#### 6.8.3.2 Miss Peggy

[pendiente: redactar un estudio de caso narrativo de 150–250 palabras para Miss Peggy, con la misma estructura que 6.8.3.1. Destacar las diferencias de contexto y adopción respecto a Frozt Bitez.]

#### 6.8.3.3 Empresa Placeholder

[pendiente: redactar un estudio de caso narrativo de 150–250 palabras para Empresa Placeholder (usar nombre definitivo cuando esté disponible), con la misma estructura que los anteriores. Destacar que esta empresa se incorporó más recientemente a la plataforma y su proceso de onboarding fue parte integral de la Fase 5.]

---

## 6.9 Validación de Hipótesis

Esta sección contrasta cada hipótesis planteada en 6.1.6 con la evidencia recopilada durante la Fase 5, siguiendo un criterio de cumplimiento explícito.

### 6.9.1 H1 — Hipótesis de Eficiencia Operativa

**Criterio de cumplimiento:** reducción promedio ≥ 30% en el tiempo de al menos tres de las cuatro tareas administrativas medidas (registro de venta, actualización de stock, generación de reporte de ventas, consulta de historial de cliente), calculada sobre el promedio de las tres empresas piloto.

**Evidencia:**

[pendiente: referenciar los valores de la Tabla 6.3.1 y calcular la reducción promedio global. Indicar en cuántas tareas se supera el 30%.]

**Veredicto:** [pendiente: Confirmada / Confirmada parcialmente / No confirmada]

### 6.9.2 H2 — Hipótesis de Precisión en Inventario

**Criterio de cumplimiento:** reducción ≥ 40 puntos porcentuales en la tasa de discrepancias de inventario en al menos dos de las tres empresas piloto.

**Evidencia:**

[pendiente: referenciar los valores de la Tabla 6.3.2. Indicar en cuántas empresas se supera el umbral del 40%.]

**Veredicto:** [pendiente: Confirmada / Confirmada parcialmente / No confirmada]

### 6.9.3 H3 — Hipótesis de Usabilidad

**Criterio de cumplimiento:** score SUS medio global ≥ 68 puntos (Bangor et al., 2008).

**Evidencia:**

[pendiente: referenciar el valor de la Tabla 6.5.2. Indicar si el score global supera el umbral de 68 y en qué clasificación cualitativa se ubica.]

**Veredicto:** [pendiente: Confirmada / Confirmada parcialmente / No confirmada]

### 6.9.4 Tabla Resumen de Validación de Hipótesis

| Hipótesis | Criterio de cumplimiento | Evidencia principal | Veredicto |
|---|---|---|---|
| **H1** — Eficiencia Operativa | Reducción ≥ 30% en tiempo de tareas (≥ 3 de 4) | Tabla 6.3.1: reducción promedio [pendiente]% | [pendiente] |
| **H2** — Precisión en Inventario | Reducción ≥ 40 pp en tasa de discrepancias (≥ 2 de 3 empresas) | Tabla 6.3.2: reducción promedio [pendiente] pp | [pendiente] |
| **H3** — Usabilidad | Score SUS medio global ≥ 68 | Tabla 6.5.2: SUS global = [pendiente] | [pendiente] |

---

## 6.10 Limitaciones de la Validación con Usuarios

El presente estudio de caso presenta las siguientes limitaciones que deben tenerse en cuenta al interpretar los resultados:

1. **Tamaño de muestra reducido (N = 3).** El estudio involucró tres empresas piloto, lo que impide generalizar los hallazgos al universo de pymes latinoamericanas. Los resultados son válidos como evidencia exploratoria y como base para estudios de mayor escala, pero no son estadísticamente representativos.

2. **Ventana de validación de dos semanas.** La Fase 5 comprendió once días hábiles de uso productivo. Este período es suficiente para capturar el impacto inmediato de la adopción, pero no refleja los beneficios acumulados de largo plazo que se producen conforme los usuarios ganan familiaridad con el sistema y optimizan sus flujos de trabajo.

3. **Auto-selección de las empresas participantes.** Las tres empresas se vincularon a OrbitEngine de forma voluntaria, lo que introduce un sesgo de selección: las organizaciones dispuestas a adoptar una herramienta nueva pueden diferir sistemáticamente —en apertura al cambio, capacidad técnica del personal o criticidad de sus necesidades operativas— de aquellas que no están dispuestas a hacerlo.

4. **Auto-reporte de los datos pre-implementación.** Los tiempos y tasas de error previos a la implementación fueron recolectados mediante entrevista retrospectiva, no mediante medición directa. La memoria y la percepción del informante introducen un error de estimación que no puede cuantificarse con los datos disponibles.

5. **Sesgo del entrevistador (equipo desarrollador = equipo investigador).** Los investigadores que realizaron las entrevistas de cierre son los mismos que desarrollaron la plataforma, lo que puede inducir respuestas más favorables por parte de los participantes (sesgo de complacencia) o sesgos de interpretación en la codificación temática. Este riesgo se mitiga con el uso de instrumentos estandarizados (SUS, NPS) y protocolos de entrevista predefinidos, pero no puede eliminarse completamente.

6. **Ausencia de grupo de control formal.** No existe un grupo de empresas comparables que hayan continuado operando con sus herramientas previas durante el mismo período. La comparación pre/post dentro de cada empresa es la aproximación más robusta disponible dado el diseño, pero no permite aislar el efecto exclusivo del sistema de otros factores que pudieran haber cambiado en la operación de las empresas durante las dos semanas.
