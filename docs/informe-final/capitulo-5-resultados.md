# Capítulo 5 — Resultados y Validación

> **Nota para el autor**: Este capítulo es el que requiere datos reales de tu proyecto. La estructura y los ejemplos presentados aquí son plantillas que debes completar con los valores y hallazgos obtenidos durante las pruebas con las empresas piloto. Las secciones marcadas con `[COMPLETAR]` deben ser llenadas con evidencia real.

---

## 5.1 Descripción del Experimento de Validación

Para validar las hipótesis del proyecto, se diseñó un plan de pruebas con empresas reales del sector comercio. El objetivo fue medir el impacto de la adopción de OrbitEngine en la eficiencia operativa de las pymes participantes.

### 5.1.1 Empresas Piloto

Se seleccionaron **[N] empresas** del sector de comercio minorista/mayorista para participar en el período de prueba de **[X] semanas** (del [fecha inicio] al [fecha fin]).

| Empresa | Sector | Empleados | Datos históricos disponibles | Sistema previo |
|---------|--------|-----------|------------------------------|----------------|
| Empresa A - [Nombre ficticio/real] | [sector] | [N] | [X] meses | Hojas de cálculo / Ninguno |
| Empresa B - [Nombre ficticio/real] | [sector] | [N] | [X] meses | [Sistema previo] |

### 5.1.2 Protocolo de Pruebas

El proceso de validación con cada empresa siguió el siguiente protocolo:

1. **Medición de línea base (pre-implementación)**: durante la semana previa a la adopción de OrbitEngine, se midió el tiempo que los empleados dedicaban a las tareas administrativas clave (registro de ventas, control de inventario, generación de reportes) mediante observación directa y registro de tiempos.

2. **Onboarding**: sesión de capacitación de 2 horas con los usuarios de cada empresa, carga de datos históricos (productos, clientes, stock inicial) y configuración del sistema.

3. **Período de uso activo**: las empresas usaron OrbitEngine como su sistema principal durante **[X] semanas**, con soporte del equipo disponible.

4. **Medición post-implementación**: al finalizar el período, se repitió la medición de tiempos para las mismas tareas y se aplicaron encuestas de satisfacción.

5. **Entrevistas de cierre**: sesiones de feedback cualitativo con cada usuario.

---

## 5.2 Resultados de Rendimiento del Sistema

### 5.2.1 Disponibilidad

Durante el período de producción (del [fecha] al [fecha]), el sistema registró:

| Métrica | Resultado | Requisito (RNF-02) |
|---------|-----------|---------------------|
| Uptime total | **[X]%** | ≥ 95% |
| Incidentes de interrupción | **[N]** | — |
| Tiempo de recuperación promedio (MTTR) | **[X] minutos** | — |

**[COMPLETAR: describir si hubo incidentes, sus causas y cómo se resolvieron.]**

### 5.2.2 Rendimiento de la API

Se realizaron mediciones de tiempos de respuesta durante el período de uso real con las empresas piloto:

| Endpoint | Método | Tiempo promedio | P95 | Requisito (RNF-01) |
|----------|--------|-----------------|-----|---------------------|
| `/api/v1/login/access-token` | POST | [X] ms | [X] ms | ≤ 500ms |
| `/api/v1/products/` | GET | [X] ms | [X] ms | ≤ 500ms |
| `/api/v1/sales/` (registro) | POST | [X] ms | [X] ms | ≤ 500ms |
| `/api/v1/reports/dashboard` | GET | [X] ms | [X] ms | ≤ 500ms |

**[COMPLETAR: insertar valores reales y comentar si se cumplieron los requisitos.]**

### 5.2.3 Cobertura de Pruebas Automatizadas

La suite de pruebas automatizadas al cierre del desarrollo alcanzó una cobertura del **74%** en el backend, superando el umbral del 60% establecido como requisito no funcional (RNF-08).

