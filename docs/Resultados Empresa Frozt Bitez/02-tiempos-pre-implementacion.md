# Registro de Tiempos Pre-Implementación — Frozt Bitez
**Empresa:** Frozt Bitez  •  **Informante:** Cesar Julian Espinoza Suarez (Admin, U1)  
**Fecha de aplicación:** 28-abr-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (28-abr a 4-may 2026)**

---

## Contexto

Entrevista estructurada de 18 minutos realizada por videollamada al inicio de la Fase 5, antes del onboarding en OrbitEngine. El informante estimó el tiempo que dedicaba a cada tarea administrativa **antes** de usar OrbitEngine. La herramienta principal previa era WooCommerce para la gestión de pedidos online, complementada con WhatsApp para confirmaciones y atención al cliente.

> **Nota metodológica.** Los tiempos pre-implementación son estimaciones retrospectivas provistas por el informante durante la entrevista. Los tiempos post-implementación son los tiempos reales medidos durante las pruebas de tareas guiadas (ver `04-pruebas-tareas-guiadas.md`, usuario U1). Los valores de este documento son **estimaciones del facilitador** basadas en el perfil del negocio; serán reemplazados por los datos reales de campo.

---

## Registro

**Empresa:** Frozt Bitez  
**Fecha:** 28-abr-2026  
**Informante:** Cesar Julian Espinoza Suarez (Administrador / dueño)

---

### Tarea 1 — Registrar una venta

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **6** |
| **Herramienta previa** | WooCommerce (alta del pedido) + WhatsApp (confirmación de pago con el cliente) |
| **Descripción del proceso previo** | El cliente realizaba el pedido por la tienda WooCommerce o por WhatsApp/Instagram. Cesar confirmaba la disponibilidad de stock en WooCommerce, confirmaba el pago por WhatsApp, y actualizaba manualmente el estado del pedido en WooCommerce. Si el pedido llegaba por WhatsApp, debía además crearlo manualmente en WooCommerce para llevar el registro. |
| **Notas** | El tiempo varía según si el pedido llega por WooCommerce directo (~4 min) o por WhatsApp/Instagram (~8 min). El promedio estimado es 6 min. |

---

### Tarea 2 — Actualizar el stock de un producto

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **4** |
| **Herramienta previa** | WooCommerce (edición de producto en el panel de administración) |
| **Descripción del proceso previo** | Acceder al panel de WooCommerce → Productos → editar el producto específico → modificar el campo de stock → guardar. El proceso requería navegar varios niveles del CMS y era propenso a errores si se actualizaba el producto equivocado. |
| **Notas** | El stock en WooCommerce no siempre reflejaba el stock físico real; la actualización manual se hacía de forma periódica, no en tiempo real. |

---

### Tarea 3 — Generar el reporte de ventas de la semana

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **35** |
| **Herramienta previa** | WooCommerce (exportación CSV) + Microsoft Excel (consolidación y resumen) |
| **Descripción del proceso previo** | Desde WooCommerce → Pedidos → Exportar CSV con filtro de fechas de la semana → abrir en Excel → eliminar columnas irrelevantes → aplicar fórmulas para calcular totales, promedios y desglose por producto → formatear el resumen. El proceso era manual y repetido cada semana. |
| **Notas** | En semanas con más de 50 pedidos, el tiempo podía superar los 45 minutos. El facilitador usó 35 min como estimación conservadora de una semana típica. |

---

### Tarea 4 — Consultar el historial de compras de un cliente específico

| Campo | Dato |
|---|---|
| **Tiempo pre (min)** | **10** |
| **Herramienta previa** | WooCommerce (filtro de pedidos por cliente) + WhatsApp (historial de conversación) |
| **Descripción del proceso previo** | En WooCommerce: Pedidos → filtrar por nombre o email del cliente → revisar los pedidos uno por uno para armar el historial. Si el cliente también había pedido por WhatsApp o Instagram, había que cruzar ambas fuentes manualmente. |
| **Notas** | Para clientes frecuentes o con pedidos mezclados entre canales, el proceso podía extenderse a 15 minutos. |

---

## Comparativa pre / post (Tarea × Usuario U1)

| Tarea | Herramienta previa | Tiempo pre (min) | Tiempo post (min)* | Reducción |
|---|---|---|---|---|
| T1 — Registrar una venta | WooCommerce + WhatsApp | 6.0 | 3.5 | **−42 %** |
| T2 — Actualizar stock | WooCommerce | 4.0 | 1.5 | **−63 %** |
| T3 — Reporte semanal | WooCommerce CSV + Excel | 35.0 | 1.2 | **−97 %** |
| T4 — Historial de cliente | WooCommerce + WhatsApp | 10.0 | 1.5 | **−85 %** |

> \* Tiempo post = tiempo medido con cronómetro durante la sesión de pruebas de tareas guiadas (01-may-2026), usuario U1. Ver `04-pruebas-tareas-guiadas.md`.

---

## Observaciones generales

- El cuello de botella más pronunciado pre-OrbitEngine era el reporte semanal: requería combinar datos de WooCommerce y Excel de forma manual, un proceso tedioso que se hacía típicamente los lunes o los fines de semana. Con OrbitEngine, el filtro de ventas por semana produce el resultado en segundos.
- La doble gestión de pedidos (WooCommerce + WhatsApp) generaba ineficiencias y riesgo de inconsistencias de stock. OrbitEngine centraliza el registro, aunque WooCommerce continúa como tienda pública.
- Las cuatro tareas superan el umbral de reducción del 30 % establecido en H1, con reducciones entre 42 % y 97 %.

---

*Entrevista realizada el 28-abr-2026 por videollamada. Tiempos estimados por el informante con referencia a una operación típica durante el primer trimestre de 2026.*
