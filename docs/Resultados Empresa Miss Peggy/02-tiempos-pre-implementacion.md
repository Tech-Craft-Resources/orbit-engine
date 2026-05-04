# Registro de Tiempos Pre-Implementación — Miss Peggy
**Empresa:** Miss Peggy  •  **Informante:** Carolina Forero (Admin / Dueña, U4)  
**Fecha de aplicación:** 27-abr-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

---

## Contexto

Entrevista estructurada de 18 minutos realizada de forma presencial en la tienda antes del onboarding en OrbitEngine. Carolina Forero estimó el tiempo que dedicaba a cada tarea administrativa **antes** de usar OrbitEngine. La herramienta principal era un archivo Excel propio ("Inventario Miss Peggy.xlsx") para el control de inventario. Las ventas se registraban en un cuaderno físico y los reportes semanales se calculaban de forma manual con calculadora. No existía un sistema de gestión de clientes ni historial de compras por clienta.

> **Nota metodológica.** Los tiempos pre-implementación son estimaciones retrospectivas provistas por la informante durante la entrevista. Los tiempos post-implementación son los tiempos reales medidos durante las pruebas de tareas guiadas (ver `04-pruebas-tareas-guiadas.md`, usuario U4). Los valores de este documento son **estimaciones del facilitador** basadas en el perfil del negocio; serán reemplazados por los datos reales de campo.

---

## Registro

**Empresa:** Miss Peggy  
**Fecha:** 27-abr-2026  
**Informante:** Carolina Forero (Dueña / Administradora)

---

### Tarea 1 — Registrar una venta

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **5** |
| **Herramienta previa** | Cuaderno físico (apunte manual de cada transacción) |
| **Descripción del proceso previo** | Para cada venta, Carolina o los vendedores anotaban en el cuaderno la fecha, los productos vendidos, la cantidad y el valor cobrado. Si la clienta pagaba por transferencia o nequi, también se anotaba la referencia de la transacción. El proceso no descontaba automáticamente el stock del Excel; esa actualización se hacía de forma periódica, no en tiempo real. |
| **Notas** | El tiempo varía según la cantidad de productos por venta: ventas de 1 ítem (~3 min) vs. ventas de 3–4 ítems (~8 min). El promedio estimado para una transacción típica es 5 min. |

---

### Tarea 2 — Actualizar el stock de un producto

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **4** |
| **Herramienta previa** | Excel ("Inventario Miss Peggy.xlsx") |
| **Descripción del proceso previo** | Abrir el archivo Excel → buscar el producto en la hoja de inventario (con Ctrl+F o desplazamiento manual) → actualizar la celda de stock → guardar. Con ~280 SKUs en el Excel, la búsqueda de un producto específico podía tardar entre 30 y 90 segundos, especialmente cuando el mismo producto de una marca aparecía en distintas presentaciones. Las actualizaciones se hacían en lotes (al final del día o cada varios días), no en tiempo real después de cada venta. |
| **Notas** | El proceso de actualización por lote acumulaba desactualizaciones; el Excel raramente reflejaba el stock real en un momento dado entre actualizaciones. |

---

### Tarea 3 — Generar el reporte de ventas de la semana

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **60** |
| **Herramienta previa** | Cuaderno físico (fuente de datos) + Excel (tabla de consolidación) + calculadora física |
| **Descripción del proceso previo** | Los domingos por la tarde, Carolina revisaba el cuaderno página por página para identificar todas las ventas de la semana. Sumaba los montos con calculadora, agrupaba por categoría de producto si lo necesitaba y transfería el resumen a una hoja de Excel separada. Con un volumen semanal de 20–35 ventas en semanas típicas, el proceso podía extenderse entre 50 y 90 minutos. |
| **Notas** | Estimación conservadora de una semana con ~25 transacciones. En semanas de sábado muy activo (8+ ventas en el día), el tiempo podía superar los 90 minutos. El reporte semanal era el proceso que más "dolía" a Carolina. |

---

### Tarea 4 — Consultar el historial de compras de un cliente específico

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **8** |
| **Herramienta previa** | Cuaderno físico (búsqueda manual por fecha y nombre) |
| **Descripción del proceso previo** | No existía un registro formal de clientes. Cuando una clienta preguntaba qué había comprado antes, Carolina buscaba en el cuaderno físico rastreando las páginas de semanas anteriores hasta encontrar las entradas que coincidieran con esa persona. El proceso era confiable para clientas muy recientes; para clientas de hace meses, requería revisar cuadernos de períodos anteriores. |
| **Notas** | En casos de clientas con muchas compras o compras antiguas, el tiempo podía extenderse a 15 minutos o más. La respuesta era frecuentemente incompleta porque algunas ventas no se habían anotado con el nombre de la clienta. |

---

## Comparativa pre / post (Tarea × Usuario U4)

| Tarea | Herramienta previa | Tiempo pre (min) | Tiempo post (min)* | Reducción |
|---|---|---|---|---|
| T1 — Registrar una venta | Cuaderno físico | 5.0 | 3.0 | **−40 %** |
| T2 — Actualizar stock | Excel | 4.0 | 1.4 | **−65 %** |
| T3 — Reporte semanal | Cuaderno + Excel + calculadora | 60.0 | 1.4 | **−98 %** |
| T4 — Historial de cliente | Cuaderno físico | 8.0 | 1.3 | **−84 %** |

> \* Tiempo post = tiempo medido con cronómetro durante la sesión de pruebas de tareas guiadas (01-may-2026), usuario U4. Ver `04-pruebas-tareas-guiadas.md`.

---

## Observaciones generales

- El cuello de botella más pronunciado pre-OrbitEngine era el reporte semanal (60 min): Carolina consolidaba a mano datos del cuaderno en Excel cada semana, un proceso manual y repetitivo que realizaba los domingos. Con OrbitEngine, el filtro de ventas por semana produce el resultado en segundos.
- La ausencia de registro de clientes era un segundo punto de fricción importante: sin historial centralizado, la respuesta a preguntas de clientas frecuentes ("¿qué me recomendaste la vez pasada?") dependía de la memoria o de una búsqueda lenta en el cuaderno.
- Las cuatro tareas superan el umbral de reducción del 30 % establecido en H1, con reducciones entre 40 % y 98 %.
- A diferencia de Frozt Bitez (que sí tenía el reporte parcialmente automatizado en WooCommerce), el proceso de reporte de Miss Peggy era 100 % manual, lo que explica el mayor tiempo pre (60 min vs. 35 min en Frozt Bitez).

---

*Entrevista realizada el 27-abr-2026 de forma presencial en la tienda de Miss Peggy, Bogotá. Tiempos estimados por la informante con referencia a una semana típica del primer trimestre de 2026.*
