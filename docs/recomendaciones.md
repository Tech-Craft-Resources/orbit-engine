# Guía de Recolección de Datos para el Capítulo 6 — Resultados de Usuarios

> **A quién va dirigida esta guía.** Está escrita para el equipo de OrbitEngine que realizará la validación con usuarios reales durante la Fase 5 (27 de abril – 8 de mayo de 2026). Su propósito es garantizar que todos los datos que alimentarán el Capítulo 6 sean recolectados de forma consistente y comparable entre las tres empresas piloto.

---

## Nota importante: ahora son tres empresas reales

El piloto de usuarios reales del **Capítulo 6** comprende **tres empresas**, no dos. Las pruebas técnicas del Capítulo 5 se ejecutaron cuando solo Frost Bitez y Miss Peggy estaban activas en producción. En el intervalo transcurrido entre el cierre de esas pruebas y el inicio de la Fase 5, **se incorporó una tercera empresa real** —denominada *Empresa Placeholder* en este borrador— que también debe participar en todas las actividades de validación descritas en esta guía.

**Consecuencia práctica:** cada formulario, sesión de pruebas y entrevista debe aplicarse a las tres empresas. Los datos de telemetría deben extraerse de las tres organizaciones. Ninguna puede quedar fuera porque su ausencia dejaría el estudio de caso incompleto.

---

## 1. Consentimiento Informado

### ¿Qué es?
Un documento que el representante de cada empresa firma antes de comenzar cualquier actividad. Sin este documento, no se puede recolectar datos de la empresa.

### Contenido mínimo del formulario
El formulario debe incluir:
- Nombre de la empresa y del firmante.
- Descripción del propósito del estudio (proyecto de grado, no comercial).
- Lista de datos que se recolectarán (tiempos de tareas, encuestas, entrevista, telemetría de uso).
- Declaración de que los datos se usarán de forma agregada y anonimizada en el informe.
- Autorización explícita para grabar la entrevista de cierre (o declaración de renuncia a la grabación).
- Derecho a retirarse en cualquier momento sin consecuencias.
- Firma y fecha.

### Cuándo obtenerlo
Al inicio de la Semana 1, antes de la sesión de onboarding. Si el representante no puede firmar presencialmente, un PDF firmado digitalmente es válido.

---

## 2. Registro de Tiempos Pre-Implementación (entrevista estructurada)

### ¿Qué es?
Una entrevista corta (15–20 minutos) en la que se le pide al informante principal de la empresa que estime cuánto tiempo dedicaba a cada tarea administrativa **antes** de usar OrbitEngine.

### Por qué importa
Estos datos son la línea base del diseño pre/post. Sin ellos no se puede calcular la reducción de tiempo (H1) ni comparar con los datos post-implementación.

### Tareas sobre las que preguntar
Para cada tarea, pregunta: *"Antes de OrbitEngine, ¿cuánto tiempo tardabas aproximadamente en hacer esto, en promedio?"*

| # | Tarea |
|---|---|
| 1 | Registrar una venta (una transacción con varios productos) |
| 2 | Actualizar el stock de un producto (entrada o salida manual) |
| 3 | Generar el reporte de ventas de la semana (listado, resumen o cualquier formato que usaran) |
| 4 | Consultar el historial de compras de un cliente específico |

### Cómo registrar
- Anota el tiempo en minutos (o en la unidad que el informante use: "me tomaba media hora" = 30 min).
- Si el informante dice "no lo hacía" o "no tenía ese registro", anota `N/A` y escribe una nota.
- Si da un rango ("entre 20 y 45 minutos"), anota el punto medio (32.5) e incluye el rango en los comentarios.
- Pregunta también: *"¿Con qué herramienta lo hacías? (Excel, cuaderno, WhatsApp, nada)"*

### Formato de registro

