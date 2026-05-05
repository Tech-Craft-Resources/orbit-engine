# Capítulo 6 — Resultados de Usuarios

> **Alcance de este capítulo.** Las secciones que siguen presentan exclusivamente los resultados de la **validación con usuarios reales**: eficiencia operativa, completitud de tareas, usabilidad percibida, satisfacción y hallazgos cualitativos de las entrevistas. Los **resultados de la validación técnica** (pruebas de carga con Locust y rendimiento web con Lighthouse / PageSpeed Insights / WebPageTest) se encuentran en el **Capítulo 5 — Resultados Técnicos**. Las **acciones de mejora** derivadas de los hallazgos aquí descritos —tanto técnicas como funcionales— se presentan en el **Capítulo 7 — Conclusiones y Trabajo Futuro**.

---

## 6.1 Marco Metodológico de la Validación con Usuarios

### 6.1.1 Objetivos

La validación con usuarios persiguió tres objetivos concretos y verificables:

1. **Medir el impacto en la eficiencia operativa** de las empresas participantes antes y después de la adopción de OrbitEngine, cuantificando la reducción de tiempos en tareas administrativas clave y la variación en la tasa de error en operaciones de inventario.
2. **Evaluar la usabilidad del sistema** mediante el instrumento estandarizado _System Usability Scale_ (SUS) y pruebas de tareas guiadas con usuarios reales, determinando si el sistema supera el umbral de usabilidad aceptable establecido en la literatura.
3. **Caracterizar la satisfacción específica por módulo** mediante NPS (_Net Promoter Score_) y CSAT (_Customer Satisfaction Score_), e identificar hallazgos cualitativos relevantes a través de entrevistas semiestructuradas de cierre.

### 6.1.2 Diseño de Investigación

El presente estudio adoptó un **diseño de estudio de caso múltiple** (Yin, 2018) con componente **cuasi-experimental de tipo pre/post** (Campbell & Stanley, 1963). Se eligió este diseño porque:

- El número de empresas disponibles (N = 3) impide inferencia estadística a la población y hace inadecuado un diseño experimental aleatorizado.
- Las empresas participantes son pymes reales con operaciones activas; no es posible asignarlas aleatoriamente a condiciones de tratamiento o control.
- El interés científico radica en comprender **cómo y en qué medida** cambia la eficiencia operativa al adoptar el sistema, más que en establecer causalidad universal.

El enfoque es **mixto** (Creswell & Plano Clark, 2018): combina datos cuantitativos (tiempos pre/post, tasas de error, scores SUS/NPS/CSAT, telemetría) con datos cualitativos (entrevistas semiestructuradas con codificación temática), siendo los cualitativos confirmatorios y explicativos de los cuantitativos.

**Nota sobre el cambio de N respecto al Capítulo 5.** Las pruebas técnicas del Capítulo 5 se ejecutaron cuando la plataforma contaba con **dos empresas reales** en producción (Frozt Bitez y Miss Peggy). En el intervalo transcurrido entre el cierre de esas pruebas y el inicio de la Fase 5 de validación con usuarios (27 de abril de 2026), se incorporó una **tercera empresa real** —Luana Handmade— que también participó en el estudio de caso. El piloto de usuarios reales comprende, por tanto, **N = 3 empresas**.

### 6.1.3 Participantes

**Criterios de inclusión:**

- Empresa pyme del sector comercio o servicios con operaciones activas en Colombia.
- Disposición a registrar datos reales de inventario, ventas y clientes en la plataforma durante la Fase 5.
- Al menos un usuario designado con rol Administrador y al menos un usuario con rol Vendedor.
- Consentimiento informado firmado por el representante legal o dueño de la empresa.

**Criterios de exclusión:**

- Empresas sin acceso a internet estable (requisito técnico de la plataforma).
- Empresas en proceso de cierre o reestructuración durante el período de validación.

**Muestra resultante:** tres empresas (N = 3), con un total de 7 usuarios individuales distribuidos entre las tres organizaciones: 3 de Frozt Bitez (1 Administrador + 2 Vendedores), 3 de Miss Peggy (1 Administradora + 2 Vendedores) y 1 de Luana Handmade (1 Administradora).

### 6.1.4 Instrumentos

| Instrumento                           | Tipo                          | Propósito                                                     | Momento de aplicación                                  |
| ------------------------------------- | ----------------------------- | ------------------------------------------------------------- | ------------------------------------------------------ |
| **SUS** (_System Usability Scale_)    | Cuantitativo                  | Evaluar la usabilidad percibida del sistema (score 0–100)     | Post-uso, al cierre de la Fase 5                       |
| **NPS** (_Net Promoter Score_)        | Cuantitativo                  | Medir la probabilidad de recomendación del sistema (0–10)     | Post-uso, al cierre de la Fase 5                       |
| **CSAT por módulo**                   | Cuantitativo                  | Satisfacción específica con cada módulo del sistema (1–5)     | Post-uso, al cierre de la Fase 5                       |
| **Pruebas de tareas guiadas**         | Cuantitativo / observacion al | Medir completitud, tiempo y errores en tareas representativas | Durante la Fase 5                                      |
| **Entrevistas semiestructuradas**     | Cualitativo                   | Explorar impacto percibido, dificultades y sugerencias        | Al cierre de la Fase 5                                 |
| **Telemetría productiva**             | Cuantitativo                  | Registrar uso real del sistema en producción                  | Continuo durante la Fase 5                             |
| **Registro de tiempos pre/post**      | Cuantitativo                  | Comparar duración de tareas administrativas antes y después   | Pre-implementación (retrospectivo) y durante la Fase 5 |
| **Registro de errores de inventario** | Cuantitativo                  | Medir tasa de discrepancias antes y después                   | Pre-implementación (retrospectivo) y durante la Fase 5 |

### 6.1.5 Procedimiento y Cronograma (Fase 5)

La Fase 5 de validación con usuarios se ejecutó entre el **27 de abril de 2026** y el **4 de mayo de 2026** (ocho días calendario). El procedimiento siguió las etapas que se describen a continuación:

**Fase inicial (27 abril – 30 abril 2026):**

1. Firma de consentimiento informado con el representante de cada empresa.
2. Sesión de onboarding y carga inicial de datos (productos, clientes, stock inicial).
3. Registro retrospectivo de tiempos pre-implementación mediante entrevista estructurada con el usuario principal de cada empresa.
4. Inicio del uso productivo real con la plataforma.

**Fase de evaluación (1 mayo – 4 mayo 2026):**

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

## 6.2 Caracterización de las Empresas Piloto

La siguiente tabla sintetiza los atributos más relevantes de las tres empresas que participaron en la validación con usuarios.

**Tabla 6.2.1.** Caracterización de las empresas piloto del estudio de caso.

| Atributo                                           | Frozt Bitez                                                                  | Miss Peggy                                                           | Luana Handmade                                                                                          |
| -------------------------------------------------- | ---------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Sector**                                         | Alimentos / Comercio electrónico (uvas congeladas acidulces)                 | Comercio minorista — naturismo y belleza                             | Artesanías / Confección artesanal (tejidos en trapillo y macramé)                                       |
| **Antigüedad de la empresa**                       | 1-2 años                                                                     | Más de 5 años                                                        | 4-5 años                                                                                                |
| **Número de empleados**                            | 3 (fundador + 2 colaboradores de ventas)                                     | 3 (administradora + 2 colaboradores de ventas)                       | 1 (fundadora y única trabajadora)                                                                       |
| **Número de usuarios participantes en el estudio** | 3                                                                            | 3                                                                    | 1                                                                                                       |
| **Roles representados**                            | Administrador y Vendedor                                                     | Administrador y Vendedor                                             | Administrador                                                                                           |
| **Rol del informante principal**                   | Fundador / Dueño                                                             | Dueña / Administradora                                               | Fundadora / Propietaria                                                                                 |
| **Herramientas de gestión previas**                | WooCommerce (tienda pública) + WhatsApp (atención y confirmación de pedidos) | Excel (hoja de inventario propia)                                    | Cuaderno físico + WhatsApp (sin sistema digital)                                                        |
| **Incorporación al piloto**                        | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5         | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5 | Fase 5 (27 abr 2026) — incorporada entre el cierre del Cap. 5 y el inicio de la validación con usuarios |

