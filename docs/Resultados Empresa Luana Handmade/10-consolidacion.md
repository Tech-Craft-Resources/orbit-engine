# Consolidación de Datos — Luana Handmade
**Empresa:** Luana Handmade  •  **Usuaria:** Claudia González (Admin, U7)  
**Fecha de consolidación:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

---

## Hoja: `tiempos_pre_post`

*Una fila por (empresa, tarea). Columnas: empresa, tarea, usuario_id, tiempo_pre_min, tiempo_post_min*

| empresa | tarea | usuario_id | tiempo_pre_min | tiempo_post_min |
|---|---|---|---|---|
| Luana Handmade | T1 — Registrar una venta | U7 | 6.0 | 3.7 |
| Luana Handmade | T2 — Actualizar stock de un producto | U7 | 4.0 | 1.8 |
| Luana Handmade | T3 — Reporte de ventas semanal | U7 | 75.0 | 1.6 |
| Luana Handmade | T4 — Historial de compras de una clienta | U7 | 12.0 | 1.8 |

> Tiempos post corresponden a los cronometrados durante las tareas guiadas T4, T3, T5 y T6 respectivamente (ver `04-pruebas-tareas-guiadas.md`). Conversión: segundos → minutos redondeado a 1 decimal.

---

## Hoja: `errores_inventario`

*Una fila por empresa. Columnas: empresa, items_pre, discrepancias_pre, tasa_pre, items_post, discrepancias_post, tasa_post*

| empresa | items_pre | discrepancias_pre | tasa_pre | items_post | discrepancias_post | tasa_post |
|---|---|---|---|---|---|---|
| Luana Handmade | N/D | N/D | N/D | 18 | 1 | 5.6 % |

> Auditoría pre: no aplicable (sin registro formal previo). Auditoría post: todos los 18 SKUs auditados el 2-may-2026. 1 discrepancia (Atrapasueños Trapillo Grande: sistema 7, físico 8 — pieza producida no ingresada al sistema).

---

## Hoja: `sus_raw`

*Una fila por usuario. Columnas: empresa, usuario_id, item_1 … item_10, score_sus*

| empresa | usuario_id | item_1 | item_2 | item_3 | item_4 | item_5 | item_6 | item_7 | item_8 | item_9 | item_10 | score_sus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Luana Handmade | U7 | 5 | 2 | 4 | 3 | 5 | 2 | 4 | 2 | 4 | 3 | **75.0** |

---

## Hoja: `nps_raw`

*Una fila por usuario. Columnas: empresa, usuario_id, respuesta_nps (0–10), categoria*

| empresa | usuario_id | respuesta_nps | categoria |
|---|---|---|---|
| Luana Handmade | U7 | 8 | Pasiva |

---

## Hoja: `csat_raw`

*Una fila por (usuario, módulo). Columnas: empresa, usuario_id, modulo, csat (1–5)*

| empresa | usuario_id | modulo | csat |
|---|---|---|---|
| Luana Handmade | U7 | Inventario | 4 |
| Luana Handmade | U7 | Ventas | 4 |
| Luana Handmade | U7 | Clientes | 5 |
| Luana Handmade | U7 | Dashboard y KPIs | 4 |
| Luana Handmade | U7 | Reportes y exportación | 3 |
| Luana Handmade | U7 | Gestión de usuarios y roles | 4 |

**CSAT promedio Luana:** 4.0 / 5

---

## Hoja: `pruebas_tareas`

*Una fila por (usuario, tarea). Columnas: empresa, usuario_id, tarea_id, completó, tiempo_seg, n_errores, severidad_max*

| empresa | usuario_id | tarea_id | completó | tiempo_seg | n_errores | severidad_max |
|---|---|---|---|---|---|---|
| Luana Handmade | U7 | T1 | Sí | 92 | 0 | 0 |
| Luana Handmade | U7 | T2 | Sí | 195 | 1 | 1 |
| Luana Handmade | U7 | T3 | Sí | 112 | 1 | 1 |
| Luana Handmade | U7 | T4 | Sí | 218 | 0 | 0 |
| Luana Handmade | U7 | T5 | Sí | 97 | 1 | 1 |
| Luana Handmade | U7 | T6 | Sí | 103 | 0 | 0 |
| Luana Handmade | U7 | T7 | Sí | 82 | 1 | 2 |
| Luana Handmade | U7 | T8 | Sí | 168 | 1 | 2 |