```
Empresa: _________________________
Fecha: ___________________________
Informante: _______________________ (cargo: _____________)

Tarea 1 — Registrar una venta:
  Tiempo pre (min): ______
  Herramienta previa: ______
  Notas: ______

Tarea 2 — Actualizar stock:
  Tiempo pre (min): ______
  Herramienta previa: ______
  Notas: ______

Tarea 3 — Reporte de ventas semanal:
  Tiempo pre (min): ______
  Herramienta previa: ______
  Notas: ______

Tarea 4 — Historial de un cliente:
  Tiempo pre (min): ______
  Herramienta previa: ______
  Notas: ______
```

---

## 3. Registro de Tasa de Error en Inventario (pre/post)

### ¿Qué es?
Una auditoría de una muestra del inventario para medir cuántos ítems tienen discrepancia entre el stock físico (lo que hay en físico) y el stock registrado (lo que dice el sistema o el registro previo).

### Fórmula
```
Tasa de error (%) = (número de ítems con discrepancia / total de ítems auditados) × 100
```

### Procedimiento pre-implementación
1. Al inicio del onboarding, antes de cargar datos en OrbitEngine, solicita al informante el registro de stock actual (su Excel, cuaderno, etc.).
2. Elige una muestra de **al menos 20 productos** (o todos si son menos de 20).
3. Para cada producto de la muestra, pide que un miembro de la empresa cuente físicamente las unidades y compara con el registro previo.
4. Anota el número de discrepancias encontradas.

### Procedimiento post-implementación
1. Al final de la Semana 2, repite el procedimiento con la misma muestra de productos.
2. Ahora el registro "oficial" es lo que dice OrbitEngine.
3. Anota el número de discrepancias entre el conteo físico y el stock en OrbitEngine.

### Notas importantes
- Usa exactamente la misma muestra de productos en pre y en post para que la comparación sea válida.
- Si la empresa no tiene un registro previo (caso de que "no registraban nada"), anota `N/D (sin registro previo)` en pre y explica en el informe que la comparación es parcial.
- Una "discrepancia" es cualquier diferencia de una o más unidades, sin importar si es positiva o negativa.

---

## 4. Pruebas de Tareas Guiadas

### ¿Qué son?
Sesiones individuales de 45–60 minutos en las que cada usuario realiza tareas predefinidas en el sistema mientras el facilitador observa, mide el tiempo y registra los errores.

### Quién participa
Todos los usuarios de cada empresa que tengan cuenta en OrbitEngine. Idealmente: el Administrador y al menos un Vendedor.

### Lista de tareas

| # | Tarea | Módulo | Duración estimada |
|---|---|---|---|
| T1 | Iniciar sesión y navegar al Dashboard | Auth / Dashboard | 2 min |
| T2 | Crear un producto nuevo en inventario (nombre, categoría, precio, stock inicial, stock mínimo) | Inventario | 5 min |
| T3 | Registrar un movimiento de entrada de stock de 10 unidades de un producto existente | Inventario | 3 min |
| T4 | Registrar una venta nueva con al menos 2 productos distintos y un cliente existente | Ventas | 7 min |
| T5 | Consultar el historial de ventas filtrando por la semana actual | Ventas | 3 min |
| T6 | Buscar un cliente por nombre y ver su historial de compras | Clientes | 3 min |
| T7 | Exportar el listado de inventario a Excel | Reportes | 2 min |
| T8 | (Solo Administrador) Crear un usuario nuevo con rol Vendedor | Usuarios | 5 min |

### Qué registrar por tarea y usuario

Para cada combinación Tarea × Usuario, anota:

- **¿Completó la tarea?** Sí / No / Parcial
- **Tiempo (segundos)**: desde que el facilitador dice "comienza" hasta que el usuario dice "listo" o el facilitador interviene.
- **Número de errores**: cuenta cada acción incorrecta o cada vez que el usuario se "pierde" y tiene que retroceder.
- **Severidad del error más grave** (escala 0–3):
  - 0 = Sin errores
  - 1 = Error leve: el usuario se recupera solo en menos de 30 segundos
  - 2 = Error moderado: el usuario necesita una pista del facilitador
  - 3 = Error crítico: la tarea no pudo completarse

