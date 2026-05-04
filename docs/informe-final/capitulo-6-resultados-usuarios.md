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

---

## 6.2 Caracterización de las Empresas Piloto

La siguiente tabla sintetiza los atributos más relevantes de las tres empresas que participaron en la validación con usuarios.

**Tabla 6.2.1.** Caracterización de las empresas piloto del estudio de caso.

| Atributo | Frozt Bitez | Miss Peggy | Luana Handmade |
|---|---|---|---|
| **Sector** | Alimentos / Comercio electrónico (uvas congeladas acidulces) | Comercio minorista — naturismo y belleza | Artesanías / Confección artesanal (tejidos en trapillo y macramé) |
| **Antigüedad de la empresa** | 1-2 años | [pendiente] | 4-5 años |
| **Número de empleados** | 3 (fundador + 2 colaboradores de ventas) | 3 (administradora + 2 colaboradores de ventas) | 1 (fundadora y única trabajadora) |
| **Número de usuarios participantes en el estudio** | 3 | 3 | 1 |
| **Roles representados** | Administrador y Vendedor | Administrador y Vendedor | Administrador |
| **Rol del informante principal** | Fundador / Dueño | Dueña / Administradora | Fundadora / Propietaria |
| **Herramientas de gestión previas** | WooCommerce (tienda pública) + WhatsApp (atención y confirmación de pedidos) | Excel (hoja de inventario propia) | Cuaderno físico + WhatsApp (sin sistema digital) |
| **Incorporación al piloto** | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5 | Fase 5 (27 abr 2026) — también presente en piloto técnico del Cap. 5 | Fase 5 (27 abr 2026) — incorporada entre el cierre del Cap. 5 y el inicio de la validación con usuarios |

---

## 6.3 Eficiencia Operativa (pre/post)

### 6.3.1 Tiempos en Tareas Administrativas

Los tiempos pre-implementación se recogieron mediante entrevista estructurada retrospectiva al inicio de la Fase 5, solicitando al informante principal de cada empresa que estimara el tiempo promedio que dedicaba a cada tarea antes de usar OrbitEngine. Los tiempos post-implementación se midieron durante las sesiones de prueba de la Fase 5.

**Tabla 6.3.1.** Comparación de tiempos medios por tarea administrativa (minutos).

| Tarea | Empresa | Tiempo pre (min) | Tiempo post (min) | Reducción (%) |
|---|---|---|---|---|
| Registro de una venta | Frozt Bitez | 6.0 | 3.5 | −42 % |
| Registro de una venta | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Registro de una venta | Luana Handmade | 6.0 | 3.7 | −38 % |
| Actualización de stock (un producto) | Frozt Bitez | 4.0 | 1.5 | −63 % |
| Actualización de stock (un producto) | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Actualización de stock (un producto) | Luana Handmade | 4.0 | 1.8 | −55 % |
| Generación de reporte de ventas semanal | Frozt Bitez | 35.0 | 1.2 | −97 % |
| Generación de reporte de ventas semanal | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Generación de reporte de ventas semanal | Luana Handmade | 75.0 | 1.6 | −98 % |
| Consulta de historial de un cliente | Frozt Bitez | 10.0 | 1.5 | −85 % |
| Consulta de historial de un cliente | Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Consulta de historial de un cliente | Luana Handmade | 12.0 | 1.8 | −85 % |
| **Promedio global** | **Todas** | **[pendiente]** | **[pendiente]** | **Provisional (2/3 empresas): −70 %** |

### 6.3.2 Tasa de Error en Operaciones de Inventario

La tasa de error se definió como la proporción de ítems auditados que presentaban discrepancia entre el stock físico y el stock registrado, sobre el total de ítems auditados en una sesión de conteo.

**Tabla 6.3.2.** Tasa de error en inventario antes y después de la implementación.

| Empresa | Ítems auditados (pre) | Discrepancias (pre) | Tasa de error pre (%) | Ítems auditados (post) | Discrepancias (post) | Tasa de error post (%) | Reducción (pp) |
|---|---|---|---|---|---|---|---|
| Frozt Bitez | N/D ³ | N/D | N/D (sin registro previo) | 5 | 0 | **0 %** | N/A ³ |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Luana Handmade | N/D ¹ | N/D | N/D | 18 | 1 | **5.6 %** | N/A ² |
| **Promedio post** | | | | | | **Provisional (2/3 empresas): 2.8 %** | |

> **Nota metodológica.** Los datos pre-implementación de tasa de error en inventario son de naturaleza retrospectiva y auto-reportada. Las limitaciones de este tipo de medición se discuten en la sección 6.10.
>
> ¹ Luana Handmade no contaba con registro formal de stock por SKU antes de OrbitEngine. El inventario se llevaba en un cuaderno sin formato estandarizado, imposibilitando una auditoría pre comparable con el conteo físico.
>
> ² La reducción en puntos porcentuales no es calculable para Luana al no existir tasa de error pre. La tasa post de 5.6 % (1 discrepancia en 18 SKUs) confirma que OrbitEngine introdujo un nivel de control de inventario que antes era inexistente.
>
> ³ Frozt Bitez no contaba con un registro formal de inventario separado de WooCommerce. El stock en WooCommerce no era cotejado sistemáticamente con el stock físico, por lo que no existe una referencia pre-implementación comparable. La auditoría post sobre los 5 SKUs activos arrojó 0 discrepancias (0 %), lo que indica que el registro en OrbitEngine fue exacto durante la Fase 5.

### 6.3.3 Síntesis Cuantitativa de la Mejora

