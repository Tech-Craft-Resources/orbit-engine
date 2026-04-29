# Cómo Terminar el Proyecto — Guía Paso a Paso

> **Estado actual:** El informe está ~85% completo. Los capítulos 1–4, referencias y los tres anexos están terminados. Lo que falta es obtener datos reales de validación para llenar el Capítulo 5 y cerrar el Capítulo 6.

---

## 1. Qué Falta (diagnóstico completo)

### 1.1 Partes críticas (sin esto no se puede entregar)

| Sección | Qué falta |
|---|---|
| `capitulo-5-resultados.md` | Datos reales del piloto: tiempos, encuestas SUS, métricas de inventario |
| `capitulo-6-conclusiones.md` | Sección 6.1 Objetivo 5 — depende del Capítulo 5 |
| `00-preliminares.md` | Nombre del jurado evaluador (aparece como `[Nombre del jurado]`) |

### 1.2 Partes menores (mejoran la calidad pero no son bloqueantes)

| Sección | Qué falta |
|---|---|
| `anexo-a-manual-usuario.md` | Capturas de pantalla reales de la app (dice "insertar captura") |
| `capitulo-3-analisis-diseno.md` | Insertar la imagen del DER desde `diseños/OrbitEngine_DER.drawio.png` |
| `capitulo-4-desarrollo.md` | Confirmar que la cobertura de pruebas es realmente 76% (`uv run bash scripts/test.sh`) |
| `anexo-a-manual-usuario.md` | FAQ #7 dice que exportar es "característica planificada" pero ya está implementado — corregir |

### 1.3 Lo que NO falta (está completo)

- Capítulos 1, 2, 3 y 4 — completos y bien redactados
- Referencias (19 fuentes APA 7)
- Anexo B (guía de despliegue) — completo
- Anexo C (documentación técnica) — completo
- `pandoc-guide.md` — ya existe y tiene el comando correcto

---

## 2. Cómo Medir las Métricas que Faltan (Capítulo 5)

El Capítulo 5 requiere datos de un piloto con empresas reales. Aquí está exactamente cómo medir cada cosa:

### 2.1 Tiempo de tareas (Sección 5.3 del informe)

Mide cuánto tarda un usuario en completar 5 tareas clave, **antes y después** de usar OrbitEngine.

**Las 5 tareas a cronometrar:**

| # | Tarea | Cómo medir "antes" | Cómo medir "después" (con OrbitEngine) |
|---|---|---|---|
| T1 | Registrar una venta | Tiempo con el método actual (cuaderno, Excel, WhatsApp) | Cronómetro desde que abren "Nueva Venta" hasta que hacen clic en "Guardar" |
| T2 | Consultar el stock de un producto | Tiempo buscando en inventario físico o Excel | Cronómetro desde módulo Inventario hasta encontrar el producto |
| T3 | Registrar un nuevo producto | Tiempo llenando su registro actual | Desde "Agregar Producto" hasta guardarlo |
| T4 | Ver el historial de un cliente | Tiempo buscando en registros manuales | Desde módulo Clientes hasta ver el historial |
| T5 | Generar reporte de ventas del día | Tiempo calculando manualmente | Desde Dashboard hasta ver los KPIs |

**Cómo hacerlo:**
1. Pide a 3–5 usuarios por empresa que realicen cada tarea mientras los observas.
2. Usa el cronómetro del celular. Anota el tiempo en segundos.
3. Repite el proceso con OrbitEngine (deja que el usuario se familiarice ~30 min antes).
4. El "antes" puedes estimarlo preguntando directamente: *"¿Cuánto tiempo te toma normalmente registrar una venta?"*

**Meta del informe:** Reducción ≥30% en tiempo promedio de las 5 tareas.

---

### 2.2 Encuesta SUS — System Usability Scale (Sección 5.4)

El SUS es un cuestionario estándar de 10 preguntas para medir usabilidad. **Puntaje ≥70 = usable, ≥85 = excelente.**