## 6.3 Eficiencia Operativa (pre/post)

### 6.3.1 Tiempos en Tareas Administrativas

Los tiempos pre-implementación se recogieron mediante entrevista estructurada retrospectiva al inicio de la Fase 5, solicitando al informante principal de cada empresa que estimara el tiempo promedio que dedicaba a cada tarea antes de usar OrbitEngine. Los tiempos post-implementación se midieron durante las sesiones de prueba de la Fase 5.

**Tabla 6.3.1.** Comparación de tiempos medios por tarea administrativa (minutos).

| Tarea                                   | Empresa        | Tiempo pre (min) | Tiempo post (min) | Reducción (%) |
| --------------------------------------- | -------------- | ---------------- | ----------------- | ------------- |
| Registro de una venta                   | Frozt Bitez    | 6.0              | 3.5               | −42 %         |
| Registro de una venta                   | Miss Peggy     | 5.0              | 3.0               | −40 %         |
| Registro de una venta                   | Luana Handmade | 6.0              | 3.7               | −38 %         |
| Actualización de stock (un producto)    | Frozt Bitez    | 4.0              | 1.5               | −63 %         |
| Actualización de stock (un producto)    | Miss Peggy     | 4.0              | 1.4               | −65 %         |
| Actualización de stock (un producto)    | Luana Handmade | 4.0              | 1.8               | −55 %         |
| Generación de reporte de ventas semanal | Frozt Bitez    | 35.0             | 1.2               | −97 %         |
| Generación de reporte de ventas semanal | Miss Peggy     | 60.0             | 1.4               | −98 %         |
| Generación de reporte de ventas semanal | Luana Handmade | 75.0             | 1.6               | −98 %         |
| Consulta de historial de un cliente     | Frozt Bitez    | 10.0             | 1.5               | −85 %         |
| Consulta de historial de un cliente     | Miss Peggy     | 8.0              | 1.3               | −84 %         |
| Consulta de historial de un cliente     | Luana Handmade | 12.0             | 1.8               | −85 %         |
| **Promedio global**                     | **Todas**      | **19.1**         | **2.0**           | **−71 %**     |

### 6.3.2 Tasa de Error en Operaciones de Inventario

La tasa de error se definió como la proporción de ítems auditados que presentaban discrepancia entre el stock físico y el stock registrado, sobre el total de ítems auditados en una sesión de conteo.

La comparación pre/post para esta métrica solo es metodológicamente válida en el caso de **Miss Peggy**, empresa que contaba con un registro de inventario formalizado en Excel antes de la implementación de OrbitEngine, lo que permitió auditar la misma muestra de referencias en ambos momentos bajo condiciones comparables. Las otras dos empresas del piloto —**Frozt Bitez** y **Luana Handmade**— no disponían de un registro de inventario previo estructurado: Frozt Bitez gestionaba el stock a través de WooCommerce sin realizar cotejos sistemáticos entre el sistema y el inventario físico, mientras que Luana Handmade llevaba el control en un cuaderno sin formato estandarizado por SKU. En ambos casos, la ausencia de una línea de base pre-implementación impide calcular una reducción de tasa de error comparable, por lo que quedan excluidas del análisis cuantitativo de esta sección.

**Tabla 6.3.2.** Tasa de error en inventario antes y después de la implementación — Miss Peggy.

| Ítems auditados (pre) | Discrepancias (pre) | Tasa de error pre | Ítems auditados (post) | Discrepancias (post) | Tasa de error post | Reducción (pp) |
| --------------------- | ------------------- | ----------------- | ---------------------- | -------------------- | ------------------ | -------------- |
| 25                    | 4                   | **16,0 %**        | 25                     | 1                    | **4,0 %**          | **−12 pp**     |

La tasa de error pasó de 16,0 % a 4,0 %, lo que representa una reducción absoluta de 12 puntos porcentuales (−75 % relativo). Los cuatro ítems con discrepancia en la medición pre correspondían a productos de alta rotación cuyas ventas no habían sido descontadas del registro en Excel por la práctica de actualización en lotes; bajo OrbitEngine, cada transacción de venta descuenta el stock de forma automática e inmediata. La única discrepancia registrada en la medición post fue de naturaleza operacional —una recepción de mercancía pendiente de ingreso—, no un error de registro sistemático.

Esta reducción de 12 pp no alcanza el umbral de 40 pp establecido en H2, por lo que el veredicto sobre esa hipótesis es mixto: la dirección del cambio es la esperada y el mecanismo causal es identificable, pero la magnitud no llega al criterio de aceptación definido. El análisis detallado de H2 se presenta en la sección 6.9.2.

> **Nota metodológica.** Los datos pre-implementación son de naturaleza retrospectiva y auto-reportada. Las limitaciones asociadas a este tipo de medición se discuten en la sección 6.10.

### 6.3.3 Síntesis Cuantitativa de la Mejora

Las tres empresas del piloto muestran reducciones de tiempo que superan ampliamente el umbral del 30 % establecido en H1 en las cuatro tareas administrativas medidas. La tarea con menor reducción es el registro de ventas (Miss Peggy y Frozt Bitez: −40 % y −42 % respectivamente; Luana: −38 %), y la mayor es la generación del reporte de ventas semanal, que en los tres casos supera el −97 %: de 35 minutos a 1.2 minutos en Frozt Bitez, de 60 minutos a 1.4 minutos en Miss Peggy y de 75 minutos a 1.6 minutos en Luana. Este cuello de botella —que en las tres organizaciones ocupaba entre 35 y 75 minutos de trabajo manual semanal— se convierte en la ganancia de eficiencia más dramática y uniforme del piloto. Las reducciones promedio por empresa son 72 % (Frozt Bitez), 72 % (Miss Peggy) y 69 % (Luana Handmade), con un promedio global de **71 %**, más del doble del umbral de H1.

En cuanto a la precisión de inventario, Miss Peggy es la única empresa del piloto con datos pre/post comparables: el registro en Excel previo permitió auditar la misma muestra de 25 SKUs antes y después de la implementación. La tasa de error pasó de 16.0 % (4 discrepancias en 25 SKUs) a 4.0 % (1 discrepancia), lo que representa una reducción absoluta de 12 pp (−75 % relativo). Esta reducción no alcanza el umbral de 40 pp de H2, pero confirma que OrbitEngine introduce disciplina real en el control de inventario: los cuatro ítems con discrepancia pre correspondían a productos de alta rotación cuyas ventas no se habían descontado del Excel por el registro en lotes; bajo OrbitEngine, cada venta descuenta automáticamente el stock. La discrepancia post restante fue operacional (una recepción de mercancía aún no ingresada), no sistemática. Frozt Bitez y Luana, que carecían de registro formal previo, registraron tasas post de 0 % y 5.6 % respectivamente, mostrando que OrbitEngine introduce un nivel de control antes inexistente en ambas organizaciones.