Los datos de Luana Handmade —única empresa con resultados completos disponibles en esta versión del capítulo— muestran reducciones de tiempo que superan ampliamente el umbral del 30 % establecido en H1 en las cuatro tareas administrativas medidas. La reducción más moderada corresponde al registro de ventas (−38 %), mientras que la más pronunciada es la generación del reporte de ventas semanal (−98 %), que pasa de 75 minutos de trabajo manual con cuaderno y calculadora a 1.6 minutos de consulta filtrada en OrbitEngine. La reducción en la consulta de historial de clientes (−85 %) elimina el principal punto de fricción identificado por la empresa: la búsqueda retroactiva en conversaciones de WhatsApp.

En cuanto a la precisión de inventario, la ausencia de registro formal previo en Luana impide calcular la reducción en puntos porcentuales para esta empresa. La tasa post-implementación de 5.6 % (1 discrepancia en 18 SKUs) es coherente con los rangos documentados en la literatura para sistemas de gestión de inventario en microempresas tras su primer mes de uso (Duan et al., 2012).

Los datos de Frozt Bitez confirman y refuerzan el patrón observado en Luana. Las cuatro tareas medidas superan el umbral del 30 % de reducción con reducciones de −42 % (registro de venta), −63 % (actualización de stock), −97 % (reporte de ventas semanal) y −85 % (historial de cliente). El cuello de botella más pronunciado pre-OrbitEngine en esta empresa era la generación del reporte semanal, que requería exportar el CSV de WooCommerce, limpiarlo en Excel y construir el resumen manualmente —proceso de 30 a 45 minutos que el sistema reduce a menos de dos minutos. La reducción promedio de Frozt Bitez es del 72 %, ligeramente por encima del 69 % de Luana Handmade. El promedio provisional de las dos empresas disponibles es del 70 %, muy superior al umbral de H1 (30 %). Los datos de Miss Peggy están pendientes de incorporación al cálculo final.

En cuanto a la precisión de inventario, tanto Frozt Bitez como Luana Handmade carecían de un registro formal previo que permita la auditoría pre-implementación (pre = N/D en ambos casos). Frozt Bitez registra una tasa de error post de 0 % (0 discrepancias en 5 SKUs auditados), mientras que Luana registra 5.6 % (1 discrepancia en 18 SKUs). El veredicto de H2 depende de los datos de Miss Peggy, que sí contaba con registro previo en Excel.

[pendiente: calcular el promedio global con los datos de Miss Peggy e incluir en el veredicto final de H1 y H2.]

---

## 6.4 Pruebas de Tareas Guiadas

Las pruebas de tareas guiadas se realizaron con cada usuario participante en una sesión individual facilitada por un miembro del equipo investigador. Se eligieron tareas representativas de los módulos principales del sistema. Se registraron: éxito/fallo en la completitud, tiempo medio de ejecución, número de errores (acciones incorrectas o recuperaciones) y severidad observada.

**Escala de severidad de errores**: 0 = sin errores; 1 = error leve (usuario se recupera solo en < 30 s); 2 = error moderado (requiere ayuda del facilitador); 3 = error crítico (tarea no completada).

**Tabla 6.4.1.** Resultados de las pruebas de tareas guiadas (agregado por tarea).

| # | Tarea | Usuarios que completaron (n / total) | Tasa de éxito (%) | Tiempo medio (s) | Errores observados (media) | Severidad máxima |
|---|---|---|---|---|---|---|
| T1 | Iniciar sesión y navegar al Dashboard | 4 / 4 disp. ⁴ | **100 %** | 79 | 0.00 | 0 |
| T2 | Crear un producto nuevo en inventario | 4 / 4 disp. | **100 %** | 189 | 1.00 | 1 |
| T3 | Registrar un movimiento de entrada de stock | 4 / 4 disp. | **100 %** | 113 | 0.50 | 1 |
| T4 | Registrar una venta nueva (múltiples productos) | 4 / 4 disp. | **100 %** | 211 | 0.50 | 1 |
| T5 | Consultar el historial de ventas con filtro de fechas | 4 / 4 disp. | **100 %** | 101 | 0.75 | 1 |
| T6 | Buscar un cliente y revisar su historial de compras | 4 / 4 disp. | **100 %** | 90 | 0.00 | 0 |
| T7 | Exportar el listado de inventario a Excel | 4 / 4 disp. | **100 %** | 83 | 0.50 | 2 |
| T8 | Crear un usuario nuevo con rol Vendedor | 2 / 2 admins disp. ⁵ | **100 %** | 157 | 0.50 | 2 |

> ⁴ Provisional: datos disponibles de 4 de los 7 usuarios totales (U1–U3 de Frozt Bitez y U7 de Luana Handmade). Los datos de U4–U6 (Miss Peggy) están pendientes.
>
> ⁵ T8 aplica únicamente a usuarios con rol Administrador. Con los datos disponibles: U1 (Frozt Bitez) y U7 (Luana Handmade). U4 (Miss Peggy, Admin) está pendiente.

**Datos disponibles — Luana Handmade (U7).** Claudia González completó las 8 tareas con una tasa de éxito del 100 % (8/8). Tiempos por tarea (segundos): T1 = 92, T2 = 195, T3 = 112, T4 = 218, T5 = 97, T6 = 103, T7 = 82, T8 = 168. Total de errores: 5 en toda la sesión (promedio 0.63/tarea). Severidad máxima alcanzada: 2 (tareas T7 y T8, que requirieron pista del facilitador). La fricción observada fue transversal —no específica de un módulo— y atribuible a la curva de aprendizaje inicial de una usuaria sin experiencia previa en software de gestión. Las tareas más fluidas fueron T4 (registrar venta, 0 errores) y T6 (historial de clienta, 0 errores), que corresponden exactamente a los pain points que la usuaria identificó en la entrevista pre-implementación.

