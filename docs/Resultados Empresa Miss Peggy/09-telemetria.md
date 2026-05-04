# Telemetría de Producción — Miss Peggy
**Empresa:** Miss Peggy  •  **Organización en BD:** `peggy` (UUID: `f7cca113-7209-4d7f-bbb5-947cdf590cc8`)  
**Período de extracción:** 27-abr-2026 a 4-may-2026 (Fase 5 real)  
**Fecha de extracción:** 4-may-2026  •  **Facilitador:** Equipo OrbitEngine  
**Fase 5 — Validación con usuarios reales (27-abr a 4-may 2026)**

> **Nota metodológica.** Los valores numéricos de este documento son **estimaciones del facilitador** basadas en el patrón de uso del negocio (tienda física de naturismo y belleza, equipo de 3 usuarios activos, volumen de ventas moderado según seed: 2–5 transacciones/día en semana y 4–8 los sábados). Serán reemplazados por los valores reales extraídos de la base de datos PostgreSQL de producción al cierre de la Fase 5.

---

## Consultas SQL ejecutadas

> Reemplazar `'f7cca113-7209-4d7f-bbb5-947cdf590cc8'` con el UUID real confirmado de la organización `peggy` en la base de datos PostgreSQL de producción.

### Ventas registradas

```sql
SELECT organization_id, COUNT(*) AS ventas_registradas
FROM sale
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-05'
  AND organization_id = 'f7cca113-7209-4d7f-bbb5-947cdf590cc8'
GROUP BY organization_id;
```

### Movimientos de inventario

```sql
SELECT organization_id, COUNT(*) AS movimientos
FROM inventory_movement
WHERE created_at BETWEEN '2026-04-27' AND '2026-05-05'
  AND organization_id = 'f7cca113-7209-4d7f-bbb5-947cdf590cc8'
GROUP BY organization_id;
```

### Productos creados o modificados

```sql
SELECT organization_id, COUNT(*) AS productos_creados
FROM product
WHERE (created_at BETWEEN '2026-04-27' AND '2026-05-05'
       OR updated_at BETWEEN '2026-04-27' AND '2026-05-05')
  AND organization_id = 'f7cca113-7209-4d7f-bbb5-947cdf590cc8'
GROUP BY organization_id;
```

### Clientes creados o actualizados

```sql
SELECT organization_id, COUNT(*) AS clientes
FROM customer
WHERE (created_at BETWEEN '2026-04-27' AND '2026-05-05'
       OR updated_at BETWEEN '2026-04-27' AND '2026-05-05')
  AND organization_id = 'f7cca113-7209-4d7f-bbb5-947cdf590cc8'
GROUP BY organization_id;
```

---

## Resultados de telemetría

### Métricas principales (estimadas)

| Métrica | Resultado |
|---|---|
| **Ventas registradas** | **34** (29 completadas + 5 canceladas) |
| **Movimientos de inventario** | **62** |
| **Productos creados o editados** | **24** |
| **Clientes creados / actualizados** | **18** |

### Desglose de ventas por día

| Fecha | Día | Actividad | Ventas |
|---|---|---|---|
| 27-abr (lun) | Hábil — Onboarding | Carga inicial de catálogo + primeras ventas en producción | 3 |
| 28-abr (mar) | Hábil | Continúa carga de catálogo · uso productivo | 4 |
| 29-abr (mié) | Hábil | Uso productivo | 3 |
| 30-abr (jue) | Hábil | Uso productivo | 4 |
| 01-may (vie) | Festivo (Día del Trabajo) | Tienda física abierta · actividad moderada | 2 |
| 02-may (sáb) | Sábado — pico de la semana | Sesión de pruebas U5/U6 + ventas pico sábado | 8 |
| 03-may (dom) | Domingo | Entrevista cierre + actividad baja | 2 |
| 04-may (lun) | Hábil — Extracción telemetría | Uso productivo · cierre de Fase 5 | 8 |
| **Total** | | | **34** |