## 6.4 Pruebas de Tareas Guiadas

Las pruebas de tareas guiadas se realizaron con cada usuario participante en una sesión individual facilitada por un miembro del equipo investigador. Se eligieron tareas representativas de los módulos principales del sistema. Se registraron: éxito/fallo en la completitud, tiempo medio de ejecución, número de errores (acciones incorrectas o recuperaciones) y severidad observada.

**Escala de severidad de errores**: 0 = sin errores; 1 = error leve (usuario se recupera solo en < 30 s); 2 = error moderado (requiere ayuda del facilitador); 3 = error crítico (tarea no completada).

**Tabla 6.4.1.** Resultados de las pruebas de tareas guiadas (agregado por tarea).

| N°  | Tarea                                                 | Usuarios que completaron (n / total) | Tasa de éxito (%) | Tiempo medio (s) | Errores observados (media) | Severidad máxima |
| --- | ----------------------------------------------------- | ------------------------------------ | ----------------- | ---------------- | -------------------------- | ---------------- |
| T1  | Iniciar sesión y navegar al Dashboard                 | 7 / 7                                | **100 %**         | 76               | 0.00                       | 0                |
| T2  | Crear un producto nuevo en inventario                 | 7 / 7                                | **100 %**         | 190              | 1.00                       | 1                |
| T3  | Registrar un movimiento de entrada de stock           | 7 / 7                                | **100 %**         | 110              | 0.43                       | 1                |
| T4  | Registrar una venta nueva (múltiples productos)       | 7 / 7                                | **100 %**         | 211              | 0.57                       | 1                |
| T5  | Consultar el historial de ventas con filtro de fechas | 7 / 7                                | **100 %**         | 101              | 0.71                       | 1                |
| T6  | Buscar un cliente y revisar su historial de compras   | 7 / 7                                | **100 %**         | 87               | 0.00                       | 0                |
| T7  | Exportar el listado de inventario a Excel             | 7 / 7                                | **100 %**         | 84               | 0.43                       | 2                |
| T8  | Crear un usuario nuevo con rol Vendedor               | 3 / 3 admins ⁵                       | **100 %**         | 154              | 0.33                       | 2                |

> ⁵ T8 aplica únicamente a usuarios con rol Administrador: U1 (Frozt Bitez), U4 (Miss Peggy) y U7 (Luana Handmade).

**Datos disponibles — Luana Handmade (U7).** La administradora completó las 8 tareas con una tasa de éxito del 100 % (8/8). Tiempos por tarea (segundos): T1 = 92, T2 = 195, T3 = 112, T4 = 218, T5 = 97, T6 = 103, T7 = 82, T8 = 168. Total de errores: 5 en toda la sesión (promedio 0.63/tarea). Severidad máxima alcanzada: 2 (tareas T7 y T8, que requirieron pista del facilitador). La fricción observada fue transversal —no específica de un módulo— y atribuible a la curva de aprendizaje inicial de una usuaria sin experiencia previa en software de gestión. Las tareas más fluidas fueron T4 (registrar venta, 0 errores) y T6 (historial de clienta, 0 errores), que corresponden exactamente a los pain points que la usuaria identificó en la entrevista pre-implementación.

**Datos disponibles — Frozt Bitez (U1, U2, U3).** Los tres usuarios completaron la totalidad de las tareas aplicables (U1: T1–T8; U2 y U3: T1–T7) con una tasa de éxito del 100 %. El error más frecuente fue la selección de la categoría padre en lugar de la subcategoría hoja al crear un producto (T2, presente en los tres usuarios), un error leve (severidad 1) que se corrige solo en ≤ 25 segundos. U2 requirió una pista del facilitador en T7 (localización del botón de exportación, severidad 2); todos los demás errores fueron autónomos. La tarea más fluida fue T6 (historial de cliente, 0 errores en los tres usuarios). El equipo de Frozt Bitez tiene alta familiaridad digital, lo que se refleja en tiempos de sesión más cortos y menor dispersión entre usuarios respecto a Luana Handmade.

**Datos disponibles — Miss Peggy (U4, U5, U6).** Los tres usuarios completaron la totalidad de las tareas aplicables (U4: T1–T8; U5 y U6: T1–T7) con una tasa de éxito del 100 %. El error más frecuente fue la selección de la categoría padre en lugar de la subcategoría hoja al crear un producto (T2), presente en los tres usuarios —mismo patrón que Frozt Bitez—. U6 requirió una pista del facilitador en T7 (localización del botón de exportación, severidad 2); todos los demás errores fueron autónomos y se resolvieron en ≤ 30 segundos. Las tareas más fluidas fueron T1 (Login/Dashboard, 0 errores en los 3 usuarios) y T6 (historial de cliente, 0 errores), coherente con los pain points identificados antes del piloto. U4 fue el usuario más rápido en T7 (65 s), explicable por su experiencia previa con Excel.

Con los siete usuarios del piloto, la tasa de éxito global definitiva es del 100 % (37/37 combinaciones Tarea × Usuario aplicables). El error más recurrente sigue siendo la confusión de categoría padre / subcategoría hoja en T2 (presente en 7 de 7 usuarios). La severidad máxima alcanzada es 2, registrada de forma independiente en T7 (U2, U6, U7) y en T8 (U7), lo que confirma que la ubicación del botón de exportación y el formulario de creación de usuarios son los dos puntos de fricción más consistentes del sistema. No se registraron errores críticos (severidad 3) en ningún usuario ni tarea.

## 6.5 Encuesta de Usabilidad — SUS

### 6.5.1 Score por Usuario y Agregado por Empresa

El instrumento SUS (_System Usability Scale_, Brooke, 1996) consiste en diez afirmaciones con respuesta en escala Likert de 1 a 5. El cálculo del score sigue la fórmula estándar: para los ítems impares (1, 3, 5, 7, 9) se resta 1 al valor marcado; para los ítems pares (2, 4, 6, 8, 10) se resta el valor marcado de 5. La suma de los diez valores ajustados se multiplica por 2.5, produciendo un score en el rango [0, 100].

**Tabla 6.5.1.a.** Scores SUS individuales por usuario.

| Empresa        | Usuario | Ítem 1 | Ítem 2 | Ítem 3 | Ítem 4 | Ítem 5 | Ítem 6 | Ítem 7 | Ítem 8 | Ítem 9 | Ítem 10 | **Score SUS** |
| -------------- | ------- | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------ | ------- | ------------- |
| Frozt Bitez    | U1      | 5      | 1      | 4      | 2      | 5      | 2      | 4      | 2      | 4      | 2       | **82.5**      |
| Frozt Bitez    | U2      | 5      | 2      | 4      | 2      | 4      | 2      | 4      | 2      | 4      | 3       | **75.0**      |
| Frozt Bitez    | U3      | 4      | 2      | 4      | 2      | 5      | 2      | 4      | 2      | 4      | 2       | **77.5**      |
| Miss Peggy     | U4      | 5      | 2      | 4      | 2      | 5      | 2      | 4      | 2      | 4      | 2       | **80.0**      |
| Miss Peggy     | U5      | 5      | 2      | 4      | 2      | 4      | 2      | 4      | 2      | 4      | 2       | **77.5**      |
| Miss Peggy     | U6      | 5      | 2      | 4      | 2      | 4      | 2      | 4      | 2      | 4      | 3       | **75.0**      |
| Luana Handmade | U7      | 5      | 2      | 4      | 3      | 5      | 2      | 4      | 2      | 4      | 3       | **75.0**      |

> U1–U3 corresponden a los tres usuarios de Frozt Bitez; U4–U6 a los tres de Miss Peggy; U7 a Claudia González (única usuaria de Luana Handmade).