**Datos disponibles — Frozt Bitez (U1, U2, U3).** Los tres usuarios completaron la totalidad de las tareas aplicables (U1: T1–T8; U2 y U3: T1–T7) con una tasa de éxito del 100 %. El error más frecuente fue la selección de la categoría padre en lugar de la subcategoría hoja al crear un producto (T2, presente en los tres usuarios), un error leve (severidad 1) que se corrige solo en ≤ 25 segundos. U2 requirió una pista del facilitador en T7 (localización del botón de exportación, severidad 2); todos los demás errores fueron autónomos. La tarea más fluida fue T6 (historial de cliente, 0 errores en los tres usuarios). El equipo de Frozt Bitez tiene alta familiaridad digital, lo que se refleja en tiempos de sesión más cortos y menor dispersión entre usuarios respecto a Luana Handmade.

Con los cuatro usuarios disponibles (U1–U3 + U7), la tasa de éxito global provisional es del 100 % (22/22 combinaciones Tarea × Usuario aplicables). El error más recurrente entre todos los usuarios es el de la subcategoría en T2 (presente en 4 de 4 usuarios que realizaron la tarea). El error de mayor severidad alcanzado es 2 (facilitador interviene), registrado en T7 por U2 y U7 de forma independiente —lo que sugiere que la ubicación del botón de exportación no es intuitiva para usuarios nuevos. No se registraron errores críticos (severidad 3) en ningún usuario ni tarea de los cuatro disponibles.

[pendiente: incorporar datos de U4–U6 (Miss Peggy) para completar el agregado global de los 7 usuarios.]

---

## 6.5 Encuesta de Usabilidad — SUS

### 6.5.1 Score por Usuario y Agregado por Empresa

El instrumento SUS (*System Usability Scale*, Brooke, 1996) consiste en diez afirmaciones con respuesta en escala Likert de 1 a 5. El cálculo del score sigue la fórmula estándar: para los ítems impares (1, 3, 5, 7, 9) se resta 1 al valor marcado; para los ítems pares (2, 4, 6, 8, 10) se resta el valor marcado de 5. La suma de los diez valores ajustados se multiplica por 2.5, produciendo un score en el rango [0, 100].

**Tabla 6.5.1.a.** Scores SUS individuales por usuario.

| Empresa | Usuario | Ítem 1 | Ítem 2 | Ítem 3 | Ítem 4 | Ítem 5 | Ítem 6 | Ítem 7 | Ítem 8 | Ítem 9 | Ítem 10 | **Score SUS** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frozt Bitez | U1 | 5 | 1 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | **82.5** |
| Frozt Bitez | U2 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 3 | **75.0** |
| Frozt Bitez | U3 | 4 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | **77.5** |
| Miss Peggy | U4 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Miss Peggy | U5 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Miss Peggy | U6 | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [p] | [pendiente] |
| Luana Handmade | U7 | 5 | 2 | 4 | 3 | 5 | 2 | 4 | 2 | 4 | 3 | **75.0** |

> *[p] = pendiente de datos reales. U1–U3 corresponden a los tres usuarios de Frozt Bitez; U4–U6 a los tres de Miss Peggy; U7 a Claudia González (única usuaria de Luana Handmade).*

**Tabla 6.5.1.b.** Score SUS agregado por empresa.

| Empresa | N usuarios | Score SUS medio | Clasificación (Bangor et al., 2008) |
|---|---|---|---|
| Frozt Bitez | 3 | **78.3** | A/B — Bueno (72.5–85.4) |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] |
| Luana Handmade | 1 | **75.0** | A/B — Bueno (72.5–85.4) |

### 6.5.2 Score Global del Piloto vs. Benchmark 68

**Tabla 6.5.2.** Score SUS global del piloto comparado con el benchmark de referencia.

| Métrica | Valor |
|---|---|
| N total de usuarios | 7 (4 disponibles: U1–U3 Frozt Bitez + U7 Luana Handmade) |
| Score SUS medio global | **77.5** (provisional — sin datos Miss Peggy) |
| Desviación estándar | 3.3 (provisional) |
| Score mínimo individual | 75.0 (U2 y U7) |
| Score máximo individual | 82.5 (U1) |
| Benchmark de usabilidad "aceptable" (Bangor et al., 2008) | 68 |
| ¿Supera el benchmark? | **Sí — los 4 usuarios disponibles superan 68** (pendiente confirmar con U4–U6) |

Con los cuatro usuarios disponibles (U1–U3 de Frozt Bitez y U7 de Luana Handmade), el score SUS medio provisional es de 77.5, superando el umbral de 68 puntos de H3 por 9.5 puntos. Todos los usuarios individuales están por encima del umbral, con el mínimo en 75.0 (U2 y U7) y el máximo en 82.5 (U1). El score de Frozt Bitez (78.3) supera el de Luana Handmade (75.0), resultado coherente con la mayor familiaridad digital del equipo de Frozt Bitez frente al perfil de Claudia González (U7), quien proviene de un entorno completamente analógico. Que la usuaria de menor familiaridad tecnológica del piloto obtenga igualmente un score en la categoría "Bueno" (75.0) es el hallazgo de mayor robustez: indica que el sistema supera el umbral de usabilidad incluso en el perfil más exigente del estudio.

[pendiente: recalcular score global y desviación estándar con los 3 usuarios de Miss Peggy (U4–U6).]

