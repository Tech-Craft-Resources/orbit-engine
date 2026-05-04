# Tasa de Error en Inventario — Luana Handmade
**Empresa:** Luana Handmade  •  **Informante/Usuaria:** Claudia González (Admin, U7)  
**Fecha de aplicación:** pre → 30-abr-2026 · post → 2-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

---

## Fórmula aplicada

```
Tasa de error (%) = (número de ítems con discrepancia / total de ítems auditados) × 100
```

---

## Auditoría Pre-Implementación

**Resultado:** N/D — Sin registro formal previo

> Claudia González no contaba con un registro sistemático de stock por SKU. El inventario se llevaba mediante anotaciones informales en un cuaderno físico sin formato estandarizado: productos aparecían en distintas páginas, con distintos nombres abreviados y sin código unificado. No fue posible establecer un listado de referencia comparable con el conteo físico para determinar una tasa de discrepancia pre.
>
> **Consecuencia para el análisis:** La comparación pre/post de la tasa de error de inventario es **parcial** para Luana Handmade. Solo se reporta la tasa post-implementación, que sirve como indicador de la precisión alcanzada tras el uso de OrbitEngine durante la Fase 5. Se documenta el estado pre como evidencia del nivel de informalidad superado.

---

## Auditoría Post-Implementación

**Fecha:** 2-may-2026 (tarde, tras la sesión de tareas guiadas)  
**Registro de referencia:** Stock en OrbitEngine al momento de la auditoría  
**Muestra:** 18 productos (todos, ya que el catálogo total es < 20 unidades)

### Resultados por producto

| SKU | Producto | Stock en OrbitEngine | Conteo físico | ¿Discrepancia? |
|---|---|---|---|---|
| LUA-BOL-BAN-TC | Bolso Bandolera Terracota | 3 | 3 | No |
| LUA-BOL-BAN-MS | Bolso Bandolera Mostaza | 3 | 3 | No |
| LUA-BOL-TOT-BG | Bolso Tote Beige Natural | 4 | 4 | No |
| LUA-BOL-TOT-VO | Bolso Tote Verde Oliva | 4 | 4 | No |
| LUA-BOL-MOC-CR | Mochila Trapillo Crudo | 3 | 3 | No |
| LUA-BOL-MOC-GP | Mochila Trapillo Gris Perla | 2 | 2 | No |
| LUA-BOL-CLU-RP | Clutch Trapillo Rosa Palo | 6 | 6 | No |
| LUA-ALF-RED-80 | Alfombra Redonda 80cm Crudo | 3 | 3 | No |
| LUA-ALF-RED-100 | Alfombra Redonda 1m Terracota | 2 | 2 | No |
| LUA-ALF-REC-120 | Alfombra Rectangular 1.2m Gris | 2 | 2 | No |
| LUA-ALF-REC-150 | Alfombra Rectangular 1.5m Beige | 1 | 1 | No |
| LUA-ALF-TBA-VS | Tapete de Baño Verde Salvia | 6 | 6 | No |
| LUA-ALF-TBA-MS | Tapete de Baño Mostaza | 7 | 7 | No |
| LUA-ACC-CES-S | Cesta Organizadora S Beige | 10 | 10 | No |
| LUA-ACC-CES-M | Cesta Organizadora M Terracota | 8 | 8 | No |
| LUA-ACC-POS-4 | Posavasos Trapillo x4 (set) | 13 | 13 | No |
| LUA-DEC-COL-MN | Colgante de Pared Macramé Natural | 5 | 5 | No |
| LUA-DEC-ATR-G | Atrapasueños Trapillo Grande | **7** | **8** | **Sí** |

### Cálculo de la tasa de error post

| Métrica | Valor |
|---|---|
| Total de ítems auditados | 18 |
| Ítems con discrepancia | 1 |
| **Tasa de error post (%)** | **5.6 %** |

### Detalle de la discrepancia encontrada

**Producto:** Atrapasueños Trapillo Grande (LUA-DEC-ATR-G)  
**Stock en OrbitEngine:** 7  
**Conteo físico:** 8  
**Diferencia:** +1 unidad (el sistema registra una unidad menos que el físico)  
**Causa probable:** Una unidad producida en los últimos días no fue registrada como entrada de inventario en OrbitEngine; Claudia reconoció tener una pieza terminada que no había ingresado al sistema todavía. No es una venta no registrada sino una producción reciente aún no cargada.

---

## Nota metodológica

> La ausencia de auditoría pre no invalida el hallazgo post. El estado previo (inventario informal sin stock por SKU) representa el caso extremo de error potencial: cualquier unidad podía estar mal contada sin saberlo. La tasa de 5.6 % post-implementación, con una sola discrepancia de naturaleza operacional menor (ítem producido no ingresado), confirma que OrbitEngine introdujo un nivel de control de inventario que antes era inexistente para Luana Handmade.

---

*Auditoría post realizada el 2-may-2026 en las instalaciones de Luana Handmade, Boyacá. El conteo físico fue realizado por Claudia González en presencia del facilitador.*