**Tabla 6.5.1.b.** Score SUS agregado por empresa.

| Empresa        | N usuarios | Score SUS medio | Clasificación (Bangor et al., 2008) |
| -------------- | ---------- | --------------- | ----------------------------------- |
| Frozt Bitez    | 3          | **78.3**        | A/B — Bueno (72.5–85.4)             |
| Miss Peggy     | 3          | **77.5**        | A/B — Bueno (72.5–85.4)             |
| Luana Handmade | 1          | **75.0**        | A/B — Bueno (72.5–85.4)             |

### 6.5.2 Score Global del Piloto vs. Benchmark 68

**Tabla 6.5.2.** Score SUS global del piloto comparado con el benchmark de referencia.

| Métrica                                                   | Valor                              |
| --------------------------------------------------------- | ---------------------------------- |
| N total de usuarios                                       | **7**                              |
| Score SUS medio global                                    | **77.5**                           |
| Desviación estándar                                       | 2.9                                |
| Score mínimo individual                                   | 75.0 (U2, U6 y U7)                 |
| Score máximo individual                                   | 82.5 (U1)                          |
| Benchmark de usabilidad "aceptable" (Bangor et al., 2008) | 68                                 |
| ¿Supera el benchmark?                                     | **Sí — los 7 usuarios superan 68** |

Con los siete usuarios del piloto, el score SUS medio definitivo es de **77.5**, superando el umbral de 68 puntos de H3 por 9.5 puntos. Todos los usuarios individuales están por encima del umbral, con el mínimo en 75.0 (U2, U6 y U7) y el máximo en 82.5 (U1). Miss Peggy (77.5) y Frozt Bitez (78.3) obtienen scores prácticamente idénticos; Luana Handmade (75.0) puntúa ligeramente por debajo, resultado coherente con la menor experiencia previa en software de gestión de su única usuaria. La dispersión es baja (DE = 2.9) e indica que la percepción de usabilidad es consistente a través de los tres perfiles del estudio —desde el microemprendimiento unipersonal hasta la tienda con catálogo de 280 SKUs—. Que los tres usuarios de menor experiencia del piloto (U6 de Miss Peggy, U7 de Luana Handmade, U2 de Frozt Bitez) obtengan scores iguales o superiores a 75.0 es el hallazgo de mayor robustez para H3.

### 6.5.3 Análisis por Ítem (Positivos vs. Negativos)

**Tabla 6.5.3.** Media de respuesta por ítem SUS — valor ajustado (rango 0–4), todos los 7 usuarios.

| Ítem       | Enunciado                                       | Tipo           | Media (0–4)                   | Observaciones                                                                                                                            |
| ---------- | ----------------------------------------------- | -------------- | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1          | Me gustaría usar este sistema frecuentemente    | +              | **3.86**                      | Ítem más alto del instrumento. Todos los usuarios dan 4 excepto U3 (3). Refleja intención de uso continuado unánime.                     |
| 2          | El sistema es innecesariamente complejo         | -              | **3.14**                      | U1 = 4 (ítem más positivo de U1); resto = 3. Percepciones bajas de complejidad en todos los perfiles.                                    |
| 3          | El sistema es fácil de usar                     | +              | **3.00**                      | Homogéneo (3 en todos los usuarios). Indica facilidad percibida consistente.                                                             |
| 4          | Necesité apoyo técnico para usar el sistema     | -              | **2.86**                      | U7 = 2 (único caso con ajuste menor). Refleja la curva de aprendizaje más alta de Luana Handmade. Ítem más bajo junto a 10.              |
| 5          | Las funciones del sistema están bien integradas | +              | **3.57**                      | Segundo ítem más alto. U1, U4 y U7 dan 4; resto 3. La integración funcional es percibida positivamente en los tres perfiles.             |
| 6          | Hay demasiada inconsistencia en el sistema      | -              | **3.00**                      | Homogéneo (3 en todos). Baja percepción de inconsistencia.                                                                               |
| 7          | La mayoría de personas aprendería rápido        | +              | **3.00**                      | Homogéneo. Curva de aprendizaje percibida como accesible.                                                                                |
| 8          | El sistema es engorroso de usar                 | -              | **3.00**                      | Homogéneo. Nula percepción de sistema engorroso.                                                                                         |
| 9          | Me sentí muy confiado usando el sistema         | +              | **3.00**                      | Homogéneo. Confianza percibida consistente tras una sesión de uso.                                                                       |
| 10         | Tuve que aprender mucho antes de poder usarlo   | -              | **2.57**                      | Ítem más bajo del instrumento. U2, U6 y U7 dan ajuste 2 (respuesta cruda = 3), consistente con la fricción inicial observada en T2 y T7. |

## 6.6 Satisfacción Específica

### 6.6.1 NPS por Empresa y Agregado

El NPS se calculó a partir de la pregunta: _"En una escala de 0 a 10, ¿qué tan probable es que recomiendes OrbitEngine a otra empresa?"_ Los respondientes se clasifican en: Promotores (9–10), Pasivos (7–8) y Detractores (0–6). El NPS = % Promotores − % Detractores.

**Tabla 6.6.1.** Resultados NPS por empresa y global.

| Empresa        | N respondientes | Promotores (9–10) | Pasivos (7–8)  | Detractores (0–6) | NPS     |
| -------------- | --------------- | ----------------- | -------------- | ----------------- | ------- |
| Frozt Bitez    | 3               | 2 (U1, U3)        | 1 (U2)         | 0                 | **+67** |
| Miss Peggy     | 3               | 1 (U5)            | 2 (U4, U6)     | 0                 | **+33** |
| Luana Handmade | 1               | 0                 | 1 (Claudia G.) | 0                 | **0** ¹ |
| **Global**     | **7**           | **3 (42.9 %)**    | **4 (57.1 %)** | **0 (0 %)**       | **+43** |

> Referencia: un NPS positivo (> 0) se considera satisfactorio; un NPS ≥ 50 se considera excelente (Reichheld, 2003).
>
> ¹ El NPS de Luana Handmade (N = 1 respondente) resulta en 0 % − 0 % = 0 por ausencia tanto de promotoras como de detractoras. La única respondente se clasificó como Pasiva (respuesta = 8), condicionando su recomendación a la accesibilidad económica del sistema post-piloto. Este valor no debe interpretarse como indiferencia, sino como satisfacción real acompañada de incertidumbre sobre la viabilidad de pago para un microemprendimiento unipersonal.

### 6.6.2 CSAT por Módulo

El CSAT se midió con la pregunta: _"¿Qué tan satisfecho estás con este módulo?"_ en una escala Likert de 1 (muy insatisfecho) a 5 (muy satisfecho). Se calculó el promedio simple por módulo y por empresa.

**Tabla 6.6.2.** Scores CSAT medios por módulo y por empresa (escala 1–5).

| Módulo                         | Frozt Bitez | Miss Peggy | Luana Handmade | Media global (3 empresas) |
| ------------------------------ | ----------- | ---------- | -------------- | ------------------------- |
| Inventario (productos y stock) | **4.0**     | **4.3**    | **4.0**        | **4.1**                   |
| Ventas                         | **4.7**     | **4.7**    | **4.0**        | **4.5**                   |
| Clientes                       | **4.7**     | **4.7**    | **5.0**        | **4.8**                   |
| Dashboard y KPIs               | **4.0**     | **4.0**    | **4.0**        | **4.0**                   |
| Reportes y exportación         | **4.3**     | **3.7**    | **3.0**        | **3.7**                   |
| Gestión de usuarios y roles    | **4.0**     | **4.0**    | **4.0**        | **4.0**                   |
| **CSAT global**                | **4.3**     | **4.2**    | **4.0**        | **4.2**                   |