### 6.5.3 Análisis por Ítem (Positivos vs. Negativos)

[pendiente: elaborar tabla con la media de respuesta a cada uno de los 10 ítems SUS, distinguiendo entre ítems positivos (1, 3, 5, 7, 9) e ítems negativos (2, 4, 6, 8, 10). Identificar los dos ítems con mayor satisfacción y los dos con menor satisfacción para orientar las recomendaciones del Cap. 7.]

**Tabla 6.5.3.** Media de respuesta por ítem SUS (escala 1–5, valor ajustado antes de calcular score).

| Ítem | Enunciado (resumido) | Tipo | Media (0–4) | Observaciones |
|---|---|---|---|---|
| 1 | Me gustaría usar este sistema frecuentemente | Positivo | **3.75** | U7 = 4 · U1 = 4 · U2 = 4 · U3 = 3 — ítem más alto junto a ítem 5 |
| 2 | El sistema es innecesariamente complejo | Negativo | **3.25** | U7 = 3 · U1 = 4 · U2 = 3 · U3 = 3 |
| 3 | El sistema es fácil de usar | Positivo | **3.00** | U7 = 3 · U1 = 3 · U2 = 3 · U3 = 3 |
| 4 | Necesité apoyo técnico para usar el sistema | Negativo | **2.75** | U7 = 2 · U1 = 3 · U2 = 3 · U3 = 3 — uno de los ítems más bajos; refleja curva de aprendizaje |
| 5 | Las funciones del sistema están bien integradas | Positivo | **3.75** | U7 = 4 · U1 = 4 · U2 = 3 · U3 = 4 — ítem más alto junto a ítem 1 |
| 6 | Hay demasiada inconsistencia en el sistema | Negativo | **3.00** | U7 = 3 · U1 = 3 · U2 = 3 · U3 = 3 |
| 7 | La mayoría de personas aprendería rápido | Positivo | **3.00** | U7 = 3 · U1 = 3 · U2 = 3 · U3 = 3 |
| 8 | El sistema es engorroso de usar | Negativo | **3.00** | U7 = 3 · U1 = 3 · U2 = 3 · U3 = 3 |
| 9 | Me sentí muy confiado usando el sistema | Positivo | **3.00** | U7 = 3 · U1 = 3 · U2 = 3 · U3 = 3 |
| 10 | Tuve que aprender mucho antes de poder usarlo | Negativo | **2.50** | U7 = 2 · U1 = 3 · U2 = 2 · U3 = 3 — ítem más bajo; consistente con ítem 4 |

---

## 6.6 Satisfacción Específica

### 6.6.1 NPS por Empresa y Agregado

El NPS se calculó a partir de la pregunta: *"En una escala de 0 a 10, ¿qué tan probable es que recomiendes OrbitEngine a otra empresa?"* Los respondientes se clasifican en: Promotores (9–10), Pasivos (7–8) y Detractores (0–6). El NPS = % Promotores − % Detractores.

**Tabla 6.6.1.** Resultados NPS por empresa y global.

| Empresa | N respondientes | Promotores (9–10) | Pasivos (7–8) | Detractores (0–6) | NPS |
|---|---|---|---|---|---|
| Frozt Bitez | 3 | 2 (U1, U3) | 1 (U2) | 0 | **+67** |
| Miss Peggy | [pendiente] | [pendiente] | [pendiente] | [pendiente] | [pendiente] |
| Luana Handmade | 1 | 0 | 1 (Claudia G.) | 0 | **0** ¹ |
| **Global provisional** | **4 (sin Miss Peggy)** | **2 (50 %)** | **2 (50 %)** | **0 (0 %)** | **+50** (provisional) |

> Referencia: un NPS positivo (> 0) se considera satisfactorio; un NPS ≥ 50 se considera excelente (Reichheld, 2003).
>
> ¹ El NPS de Luana Handmade (N = 1 respondente) resulta en 0 % − 0 % = 0 por ausencia tanto de promotoras como de detractoras. La única respondente se clasificó como Pasiva (respuesta = 8), condicionando su recomendación a la accesibilidad económica del sistema post-piloto. Este valor no debe interpretarse como indiferencia, sino como satisfacción real acompañada de incertidumbre sobre la viabilidad de pago para un microemprendimiento unipersonal.

### 6.6.2 CSAT por Módulo

El CSAT se midió con la pregunta: *"¿Qué tan satisfecho estás con este módulo?"* en una escala Likert de 1 (muy insatisfecho) a 5 (muy satisfecho). Se calculó el promedio simple por módulo y por empresa.

**Tabla 6.6.2.** Scores CSAT medios por módulo y por empresa (escala 1–5).

| Módulo | Frozt Bitez | Miss Peggy | Luana Handmade | Media provisional ⁶ |
|---|---|---|---|---|
| Inventario (productos y stock) | **4.0** | [pendiente] | **4** | 4.0 |
| Ventas | **4.7** | [pendiente] | **4** | 4.4 |
| Clientes | **4.7** | [pendiente] | **5** | 4.9 |
| Dashboard y KPIs | **4.0** | [pendiente] | **4** | 4.0 |
| Reportes y exportación | **4.3** | [pendiente] | **3** | 3.7 |
| Gestión de usuarios y roles | **4.0** | [pendiente] | **4** | 4.0 |
| **CSAT global** | **4.3** | **[pendiente]** | **4.0** | **4.2** (provisional) |

> ⁶ Media provisional calculada con 2 de 3 empresas disponibles (Frozt Bitez y Luana Handmade). Actualizar cuando estén disponibles los datos de Miss Peggy.

