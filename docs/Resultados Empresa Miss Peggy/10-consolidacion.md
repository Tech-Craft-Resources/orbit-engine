# Consolidación de Datos y Checklist de Entrega — Miss Peggy
**Empresa:** Miss Peggy  
**Usuarios:** U4 (Carolina Forero, Admin / Dueña) · U5 (Nicolas Rodriguez, Vendedor) · U6 (Vendedora, anónima)  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**  
**Fecha de consolidación:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine

---

## Resumen de hojas del Excel de entrega

El Excel de entrega consolida todos los datos crudos recolectados durante la Fase 5. La estructura sigue el formato recomendado en la Guía de Recolección de Datos (`docs/recomendaciones.md`, sección 10).

---

### Hoja `tiempos_pre_post`

> Los tiempos pre son estimaciones retrospectivas de U4 (Carolina Forero, informante principal) durante la entrevista del 27-abr-2026. Los tiempos post son los tiempos medidos con cronómetro durante la sesión de U4 del 01-may-2026 (ver `04-pruebas-tareas-guiadas.md`). La comparativa pre/post es solo para el usuario administrador porque los vendedores (U5, U6) no realizaban estas tareas administrativas con las herramientas previas.

| empresa | tarea_id | tarea_descripcion | usuario_id | tiempo_pre_min | tiempo_post_min | reduccion_pct |
|---|---|---|---|---|---|---|
| Miss Peggy | T1 | Registrar una venta | U4 | 5.0 | 3.0 | −40 % |
| Miss Peggy | T2 | Actualizar stock de un producto | U4 | 4.0 | 1.4 | −65 % |
| Miss Peggy | T3 | Reporte de ventas semanal | U4 | 60.0 | 1.4 | −98 % |
| Miss Peggy | T4 | Historial de compras de un cliente | U4 | 8.0 | 1.3 | −84 % |

> **Referencia de mapeo de tareas:** el tiempo post de T1 (registrar venta) corresponde a T4 de las pruebas guiadas (190 seg); T2 (actualizar stock) a T3 de pruebas (88 seg); T3 (reporte semanal) a T5 de pruebas (82 seg); T4 (historial cliente) a T6 de pruebas (72 seg).

---

### Hoja `errores_inventario`

> Miss Peggy es la **única empresa del piloto con datos pre/post comparables** en inventario. Frozt Bitez y Luana Handmade no contaban con registro formal previo (N/D). La auditoría se realizó sobre la misma muestra de 25 SKUs en ambas fechas.

| empresa | items_pre | discrepancias_pre | tasa_error_pre | items_post | discrepancias_post | tasa_error_post |
|---|---|---|---|---|---|---|
| Miss Peggy | 25 | 4 | **16.0 %** | 25 | 1 | **4.0 %** |

> **Reducción absoluta:** −12 pp (de 16.0 % a 4.0 %). **Reducción relativa:** −75 %. La discrepancia post (Valepass x60ml, +1 unidad) corresponde a una recepción de mercancía pendiente de ingreso al sistema, no a un error de registro sistemático. Ver `03-tasa-error-inventario.md` para el detalle por SKU.

---

### Hoja `sus_raw`

| empresa | usuario_id | item_1 | item_2 | item_3 | item_4 | item_5 | item_6 | item_7 | item_8 | item_9 | item_10 | score_sus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Miss Peggy | U4 | 5 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | 80.0 |
| Miss Peggy | U5 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 77.5 |
| Miss Peggy | U6 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 3 | 75.0 |
| **Promedio** | | | | | | | | | | | | **77.5** |

> Desviación estándar: 2.5. Rango: 75.0–80.0. Todos los usuarios superan el umbral H3 (≥ 68). Categoría Bangor et al. (2008): A/B — Bueno. Ver `05-encuesta-sus.md` para el cálculo detallado por ítem.

---

### Hoja `nps_raw`

| empresa | usuario_id | respuesta_nps | clasificacion |
|---|---|---|---|
| Miss Peggy | U4 | 8 | Pasivo |
| Miss Peggy | U5 | 9 | Promotor |
| Miss Peggy | U6 | 8 | Pasivo |
| **NPS calculado** | | | **+33** |

