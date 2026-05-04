# Tasa de Error en Inventario — Miss Peggy
**Empresa:** Miss Peggy  •  **Informante:** Carolina Forero (Admin / Dueña, U4)  
**Fechas:** Pre = 27-abr-2026 · Post = 3-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

> **Nota de contexto.** Miss Peggy es la **única empresa del piloto** que contaba con un registro formal de inventario previo (Excel). Frozt Bitez y Luana Handmade no tenían registros pre-implementación comparables, por lo que Miss Peggy es la empresa determinante para el veredicto de la hipótesis H2 (reducción ≥ 40 % en tasa de discrepancias de inventario).

---

## Fórmula

```
Tasa de error (%) = (número de ítems con discrepancia / total de ítems auditados) × 100
```

---

## Auditoría Pre-Implementación

**Fecha:** 27-abr-2026 (antes de cargar datos en OrbitEngine)  
**Registro de referencia:** Excel "Inventario Miss Peggy.xlsx" (actualización más reciente: semana del 21-abr-2026)  
**Muestra:** 25 SKUs, seleccionados para representar las dos líneas de producto (15 de Naturismo + 10 de Belleza) y distintos rangos de rotación (alta, media y baja).

### Resultados por producto — Pre

| # | SKU | Producto | Stock en Excel | Conteo físico | ¿Discrepancia? |
|---|---|---|---|---|---|
| 1 | MP-HA-001 | Biotina Healthy America | 4 | 4 | No |
| 2 | MP-HA-007 | Creatina x300g Healthy America | 5 | 5 | No |
| 3 | MP-HA-017 | Super Magnesium Healthy America | 10 | 10 | No |
| 4 | MP-NS-001 | Ácido Hialurónico cápsulas tópicas (Natural Systems) | 120 | 117 | **Sí (−3)** |
| 5 | MP-NS-002 | Aloe Vera y Retinol cápsulas tópicas (Natural Systems) | 227 | 223 | **Sí (−4)** |
| 6 | MP-NS-021 | Omega 3 x100 sofgels Natural Systems | 10 | 10 | No |
| 7 | MP-NF-007 | Cremas Naturales NF | 19 | 19 | No |
| 8 | MP-NF-008 | Esencias Freshly | 26 | 24 | **Sí (−2)** |
| 9 | MP-NF-011 | Jabones Naturales NF | 15 | 15 | No |
| 10 | MP-NF-012 | Mieltertos Pastillas | 16 | 16 | No |
| 11 | MP-NTA-010 | Valepass x60ml (Naturfar) | 6 | 6 | No |
| 12 | MP-WI-001 | Acacia x40g (Wilintong) | 26 | 26 | No |
| 13 | MP-WI-006 | Dulces de Miel (Wilintong) | 266 | 266 | No |
| 14 | MP-WI-008 | Flor de Jamaica x100g (Wilintong) | 17 | 17 | No |
| 15 | MP-WI-013 | Polen x125g (Wilintong) | 1 | 1 | No |
| 16 | MP-LD-001 | Cera depilatoria en perlas Ledmar 250g | 15 | 12 | **Sí (−3)** |
| 17 | MP-LD-002 | Cera caliente x500g Ledmar | 8 | 8 | No |
| 18 | MP-LD-003 | Crema depilatoria x200ml Ledmar | 6 | 6 | No |
| 19 | MP-MS-001 | Tinte María Salomé Castaño Natural x90g | 12 | 12 | No |
| 20 | MP-MS-002 | Tinte María Salomé Rubio Miel x90g | 9 | 9 | No |
| 21 | MP-PK-001 | Shampoo Prokpil Nutritivo x400ml | 4 | 4 | No |
| 22 | MP-MG-001 | Esmalte Masglo (surtido colores) | 38 | 38 | No |
| 23 | MP-NL-001 | Esmalte Nailen (surtido colores) | 22 | 22 | No |
| 24 | MP-RK-001 | Crema alisadora Recamier x500g | 3 | 3 | No |
| 25 | MP-DV-001 | Kit tintes Duvy Class | 5 | 5 | No |

### Cálculo de la tasa de error pre

| Métrica pre | Valor |
|---|---|
| **Total ítems auditados** | 25 |
| **Ítems con discrepancia** | 4 |
| **Tasa de error pre (%)** | **16.0 %** |

### Detalle de las discrepancias pre encontradas

| SKU | Causa probable |
|---|---|
| MP-NS-001 (Ácido Hialurónico) | Producto de alta rotación (3+ unidades/semana); el Excel no se actualizaba tras cada venta individual, sino en lotes periódicos. Varias ventas recientes sin descontar. |
| MP-NS-002 (Aloe Vera + Retinol) | Mismo patrón: producto de altísima rotación (cápsulas tópicas vendidas frecuentemente en unidades sueltas). Excel rezagado respecto al stock físico. |
| MP-NF-008 (Esencias Freshly) | Producto de rotación media-alta; 2 unidades vendidas desde la última actualización del Excel que no se habían descontado. |
| MP-LD-001 (Cera Ledmar perlas) | Producto de belleza de alta demanda los sábados (tratamientos de depilación); 3 unidades vendidas sin registrar en Excel. Posible confusión con presentación de frasco. |

---

## Auditoría Post-Implementación

**Fecha:** 3-may-2026 (final de la Fase 5)  
**Registro de referencia:** Stock en OrbitEngine al momento de la auditoría  
**Muestra:** Los mismos 25 SKUs de la auditoría pre

### Resultados por producto — Post

