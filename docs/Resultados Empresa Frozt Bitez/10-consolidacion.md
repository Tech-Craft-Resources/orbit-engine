# Consolidación de Datos y Checklist de Entrega — Frozt Bitez
**Empresa:** Frozt Bitez  
**Fase 5 — Validación con usuarios reales (28-abr a 4-may 2026)**  
**Fecha de consolidación:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine

---

## Resumen de hojas del Excel de entrega

El Excel de entrega consolida todos los datos crudos recolectados durante la Fase 5. La estructura sigue el formato recomendado en la Guía de Recolección de Datos (`docs/recomendaciones.md`, sección 10).

### Hoja `tiempos_pre_post`

| empresa | tarea_id | tarea_descripcion | usuario_id | tiempo_pre_min | tiempo_post_min | reduccion_pct |
|---|---|---|---|---|---|---|
| Frozt Bitez | T1 | Registrar una venta | U1 | 6.0 | 3.5 | −42 % |
| Frozt Bitez | T2 | Actualizar stock | U1 | 4.0 | 1.5 | −63 % |
| Frozt Bitez | T3 | Reporte ventas semanal | U1 | 35.0 | 1.2 | −97 % |
| Frozt Bitez | T4 | Historial de cliente | U1 | 10.0 | 1.5 | −85 % |

> Los tiempos pre son estimaciones retrospectivas del informante (U1). Los tiempos post son los tiempos medidos con cronómetro durante la sesión de U1 el 01-may-2026.

---

### Hoja `errores_inventario`

| empresa | items_pre | discrepancias_pre | tasa_error_pre | items_post | discrepancias_post | tasa_error_post |
|---|---|---|---|---|---|---|
| Frozt Bitez | N/D | N/D | N/D (sin registro previo) | 5 | 0 | 0 % |

---

### Hoja `sus_raw`

| empresa | usuario_id | item_1 | item_2 | item_3 | item_4 | item_5 | item_6 | item_7 | item_8 | item_9 | item_10 | score_sus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Frozt Bitez | U1 | 5 | 1 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | 82.5 |
| Frozt Bitez | U2 | 5 | 2 | 4 | 2 | 4 | 2 | 4 | 2 | 4 | 3 | 75.0 |
| Frozt Bitez | U3 | 4 | 2 | 4 | 2 | 5 | 2 | 4 | 2 | 4 | 2 | 77.5 |
| **Promedio** | | | | | | | | | | | | **78.3** |

---

### Hoja `nps_raw`

| empresa | usuario_id | respuesta_nps | clasificacion |
|---|---|---|---|
| Frozt Bitez | U1 | 9 | Promotor |
| Frozt Bitez | U2 | 8 | Pasivo |
| Frozt Bitez | U3 | 9 | Promotor |
| **NPS calculado** | | | **+67** |

---

### Hoja `csat_raw`

| empresa | usuario_id | modulo | csat |
|---|---|---|---|
| Frozt Bitez | U1 | Inventario | 4 |
| Frozt Bitez | U1 | Ventas | 5 |
| Frozt Bitez | U1 | Clientes | 5 |
| Frozt Bitez | U1 | Dashboard y KPIs | 4 |
| Frozt Bitez | U1 | Reportes y exportación | 5 |
| Frozt Bitez | U1 | Gestión de usuarios y roles | 4 |
| Frozt Bitez | U2 | Inventario | 4 |
| Frozt Bitez | U2 | Ventas | 4 |
| Frozt Bitez | U2 | Clientes | 4 |
| Frozt Bitez | U2 | Dashboard y KPIs | 4 |
| Frozt Bitez | U2 | Reportes y exportación | 4 |
| Frozt Bitez | U3 | Inventario | 4 |
| Frozt Bitez | U3 | Ventas | 5 |
| Frozt Bitez | U3 | Clientes | 5 |
| Frozt Bitez | U3 | Dashboard y KPIs | 4 |
| Frozt Bitez | U3 | Reportes y exportación | 4 |
| **CSAT promedio global** | | | **4.3** |

---

### Hoja `pruebas_tareas`

