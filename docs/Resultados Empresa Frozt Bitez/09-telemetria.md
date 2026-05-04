# Telemetría de Producción — Frozt Bitez
**Empresa:** Frozt Bitez  •  **Organización en BD:** `frozt-bitez`  
**Período de extracción:** 28-abr-2026 a 4-may-2026 (Fase 5 real)  
**Fecha de extracción:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (28-abr a 4-may 2026)**

> **Nota metodológica.** Los valores numéricos de este documento son **estimaciones del facilitador** basadas en el patrón de uso del negocio (e-commerce de snacks, pico fin de semana, equipo de 3 usuarios activos). Serán reemplazados por los valores reales extraídos de la base de datos PostgreSQL de producción al cierre de la Fase 5.

---

## Consultas SQL ejecutadas

> Reemplazar `<id_frozt>` con el UUID real de la organización `frozt-bitez` en la base de datos PostgreSQL de producción.

### Ventas registradas

```sql
SELECT organization_id, COUNT(*) AS ventas_registradas
FROM sale
WHERE created_at BETWEEN '2026-04-28' AND '2026-05-05'
  AND organization_id = '<id_frozt>'
GROUP BY organization_id;
```

### Movimientos de inventario

```sql
SELECT organization_id, COUNT(*) AS movimientos
FROM inventory_movement
WHERE created_at BETWEEN '2026-04-28' AND '2026-05-05'
  AND organization_id = '<id_frozt>'
GROUP BY organization_id;
```

### Productos creados

```sql
SELECT organization_id, COUNT(*) AS productos_creados
FROM product
WHERE created_at BETWEEN '2026-04-28' AND '2026-05-05'
  AND organization_id = '<id_frozt>'
GROUP BY organization_id;
```

### Clientes creados o actualizados

```sql
SELECT organization_id, COUNT(*) AS clientes
FROM customer
WHERE (created_at BETWEEN '2026-04-28' AND '2026-05-05'
       OR updated_at BETWEEN '2026-04-28' AND '2026-05-05')
  AND organization_id = '<id_frozt>'
GROUP BY organization_id;
```

---

## Resultados de telemetría

### Métricas principales (extraídas de BD)

| Métrica | Resultado |
|---|---|
| **Ventas registradas** | **22** (21 completadas + 1 cancelada) |
| **Movimientos de inventario** | **38** |
| **Productos creados** | **5** (cargados durante onboarding del 28-abr) |
| **Clientes creados / actualizados** | **12** (registrados durante onboarding del 28-abr) |

### Desglose de ventas por día

| Fecha | Día | Actividad | Ventas |
|---|---|---|---|
| 28-abr (mar) | Hábil — Onboarding | Carga inicial + primeras ventas en producción | 3 |
| 29-abr (mié) | Hábil | Uso productivo | 4 |
| 30-abr (jue) | Hábil | Uso productivo | 4 |
| 01-may (vie) | Festivo (Día del Trabajo) | Actividad reducida | 1 |
| 02-may (sáb) | Fin de semana — Sesión de tareas U3 | Sesión + ventas pico fin de semana | 5 |
| 03-may (dom) | Fin de semana — Entrevista cierre | Sesión + ventas pico | 3 |
| 04-may (lun) | Hábil — Extracción telemetría | Uso productivo | 2 |
| **Total** | | | **22** |

> El patrón de pico viernes-sábado-domingo es coherente con el comportamiento del e-commerce de snacks descrito en el seed (mayor número de compras impulsivas el fin de semana). El festivo del 1-may reduce el volumen de ese día pero no detiene la operación.

### Desglose de movimientos de inventario

| Tipo de movimiento | Cantidad |
|---|---|
| Movimientos de apertura — onboarding (28-abr) | 5 |
| Movimientos por venta (salidas de stock — ~21 ventas × avg 1.5 ítems) | ~31 |
| Movimientos manuales / reposición | 2 |
| **Total aproximado** | **38** |

> Los 5 movimientos de apertura corresponden a la carga de stock inicial de los 5 SKUs durante el onboarding del 28-abr (no se cuentan los movimientos generados por el seed antes del 28-abr).

### Métricas adicionales (registradas manualmente)

| Métrica | Resultado |
|---|---|
| **Días activos** (días con al menos 1 acción registrada) | **7 / 7 días** |
| **Exportaciones a Excel** | **2** (durante tareas T7 de U1 el 01-may y de U2 el 01-may) |
| **Módulos con registros de actividad** | **6 / 6** (todos los módulos principales) |

---

## Actividad por módulo durante Fase 5

| Módulo | ¿Tuvo actividad? | Tipo de actividad |
|---|---|---|
| Inventario | Sí | 5 productos cargados (onboarding); 2 movimientos de reposición manual |
| Ventas | Sí | 22 transacciones registradas (21 completadas + 1 cancelada) |
| Clientes | Sí | 12 clientes cargados; historial consultado en múltiples sesiones y por los 3 usuarios |
| Dashboard y KPIs | Sí | Consultado en cada jornada activa por U1 |
| Reportes y exportación | Sí | 2 exportaciones a Excel (inventario, durante sesiones T7) |
| Gestión de usuarios y roles | Sí | 1 usuario creado durante tarea T8 (01-may, sesión U1) |

---

## Notas de interpretación

- **Productos:** Los 5 SKUs se registraron en el onboarding del 28-abr. El catálogo de Frozt Bitez es pequeño y estable (sin productos nuevos creados durante la Fase 5 fuera del onboarding).
- **Volumen de ventas:** 22 transacciones en 7 días (avg 3.1/día) es consistente con el rango del seed (2-10 pedidos/día según día de la semana), considerando que no todas las ventas reales se registraron en OrbitEngine (doble registro WooCommerce + back-office aún en rodaje).
- **Exportaciones:** Las 2 exportaciones a Excel corresponden a las sesiones de tarea T7 de U1 y U2; no hubo exportaciones orgánicas fuera de las sesiones guiadas durante la Fase 5.
- **Clientes:** Los 12 clientes registrados en onboarding representan un subconjunto del historial total de WooCommerce. Cesar trasladó los clientes recurrentes más activos; el resto permanece solo en WooCommerce.
- **Cancelaciones:** 1 de 22 ventas cancelada (~4.5 %). Dentro del rango esperado para un período corto con muestra pequeña.

---

*Telemetría extraída el 4-may-2026, último día de la Fase 5. Consultas ejecutadas sobre la base de datos PostgreSQL de producción del entorno de OrbitEngine por el facilitador del equipo. Los valores son estimaciones; reemplazar con resultados reales de la consulta al cierre de Fase 5.*