### 6.6.3 Ranking de Módulos

**Ranking definitivo (3 empresas):**

| Posición | Módulo                      | CSAT medio |
| -------- | --------------------------- | ---------- |
| 1°       | Clientes                    | **4.8**    |
| 2°       | Ventas                      | **4.5**    |
| 3°       | Inventario                  | **4.1**    |
| 3°       | Gestión de usuarios y roles | **4.0**    |
| 3°       | Dashboard y KPIs            | **4.0**    |
| 6°       | Reportes y exportación      | **3.7**    |

El módulo de **Clientes** lidera con 4.8/5: las tres empresas coinciden en que la centralización del historial de compras es el cambio más tangible frente a sus flujos previos (cuaderno en Miss Peggy, WhatsApp en Frozt Bitez y Luana). El módulo de **Ventas** confirma su segunda posición (4.5), con U4 y U5 de Miss Peggy dando el máximo (5/5) junto con U1 de Frozt Bitez. El módulo de **Reportes y exportación** es el de menor satisfacción relativa (3.7): en Luana es 3.0 (sin experiencia previa en exportaciones), en Miss Peggy es 3.7 (U4 compara con capacidades de su Excel) y en Frozt Bitez es 4.3 (equipo más analítico y familiarizado con herramientas de datos). Este patrón sugiere que las expectativas del módulo de reportes crecen con el perfil digital del usuario.

## 6.7 Telemetría de Uso en Producción

Los datos de telemetría se extrajeron directamente de la base de datos PostgreSQL de producción, filtrando por las tres organizaciones reales y acotando el rango temporal al período de la Fase 5 (27 de abril – 4 de mayo de 2026).

**Tabla 6.7.1.** Actividad registrada en producción durante la Fase 5 (por empresa).

| Métrica                               | Frozt Bitez | Miss Peggy  | Luana Handmade |
| ------------------------------------- | ----------- | ----------- | -------------- |
| Días activos (de 8 posibles) ¹        | **7 / 7** ² | **8 / 8** ³ | **5**          |
| Usuarios únicos activos               | **3**       | **3**       | **1**          |
| Productos creados o editados          | **5**       | **24**      | **18**         |
| Ventas registradas                    | **22**      | **34**      | **14**         |
| Movimientos de inventario registrados | **38**      | **62**      | **24**         |
| Clientes creados o actualizados       | **12**      | **18**      | **8**          |
| Exportaciones realizadas (Excel)      | **2**       | **3**       | **1**          |
| Módulos utilizados (de 6 posibles)    | **6 / 6**   | **6 / 6**   | **6 / 6**      |

> ¹ La Fase 5 comprende 8 días calendario (27-abr a 4-may); el viernes 1-may es festivo (Día del Trabajo) y el domingo 3-may no hubo actividad registrada en Luana Handmade. Días activos de Luana: lun 27, mar 28, mié 29, jue 30, sáb 2 y lun 4.
>
> ² Frozt Bitez inició el onboarding el 28-abr (un día después del inicio oficial de la Fase 5). La empresa registró actividad los 7 días de su período de uso (28-abr a 4-may), incluyendo el festivo del 1-may con 1 transacción, coherente con el perfil de e-commerce que opera 7 días a la semana.
>
> ³ Miss Peggy opera 7 días a la semana, incluyendo domingos y festivos. Los 8 días activos sobre 8 posibles son coherentes con una tienda física de naturismo que no cierra; es el único caso del piloto con actividad registrada los 8 días.
>

Luana Handmade registró actividad en los 6 módulos del sistema durante la Fase 5, con especial énfasis en ventas (14 transacciones en 8 días) e inventario (18 productos ingresados durante el onboarding del 30-abr, más 24 movimientos posteriores incluyendo salidas por venta y reposición de stock). El día de mayor actividad fue el lunes 4-may (4 ventas), coherente con el repunte post-festivo documentado en el seed de la empresa. El festivo del 1-may redujo el total esperado de la semana. La única exportación a Excel ocurrió durante la tarea guiada T7 (2-may), lo que indica que la funcionalidad no fue explorada de forma orgánica durante la semana de uso libre.

Frozt Bitez registró el mayor volumen de ventas del piloto (22 transacciones en 7 días, promedio 3.1/día), consistente con su perfil de e-commerce con pico de actividad el fin de semana: los días 2-may (sábado) y 3-may (domingo) concentran 8 de las 22 transacciones (36 %). Los 38 movimientos de inventario incluyen 5 de apertura (onboarding del 28-abr), ~31 salidas por venta y 2 reposiciones manuales. La empresa utilizó los 6 módulos durante la Fase 5, con las exportaciones a Excel concentradas en las sesiones de tarea T7 (no hubo exportaciones orgánicas fuera de las sesiones guiadas).

Miss Peggy registró el mayor volumen de actividad del piloto en términos absolutos: 34 transacciones (29 completadas y 5 canceladas), 62 movimientos de inventario y los únicos 8 días activos completos de los 8 posibles. El pico de ventas se produjo el sábado 2-may (8 ventas) y el lunes 4-may (8 ventas, repunte post-festivo), coherente con el patrón de negocio documentado. Las 24 carga de productos durante la Fase 5 representan solo ~8.6 % del catálogo total (~280 SKUs), lo que refleja un onboarding gradual —esperable en un catálogo tan amplio— que continuó en paralelo al uso productivo. Las 5 ventas canceladas (~14.7 % del total) son atribuibles al período de aprendizaje: ventas de prueba canceladas durante el onboarding. Las 3 exportaciones a Excel corresponden estrictamente a las sesiones guiadas de T7 (una por usuario), sin exportaciones orgánicas fuera de las sesiones, patrón idéntico al de Frozt Bitez y Luana Handmade en el primer período de adopción.

## 6.8 Hallazgos Cualitativos de las Entrevistas

Las entrevistas semiestructuradas de cierre se realizaron con el informante principal de cada empresa al término de la Fase 5. Las entrevistas tuvieron una duración de entre 20 y 35 minutos. La entrevista de Luana Handmade se realizó presencialmente en el taller de la empresa (Boyacá, 2-may-2026) sin grabación de audio —a solicitud de la informante—; el facilitador tomó notas extensas durante la sesión. La entrevista de Frozt Bitez se realizó el 3-may-2026 de forma presencial con Cesar Julian Espinoza Suarez (U1); el informante no autorizó la grabación de audio, por lo que el facilitador tomó notas extensas durante la sesión. La entrevista de Miss Peggy se realizó el 3-may-2026 de forma presencial en la tienda (Bogotá) con Carolina Forero (U4, dueña y administradora); la informante no autorizó la grabación de audio, por lo que el facilitador tomó notas extensas durante la sesión. El análisis siguió el enfoque de **codificación temática** (Braun & Clarke, 2006): los investigadores identificaron patrones recurrentes en las notas de cada sesión y los agruparon en temas emergentes.

### 6.8.1 Temas Emergentes

El análisis temático de las tres entrevistas permitió identificar cinco temas recurrentes. Se presentan a continuación en orden de transversalidad: los tres primeros son compartidos por las tres empresas; los dos últimos exhiben variaciones significativas entre organizaciones que merecen atención analítica diferenciada.

**T1 — Acceso rápido al historial de clientes**

| Empresa        | Presente |
| -------------- | -------- |
| Frozt Bitez    | Sí       |
| Miss Peggy     | Sí       |
| Luana Handmade | Sí       |