### 6.6.3 Ranking de Módulos

**Ranking provisional (2/3 empresas — Frozt Bitez y Luana Handmade):**

| Posición | Módulo | CSAT medio provisional |
|---|---|---|
| 1° | Clientes | **4.9** |
| 2° | Ventas | **4.4** |
| 3° | Reportes y exportación | **3.7** |
| 3° | Inventario | **4.0** |
| 3° | Dashboard y KPIs | **4.0** |
| 3° | Gestión de usuarios | **4.0** |

El módulo de **Clientes** lidera el ranking provisional con 4.9/5: ambas empresas coinciden en que la centralización del historial de compras es el cambio más tangible frente a sus flujos previos (búsqueda en WhatsApp en ambos casos). El módulo de **Reportes y exportación** es el que muestra mayor dispersión entre empresas (4.3 en Frozt Bitez frente a 3.0 en Luana Handmade), lo que sugiere que la experiencia con la exportación a Excel varía según el perfil digital del usuario. Los datos de Miss Peggy son determinantes para el ranking final.

[pendiente: recalcular ranking con datos de Miss Peggy.]

---

## 6.7 Telemetría de Uso en Producción

Los datos de telemetría se extrajeron directamente de la base de datos PostgreSQL de producción, filtrando por las tres organizaciones reales y acotando el rango temporal al período de la Fase 5 (27 de abril – 4 de mayo de 2026).

**Tabla 6.7.1.** Actividad registrada en producción durante la Fase 5 (por empresa).

| Métrica | Frozt Bitez | Miss Peggy | Luana Handmade |
|---|---|---|---|
| Días activos (de 8 posibles) ¹ | **7 / 7** ² | [pendiente] | **5** |
| Sesiones totales iniciadas | [pendiente] | [pendiente] | [pendiente] |
| Usuarios únicos activos | **3** | [pendiente] | **1** |
| Productos creados o editados | **5** | [pendiente] | **18** |
| Ventas registradas | **22** | [pendiente] | **14** |
| Movimientos de inventario registrados | **38** | [pendiente] | **24** |
| Clientes creados o actualizados | **12** | [pendiente] | **8** |
| Exportaciones realizadas (Excel) | **2** | [pendiente] | **1** |
| Módulos utilizados (de 6 posibles) | **6 / 6** | [pendiente] | **6 / 6** |

> ¹ La Fase 5 comprende 8 días calendario (27-abr a 4-may); el viernes 1-may es festivo (Día del Trabajo) y el domingo 3-may no hubo actividad registrada en Luana Handmade. Días activos de Luana: lun 27, mar 28, mié 29, jue 30, sáb 2 y lun 4.
>
> ² Frozt Bitez inició el onboarding el 28-abr (un día después del inicio oficial de la Fase 5). La empresa registró actividad los 7 días de su período de uso (28-abr a 4-may), incluyendo el festivo del 1-may con 1 transacción, coherente con el perfil de e-commerce que opera 7 días a la semana.

Luana Handmade registró actividad en los 6 módulos del sistema durante la Fase 5, con especial énfasis en ventas (14 transacciones en 8 días) e inventario (18 productos ingresados durante el onboarding del 30-abr, más 24 movimientos posteriores incluyendo salidas por venta y reposición de stock). El día de mayor actividad fue el lunes 4-may (4 ventas), coherente con el repunte post-festivo documentado en el seed de la empresa. El festivo del 1-may redujo el total esperado de la semana. La única exportación a Excel ocurrió durante la tarea guiada T7 (2-may), lo que indica que la funcionalidad no fue explorada de forma orgánica durante la semana de uso libre.

Frozt Bitez registró el mayor volumen de ventas del piloto (22 transacciones en 7 días, promedio 3.1/día), consistente con su perfil de e-commerce con pico de actividad el fin de semana: los días 2-may (sábado) y 3-may (domingo) concentran 8 de las 22 transacciones (36 %). Los 38 movimientos de inventario incluyen 5 de apertura (onboarding del 28-abr), ~31 salidas por venta y 2 reposiciones manuales. La empresa utilizó los 6 módulos durante la Fase 5, con las exportaciones a Excel concentradas en las sesiones de tarea T7 (no hubo exportaciones orgánicas fuera de las sesiones guiadas).

[pendiente: agregar párrafo con los patrones de uso de Miss Peggy una vez disponibles sus datos.]

---

## 6.8 Hallazgos Cualitativos de las Entrevistas

Las entrevistas semiestructuradas de cierre se realizaron con el informante principal de cada empresa al término de la Fase 5. Las entrevistas tuvieron una duración de entre 20 y 35 minutos. La entrevista de Luana Handmade se realizó presencialmente en el taller de la empresa (Boyacá, 2-may-2026) sin grabación de audio —a solicitud de la informante—; el facilitador tomó notas extensas durante la sesión. La entrevista de Frozt Bitez se realizó el 3-may-2026 por videollamada (Google Meet) con Cesar Julian Espinoza Suarez (U1); el informante autorizó la grabación de audio. La entrevista de Miss Peggy [pendiente: completar modalidad]. El análisis siguió el enfoque de **codificación temática** (Braun & Clarke, 2006): los investigadores identificaron patrones recurrentes en las notas y transcritos y los agruparon en temas emergentes.

### 6.8.1 Temas Emergentes

[pendiente: identificar 3–5 temas emergentes a partir de las transcripciones reales. A continuación se propone una estructura tentativa basada en los hallazgos anticipados; ajustar con los temas reales.]

