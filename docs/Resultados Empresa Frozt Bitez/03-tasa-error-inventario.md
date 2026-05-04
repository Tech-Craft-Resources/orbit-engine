# Tasa de Error en Inventario — Frozt Bitez
**Empresa:** Frozt Bitez  •  **Informante:** Cesar Julian Espinoza Suarez (Admin, U1)  
**Fechas:** Pre = N/D · Post = 3-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (28-abr a 4-may 2026)**

---

## Fórmula

```
Tasa de error (%) = (número de ítems con discrepancia / total de ítems auditados) × 100
```

---

## Auditoría Pre-Implementación

| Campo | Resultado |
|---|---|
| **Registro previo disponible** | **No** — sin registro formal de inventario |
| **Explicación** | Frozt Bitez manejaba el stock a través del campo de inventario en WooCommerce, pero este valor no se cotejaba de forma sistemática con el stock físico real. No existía un registro de inventario independiente (Excel, cuaderno u otro) que pudiera usarse como referencia para la auditoría pre. |
| **Tasa de error pre** | **N/D (sin registro previo verificable)** |

> **Nota.** La ausencia de registro formal es coherente con el perfil del negocio: e-commerce de volumen reducido (5 SKUs) cuyos pedidos online actualizan el stock en WooCommerce, pero sin auditoría física periódica. WooCommerce no garantiza que el stock registrado refleje el stock físico real (devoluciones, mermas por cadena de frío o pérdidas no registradas quedan fuera del sistema). La comparación pre/post para esta empresa no es calculable en términos de reducción porcentual, igual que en el caso de Luana Handmade.

---

## Auditoría Post-Implementación

**Fecha:** 3-may-2026 (final de la Fase 5)  
**Muestra auditada:** Los 5 SKUs activos de Frozt Bitez (catálogo completo)

| # | SKU | Producto | Stock OrbitEngine | Conteo físico | ¿Discrepancia? |
|---|---|---|---|---|---|
| 1 | FB-001 | Frozt Bitez Maracumango | 18 | 18 | No |
| 2 | FB-002 | Frozt Bitez Limonada Cerezada | 15 | 15 | No |
| 3 | FB-003 | Frozt Bitez Sandía | 14 | 14 | No |
| 4 | FB-004 | Frozt Bitez Frutos Rojos | 13 | 13 | No |
| 5 | FB-005 | Combo Favoritos (Maracumango + Sandía + Frutos Rojos) | 9 | 9 | No |

| Métrica post | Valor |
|---|---|
| **Total ítems auditados** | 5 |
| **Ítems con discrepancia** | 0 |
| **Tasa de error post** | **0 % (0 / 5)** |

---

## Análisis

| Métrica | Pre | Post |
|---|---|---|
| Ítems auditados | — | 5 |
| Discrepancias encontradas | — | 0 |
| Tasa de error (%) | N/D | 0 % |
| Reducción calculable | **No aplica** (pre = N/D) | — |

### Interpretación

- La tasa de error post de 0 % indica que, durante la Fase 5, el stock registrado en OrbitEngine correspondió exactamente al stock físico para los 5 SKUs del catálogo.
- Este resultado es esperable dado el volumen reducido del catálogo (5 SKUs) y el hecho de que los 3 usuarios del equipo registraron activamente sus ventas y movimientos en OrbitEngine durante el período de validación.
- La ausencia de registro previo verificable impide calcular la reducción de discrepancias que exige H2. El veredicto de H2 depende de los datos de Miss Peggy, que sí contaba con un registro previo formal.
- A efectos del estudio, Frozt Bitez aporta un **dato post positivo** (0 % error) pero no contribuye directamente a la verificación de H2 (que requiere comparación pre/post con reducción ≥ 40 %).

---

*Auditoría post realizada el 3-may-2026 mediante conteo físico de los 5 SKUs en las instalaciones de Frozt Bitez (Bogotá). El conteo fue realizado por U1 en presencia del facilitador (videollamada con cámara activa). La referencia de stock se tomó directamente del sistema OrbitEngine al momento del conteo.*