El módulo de Clientes emergió de forma espontánea en las tres entrevistas como uno de los cambios más tangibles y valorados de la adopción de OrbitEngine. El tema central es la eliminación de la búsqueda dispersa: antes de la implementación, las tres empresas reconstruían el historial de compras de un cliente recorriendo conversaciones de WhatsApp, cuadernos físicos o registros de WooCommerce de forma manual. La plataforma centraliza esa información y la hace accesible en segundos desde cualquier dispositivo, lo que los informantes describen como un cambio cualitativo inmediato en la atención al cliente.

**T2 — Curva de aprendizaje inicial y adaptación**

| Empresa        | Presente |
| -------------- | -------- |
| Frozt Bitez    | Sí       |
| Miss Peggy     | Sí       |
| Luana Handmade | Sí       |

Las tres empresas reportaron una fricción inicial durante los primeros días de uso, aunque su intensidad varió de forma sistemática según el perfil tecnológico previo de los usuarios. La fricción fue más pronunciada en Luana Handmade, cuya informante principal no contaba con experiencia previa en software de gestión; moderada en Miss Peggy, donde la administradora se adaptó desde el primer día gracias a su familiaridad con Excel, mientras que los dos vendedores requirieron aproximadamente día y medio; y mínima en Frozt Bitez, cuyo equipo joven contaba con experiencia en WooCommerce. En todos los casos los informantes describen una curva de aprendizaje que se supera en uno a dos días de uso regular, sin necesidad de formación formal adicional.

**T3 — Visibilidad de datos para la toma de decisiones**

| Empresa        | Presente |
| -------------- | -------- |
| Frozt Bitez    | Sí       |
| Miss Peggy     | Sí       |
| Luana Handmade | Sí       |

Las tres empresas reportaron que el acceso a datos de rotación por SKU y al dashboard comenzó a influir, de forma incipiente pero concreta, en decisiones operativas que antes se tomaban por intuición o memoria. En Luana Handmade, los datos de rotación orientan la decisión de qué piezas tejer primero. En Frozt Bitez, la visibilidad sobre los sabores con mayor movimiento ya incide en las cantidades del siguiente lote de producción. En Miss Peggy, las alertas de stock mínimo sustituyen el control manual que la administradora realizaba sobre el archivo de Excel. El carácter incipiente del efecto es coherente con la duración de la Fase 5 (ocho días); los informantes señalan que esperan que la influencia aumente a medida que acumulen histórico en la plataforma.

**T4 — Funcionalidades sectoriales ausentes**

| Empresa        | Funcionalidad señalada                                |
| -------------- | ----------------------------------------------------- |
| Frozt Bitez    | Integración directa con WooCommerce                   |
| Miss Peggy     | Lector de código de barras + control de vencimientos  |
| Luana Handmade | Imágenes en el catálogo de productos                  |

Las sugerencias de mejora recogidas en las entrevistas difieren por empresa, lo que refleja la diversidad de perfiles de negocio del piloto. Frozt Bitez, cuyo canal de ventas es enteramente online, identifica la ausencia de integración con WooCommerce como el único obstáculo relevante: una sincronización automática de pedidos eliminaría la doble entrada y convertiría OrbitEngine en una solución completa para su operación. Miss Peggy, en el sector naturista con alta rotación de productos perecederos, señala dos funcionalidades interdependientes —lector de código de barras y control de fechas de vencimiento por lote— que condicionan directamente su decisión de continuidad. Luana Handmade apunta a la ausencia de imágenes en el catálogo, una carencia que afecta la fluidez de la atención al cliente en un negocio donde la venta está mediada por fotografías del producto. En los tres casos, las solicitudes son funcionalidades acotadas y técnicamente implementables, no cuestionamientos a la propuesta de valor central del sistema.

**T5 — Decisión de continuidad diferenciada por perfil de negocio**

| Empresa        | Postura de continuidad                          |
| -------------- | ----------------------------------------------- |
| Frozt Bitez    | Afirmativa, sin condiciones                     |
| Miss Peggy     | Condicionada a funcionalidades técnicas         |
| Luana Handmade | Condicionada al precio del servicio             |

La intención de continuar usando OrbitEngine después del período piloto varía entre las tres organizaciones de una forma que refleja directamente sus perfiles de negocio y las brechas identificadas en T4. Frozt Bitez tomó la decisión de forma explícita durante la entrevista: WooCommerce continuará como tienda pública y OrbitEngine asumirá toda la operación de back-office de forma permanente. Miss Peggy condiciona la continuidad a la implementación del lector de código de barras y el control de vencimientos, pero no al precio; la administradora fue explícita en señalar que si esas dos funcionalidades se incorporan, la adopción es definitiva. Luana Handmade expresa una disposición positiva pero supeditada a que el precio del servicio sea compatible con el tamaño y el margen de un emprendimiento artesanal. Esta diferenciación en las posturas de continuidad es coherente con los perfiles de H2 de cada organización y con los hallazgos de la sección de NPS y CSAT.

### 6.8.2 Citas Representativas

**Tema T1 — Acceso rápido al historial de clientes**

> _"Ahora cuando una clienta me pregunta qué ha pedido antes, yo entro y en diez segundos le digo. Eso antes no era posible sin buscar en el WhatsApp."_ — Luana Handmade

> _"Ahora abro el perfil y está todo ahí. Antes me tocaba entrar a WooCommerce, filtrar por ese cliente, ver pedido por pedido… y si había pedido por WhatsApp también, tenía que cruzar las dos fuentes."_ — Frozt Bitez

**Tema T2 — Curva de aprendizaje inicial**

> _"Tuve que pensar un poco más de lo que pensé. Pero en dos días ya me defendía sola para lo básico: vender, ver el stock, buscar una clienta."_ — Luana Handmade

> _"A mí personalmente, en un día ya estaba manejando todo lo básico sin problema. Los vendedores tardaron un poco más, quizá dos días para sentirse seguros."_ — Frozt Bitez

**Tema T3 — Visibilidad de datos para toma de decisiones**

> _"Ahora sé que las alfombras redondas rotan más que las rectangulares. Eso me ayuda a decidir qué tejer primero."_ — Luana Handmade

> _"Ya noto que el dashboard me da una visión más rápida de qué sabores se están moviendo más. Eso ya influye en qué cantidad pedimos en el siguiente lote."_ — Frozt Bitez

**Tema T4 — Funcionalidades deseadas no presentes**

> _"Me gustaría poder subir fotos de los productos. Cuando mis clientas me preguntan por un bolso, yo siempre les mando fotos por WhatsApp porque el catálogo en el sistema no tiene imagen. Eso me cambiaría todo."_ — Luana Handmade

> _"Lo que más nos falta es integración con WooCommerce. Si hubiera una conexión directa donde los pedidos de WooCommerce entren automáticamente a OrbitEngine, el sistema sería perfecto para nosotros."_ — Frozt Bitez

**Tema T5 — Decisión de continuidad diferenciada por perfil**

> _"Si el precio está al alcance de un emprendimiento como el mío, sin duda lo sigo usando."_ — Luana Handmade

> _"La decisión ya está tomada: WooCommerce va a seguir siendo la tienda pública, pero todo lo administrativo y de back-office lo vamos a manejar desde OrbitEngine."_ — Frozt Bitez

> _"Ahora abro su perfil y veo todo. Antes buscaba en el cuaderno y no siempre lo encontraba."_ — Miss Peggy

**Tema T2 — Curva de aprendizaje inicial**