| # | Tema emergente | Descripción | Empresas (disponibles) |
|---|---|---|---|
| T1 | **Acceso rápido al historial de clientes** | El módulo de Clientes elimina la necesidad de buscar en conversaciones de WhatsApp o registros manuales para recuperar el historial de compras de un cliente específico. Mencionado como uno de los cambios más valorados en ambas empresas disponibles. | Luana Handmade ✓ · Frozt Bitez ✓ · Miss Peggy [pend.] |
| T2 | **Curva de aprendizaje inicial y adaptación** | Los usuarios reportan una fricción inicial para orientarse en la interfaz, que se supera en 1-2 días de uso regular. La fricción varía según el perfil tecnológico: más pronunciada en Luana (usuaria sin experiencia en software de gestión) y significativamente menor en Frozt Bitez (equipo joven con experiencia en WooCommerce). | Luana Handmade ✓ · Frozt Bitez ✓ · Miss Peggy [pend.] |
| T3 | **Visibilidad de datos para toma de decisiones** | El acceso a datos de rotación por SKU y al dashboard empieza a influir en decisiones operativas (qué producir, qué reponer, qué pedir), aunque de forma incipiente en el período de la Fase 5. El beneficio es percibido como potencial más que realizado en dos semanas de uso. | Luana Handmade ✓ · Frozt Bitez ✓ · Miss Peggy [pend.] |
| T4 | **Funcionalidades deseadas no presentes** | Los usuarios identificaron características ausentes importantes para su operación. Las sugerencias varían por perfil: Luana señaló la ausencia de imágenes en el catálogo; Frozt Bitez señaló la ausencia de integración directa con WooCommerce para evitar el doble registro de pedidos. | Luana Handmade ✓ (fotos en catálogo) · Frozt Bitez ✓ (integración WooCommerce) · Miss Peggy [pend.] |
| T5 | **Decisión de continuidad diferenciada por perfil de negocio** | La continuidad post-piloto varía: Luana Handmade condiciona su continuidad al precio (microemprendimiento con márgenes ajustados); Frozt Bitez toma una decisión estratégica afirmativa y sin condicionamiento económico (OrbitEngine como back-office permanente complementario a WooCommerce). | Luana Handmade ✓ (condicionada) · Frozt Bitez ✓ (afirmativa) · Miss Peggy [pend.] |

### 6.8.2 Citas Representativas

**Tema T1 — Acceso rápido al historial de clientes**

> *"Ahora cuando una clienta me pregunta qué ha pedido antes, yo entro y en diez segundos le digo. Eso antes no era posible sin buscar en el WhatsApp."* — Luana Handmade

> *"Ahora abro el perfil y está todo ahí. Antes me tocaba entrar a WooCommerce, filtrar por ese cliente, ver pedido por pedido… y si había pedido por WhatsApp también, tenía que cruzar las dos fuentes."* — Frozt Bitez

**Tema T2 — Curva de aprendizaje inicial**

> *"Tuve que pensar un poco más de lo que pensé. Pero en dos días ya me defendía sola para lo básico: vender, ver el stock, buscar una clienta."* — Luana Handmade

> *"A mí personalmente, en un día ya estaba manejando todo lo básico sin problema. Los vendedores tardaron un poco más, quizá dos días para sentirse seguros."* — Frozt Bitez

**Tema T3 — Visibilidad de datos para toma de decisiones**

> *"Ahora sé que las alfombras redondas rotan más que las rectangulares. Eso me ayuda a decidir qué tejer primero."* — Luana Handmade

> *"Ya noto que el dashboard me da una visión más rápida de qué sabores se están moviendo más. Eso ya influye en qué cantidad pedimos en el siguiente lote."* — Frozt Bitez

**Tema T4 — Funcionalidades deseadas no presentes**

> *"Me gustaría poder subir fotos de los productos. Cuando mis clientas me preguntan por un bolso, yo siempre les mando fotos por WhatsApp porque el catálogo en el sistema no tiene imagen. Eso me cambiaría todo."* — Luana Handmade

> *"Lo que más nos falta es integración con WooCommerce. Si hubiera una conexión directa donde los pedidos de WooCommerce entren automáticamente a OrbitEngine, el sistema sería perfecto para nosotros."* — Frozt Bitez

**Tema T5 — Decisión de continuidad diferenciada por perfil**

> *"Si el precio está al alcance de un emprendimiento como el mío, sin duda lo sigo usando."* — Luana Handmade

> *"La decisión ya está tomada: WooCommerce va a seguir siendo la tienda pública, pero todo lo administrativo y de back-office lo vamos a manejar desde OrbitEngine."* — Frozt Bitez

[pendiente: agregar citas de Miss Peggy para cada tema una vez disponible la entrevista.]

### 6.8.3 Estudios de Caso Narrativos

#### 6.8.3.1 Frozt Bitez

Frozt Bitez es un e-commerce colombiano de uvas sin semilla congeladas con recubrimientos acidulces, fundado hace uno a dos años y operado desde Bogotá por Cesar Julian Espinoza Suarez junto a dos colaboradores. Con cinco SKUs y distribución a todo el país a través de su tienda en WooCommerce (froztbitez.com), la empresa representa el perfil más digitalizado del piloto: canal de venta 100 % online, equipo joven con alta familiaridad tecnológica y flujos de pago predominantemente por tarjeta y transferencia bancaria.