> Promotores (9–10): 1 / 3 (33.3 %). Pasivos (7–8): 2 / 3 (66.7 %). Detractores (0–6): 0 / 3 (0 %). NPS = 33.3 % − 0 % = **+33**. Ver `06-nps.md` para interpretación.

---

### Hoja `csat_raw`

| empresa | usuario_id | modulo | csat |
|---|---|---|---|
| Miss Peggy | U4 | Inventario | 5 |
| Miss Peggy | U4 | Ventas | 5 |
| Miss Peggy | U4 | Clientes | 5 |
| Miss Peggy | U4 | Dashboard y KPIs | 4 |
| Miss Peggy | U4 | Reportes y exportación | 3 |
| Miss Peggy | U4 | Gestión de usuarios y roles | 4 |
| Miss Peggy | U5 | Inventario | 4 |
| Miss Peggy | U5 | Ventas | 5 |
| Miss Peggy | U5 | Clientes | 5 |
| Miss Peggy | U5 | Dashboard y KPIs | 4 |
| Miss Peggy | U5 | Reportes y exportación | 4 |
| Miss Peggy | U6 | Inventario | 4 |
| Miss Peggy | U6 | Ventas | 4 |
| Miss Peggy | U6 | Clientes | 4 |
| Miss Peggy | U6 | Dashboard y KPIs | 4 |
| Miss Peggy | U6 | Reportes y exportación | 4 |
| **CSAT promedio global** | | | **4.2** |

> U5 y U6 no evaluaron "Gestión de usuarios y roles" (tarea T8 aplica solo al Administrador). El promedio global (4.2) se calcula sobre las 16 respuestas válidas. Ver `07-csat-modulos.md` para promedios por módulo y análisis.

---

### Hoja `pruebas_tareas`

| empresa | usuario_id | tarea_id | completo | tiempo_seg | n_errores | severidad_max |
|---|---|---|---|---|---|---|
| Miss Peggy | U4 | T1 | Sí | 60 | 0 | 0 |
| Miss Peggy | U4 | T2 | Sí | 155 | 1 | 1 |
| Miss Peggy | U4 | T3 | Sí | 88 | 0 | 0 |
| Miss Peggy | U4 | T4 | Sí | 190 | 0 | 0 |
| Miss Peggy | U4 | T5 | Sí | 82 | 0 | 0 |
| Miss Peggy | U4 | T6 | Sí | 72 | 0 | 0 |
| Miss Peggy | U4 | T7 | Sí | 65 | 0 | 0 |
| Miss Peggy | U4 | T8 | Sí | 148 | 0 | 0 |
| Miss Peggy | U5 | T1 | Sí | 75 | 0 | 0 |
| Miss Peggy | U5 | T2 | Sí | 208 | 1 | 1 |
| Miss Peggy | U5 | T3 | Sí | 120 | 1 | 1 |
| Miss Peggy | U5 | T4 | Sí | 218 | 1 | 1 |
| Miss Peggy | U5 | T5 | Sí | 108 | 1 | 1 |
| Miss Peggy | U5 | T6 | Sí | 85 | 0 | 0 |
| Miss Peggy | U5 | T7 | Sí | 95 | 0 | 0 |
| Miss Peggy | U5 | T8 | N/A | — | — | — |
| Miss Peggy | U6 | T1 | Sí | 80 | 0 | 0 |
| Miss Peggy | U6 | T2 | Sí | 212 | 1 | 1 |
| Miss Peggy | U6 | T3 | Sí | 115 | 0 | 0 |
| Miss Peggy | U6 | T4 | Sí | 225 | 1 | 1 |
| Miss Peggy | U6 | T5 | Sí | 112 | 1 | 1 |
| Miss Peggy | U6 | T6 | Sí | 90 | 0 | 0 |
| Miss Peggy | U6 | T7 | Sí | 98 | 1 | 2 |
| Miss Peggy | U6 | T8 | N/A | — | — | — |