**Las 10 preguntas del SUS** (escala 1–5: "Muy en desacuerdo" a "Muy de acuerdo"):

1. Creo que me gustaría usar este sistema con frecuencia.
2. Encontré el sistema innecesariamente complejo.
3. Pensé que el sistema era fácil de usar.
4. Creo que necesitaría el apoyo de una persona técnica para poder usar este sistema.
5. Encontré que las distintas funciones del sistema estaban bien integradas.
6. Pensé que había demasiada inconsistencia en este sistema.
7. Imagino que la mayoría de personas aprendería a usar este sistema muy rápidamente.
8. Encontré el sistema muy complicado de usar.
9. Me sentí muy seguro/a usando el sistema.
10. Necesité aprender muchas cosas antes de poder usar el sistema.

**Cómo calcular el puntaje SUS:**
- Preguntas impares (1,3,5,7,9): puntaje = (respuesta del usuario − 1)
- Preguntas pares (2,4,6,8,10): puntaje = (5 − respuesta del usuario)
- Suma los 10 puntajes ajustados y multiplica por 2.5
- Resultado va de 0 a 100.

**Cómo aplicarlo:**
1. Crea un Google Form con las 10 preguntas en escala Likert 1–5.
2. Aplícalo a cada usuario **justo después** de que completen las 5 tareas.
3. Con 3 empresas piloto y ~3 usuarios por empresa, tendrás 9 respuestas — suficiente para el informe académico.

---

### 2.3 Precisión del inventario (Sección 5.3)

Mide qué tan bien el sistema refleja el inventario físico real.

**Cómo medirlo:**

1. Al inicio del piloto (antes de usar OrbitEngine), registra los productos en el sistema.
2. Al final del período de piloto (2–3 semanas), haz un **conteo físico** de productos seleccionados (elige 20–30 ítems representativos).
3. Compara el conteo físico con lo que muestra OrbitEngine.
4. Calcula: `Precisión = (productos correctos / total contados) × 100%`

**Fórmula para el informe:**
```
Discrepancias encontradas / Total de ítems contados = Tasa de error
```

**Meta del informe:** Precisión ≥95% (es decir, tasa de error ≤5%).

**Benchmark "antes":** Pregunta a los propietarios cuántas veces al mes encuentran diferencias entre su registro y el inventario físico. Eso es tu baseline.

---

### 2.4 Disponibilidad del sistema (Sección 5.2)

Esto es fácil de obtener si el sistema está desplegado en AWS.

**Cómo medirlo:**
- Ve a **AWS CloudWatch** → Alarmas → revisa los logs de downtime durante el período del piloto.
- Alternativamente, usa un monitor gratuito como **UptimeRobot** (uptimerobot.com): crea un monitor de tipo HTTP que haga ping a tu API cada 5 minutos y te reporta uptime %.

**Meta del informe:** ≥95% de disponibilidad durante el período de piloto.

---

### 2.5 Tiempos de respuesta de la API (Sección 5.2)

**Cómo medirlo sin herramientas costosas:**

```bash
# Desde la terminal, mide el tiempo de respuesta de endpoints clave
curl -o /dev/null -s -w "%{time_total}\n" https://tu-dominio.com/api/v1/products/
curl -o /dev/null -s -w "%{time_total}\n" https://tu-dominio.com/api/v1/sales/
curl -o /dev/null -s -w "%{time_total}\n" https://tu-dominio.com/api/v1/dashboard/stats
```

Registra 10 mediciones por endpoint y calcula el promedio. **Meta: <500ms promedio.**

Alternativamente, usa **Postman** (gratuito): crea una colección con los endpoints principales, ejecútala y Postman muestra el tiempo de respuesta de cada llamada.

---

### 2.6 Cobertura de pruebas (Sección 5.2)

Ejecuta esto y anota el número exacto para el informe:

```bash
cd backend
uv run bash scripts/test.sh
```

El reporte final muestra `TOTAL ... X%`. Ese es el número que va en el Capítulo 5 (actualmente dice 76% como estimación).

---

## 3. Cómo Compilar el PDF con Pandoc (profesional)

El archivo `informe-final/pandoc-guide.md` ya tiene la guía completa, pero aquí está el resumen ejecutable:

### 3.1 Prerrequisitos

```powershell
# Verificar instalaciones
pandoc --version    # Necesitas 3.0+
xelatex --version   # Si falla, instala MiKTeX desde https://miktex.org/download
```

### 3.2 Crear el archivo de metadatos

Crea `Docs/informe-final/metadata.yaml` con este contenido mínimo (ajusta nombres):

```yaml
---
title: >-
  OrbitEngine: Plataforma SaaS para la Gestión Integral de Procesos
  Internos en Pequeñas y Medianas Empresas utilizando Inteligencia Artificial
subtitle: "Proyecto de Grado"
author:
  - "Rodríguez Forero, Nicolás"
  - "Velasco González, Daniel"
  - "Rincón Suárez, Fabián"
date: "Abril 2026"
lang: es-CO
documentclass: report
fontsize: 12pt
linestretch: 1.5
geometry:
  - top=3cm
  - bottom=2.5cm
  - left=3cm
  - right=2.5cm
mainfont: "Times New Roman"
sansfont: "Arial"
monofont: "Consolas"
toc: true
toc-depth: 3
numbersections: true
colorlinks: true
linkcolor: "black"
urlcolor: "blue"
header-includes:
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  - \fancyhead[R]{\small OrbitEngine}
  - \fancyfoot[C]{\thepage}
  - \renewcommand{\headrulewidth}{0.4pt}
  - \renewcommand{\contentsname}{Tabla de Contenidos}
  - \renewcommand{\figurename}{Figura}
  - \renewcommand{\tablename}{Tabla}
  - \usepackage{longtable}
  - \usepackage{booktabs}
  - \usepackage{fvextra}
  - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}
---
```

### 3.3 Comando de compilación

Ejecuta desde la carpeta `Docs/`:

```powershell
cd Docs
pandoc `
  informe-final/metadata.yaml `
  informe-final/00-preliminares.md `
  informe-final/capitulo-1-introduccion.md `
  informe-final/capitulo-2-marco-referencia.md `
  informe-final/capitulo-3-analisis-diseno.md `
  informe-final/capitulo-4-desarrollo.md `
  informe-final/capitulo-5-resultados.md `
  informe-final/capitulo-6-conclusiones.md `
  informe-final/referencias.md `
  informe-final/anexo-a-manual-usuario.md `
  informe-final/anexo-b-manual-despliegue.md `
  informe-final/anexo-c-documentacion-tecnica.md `
  -o informe-orbitengine.pdf `
  --pdf-engine=xelatex `
  --from="markdown+smart+pipe_tables" `
  --highlight-style=tango `
  --number-sections `
  --toc `
  --toc-depth=3 `
  --top-level-division=chapter
```

### 3.4 Nota sobre los Anexos

Agrega `\appendix` al inicio de `anexo-a-manual-usuario.md` para que los anexos se numeren A, B, C en lugar de seguir la numeración de capítulos:

```markdown
\appendix

# Anexo A — Manual de Usuario
```

### 3.5 Si hay errores comunes

| Error | Solución |
|---|---|
| `File 'fvextra.sty' not found` | Abre MiKTeX Console e instala el paquete `fvextra` |
| `File 'booktabs.sty' not found` | Instala `booktabs` desde MiKTeX Console |
| Tildes/ñ aparecen como `?` | Verifica que `mainfont` esté en `metadata.yaml` y usas `--pdf-engine=xelatex` |
| Tablas se salen del margen | Agrega `\small` antes de la tabla en el `.md` |
| Código se desborda | Ya está cubierto por `fvextra` con `breaklines` |