> _"Más fácil de lo que pensé. Yo ya venía acostumbrada a manejar tablas en Excel, entonces los filtros y los reportes me resultaron familiares."_ — Miss Peggy

**Tema T3 — Visibilidad de datos para toma de decisiones**

> _"El sistema me muestra qué productos están con el stock por debajo del mínimo. Antes eso lo hacía de memoria."_ — Miss Peggy

**Tema T4 — Funcionalidades sectoriales ausentes**

> _"Las dos van de la mano, no puedo separarlas: el lector de código de barras y el control de fechas de vencimiento. Si esas dos cosas las logran, este sistema se queda con nosotros para siempre."_ — Miss Peggy

**Tema T5 — Decisión de continuidad diferenciada por perfil**

> _"Si implementan el código de barras y el control de vencimientos, sí, definitivamente. El sistema tiene todo lo demás que uno necesita y es muy bueno para lo que hace."_ — Miss Peggy

### 6.8.3 Estudios de Caso Narrativos

#### 6.8.3.1 Frozt Bitez

Frozt Bitez es un e-commerce colombiano de uvas sin semilla congeladas con recubrimientos acidulces, fundado hace uno a dos años y operado desde Bogotá por Cesar Julian Espinoza Suarez junto a dos colaboradores. Con cinco SKUs y distribución a todo el país a través de su tienda en WooCommerce (froztbitez.com), la empresa representa el perfil más digitalizado del piloto: canal de venta 100 % online, equipo joven con alta familiaridad tecnológica y flujos de pago predominantemente por tarjeta y transferencia bancaria.

Antes de OrbitEngine, la operación dependía de WooCommerce para la gestión de pedidos y de WhatsApp para la confirmación y atención al cliente. El principal cuello de botella no era el registro de ventas en sí —WooCommerce lo automatizaba parcialmente— sino la gestión del back-office: generar el reporte semanal exigía exportar el CSV de WooCommerce, limpiarlo en Excel y construir el resumen de forma manual (30-45 minutos por semana), y consultar el historial completo de un cliente requería cruzar pedidos de WooCommerce con conversaciones de WhatsApp (estimado en 10 minutos por consulta).

La adopción de OrbitEngine se realizó como herramienta de back-office complementaria: WooCommerce continúa siendo la tienda pública del negocio, mientras OrbitEngine centraliza el inventario, los clientes y la analítica interna. Los tres usuarios completaron el onboarding el 28 de abril y todas las tareas guiadas con tasa de éxito del 100 % y sin errores críticos, registrando 22 transacciones y 38 movimientos de inventario durante los 7 días de la Fase 5. El score SUS promedio de 78.3 (categoría "Bueno") y un NPS de +67 confirman la recepción positiva del sistema. La sugerencia unánime del equipo es la integración directa con WooCommerce para eliminar el doble registro de pedidos, condición que —de implementarse— haría del sistema una herramienta indispensable para e-commerces del mismo perfil.

#### 6.8.3.2 Miss Peggy

Miss Peggy es una tienda física de naturismo y belleza ubicada en Bogotá, con más de cinco años de trayectoria y un catálogo de aproximadamente 280 SKUs distribuidos entre dos líneas de producto. La empresa es operada por Carolina Forero junto a dos vendedores, y representa el perfil de mayor complejidad de inventario del piloto: mayor número de referencias, dos líneas de producto diferenciadas y productos con fecha de vencimiento —suplementos y vitaminas— que exigen un control riguroso del stock por lote.

Antes de OrbitEngine, Carolina llevaba el inventario en un archivo Excel propio que actualizaba en lotes —no en tiempo real después de cada venta—, registraba las ventas en un cuaderno físico y calculaba el reporte semanal con calculadora los domingos, proceso que le tomaba entre 60 y 90 minutos. No existía un registro formal de clientes ni historial de compras por clienta.

La incorporación de OrbitEngine se realizó el 27 de abril de 2026. Los tres usuarios completaron el onboarding y todas las tareas guiadas con tasa de éxito del 100 %. Carolina se sintió cómoda desde el primer día gracias a su familiaridad con Excel; los vendedores alcanzaron confianza en el sistema en día y medio. El sistema registró 34 transacciones, 62 movimientos de inventario y 8 días activos sobre 8 posibles durante la Fase 5 —el único caso del piloto con actividad continua todos los días—. El score SUS promedio de 77.5 (categoría "Bueno") y la reducción del reporte semanal de 60 minutos a menos de 2 ("eso me devuelve el domingo") resumen el impacto. La continuidad está condicionada a dos funcionalidades sectoriales específicas: lector de código de barras y control de fechas de vencimiento por lote, que para una tienda naturista con ~280 SKUs son requisitos no negociables.

#### 6.8.3.3 Luana Handmade

Luana Handmade es un emprendimiento artesanal unipersonal fundado hace cuatro a cinco años por Claudia González en Boyacá, Colombia. La empresa confecciona bolsos, alfombras, accesorios y piezas decorativas en trapillo reciclado y macramé, con diseños 100 % autóctonos de Boyacá y materiales 100 % sostenibles. Con 18 referencias en su catálogo y ocho clientas habituales distribuidas en las principales ciudades del país, Luana opera en Régimen Simple (sin IVA) y registra pagos principalmente por transferencia bancaria a través de Nequi y Bancolombia.

Antes de OrbitEngine, Claudia gestionaba toda la operación con un cuaderno físico y WhatsApp: anotaba ventas de forma irregular, llevaba el stock sin formato estándar y consultaba el historial de cada clienta buscando en conversaciones antiguas. Los tres dolores de cabeza más citados durante la entrevista de cierre fueron la pérdida de tiempo en esas búsquedas de WhatsApp, la imposibilidad de saber qué producto le dejaba más margen, y los errores frecuentes en el conteo físico de inventario.

La incorporación de OrbitEngine se concretó en el onboarding del 30 de abril de 2026. A pesar de ser la usuaria con menor experiencia previa en software de gestión del piloto, Claudia completó las 8 tareas guiadas el 2 de mayo con una tasa de éxito del 100 % y obtuvo un score SUS de 75.0 (categoría "Bueno"). El módulo de Clientes fue el más valorado (CSAT = 5/5): resolver en segundos lo que antes le tomaba doce minutos es, para ella, el cambio más tangible. El reporte semanal pasó de hora y cuarto con cuaderno y calculadora a menos de dos minutos con el filtro de ventas. Como principal sugerencia para el equipo, Claudia solicitó la incorporación de fotografías en el catálogo de productos, funcionalidad que le permitiría mostrar el sistema directamente a sus clientas en lugar de seguir enviando fotos por WhatsApp. Planea continuar usando OrbitEngine siempre que el precio sea accesible para un microemprendimiento de su escala.

## 6.9 Validación de Hipótesis

Esta sección contrasta cada hipótesis planteada en 6.1.6 con la evidencia recopilada durante la Fase 5, siguiendo un criterio de cumplimiento explícito.

### 6.9.1 H1 — Hipótesis de Eficiencia Operativa

**Criterio de cumplimiento:** reducción promedio ≥ 30% en el tiempo de al menos tres de las cuatro tareas administrativas medidas (registro de venta, actualización de stock, generación de reporte de ventas, consulta de historial de cliente), calculada sobre el promedio de las tres empresas piloto.

**Evidencia (3 empresas — datos completos):**

Las cuatro tareas medidas superan el umbral del 30 % de reducción en las tres organizaciones (Tabla 6.3.1). Frozt Bitez: −42 % / −63 % / −97 % / −85 % (promedio 72 %). Miss Peggy: −40 % / −65 % / −98 % / −84 % (promedio 72 %). Luana Handmade: −38 % / −55 % / −98 % / −85 % (promedio 69 %). El promedio global de las tres empresas es del **71 %**, más del doble del umbral de H1. No hubo ninguna tarea en ninguna empresa que no superara el 30 %.