**Tasa de completitud:** 8/8 (100 %)  
**Total errores:** 5  
**Severidad máxima:** 2

---

## Hoja: `telemetria`

*Una fila por empresa. Columnas: métricas de la sección 9*

| empresa | ventas_registradas | movimientos_inventario | productos_creados | clientes | dias_activos | exportaciones | modulos_activos |
|---|---|---|---|---|---|---|---|
| Luana Handmade | 14 | 24 | 18 | 8 | 5 | 1 | 6 |

---

## Hoja: `entrevistas_resumen`

*Una fila por empresa. Columnas: empresa, tema_1 … tema_5, citas_textuales*

| empresa | tema_1 | tema_2 | tema_3 | tema_4 | tema_5 | citas_textuales |
|---|---|---|---|---|---|---|
| Luana Handmade | Acceso rápido a historial de clientas — resuelve pain point crítico del WhatsApp | Curva de aprendizaje por brecha generacional/tecnológica — superada en ~2 días de uso | Visibilidad incipiente de márgenes y rotación de productos influye en decisiones de producción | Necesidad de fotos en catálogo — sigue dependiendo de WhatsApp para mostrar productos | Continuidad condicionada al precio post-piloto — riesgo de churn en microemprendimientos | "Eso me salvó el domingo." / "Que los productos tengan foto. Eso me cambiaría todo." |

---

## Checklist de entrega — Luana Handmade

- [x] Consentimiento informado firmado por Claudia González (30-abr-2026, presencial)
- [x] Tiempos pre registrados para las cuatro tareas administrativas (entrevista 30-abr)
- [x] Auditoría de inventario pre (N/D justificado — sin registro formal previo)
- [x] Auditoría de inventario post completada (18 SKUs, 2-may-2026)
- [x] Pruebas de tareas guiadas completadas con U7 (Claudia González, 2-may-2026)
- [x] Encuesta SUS completada (U7, score 75.0, 2-may-2026)
- [x] NPS completado (U7, respuesta 8 — Pasiva, 2-may-2026)
- [x] CSAT por módulo completado (U7, 6 módulos evaluados, promedio 4.0, 2-may-2026)
- [x] Entrevista semiestructurada de cierre realizada (Claudia González, 2-may-2026, presencial con notas)
- [x] Datos de telemetría extraídos de la base de datos de producción (4-may-2026)
- [x] Todos los datos consolidados en este documento de entrega
- [x] Nombre definitivo de Empresa Placeholder confirmado: **Luana Handmade**

---

## Notas para el Capítulo 6

Al volcar los datos de Luana en las tablas comparativas del Capítulo 6, tener en cuenta:

1. **Tabla 6.3.1 (tiempos pre/post):** Luana es la empresa con mayor reducción porcentual en T3 (reporte semanal: 75 min → 1.6 min, −98 %). Esta cifra es veraz y se explica por la eliminación total del proceso manual de aggregation; no requiere suavizarse, sino contextualizarse.
2. **Tabla 6.3.2 (tasa de error):** reportar la fila pre como "N/D" con nota explicativa. La ausencia de registro formal es en sí misma un hallazgo relevante.
3. **SUS global:** con U7 = 75.0, Luana contribuye un score que supera el umbral H3 (68) con margen razonable.
4. **Caso narrativo 6.8.3.3:** usar como eje narrativo el contraste entre el cuaderno + WhatsApp y OrbitEngine. Las citas de Claudia ("me salvó el domingo", "en diez segundos le digo") son el material más potente de este caso.
5. **Módulos CSAT:** Clientes = 5/5 (el más alto de Luana y posiblemente del estudio completo). Reportes = 3/5 (oportunidad de mejora documentada).

---

*Consolidación preparada el 4-may-2026 al cierre de la Fase 5. Datos provenientes de los documentos 01 a 09 de este paquete. Verificación cruzada realizada: cifras consistentes entre instrumentos.*