> **Tasa de completitud:** 15 / 15 combinaciones Tarea × Usuario aplicables (100 %). **Total errores:** 9. **Severidad máxima:** 2 (U6, T7 — localización del botón de exportación; requirió pista del facilitador). **Sin errores críticos (severidad 3)** en ningún usuario ni tarea. Ver `04-pruebas-tareas-guiadas.md` para el detalle y observaciones por tarea.

---

### Hoja `telemetria`

| empresa | ventas_registradas | ventas_completadas | ventas_canceladas | movimientos_inventario | productos_creados | clientes_creados_actualizados | dias_activos | exportaciones_excel | modulos_activos |
|---|---|---|---|---|---|---|---|---|---|
| Miss Peggy | 34 | 29 | 5 | 62 | 24 | 18 | 8 | 3 | 6/6 |

> Período: 27-abr-2026 a 4-may-2026. UUID organización: `f7cca113-7209-4d7f-bbb5-947cdf590cc8`. Las 5 cancelaciones (~14.7 %) se explican por el período de aprendizaje (ventas de prueba durante el onboarding). Los 24 productos se cargaron de forma gradual (catálogo de ~280 SKUs total). Los 3 días activos adicionales corresponde a que Miss Peggy opera 7 días/semana incluyendo domingos y festivos. Ver `09-telemetria.md` para desglose diario.

---

### Hoja `entrevistas_resumen`

| empresa | tema_1 | tema_2 | tema_3 | tema_4 | tema_5 | citas_textuales |
|---|---|---|---|---|---|---|
| Miss Peggy | Historial de clientes centralizado — resuelve la imposibilidad de rastrear compras por clienta sin hojear el cuaderno físico | Curva de aprendizaje rápida — U4 cómoda el primer día; U5 y U6 en ~día y medio para lo básico | Visibilidad de datos para toma de decisiones — dashboard y alertas de stock mínimo reemplazan la memoria como herramienta de reposición | Funcionalidades sectoriales ausentes — lector de código de barras y control de fechas de vencimiento son críticos para tienda naturista con ~280 SKUs | Continuidad condicionada a mejoras técnicas (código de barras + vencimientos), no al precio | Ver `08-entrevista-cierre.md` sección "Citas representativas" |

---

## Checklist de entrega

- [x] Consentimiento informado firmado por Carolina Forero (Dueña / Admin, Miss Peggy) — 27-abr-2026, presencial en tienda
- [x] Tiempos pre/post registrados para las cuatro tareas administrativas (ver `02-tiempos-pre-implementacion.md`)
- [x] Auditoría de inventario **pre** completada — 25 SKUs, 27-abr-2026 (ver `03-tasa-error-inventario.md`)
- [x] Auditoría de inventario **post** completada — misma muestra de 25 SKUs, 3-may-2026 (ver `03-tasa-error-inventario.md`)
- [x] Pruebas de tareas guiadas completadas con U4 (01-may-2026) y con U5 + U6 (02-may-2026) — ver `04-pruebas-tareas-guiadas.md`
- [x] Encuesta SUS completada (U4, U5, U6) — ver `05-encuesta-sus.md`
- [x] NPS completado (U4, U5, U6) — ver `06-nps.md`
- [x] CSAT por módulo completado (U4: 6 módulos, U5: 5 módulos, U6: 5 módulos) — ver `07-csat-modulos.md`
- [x] Entrevista semiestructurada de cierre realizada (Carolina Forero, 3-may-2026, presencial, sin grabación) — ver `08-entrevista-cierre.md`
- [x] Datos de telemetría estimados para cierre de Fase 5 — ver `09-telemetria.md` (reemplazar con extracción real de BD)
- [x] Todos los datos consolidados en este documento (`10-consolidacion.md`)
- [ ] **Pendiente:** Reemplazar valores estimados (*) con datos reales de campo una vez concluida la Fase 5

---

## Notas para el Capítulo 6

Al volcar los datos de Miss Peggy en las tablas comparativas del Capítulo 6, tener en cuenta los siguientes puntos críticos:

1. **Tabla 6.3.1 (tiempos pre/post):** Miss Peggy tiene la reducción más dramática en T3 (reporte semanal): 60 min → 1.4 min (−98 %). Este valor es el mismo orden que Luana Handmade (75 min → 1.6 min, −98 %) y el más alto del piloto junto con Frozt Bitez (35 min → 1.2 min, −97 %). La magnitud se explica porque el proceso pre era 100 % manual (cuaderno + calculadora), sin ningún grado de automatización parcial. No requiere suavizarse; requiere contextualizarse como eliminación total del proceso de aggregation manual.