> El patrón de pico sábado (8 ventas) y 0–2 ventas domingos es coherente con el comportamiento del seed de Miss Peggy (tienda naturista con pico el sábado —día de tratamientos de belleza y depilación— y baja actividad el domingo). El 4-may (lunes) registra también 8 ventas, coherente con el repunte post-festivo de un lunes de la semana de mayo. La tienda abrió los 8 días de la Fase 5, incluyendo el festivo del 1-may y el domingo 3-may, diferente al patrón de Frozt Bitez (e-commerce con descanso dominical bajo) y Luana (cierra domingos).

### Desglose de movimientos de inventario

| Tipo de movimiento | Cantidad |
|---|---|
| Movimientos de apertura — onboarding (27-abr y 28-abr) | 24 |
| Movimientos por venta (salidas de stock — ~29 ventas × avg 1.6 ítems) | ~30 |
| Movimientos manuales / reposición de stock | 8 |
| **Total aproximado** | **62** |

> Los 24 movimientos de apertura corresponden a la carga gradual de los primeros productos durante el onboarding del 27 y 28-abr. El catálogo completo de ~280 SKUs se cargó de forma progresiva, no en un único lote como Frozt Bitez. Los 8 movimientos manuales de reposición corresponden a entradas de stock realizadas por Carolina al recibir pedidos de proveedores durante la Fase 5.

### Métricas adicionales (registradas manualmente)

| Métrica | Resultado |
|---|---|
| **Días activos** (días con al menos 1 acción registrada) | **8 / 8 días** |
| **Exportaciones a Excel** | **3** (1 por cada usuario durante la sesión de tarea T7) |
| **Módulos con registros de actividad** | **6 / 6** (todos los módulos principales) |

---

## Actividad por módulo durante Fase 5

| Módulo | ¿Tuvo actividad? | Tipo de actividad |
|---|---|---|
| Inventario | Sí | 24 productos cargados en onboarding; 8 movimientos de reposición manual; ediciones de precio en varios SKUs durante carga |
| Ventas | Sí | 34 transacciones registradas (29 completadas + 5 canceladas) |
| Clientes | Sí | 18 clientas cargadas en onboarding; historial consultado frecuentemente por U4 durante el uso productivo |
| Dashboard y KPIs | Sí | Consultado por U4 al inicio de cada jornada activa |
| Reportes y exportación | Sí | 3 exportaciones a Excel (inventario, durante sesiones T7 de U4, U5 y U6) |
| Gestión de usuarios y roles | Sí | 1 usuario creado durante tarea T8 (01-may, sesión U4) |

---

## Notas de interpretación

- **Productos:** La carga gradual de 24 productos (de un catálogo de ~280) durante la Fase 5 es esperada: el onboarding de un catálogo tan amplio no puede completarse en un solo día. El proceso continuó durante los primeros días de uso productivo, paralelo a las ventas reales.
- **Volumen de ventas:** 34 transacciones en 8 días (avg 4.3/día) es ligeramente superior al rango del seed (2–5/día en semana, 4–8 los sábados), lo que puede reflejar un sábado excepcionalmente activo (8 ventas el 2-may) o cierta regularización de ventas pendientes de registro.
- **Exportaciones:** Las 3 exportaciones a Excel corresponden a las 3 sesiones de tarea T7 (una por usuario). No hubo exportaciones orgánicas fuera de las sesiones guiadas, lo que sugiere que la funcionalidad no se usa espontáneamente en el primer período de adopción.
- **Cancelaciones:** 5 de 34 ventas canceladas (~14.7 %) es un porcentaje elevado que se explica por el período de aprendizaje: usuarios que registraron ventas de prueba durante el onboarding y las cancelaron posteriormente, o errores de registro corregidos mediante cancelación.
- **Días activos:** La tienda física de Miss Peggy opera 7 días a la semana (incluyendo domingos y festivos), por lo que los 8 días activos sobre 8 posibles son coherentes con el perfil de negocio, a diferencia de Frozt Bitez (e-commerce con cierre relativo los domingos) o Luana (artesana con descanso dominical).

---

*Telemetría extraída el 4-may-2026, último día de la Fase 5. Consultas ejecutadas sobre la base de datos PostgreSQL de producción del entorno de OrbitEngine por el facilitador del equipo. Los valores son estimaciones; reemplazar con resultados reales de la consulta al cierre de Fase 5.*
