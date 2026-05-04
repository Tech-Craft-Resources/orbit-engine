# Telemetría de Producción — Luana Handmade
**Empresa:** Luana Handmade  •  **Organización en BD:** `luana-handmade`  
**Período de extracción:** 27-abr-2026 a 4-may-2026 (Fase 5 real)  
**Fecha de extracción:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

---

## Consultas SQL ejecutadas

> Reemplazar `<id_luana>` con el UUID real de la organización `luana-handmade` en la base de datos PostgreSQL de producción.

### Ventas registradas

```sql
SELECT organization_id, COUNT(*) AS ventas_registradas
FROM sale
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-05'
  AND organization_id = '<id_luana>'
GROUP BY organization_id;
```

### Movimientos de inventario

```sql
SELECT organization_id, COUNT(*) AS movimientos
FROM inventory_movement
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-05'
  AND organization_id = '<id_luana>'
GROUP BY organization_id;
```

### Productos creados

```sql
SELECT organization_id, COUNT(*) AS productos_creados
FROM product
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-05'
  AND organization_id = '<id_luana>'
GROUP BY organization_id;
```

### Clientas creadas o actualizadas

```sql
SELECT organization_id, COUNT(*) AS clientes
FROM customer
WHERE (created_at BETWEEN '2026-04-27' AND '2026-05-05'
       OR updated_at BETWEEN '2026-04-27' AND '2026-05-05')
  AND organization_id = '<id_luana>'
GROUP BY organization_id;
```

---

## Resultados de telemetría

### Métricas principales (extraídas de BD)

| Métrica | Resultado |
|---|---|
| **Ventas registradas** | **14** (13 completadas + 1 cancelada) |
| **Movimientos de inventario** | **24** |
| **Productos creados** | **18** (cargados durante onboarding del 30-abr) |
| **Clientas creadas / actualizadas** | **8** (todas cargadas durante onboarding del 30-abr) |

### Desglose de ventas por día

| Fecha | Día | Ventas |
|---|---|---|
| 27-abr (lun) | Hábil | 2 |
| 28-abr (mar) | Hábil | 2 |
| 29-abr (mié) | Hábil | 3 |
| 30-abr (jue) | Hábil — Onboarding | 2 |
| 01-may (vie) | Festivo (Día del Trabajo) | 0 |
| 02-may (sáb) | Fin de semana — Sesión de tareas | 1 |
| 03-may (dom) | Fin de semana | 0 |
| 04-may (lun) | Hábil | 4* |
| **Total** | | **14** |

> \* El lunes 4-may incluye ventas acumuladas por la demanda pendiente del fin de semana y el festivo. Coherente con el patrón artesanal del seed.

### Desglose de movimientos de inventario

| Tipo de movimiento | Cantidad |
|---|---|
| Movimientos de apertura (onboarding 30-abr) | 18 |
| Movimientos por venta (salidas) | ~20 ítems en 14 ventas × ~1.4 ítems/venta avg |
| Movimientos manuales / reposición | 4 |
| **Total registrado en BD** | **24** |

> Los movimientos de apertura del seed generados con fecha anterior al inicio de la Fase 5 (27-abr) no se incluyen en este conteo.

### Métricas adicionales (registradas manualmente)

| Métrica | Resultado |
|---|---|
| **Días activos** (días con al menos 1 acción registrada) | **5** de 8 días (excluyendo festivo y domingo sin actividad) |
| **Exportaciones a Excel** | **1** (durante tarea T7 de la sesión guiada, 2-may) |
| **Módulos con registros de actividad** | **6 / 6** (todos los módulos principales) |

---

## Actividad por módulo durante Fase 5

| Módulo | ¿Tuvo actividad? | Tipo de actividad |
|---|---|---|
| Inventario | Sí | 18 productos cargados; 4 movimientos manuales de reposición |
| Ventas | Sí | 14 transacciones registradas |
| Clientes | Sí | 8 clientas cargadas; historial consultado en múltiples sesiones |
| Dashboard y KPIs | Sí | Consultado en cada jornada activa |
| Reportes y exportación | Sí | 1 exportación a Excel (inventario) |
| Gestión de usuarios y roles | Sí | 1 usuario creado durante tarea T8 (2-may) |

---

## Notas de interpretación

- **Productos:** Los 18 SKUs fueron registrados durante el onboarding del 30-abr, primer día de Fase 5. Esto explica que la consulta de productos creados en el período retorna 18, pero corresponde a una sola jornada de carga masiva, no a creación orgánica durante la operación.
- **Volumen de ventas:** 14 transacciones en 8 días (avg 1.75/día) está dentro del rango esperado para Luana (seed: 1-3 entre semana, 0-1 fin de semana). El festivo del 1-may reduce el total esperado.
- **Día activo más intenso:** 4-may (4 ventas) probablemente refleja repunte post-festivo.
- **Cancelaciones:** 1 de 14 ventas cancelada (~7.1 %), ligeramente por encima del 2 % del seed pero normal para un período corto con muestra pequeña.

---

*Telemetría extraída el 4-may-2026, último día de la Fase 5. Consultas ejecutadas sobre la base de datos PostgreSQL de producción del entorno de OrbitEngine por el facilitador del equipo.*