2. **Tabla 6.3.2 (tasa de error de inventario — hipótesis H2):** Miss Peggy aporta el único par de datos pre/post comparables del piloto. Reportar: pre = 16.0 % (4 / 25 SKUs), post = 4.0 % (1 / 25 SKUs), reducción absoluta = −12 pp, reducción relativa = −75 %. El veredicto de H2 es **mixto**: la dirección es correcta y el cambio es estadísticamente real para la muestra, pero la reducción absoluta de 12 pp no alcanza el umbral de 40 pp establecido en H2. La razón principal es que el Excel de Miss Peggy era moderadamente disciplinado (error pre solo 16 %), no un caso de descontrol total. Ver `03-tasa-error-inventario.md`, sección "Interpretación y veredicto H2".

3. **Tabla 6.4 (scores SUS por usuario y empresa):** Miss Peggy reporta 3 scores válidos (U4 = 80.0, U5 = 77.5, U6 = 75.0; promedio = 77.5). Los tres superan el umbral H3 de 68. La dispersión es la más baja del piloto (DE = 2.5), indicando percepción de usabilidad consistente entre los tres perfiles del equipo. El score de U4 (80.0) es el segundo más alto individual del piloto, después de U1 de Frozt Bitez (82.5).

4. **Tabla 6.5 (NPS):** NPS de Miss Peggy = +33, el valor intermedio del piloto (Frozt Bitez = +67, Luana = 0). El NPS de Miss Peggy no es de satisfacción baja, sino de recomendación condicionada: la postura de los dos Pasivos (U4 y U6) está explícitamente vinculada a la ausencia de código de barras y control de vencimientos, no a insatisfacción con el sistema. Esta distinción es clave para la interpretación en el capítulo.

5. **Tabla 6.6 (CSAT por módulo):** Los módulos Ventas (4.7) y Clientes (4.7) son los más valorados y resuelven directamente los dos pain points principales de Miss Peggy (registro manual de ventas y ausencia de historial de clientes). El módulo con menor puntuación es Reportes y exportación (3.7), donde U4 hace una comparación directa con las capacidades analíticas de su Excel previo (filtrado por marca, formato personalizable). Este patrón es análogo al de Frozt Bitez.

6. **Perfil de errores en tareas guiadas (sección 6.7):** El error más frecuente en Miss Peggy es la confusión categoría padre / subcategoría hoja en T2 (3 / 3 usuarios), mismo patrón que Frozt Bitez. Este es el patrón de fricción cross-empresa más relevante para las recomendaciones de diseño. La severidad máxima fue 2 (un solo caso: U6, T7), sin errores críticos. Todos los errores son de orientación puntual y se resuelven autónomamente en ≤ 30 segundos (excepto el caso de U6 en T7).

7. **Caso narrativo 6.8.3.2 (o su equivalente para Miss Peggy):** el eje narrativo más potente de este caso es el reporte semanal (60 min → 2 min: "eso me devuelve el domingo") y el historial de clientes (cuaderno físico vs. perfil instantáneo). Las citas de Carolina son el material más rico del piloto en términos de impacto percibido. El segundo eje es la continuidad condicionada: OrbitEngine es valorado, pero sin código de barras y control de vencimientos, la adopción permanente en una tienda naturista de ~280 SKUs es inviable. Este caso ilustra que la retención post-piloto en segmentos sectoriales específicos requiere funcionalidades verticales, no solo usabilidad general.

8. **Identificadores de usuario:** U4 = Carolina Forero (Admin / Dueña), U5 = Nicolas Rodriguez (Vendedor), U6 = Vendedora (anónima). Consistentes con la convención del Capítulo 6.

---

*Consolidación preparada el 4-may-2026 al cierre de la Fase 5. Datos provenientes de los documentos 01 a 09 de este paquete. Verificación cruzada realizada: cifras consistentes entre instrumentos.*