### Reglas del facilitador durante la prueba
- **No ayudes espontáneamente.** Solo interviene cuando el usuario lleva más de 3 minutos bloqueado en la misma tarea o cuando solicita ayuda explícita.
- Si el usuario pregunta "¿lo estoy haciendo bien?", responde: *"Haz lo que te parezca natural."*
- Si el usuario se bloquea gravemente, anota el error como severidad 3 y pasa a la siguiente tarea.
- Después de cada tarea, pregunta: *"¿Algo te pareció confuso o difícil en esto?"* y anota la respuesta.

---

## 5. Encuesta SUS (System Usability Scale)

### ¿Qué es?
Un cuestionario de 10 preguntas estandarizado para medir la usabilidad percibida del sistema. Produce un score de 0 a 100.

### Cuándo aplicarla
Después de la sesión de pruebas de tareas guiadas. Inmediatamente después, para que la experiencia esté fresca.

### Los 10 ítems SUS (usar exactamente este texto)

Instrucción: *"Por favor indica tu nivel de acuerdo con cada afirmación sobre OrbitEngine, donde 1 = Totalmente en desacuerdo y 5 = Totalmente de acuerdo."*

| # | Afirmación |
|---|---|
| 1 | Me gustaría usar este sistema con frecuencia. |
| 2 | El sistema es innecesariamente complejo. |
| 3 | El sistema es fácil de usar. |
| 4 | Necesitaría el apoyo de un técnico para poder usar este sistema. |
| 5 | Las distintas funciones del sistema están bien integradas. |
| 6 | Hay demasiada inconsistencia en el sistema. |
| 7 | La mayoría de las personas aprendería a usar este sistema muy rápidamente. |
| 8 | El sistema es muy engorroso de usar. |
| 9 | Me sentí muy confiado usando el sistema. |
| 10 | Tuve que aprender muchas cosas antes de poder empezar a usar el sistema. |

### Cómo calcular el score SUS

1. Para los **ítems impares** (1, 3, 5, 7, 9): `valor_ajustado = respuesta - 1`
2. Para los **ítems pares** (2, 4, 6, 8, 10): `valor_ajustado = 5 - respuesta`
3. Suma los 10 valores ajustados y multiplica por 2.5.

**Ejemplo:**
- Ítem 1: respuesta 4 → 4 - 1 = 3
- Ítem 2: respuesta 2 → 5 - 2 = 3
- Suma total de los 10 ajustados = 32 → Score SUS = 32 × 2.5 = **80**

### Interpretación (Bangor et al., 2008)

| Score | Calificación | Adjetivo |
|---|---|---|
| ≥ 85.5 | A+ | Excelente |
| 72.5 – 85.4 | A/B | Bueno |
| 52.0 – 72.4 | C | Aceptable / Marginal |
| < 52.0 | F | Inaceptable |

El umbral de H3 es **68 puntos** (punto medio entre las categorías A y C, considerado el mínimo de usabilidad "aceptable" por Bangor et al.).

### Formato de registro

```
Empresa: _________________________
Usuario: U__  (no anotar nombre completo, solo un identificador)
Fecha: ___________________________

Ítem 1: ___  Ítem 2: ___  Ítem 3: ___  Ítem 4: ___  Ítem 5: ___
Ítem 6: ___  Ítem 7: ___  Ítem 8: ___  Ítem 9: ___  Ítem 10: ___

Score SUS calculado: ___
```

---

## 6. NPS (Net Promoter Score)

### ¿Qué es?
Una única pregunta que mide la probabilidad de que el usuario recomiende OrbitEngine a otra empresa.

### La pregunta (usar exactamente este texto)
*"En una escala de 0 a 10, ¿qué tan probable es que recomiendes OrbitEngine a otra empresa o conocido? (0 = Definitivamente no recomendaría; 10 = Definitivamente recomendaría)"*

### Cuándo aplicarla
Junto con la encuesta SUS, al final de la sesión de tareas guiadas.

### Cómo calcular el NPS

- **Promotores**: respuestas 9–10
- **Pasivos**: respuestas 7–8
- **Detractores**: respuestas 0–6

```
NPS = (% Promotores) - (% Detractores)
```

El NPS puede ir de -100 a +100. Un NPS positivo es aceptable; ≥ 50 se considera excelente.

---