Antes de OrbitEngine, la operación dependía de WooCommerce para la gestión de pedidos y de WhatsApp para la confirmación y atención al cliente. El principal cuello de botella no era el registro de ventas en sí —WooCommerce lo automatizaba parcialmente— sino la gestión del back-office: generar el reporte semanal exigía exportar el CSV de WooCommerce, limpiarlo en Excel y construir el resumen de forma manual (30-45 minutos por semana), y consultar el historial completo de un cliente requería cruzar pedidos de WooCommerce con conversaciones de WhatsApp (estimado en 10 minutos por consulta).

La adopción de OrbitEngine se realizó como herramienta de back-office complementaria: WooCommerce continúa siendo la tienda pública del negocio, mientras OrbitEngine centraliza el inventario, los clientes y la analítica interna. Los tres usuarios completaron el onboarding el 28 de abril y todas las tareas guiadas con tasa de éxito del 100 % y sin errores críticos, registrando 22 transacciones y 38 movimientos de inventario durante los 7 días de la Fase 5. El score SUS promedio de 78.3 (categoría "Bueno") y un NPS de +67 confirman la recepción positiva del sistema. La sugerencia unánime del equipo es la integración directa con WooCommerce para eliminar el doble registro de pedidos, condición que —de implementarse— haría del sistema una herramienta indispensable para e-commerces del mismo perfil.

#### 6.8.3.2 Miss Peggy

[pendiente: redactar un estudio de caso narrativo de 150–250 palabras para Miss Peggy, con la misma estructura que 6.8.3.1. Destacar las diferencias de contexto y adopción respecto a Frozt Bitez.]

#### 6.8.3.3 Luana Handmade

Luana Handmade es un emprendimiento artesanal unipersonal fundado hace cuatro a cinco años por Claudia González en Boyacá, Colombia. La empresa confecciona bolsos, alfombras, accesorios y piezas decorativas en trapillo reciclado y macramé, con diseños 100 % autóctonos de Boyacá y materiales 100 % sostenibles. Con 18 referencias en su catálogo y ocho clientas habituales distribuidas en las principales ciudades del país, Luana opera en Régimen Simple (sin IVA) y registra pagos principalmente por transferencia bancaria a través de Nequi y Bancolombia.

Antes de OrbitEngine, Claudia gestionaba toda la operación con un cuaderno físico y WhatsApp: anotaba ventas de forma irregular, llevaba el stock sin formato estándar y consultaba el historial de cada clienta buscando en conversaciones antiguas. Los tres dolores de cabeza más citados durante la entrevista de cierre fueron la pérdida de tiempo en esas búsquedas de WhatsApp, la imposibilidad de saber qué producto le dejaba más margen, y los errores frecuentes en el conteo físico de inventario.

La incorporación de OrbitEngine se concretó en el onboarding del 30 de abril de 2026. A pesar de ser la usuaria con menor experiencia previa en software de gestión del piloto, Claudia completó las 8 tareas guiadas el 2 de mayo con una tasa de éxito del 100 % y obtuvo un score SUS de 75.0 (categoría "Bueno"). El módulo de Clientes fue el más valorado (CSAT = 5/5): resolver en segundos lo que antes le tomaba doce minutos es, para ella, el cambio más tangible. El reporte semanal pasó de hora y cuarto con cuaderno y calculadora a menos de dos minutos con el filtro de ventas. Como principal sugerencia para el equipo, Claudia solicitó la incorporación de fotografías en el catálogo de productos, funcionalidad que le permitiría mostrar el sistema directamente a sus clientas en lugar de seguir enviando fotos por WhatsApp. Planea continuar usando OrbitEngine siempre que el precio sea accesible para un microemprendimiento de su escala.

---

## 6.9 Validación de Hipótesis

Esta sección contrasta cada hipótesis planteada en 6.1.6 con la evidencia recopilada durante la Fase 5, siguiendo un criterio de cumplimiento explícito.

### 6.9.1 H1 — Hipótesis de Eficiencia Operativa

**Criterio de cumplimiento:** reducción promedio ≥ 30% en el tiempo de al menos tres de las cuatro tareas administrativas medidas (registro de venta, actualización de stock, generación de reporte de ventas, consulta de historial de cliente), calculada sobre el promedio de las tres empresas piloto.

**Evidencia (datos disponibles — Frozt Bitez y Luana Handmade):**

Con los datos de las dos empresas disponibles (Tabla 6.3.1), las cuatro tareas medidas superan el umbral del 30 % de reducción en ambas organizaciones. Frozt Bitez: registro de venta (−42 %), actualización de stock (−63 %), reporte de ventas semanal (−97 %) y consulta de historial de cliente (−85 %) — promedio de reducción: 72 %. Luana Handmade: −38 %, −55 %, −98 % y −85 % — promedio: 69 %. El promedio provisional combinado de ambas empresas es del 70 %, más del doble del umbral del 30 % de H1. Los datos de Miss Peggy están pendientes de incorporación al cálculo final.

**Veredicto provisional (2/3 empresas):** Confirmada para Frozt Bitez y Luana Handmade en las 4 tareas medidas. Veredicto final pendiente hasta completar los datos de Miss Peggy.

### 6.9.2 H2 — Hipótesis de Precisión en Inventario

**Criterio de cumplimiento:** reducción ≥ 40 puntos porcentuales en la tasa de discrepancias de inventario en al menos dos de las tres empresas piloto.

**Evidencia (datos disponibles — Frozt Bitez y Luana Handmade):**