| # | SKU | Producto | Stock en OrbitEngine | Conteo físico | ¿Discrepancia? |
|---|---|---|---|---|---|
| 1 | MP-HA-001 | Biotina Healthy America | 3 | 3 | No |
| 2 | MP-HA-007 | Creatina x300g Healthy America | 3 | 3 | No |
| 3 | MP-HA-017 | Super Magnesium Healthy America | 7 | 7 | No |
| 4 | MP-NS-001 | Ácido Hialurónico cápsulas tópicas | 104 | 104 | No |
| 5 | MP-NS-002 | Aloe Vera y Retinol cápsulas tópicas | 210 | 210 | No |
| 6 | MP-NS-021 | Omega 3 x100 sofgels Natural Systems | 8 | 8 | No |
| 7 | MP-NF-007 | Cremas Naturales NF | 17 | 17 | No |
| 8 | MP-NF-008 | Esencias Freshly | 20 | 20 | No |
| 9 | MP-NF-011 | Jabones Naturales NF | 13 | 13 | No |
| 10 | MP-NF-012 | Mieltertos Pastillas | 12 | 12 | No |
| 11 | MP-NTA-010 | Valepass x60ml (Naturfar) | 6 | 7 | **Sí (+1)** |
| 12 | MP-WI-001 | Acacia x40g (Wilintong) | 21 | 21 | No |
| 13 | MP-WI-006 | Dulces de Miel (Wilintong) | 248 | 248 | No |
| 14 | MP-WI-008 | Flor de Jamaica x100g (Wilintong) | 12 | 12 | No |
| 15 | MP-WI-013 | Polen x125g (Wilintong) | 1 | 1 | No |
| 16 | MP-LD-001 | Cera depilatoria en perlas Ledmar 250g | 8 | 8 | No |
| 17 | MP-LD-002 | Cera caliente x500g Ledmar | 6 | 6 | No |
| 18 | MP-LD-003 | Crema depilatoria x200ml Ledmar | 5 | 5 | No |
| 19 | MP-MS-001 | Tinte María Salomé Castaño Natural x90g | 10 | 10 | No |
| 20 | MP-MS-002 | Tinte María Salomé Rubio Miel x90g | 7 | 7 | No |
| 21 | MP-PK-001 | Shampoo Prokpil Nutritivo x400ml | 3 | 3 | No |
| 22 | MP-MG-001 | Esmalte Masglo (surtido colores) | 33 | 33 | No |
| 23 | MP-NL-001 | Esmalte Nailen (surtido colores) | 19 | 19 | No |
| 24 | MP-RK-001 | Crema alisadora Recamier x500g | 2 | 2 | No |
| 25 | MP-DV-001 | Kit tintes Duvy Class | 4 | 4 | No |

### Cálculo de la tasa de error post

| Métrica post | Valor |
|---|---|
| **Total ítems auditados** | 25 |
| **Ítems con discrepancia** | 1 |
| **Tasa de error post (%)** | **4.0 %** |

### Detalle de la discrepancia post encontrada

**Producto:** Valepass x60ml — MP-NTA-010  
**Stock en OrbitEngine:** 6  
**Conteo físico:** 7  
**Diferencia:** +1 unidad (el sistema registra una unidad menos que el físico)  
**Causa probable:** Una unidad llegó como parte de un pedido al proveedor el 2-may-2026. U4 (Carolina) la recibió y la colocó en la estantería pero aún no había registrado el movimiento de entrada en OrbitEngine al momento de la auditoría del 3-may. No es una venta no registrada sino una recepción de mercancía pendiente de ingreso.

---

## Análisis comparativo

| Métrica | Pre | Post |
|---|---|---|
| Ítems auditados | 25 | 25 |
| Discrepancias encontradas | 4 | 1 |
| Tasa de error (%) | **16.0 %** | **4.0 %** |
| Reducción absoluta | **−12 pp** | — |
| Reducción porcentual relativa | **−75 %** (de 16 % a 4 %) | — |

### Interpretación y veredicto H2

La adopción de OrbitEngine redujo la tasa de discrepancias de 16.0 % a 4.0 % en la muestra auditada. La dirección del cambio confirma la hipótesis H2: el sistema introduce disciplina en el control de inventario y reduce significativamente los errores de registro.

Sin embargo, la **reducción absoluta de 12 puntos porcentuales no alcanza el umbral del 40 % establecido en H2**. Las razones son:

1. El registro previo en Excel de Miss Peggy era relativamente disciplinado comparado con un caso hipotético de descontrol total. La informante actualizaba el Excel de forma periódica (aunque no en tiempo real), lo que produjo un error pre moderado (16 %) en lugar de uno severo.
2. Las 4 discrepancias pre se concentran en productos de alta rotación vendidos en unidades sueltas (cápsulas tópicas, esencias, ceras de belleza), donde cualquier sistema manual tiende a rezagarse.
3. La discrepancia post (1 ítem) es de naturaleza operacional menor: una recepción de mercancía aún no ingresada, no un error de registro sistemático.

**Veredicto H2 para Miss Peggy:** la hipótesis se cumple en **dirección** (el cambio es real y positivo) pero **no en magnitud** (12 pp vs. 40 pp requeridos). Se reporta como resultado mixto; ver sección 6.9.2 del informe principal.

---

*Auditorías realizadas en las instalaciones de Miss Peggy, Bogotá. Pre: 27-abr-2026 (antes del onboarding), conteo físico realizado por Carolina Forero en presencia del facilitador. Post: 3-may-2026, misma muestra, referencia tomada del stock en OrbitEngine al momento del conteo.*