## 7. CSAT por Módulo (Customer Satisfaction Score)

### ¿Qué es?
Una serie de preguntas de satisfacción específica, una por módulo de OrbitEngine. Mide cuán satisfecho está el usuario con cada parte del sistema.

### La pregunta base (adaptar por módulo)
*"¿Qué tan satisfecho/a estás con el módulo de [nombre del módulo]?"*
Escala: **1 = Muy insatisfecho — 5 = Muy satisfecho**

### Módulos a evaluar

| # | Módulo | Descripción que dar al usuario |
|---|---|---|
| 1 | Inventario | Gestión de productos, stock y categorías |
| 2 | Ventas | Registro de transacciones e historial de ventas |
| 3 | Clientes | Base de clientes e historial de compras |
| 4 | Dashboard y KPIs | Indicadores en tiempo real (ventas, stock bajo, tendencias) |
| 5 | Reportes y exportación | Exportación a Excel del inventario, ventas y clientes |
| 6 | Gestión de usuarios y roles | Administración de cuentas y permisos |

### Cuándo aplicarlo
Junto con el SUS y el NPS, al final de la sesión de tareas guiadas. Solo pregunta por los módulos que el usuario haya utilizado efectivamente (omite un módulo si el usuario nunca lo usó).

---

## 8. Entrevista Semiestructurada de Cierre

### ¿Qué es?
Una conversación guiada de 20–35 minutos con el informante principal de cada empresa al final de la Fase 5. Su propósito es recoger el impacto percibido, las dificultades y las sugerencias de forma cualitativa y profunda.

### Cuándo realizarla
En la Semana 2, después de las sesiones de pruebas de tareas de todos los usuarios de la empresa. Una entrevista por empresa (con el informante principal o con el dueño).

### Preparación
- Solicita autorización para grabar (o tomar notas extensas si no hay autorización).
- Realiza la entrevista en un lugar tranquilo, sin interrupciones.
- Si es presencial: mejor. Si es por videollamada: también es válido.

### Guía de preguntas (semiestructurada: no leer como cuestionario, guiar como conversación)

**Bloque 1 — Contexto previo**
1. *Antes de OrbitEngine, ¿cómo gestionabas el inventario y las ventas? ¿Qué herramientas usabas?*
2. *¿Cuáles eran los mayores dolores de cabeza operativos que tenías?*

**Bloque 2 — Proceso de adopción**
3. *¿Cómo fue el proceso de empezar a usar OrbitEngine? ¿Qué fue fácil y qué fue difícil?*
4. *¿Cuánto tiempo aproximadamente les tomó a ti y a tu equipo sentirse cómodos con el sistema?*

**Bloque 3 — Impacto percibido**
5. *¿Qué cambios concretos has notado en tu operación desde que empezaste a usar OrbitEngine?*
6. *¿Hay algo que antes te tomaba mucho tiempo y ahora es más rápido? ¿Cuánto más rápido, aproximadamente?*
7. *¿Ha cambiado la forma en que tomas decisiones sobre el negocio? ¿En qué sentido?*

**Bloque 4 — Dificultades y sugerencias**
8. *¿Hubo alguna funcionalidad que encontraste confusa o difícil de usar?*
9. *¿Hubo algo que buscaste en el sistema y no encontraste?*
10. *Si pudieras pedirle al equipo una sola mejora, ¿cuál sería?*

**Bloque 5 — Cierre**
11. *¿Planeas seguir usando OrbitEngine después de que termine este período de prueba?*
12. *¿Hay algo que quieras agregar que no te haya preguntado?*

### Cómo transcribir y codificar
1. Transcribe las respuestas a las preguntas 5, 6, 7, 8, 9 y 10 de forma textual o en paráfrasis cercana.
2. Agrupa las respuestas de las tres empresas en una tabla o documento comparativo.
3. Identifica temas recurrentes (frases o ideas que aparecen en más de una empresa). Esos son los "temas emergentes" de la sección 6.8.1.
4. Selecciona 1–2 citas textuales llamativas por tema para incluir en la sección 6.8.2.

---

## 9. Extracción de Telemetría de Producción