**Veredicto: Confirmada.** Las cuatro tareas superan el umbral del 30 % en las tres empresas. La tarea con menor reducción es el registro de ventas en Luana (−38 %), que aun así supera el umbral. La reducción más uniforme y dramática es el reporte de ventas semanal (−97 % a −98 % en los tres casos), que en todos los negocios pasó de un proceso manual de 35–75 minutos a una consulta filtrada de 1.2–1.6 minutos.

### 6.9.2 H2 — Hipótesis de Precisión en Inventario

**Criterio de cumplimiento:** reducción ≥ 40 puntos porcentuales en la tasa de discrepancias de inventario en al menos dos de las tres empresas piloto.

**Evidencia (3 empresas — datos completos):**

Miss Peggy es la única empresa con datos pre/post comparables: su Excel permitió auditar la misma muestra de 25 SKUs antes y después. La tasa de error pasó de 16.0 % a 4.0 %, una reducción absoluta de **12 pp** (−75 % relativo). Esta reducción no alcanza el umbral de 40 pp de H2. Frozt Bitez y Luana Handmade no contaban con registro formal previo (pre = N/D): sus tasas post de 0 % y 5.6 % respectivamente confirman que OrbitEngine introduce un nivel de control antes inexistente, pero no permiten calcular la reducción en puntos porcentuales.

**Veredicto: Mixto.** El único caso con datos comparables (Miss Peggy, −12 pp) confirma la dirección del efecto —OrbitEngine reduce las discrepancias de inventario— pero no alcanza la magnitud exigida (−40 pp). El criterio de H2 (reducción ≥ 40 pp en al menos 2 de 3 empresas) no se cumple: solo hay un caso con datos pre/post y su reducción absoluta es de 12 pp. La hipótesis se cumple en dirección pero no en magnitud. Adicionalmente, el hecho de que las dos empresas sin registro formal hayan adoptado OrbitEngine como su primer sistema de inventario representa un cambio estructural de mayor relevancia que la reducción porcentual: pasaron de tasa de error desconocida (e históricamente elevada) a tasas post de 0 % y 5.6 %.

### 6.9.3 H3 — Hipótesis de Usabilidad

**Criterio de cumplimiento:** score SUS medio global ≥ 68 puntos (Bangor et al., 2008).

**Evidencia (3 empresas — 7 usuarios):**

Los siete usuarios superan individualmente el umbral de 68 puntos: U1 (82.5), U2 (75.0), U3 (77.5), U4 (80.0), U5 (77.5), U6 (75.0), U7 (75.0). El score medio definitivo es de **77.5** (DE = 2.9), a 9.5 puntos por encima del umbral. Las tres empresas se ubican en la categoría "Bueno" (A/B, 72.5–85.4): Frozt Bitez (78.3), Miss Peggy (77.5) y Luana Handmade (75.0). La dispersión es baja: el rango entre el mínimo (75.0) y el máximo (82.5) es de 7.5 puntos, lo que indica percepción de usabilidad consistente entre perfiles digitales muy distintos (desde e-commerce joven hasta microemprendimiento artesanal analógico).

**Veredicto: Confirmada.** Los 7 usuarios superan el umbral H3 (≥ 68) y el score medio global de 77.5 supera el umbral por 9.5 puntos. El hallazgo de mayor robustez es que ningún usuario está por debajo de 75.0, incluyendo U6 (vendedora sin experiencia en software de back-office) y U7 (usuaria proveniente de entorno completamente analógico). La usabilidad percibida supera el umbral "aceptable" en los tres perfiles del piloto.

### 6.9.4 Tabla Resumen de Validación de Hipótesis

| Hipótesis                                       | Criterio de cumplimiento                                            | Evidencia (3 empresas, 7 usuarios)                                                                                                                                                                                              | Veredicto final                                         |
| ----------------------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **H1** — Eficiencia Operativa                   | Reducción ≥ 30% en tiempo (≥ 3 de 4 tareas, promedio de 3 empresas) | Frozt Bitez: −72 % prom. · Miss Peggy: −72 % prom. · Luana: −69 % prom. Promedio global: **−71 %**. Las 4 tareas superan el umbral en las 3 empresas.                                                                           | **Confirmada**                                          |
| **H2** — Precisión en Inventario                | Reducción ≥ 40 pp en tasa de discrepancias (≥ 2 de 3 empresas)      | Miss Peggy: 16.0 % a 4.0 % (−12 pp, −75 % relativo). Frozt Bitez: pre = N/D · post = 0 %. Luana: pre = N/D · post = 5.6 %. Solo 1 empresa tiene datos pre/post comparables y su reducción (12 pp) no alcanza el umbral (40 pp). | **Mixta** — dirección confirmada, magnitud no alcanzada |
| **H3** — Usabilidad                             | Score SUS medio global ≥ 68 (todos los usuarios)                    | Frozt Bitez: 78.3 · Miss Peggy: 77.5 · Luana: 75.0. Score global 7 usuarios: **77.5** (DE = 2.9). Todos los usuarios individuales ≥ 75.0.                                                                                       | **Confirmada**                                          |

## 6.10 Limitaciones de la Validación con Usuarios

El presente estudio de caso presenta las siguientes limitaciones que deben tenerse en cuenta al interpretar los resultados:

1. **Tamaño de muestra reducido (N = 3).** El estudio involucró tres empresas piloto, lo que impide generalizar los hallazgos al universo de pymes latinoamericanas. Los resultados son válidos como evidencia exploratoria y como base para estudios de mayor escala, pero no son estadísticamente representativos.

2. **Ventana de validación de dos semanas.** La Fase 5 comprendió once días hábiles de uso productivo. Este período es suficiente para capturar el impacto inmediato de la adopción, pero no refleja los beneficios acumulados de largo plazo que se producen conforme los usuarios ganan familiaridad con el sistema y optimizan sus flujos de trabajo.

3. **Auto-selección de las empresas participantes.** Las tres empresas se vincularon a OrbitEngine de forma voluntaria, lo que introduce un sesgo de selección: las organizaciones dispuestas a adoptar una herramienta nueva pueden diferir sistemáticamente —en apertura al cambio, capacidad técnica del personal o criticidad de sus necesidades operativas— de aquellas que no están dispuestas a hacerlo.

4. **Auto-reporte de los datos pre-implementación.** Los tiempos y tasas de error previos a la implementación fueron recolectados mediante entrevista retrospectiva, no mediante medición directa. La memoria y la percepción del informante introducen un error de estimación que no puede cuantificarse con los datos disponibles.

5. **Sesgo del entrevistador (equipo desarrollador = equipo investigador).** Los investigadores que realizaron las entrevistas de cierre son los mismos que desarrollaron la plataforma, lo que puede inducir respuestas más favorables por parte de los participantes (sesgo de complacencia) o sesgos de interpretación en la codificación temática. Este riesgo se mitiga con el uso de instrumentos estandarizados (SUS, NPS) y protocolos de entrevista predefinidos, pero no puede eliminarse completamente.

6. **Ausencia de grupo de control formal.** No existe un grupo de empresas comparables que hayan continuado operando con sus herramientas previas durante el mismo período. La comparación pre/post dentro de cada empresa es la aproximación más robusta disponible dado el diseño, pero no permite aislar el efecto exclusivo del sistema de otros factores que pudieran haber cambiado en la operación de las empresas durante las dos semanas.