```
Módulo               Sentencias   Cubiertas   Cobertura
-----------------------------------------------------------
app/api/             [N]          [N]         [X]%
app/crud.py          [N]          [N]         [X]%
app/core/security    [N]          [N]         [X]%
-----------------------------------------------------------
TOTAL                [N]          [N]         74%
```

**[COMPLETAR: reemplazar con los valores reales del reporte de coverage de pytest.]**

---

## 5.3 Resultados de Eficiencia Operativa

### 5.3.1 Reducción de Tiempo en Tareas Administrativas

Se midió el tiempo promedio que los usuarios de las empresas piloto dedicaban a tres tareas clave antes y después de implementar OrbitEngine:

**Tarea 1: Registro de una venta con 5 productos**

| Empresa | Tiempo antes | Tiempo después | Reducción |
|---------|-------------|----------------|-----------|
| Empresa A | [X] min | [X] min | **[X]%** |
| Empresa B | [X] min | [X] min | **[X]%** |
| **Promedio** | **[X] min** | **[X] min** | **[X]%** |

**Tarea 2: Verificación del estado de inventario (stock actual de todos los productos)**

| Empresa | Tiempo antes | Tiempo después | Reducción |
|---------|-------------|----------------|-----------|
| Empresa A | [X] min | [X] min | **[X]%** |
| Empresa B | [X] min | [X] min | **[X]%** |
| **Promedio** | **[X] min** | **[X] min** | **[X]%** |

**Tarea 3: Generación de reporte de ventas de la semana**

| Empresa | Tiempo antes | Tiempo después | Reducción |
|---------|-------------|----------------|-----------|
| Empresa A | [X] min | [X] min | **[X]%** |
| Empresa B | [X] min | [X] min | **[X]%** |
| **Promedio** | **[X] min** | **[X] min** | **[X]%** |

**[COMPLETAR: insertar los tiempos medidos. La hipótesis del proyecto establece una reducción ≥ 30%.]**

### 5.3.2 Reducción de Errores de Inventario

Se realizó una auditoría de inventario (conteo físico vs. sistema) antes y después de la implementación:

| Empresa | Discrepancias antes / 100 productos | Discrepancias después / 100 productos | Reducción |
|---------|--------------------------------------|---------------------------------------|-----------|
| Empresa A | [X] | [X] | **[X]%** |
| Empresa B | [X] | [X] | **[X]%** |

**[COMPLETAR. La hipótesis establece una reducción ≥ 40%.]**

---

## 5.4 Resultados de Usabilidad

### 5.4.1 Pruebas de Completitud de Tareas

Se solicitó a los usuarios que completaran una lista de tareas sin asistencia del equipo de desarrollo, observando si lograban completarlas exitosamente:

| Tarea | Usuarios que completaron exitosamente | Tasa |
|-------|--------------------------------------|------|
| Registrar una venta con descuento | [N] / [Total] | **[X]%** |
| Agregar un nuevo producto al inventario | [N] / [Total] | **[X]%** |
| Consultar el perfil y el historial de un cliente | [N] / [Total] | **[X]%** |
| Generar y exportar un reporte de ventas | [N] / [Total] | **[X]%** |
| **Promedio** | | **[X]%** |

**[COMPLETAR. El requisito RNF-06 establece que los flujos principales deben completarse en ≤ 5 pasos. El objetivo de usabilidad es ≥ 85% de tasa de completitud.]**

### 5.4.2 Encuesta de Satisfacción (System Usability Scale — SUS)

Se aplicó la escala SUS estándar (Brooke, 1996), que consiste en 10 ítems evaluados en una escala Likert de 1 a 5. El puntaje SUS se calcula en una escala de 0 a 100, donde:
- < 50: inaceptable
- 50–70: marginal
- 70–85: bueno
- > 85: excelente

| Empresa | Usuarios encuestados | Puntaje SUS promedio | Calificación |
|---------|----------------------|----------------------|--------------|
| Empresa A | [N] | **[X]** | [Categoría] |
| Empresa B | [N] | **[X]** | [Categoría] |
| **Global** | **[N]** | **[X]** | **[Categoría]** |