### Qué datos extraer
Directamente desde la base de datos PostgreSQL de producción, filtrado por las tres organizaciones reales y el rango de fechas de la Fase 5 (2026-04-27 a 2026-05-08).

### Consultas sugeridas

```sql
-- Sesiones / actividad por organización
-- (ajustar según cómo estén registradas las sesiones en el modelo)

-- Ventas registradas por organización
SELECT organization_id, COUNT(*) AS ventas_registradas
FROM sale
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-09'
  AND organization_id IN (<id_frost>, <id_miss_peggy>, <id_placeholder>)
GROUP BY organization_id;

-- Movimientos de inventario por organización
SELECT organization_id, COUNT(*) AS movimientos
FROM inventory_movement
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-09'
  AND organization_id IN (<id_frost>, <id_miss_peggy>, <id_placeholder>)
GROUP BY organization_id;

-- Productos creados por organización
SELECT organization_id, COUNT(*) AS productos_creados
FROM product
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-09'
  AND organization_id IN (<id_frost>, <id_miss_peggy>, <id_placeholder>)
GROUP BY organization_id;

-- Clientes creados o actualizados por organización
SELECT organization_id, COUNT(*) AS clientes
FROM customer
WHERE (created_at BETWEEN '2026-04-27' AND '2026-05-09'
       OR updated_at BETWEEN '2026-04-27' AND '2026-05-09')
  AND organization_id IN (<id_frost>, <id_miss_peggy>, <id_placeholder>)
GROUP BY organization_id;
```

> Reemplaza `<id_frost>`, `<id_miss_peggy>` y `<id_placeholder>` con los UUIDs reales de cada organización en la base de datos.

### Datos adicionales a registrar manualmente
- Días activos: número de días distintos en los que hubo al menos una acción registrada por parte de cada organización.
- Exportaciones: número de veces que se descargó un Excel (si hay un log de esa acción en el backend).
- Módulos utilizados: cuántos de los 6 módulos principales tiene registros de actividad cada empresa durante la Fase 5.

---

## 10. Consolidación y Entrega de Datos

### Formato de entrega recomendado
Organiza todos los datos recolectados en un archivo Excel con las siguientes hojas:

| Hoja | Contenido |
|---|---|
| `tiempos_pre_post` | Una fila por (empresa, tarea, usuario). Columnas: tiempo_pre_min, tiempo_post_min. |
| `errores_inventario` | Una fila por empresa. Columnas: items_pre, discrepancias_pre, items_post, discrepancias_post. |
| `sus_raw` | Una fila por usuario. Columnas: empresa, usuario_id, item_1 … item_10, score_sus. |
| `nps_raw` | Una fila por usuario. Columnas: empresa, usuario_id, respuesta_nps (0–10). |
| `csat_raw` | Una fila por (usuario, módulo). Columnas: empresa, usuario_id, modulo, csat (1–5). |
| `pruebas_tareas` | Una fila por (usuario, tarea). Columnas: empresa, usuario_id, tarea_id, completó, tiempo_seg, n_errores, severidad_max. |
| `telemetria` | Una fila por empresa. Columnas: las métricas de la sección 9. |
| `entrevistas_resumen` | Una fila por empresa. Columnas: tema_1 … tema_5 (resumen de hallazgos por tema), citas_textuales. |

### Lista de verificación antes de redactar el Capítulo 6

- [ ] Consentimiento informado firmado por las tres empresas
- [ ] Tiempos pre/post registrados para las cuatro tareas administrativas
- [ ] Auditoría de inventario pre y post para las tres empresas
- [ ] Pruebas de tareas guiadas completadas con todos los usuarios
- [ ] Encuestas SUS completadas (todos los usuarios)
- [ ] NPS completado (todos los usuarios)
- [ ] CSAT por módulo completado (todos los usuarios)
- [ ] Entrevistas semiestructuradas de cierre realizadas (una por empresa)
- [ ] Datos de telemetría extraídos de la base de datos de producción
- [ ] Todos los datos consolidados en el Excel de entrega
- [ ] Nombre definitivo de Empresa Placeholder confirmado