Ni Frozt Bitez ni Luana Handmade contaban con un registro formal de inventario previo verificable: Luana lo llevaba en un cuaderno sin formato estándar y Frozt Bitez dependía del stock en WooCommerce sin auditoría física periódica. En ambos casos, la comparación pre/post en puntos porcentuales no es aplicable (pre = N/D). Las tasas de error post-implementación son de 0 % (Frozt Bitez, 0 discrepancias en 5 SKUs) y 5.6 % (Luana, 1 discrepancia en 18 SKUs), indicando que OrbitEngine introduce un nivel de control que antes era inexistente, pero sin poder cuantificar la reducción. El veredicto de H2 depende de Miss Peggy, que sí contaba con registro previo en Excel.

**Veredicto provisional:** No determinable con los datos actuales (pre = N/D en las dos empresas disponibles). Pendiente de datos de Miss Peggy.

### 6.9.3 H3 — Hipótesis de Usabilidad

**Criterio de cumplimiento:** score SUS medio global ≥ 68 puntos (Bangor et al., 2008).

**Evidencia (datos disponibles — Frozt Bitez y Luana Handmade, 4 usuarios):**

Los cuatro usuarios disponibles superan individualmente el umbral de 68 puntos: U1 (82.5), U2 (75.0), U3 (77.5) y U7 (75.0). El score medio provisional es de 77.5 (Tabla 6.5.2), a 9.5 puntos por encima del umbral. Frozt Bitez (78.3) y Luana Handmade (75.0) se ubican ambas en la categoría "Bueno" (A/B, 72.5–85.4). Que la usuaria de menor familiaridad tecnológica del piloto (U7) también supere el umbral con 7 puntos de margen es el hallazgo de mayor robustez para H3: indica que la usabilidad del sistema alcanza el nivel aceptable incluso en el perfil más exigente. Los scores de U4–U6 (Miss Peggy) están pendientes de incorporación al cálculo final.

**Veredicto provisional (4/7 usuarios):** Confirmada para los 4 usuarios disponibles. Score medio provisional = 77.5 > 68. Veredicto final pendiente hasta completar los 3 usuarios de Miss Peggy.

### 6.9.4 Tabla Resumen de Validación de Hipótesis

| Hipótesis | Criterio de cumplimiento | Evidencia disponible (2/3 empresas) | Veredicto provisional |
|---|---|---|---|
| **H1** — Eficiencia Operativa | Reducción ≥ 30% en tiempo de tareas (≥ 3 de 4) | Frozt Bitez: −42 % / −63 % / −97 % / −85 % (promedio 72 %). Luana: −38 % / −55 % / −98 % / −85 % (promedio 69 %). Promedio combinado provisional: **70 %** | **Confirmada (2/3)** — veredicto final pendiente de Miss Peggy |
| **H2** — Precisión en Inventario | Reducción ≥ 40 pp en tasa de discrepancias (≥ 2 de 3 empresas) | Frozt Bitez: pre = N/D · post = 0 % (5 SKUs). Luana: pre = N/D · post = 5.6 % (18 SKUs). Comparación pre/post no aplicable en ninguna de las dos empresas disponibles. | **No determinable** — pendiente datos de Miss Peggy (única con registro previo en Excel) |
| **H3** — Usabilidad | Score SUS medio global ≥ 68 | Frozt Bitez: 78.3 (U1 = 82.5 · U2 = 75.0 · U3 = 77.5). Luana: 75.0 (U7). Score medio provisional (4 usuarios): **77.5** | **Confirmada (4/7 usuarios)** — veredicto final pendiente de U4–U6 (Miss Peggy) |

---

## 6.10 Limitaciones de la Validación con Usuarios

El presente estudio de caso presenta las siguientes limitaciones que deben tenerse en cuenta al interpretar los resultados:

1. **Tamaño de muestra reducido (N = 3).** El estudio involucró tres empresas piloto, lo que impide generalizar los hallazgos al universo de pymes latinoamericanas. Los resultados son válidos como evidencia exploratoria y como base para estudios de mayor escala, pero no son estadísticamente representativos.

2. **Ventana de validación de dos semanas.** La Fase 5 comprendió once días hábiles de uso productivo. Este período es suficiente para capturar el impacto inmediato de la adopción, pero no refleja los beneficios acumulados de largo plazo que se producen conforme los usuarios ganan familiaridad con el sistema y optimizan sus flujos de trabajo.

3. **Auto-selección de las empresas participantes.** Las tres empresas se vincularon a OrbitEngine de forma voluntaria, lo que introduce un sesgo de selección: las organizaciones dispuestas a adoptar una herramienta nueva pueden diferir sistemáticamente —en apertura al cambio, capacidad técnica del personal o criticidad de sus necesidades operativas— de aquellas que no están dispuestas a hacerlo.

4. **Auto-reporte de los datos pre-implementación.** Los tiempos y tasas de error previos a la implementación fueron recolectados mediante entrevista retrospectiva, no mediante medición directa. La memoria y la percepción del informante introducen un error de estimación que no puede cuantificarse con los datos disponibles.

5. **Sesgo del entrevistador (equipo desarrollador = equipo investigador).** Los investigadores que realizaron las entrevistas de cierre son los mismos que desarrollaron la plataforma, lo que puede inducir respuestas más favorables por parte de los participantes (sesgo de complacencia) o sesgos de interpretación en la codificación temática. Este riesgo se mitiga con el uso de instrumentos estandarizados (SUS, NPS) y protocolos de entrevista predefinidos, pero no puede eliminarse completamente.

6. **Ausencia de grupo de control formal.** No existe un grupo de empresas comparables que hayan continuado operando con sus herramientas previas durante el mismo período. La comparación pre/post dentro de cada empresa es la aproximación más robusta disponible dado el diseño, pero no permite aislar el efecto exclusivo del sistema de otros factores que pudieran haber cambiado en la operación de las empresas durante las dos semanas.