**[COMPLETAR con los puntajes reales. El objetivo del proyecto establece una satisfacción ≥ 4.0/5.0 (equivalente a ~70+ en SUS).]**

### 5.4.3 Retroalimentación Cualitativa

Las entrevistas de cierre con los usuarios revelaron los siguientes temas recurrentes:

**Aspectos valorados positivamente:**
- [COMPLETAR con citas o resúmenes de feedback positivo real]
- Ejemplo: "Ya no tengo que buscar en tres hojas de cálculo para saber cuánto vendí la semana pasada."
- Ejemplo: "Las alertas de stock son lo que más nos ayuda; antes se nos acababan los productos sin darnos cuenta."

**Aspectos con oportunidad de mejora:**
- [COMPLETAR con feedback crítico real]
- Ejemplo: "El proceso de registro de ventas es rápido, pero buscar un producto con nombre similar a otro puede confundirse."
**Solicitudes de funcionalidades futuras:**
- [COMPLETAR con solicitudes reales de los usuarios]

---

## 5.5 Validación de Hipótesis

El proyecto planteó como hipótesis principal:

> *"Una plataforma SaaS modular mejora significativamente la eficiencia operativa de las pymes en términos de reducción de tiempo en tareas administrativas, reducción de errores de inventario y calidad de la toma de decisiones."*

La siguiente tabla resume el estado de validación de cada hipótesis específica:

| Hipótesis | Indicador | Objetivo | Resultado | Estado |
|-----------|-----------|----------|-----------|--------|
| H1: Reducción de tiempo en tareas administrativas | % reducción tiempo promedio | ≥ 30% | **[X]%** | [✅ Validada / ⚠️ Parcialmente / ❌ No validada] |
| H2: Reducción de errores de inventario | % reducción de discrepancias | ≥ 40% | **[X]%** | [✅ / ⚠️ / ❌] |
| H3: Satisfacción de usuario aceptable | Puntaje SUS | ≥ 70/100 | **[X]** | [✅ / ⚠️ / ❌] |
| H4: Tasa de completitud de tareas alta | % tareas completadas sin ayuda | ≥ 85% | **[X]%** | [✅ / ⚠️ / ❌] |

**[COMPLETAR con los resultados reales y el análisis correspondiente.]**

---

## 5.6 Discusión

### 5.6.1 Interpretación de los Resultados

**[COMPLETAR con el análisis de tus resultados reales. La siguiente es una guía de los puntos a discutir:]**

**Sobre la eficiencia operativa**: discutir si la reducción de tiempo observada es estadísticamente significativa o si el número de usuarios es demasiado pequeño para hacer una afirmación robusta. Contextualizarla con los rangos reportados en la literatura (20%–35% según Rodriguez-Abitia et al., 2020).

**Sobre la usabilidad**: interpretar el puntaje SUS en el contexto del perfil de usuario (bajo nivel de alfabetización digital). Un puntaje "bueno" (70-85) con este perfil es un resultado valioso. Identificar qué aspectos de la UI fueron más difíciles de usar y qué lecciones se extraen.

### 5.6.2 Limitaciones del Experimento

1. **Tamaño de muestra reducido**: la validación se realizó con [N] empresas piloto, lo que limita la generalización de los resultados. Un estudio con mayor número de empresas sería necesario para conclusiones más robustas.
2. **Período de prueba corto**: el efecto de aprendizaje del usuario puede haber reducido la diferencia observable entre el "antes" y el "después". Un período de adaptación más largo podría mostrar mayores mejoras.
3. **Sesgo de selección**: las empresas participantes pueden ser más receptivas a la tecnología que el promedio, lo que favorece resultados positivos no representativos del universo de pymes.
4. **Sesgo de experiencia previa**: las empresas con alguna experiencia previa en herramientas digitales (Excel avanzado, software de facturación) mostraron curvas de adopción más rápidas, lo que puede haber influido positivamente en las métricas de usabilidad para ese subgrupo.