| empresa | usuario_id | tarea_id | completo | tiempo_seg | n_errores | severidad_max |
|---|---|---|---|---|---|---|
| Frozt Bitez | U1 | T1 | Sí | 65 | 0 | 0 |
| Frozt Bitez | U1 | T2 | Sí | 155 | 1 | 1 |
| Frozt Bitez | U1 | T3 | Sí | 95 | 0 | 0 |
| Frozt Bitez | U1 | T4 | Sí | 185 | 0 | 0 |
| Frozt Bitez | U1 | T5 | Sí | 88 | 0 | 0 |
| Frozt Bitez | U1 | T6 | Sí | 75 | 0 | 0 |
| Frozt Bitez | U1 | T7 | Sí | 70 | 0 | 0 |
| Frozt Bitez | U1 | T8 | Sí | 145 | 0 | 0 |
| Frozt Bitez | U2 | T1 | Sí | 78 | 0 | 0 |
| Frozt Bitez | U2 | T2 | Sí | 210 | 1 | 1 |
| Frozt Bitez | U2 | T3 | Sí | 118 | 1 | 1 |
| Frozt Bitez | U2 | T4 | Sí | 225 | 1 | 1 |
| Frozt Bitez | U2 | T5 | Sí | 105 | 1 | 1 |
| Frozt Bitez | U2 | T6 | Sí | 88 | 0 | 0 |
| Frozt Bitez | U2 | T7 | Sí | 92 | 1 | 2 |
| Frozt Bitez | U2 | T8 | N/A | — | — | — |
| Frozt Bitez | U3 | T1 | Sí | 82 | 0 | 0 |
| Frozt Bitez | U3 | T2 | Sí | 195 | 1 | 1 |
| Frozt Bitez | U3 | T3 | Sí | 125 | 0 | 0 |
| Frozt Bitez | U3 | T4 | Sí | 215 | 1 | 1 |
| Frozt Bitez | U3 | T5 | Sí | 115 | 1 | 1 |
| Frozt Bitez | U3 | T6 | Sí | 95 | 0 | 0 |
| Frozt Bitez | U3 | T7 | Sí | 88 | 0 | 0 |
| Frozt Bitez | U3 | T8 | N/A | — | — | — |

---

### Hoja `telemetria`

| empresa | ventas_registradas | ventas_completadas | ventas_canceladas | movimientos_inventario | productos_creados | clientes_creados_actualizados | dias_activos | exportaciones_excel | modulos_activos |
|---|---|---|---|---|---|---|---|---|---|
| Frozt Bitez | 22 | 21 | 1 | 38 | 5 | 12 | 7 | 2 | 6/6 |

---

### Hoja `entrevistas_resumen`

| empresa | tema_1 | tema_2 | tema_3 | tema_4 | tema_5 | citas_textuales |
|---|---|---|---|---|---|---|
| Frozt Bitez | Back-office centralizado como complemento a WooCommerce | Ahorro drástico en reportes de ventas (35 min → ~1 min) | Historial de clientes centralizado sin cruzar fuentes | Demanda de integración con WooCommerce (doble registro) | Continuidad firme y estratégica (sí, en paralelo con WooCommerce) | Ver `08-entrevista-cierre.md` sección "Citas representativas" |

---

## Checklist de entrega

- [x] Consentimiento informado firmado por Frozt Bitez (Cesar Julian Espinoza Suarez, 28-abr-2026)
- [x] Tiempos pre/post registrados para las cuatro tareas administrativas (ver `02-tiempos-pre-implementacion.md`)
- [x] Auditoría de inventario post-implementación completada (ver `03-tasa-error-inventario.md`) — pre = N/D
- [x] Pruebas de tareas guiadas completadas con U1, U2 y U3 (ver `04-pruebas-tareas-guiadas.md`)
- [x] Encuestas SUS completadas (U1, U2, U3) — ver `05-encuesta-sus.md`
- [x] NPS completado (U1, U2, U3) — ver `06-nps.md`
- [x] CSAT por módulo completado (U1, U2, U3) — ver `07-csat-modulos.md`
- [x] Entrevista semiestructurada de cierre realizada (U1, 3-may-2026) — ver `08-entrevista-cierre.md`
- [x] Datos de telemetría estimados — ver `09-telemetria.md` (reemplazar con extracción real de BD)
- [x] Todos los datos consolidados en este documento (`10-consolidacion.md`)
- [ ] **Pendiente:** Reemplazar valores estimados (*) con datos reales de campo una vez concluida la Fase 5

---

## Notas finales

1. Los identificadores **U1 / U2 / U3** corresponden a los tres usuarios de Frozt Bitez y son consistentes con la convención del Capítulo 6 (líneas 205-207 y 213 de `capitulo-6-resultados-usuarios.md`).
2. Los valores marcados como estimaciones del facilitador en los documentos individuales deben ser validados con los datos reales de campo antes de incluirse en el informe final.
3. La continuidad post-piloto de Frozt Bitez es diferente a la de Luana Handmade (condicionada al precio): Frozt Bitez toma una decisión estratégica afirmativa de usar OrbitEngine como back-office permanente en paralelo con WooCommerce.
4. La ausencia de registro formal de inventario previo (pre = N/D) impide verificar H2 con datos de esta empresa. El veredicto de H2 depende de Miss Peggy.