---

## 4. Paso a Paso para Terminar el Proyecto

### Semana 1 — Piloto y recolección de datos

- [ ] **Día 1:** Confirma las empresas piloto (1–3 empresas es suficiente para un proyecto de grado). Miss Peggy ya tiene datos de seed, úsala si participó.
- [ ] **Día 1–2:** Aplica las 5 tareas cronometradas con cada empresa (ver Sección 2.1).
- [ ] **Día 2–3:** Aplica el cuestionario SUS a cada usuario (ver Sección 2.2).
- [ ] **Día 3:** Haz el conteo físico de inventario y compáralo con el sistema (ver Sección 2.3).
- [ ] **Día 3–4:** Mide tiempos de respuesta de la API con `curl` (ver Sección 2.5).
- [ ] **Día 4:** Ejecuta `uv run bash scripts/test.sh` y anota la cobertura real (ver Sección 2.6).
- [ ] **Día 4–5:** Toma capturas de pantalla de los módulos principales para el Anexo A.

### Semana 2 — Redacción y cierre

- [ ] **Día 6–7:** Rellena `capitulo-5-resultados.md` con todos los datos recolectados.
- [ ] **Día 7:** Completa la sección 6.1 Objetivo 5 en `capitulo-6-conclusiones.md`.
- [ ] **Día 8:** Consigue el nombre del jurado evaluador y actualiza `00-preliminares.md`.
- [ ] **Día 8:** Corrige el FAQ #7 del Anexo A (exportar ya está implementado, no es "planificado").
- [ ] **Día 8:** Inserta la imagen `diseños/OrbitEngine_DER.drawio.png` en `capitulo-3-analisis-diseno.md`.
- [ ] **Día 9:** Crea `informe-final/metadata.yaml` con los datos correctos.
- [ ] **Día 9:** Agrega `\appendix` al inicio de `anexo-a-manual-usuario.md`.
- [ ] **Día 9:** Compila el PDF con el comando de la Sección 3.3 y revisa el resultado.
- [ ] **Día 10:** Revisión final de ortografía, consistencia y formato del PDF.
- [ ] **Día 10:** Entrega.

### Atajos si el tiempo es limitado

Si no puedes hacer el piloto formal con usuarios reales, el mínimo aceptable para un proyecto académico es:
- **1 empresa piloto, 2 usuarios, medir las 5 tareas cronometradas**
- **Aplicar el SUS a esos mismos 2 usuarios**
- Esto da datos reales aunque sean de muestra pequeña — reconócelo en las limitaciones (ya está contemplado en 6.3)

---

## 5. Estructura Final del PDF Esperada

```
Portada (00-preliminares.md)
Acta de aprobación
Resumen / Abstract
Tabla de Contenidos (auto-generada por Pandoc)

Capítulo 1: Introducción
Capítulo 2: Marco de Referencia
Capítulo 3: Análisis y Diseño
Capítulo 4: Desarrollo e Implementación
Capítulo 5: Resultados y Validación   ← LLENAR CON DATOS REALES
Capítulo 6: Conclusiones              ← COMPLETAR OBJETIVO 5

Referencias

Anexo A: Manual de Usuario            ← AGREGAR CAPTURAS
Anexo B: Manual de Despliegue
Anexo C: Documentación Técnica
```

**Longitud estimada del PDF:** 90–110 páginas con capturas y diagramas.

---

## 6. Resumen en 3 Líneas

1. **Lo único que realmente falta** es el Capítulo 5 con datos reales de validación. Todo lo demás está escrito.
2. **Para obtener esos datos** necesitas: cronometrar 5 tareas con usuarios reales + aplicar el cuestionario SUS de 10 preguntas + medir precisión de inventario.
3. **Para generar el PDF** crea `metadata.yaml` y ejecuta el comando `pandoc` de la Sección 3.3 desde la carpeta `Docs/`.
