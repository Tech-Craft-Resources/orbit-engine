# Guía de Configuración de Pandoc para el Informe de Grado

OrbitEngine — Instrucciones para generar el PDF final desde Markdown

---

## 1. Diagnóstico del Comando Actual

Tu comando actual tiene los siguientes problemas que producen un PDF de aspecto poco profesional:

```bash
# ❌ Comando actual con problemas anotados
pandoc informe.md -o Informe.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=0.5in \    # ← margen 1.27 cm: demasiado estrecho para tesis
  -V documentclass=extarticle \ # ← no numera capítulos automáticamente
  -V fontsize=8pt               # ← ilegible en impresión
```

Los problemas concretos:
- **`margin=0.5in`** produce márgenes de ~1.3 cm. Una tesis requiere al menos 2.5–3 cm para encuadernación.
- **`extarticle`** no diferencia entre `#` (capítulo) y `##` (sección) visualmente en la misma medida que `report`.
- **`fontsize=8pt`** es inviable para lectura: el estándar académico es 11pt o 12pt con interlineado 1.5.

---

## 2. Solución: YAML Frontmatter + Comando Mejorado

La mejor práctica con Pandoc es definir **toda la configuración tipográfica en un bloque YAML** al inicio del documento (o en un archivo separado), y usar el comando de Pandoc solo para lógica de compilación.

### 2.1 Crear el archivo de metadatos: `docs/informe-final/metadata.yaml`

Crea este archivo **separado** (no dentro de ningún capítulo). Pandoc lo leerá con la opción `--metadata-file`:

```yaml
---
# ─── METADATOS DEL DOCUMENTO ────────────────────────────────────────────────
title: >-
  OrbitEngine: Plataforma SaaS para la Gestión Integral de Procesos
  Internos en Pequeñas y Medianas Empresas utilizando Inteligencia Artificial
subtitle: "Proyecto de Grado"
author:
  - "Apellido, Nombre — Código estudiantil"
  - "Apellido, Nombre — Código estudiantil"
  - "Apellido, Nombre — Código estudiantil"
date: "Abril 2026"
institution: "Universidad [Nombre]"
department: "Facultad de [Nombre] — Programa de [Nombre]"
advisor: "Nombre del Asesor"
lang: es-CO

# ─── TIPOGRAFÍA Y DISEÑO ────────────────────────────────────────────────────
documentclass: report          # 'report' soporta \chapter{} correctamente
fontsize: 12pt
linestretch: 1.5               # Interlineado 1.5

# Márgenes: estándar para tesis (Colombia: izq/sup 3cm, der/inf 2.5cm)
geometry:
  - top=3cm
  - bottom=2.5cm
  - left=3cm
  - right=2.5cm
  - bindingoffset=0.5cm       # margen extra para encuadernación

# Fuentes (xelatex las carga desde el sistema)
# Opción A — Fuentes del sistema que probablemente ya tienes:
mainfont: "Times New Roman"
sansfont: "Arial"
monofont: "Consolas"
# Opción B — Si instalas TeX Gyre (recomendado, ver sección 6):
# mainfont: "TeX Gyre Termes"
# sansfont: "TeX Gyre Heros"
# monofont: "TeX Gyre Cursor"

# ─── TABLA DE CONTENIDOS ────────────────────────────────────────────────────
toc: true                      # Genera tabla de contenidos automática
toc-depth: 3                   # Niveles: capítulo, sección, subsección
lof: false                     # Lista de figuras (cambiar a true si tienes figuras)
lot: false                     # Lista de tablas (cambiar a true si tienes tablas)
numbersections: true           # Numera todos los encabezados automáticamente

# ─── ENLACES Y COLORES ──────────────────────────────────────────────────────
colorlinks: true
linkcolor: "black"             # Links internos en negro (aspecto formal)
urlcolor: "blue"               # URLs externas en azul
citecolor: "black"

# ─── ENCABEZADOS Y PIE DE PÁGINA ────────────────────────────────────────────
header-includes:
  # Paquete para encabezados y pie de página personalizados
  - \usepackage{fancyhdr}
  - \pagestyle{fancy}
  - \fancyhf{}
  # Encabezado: nombre corto del proyecto a la derecha
  - \fancyhead[R]{\small OrbitEngine}
  # Número de página centrado en el pie
  - \fancyfoot[C]{\thepage}
  # Línea bajo el encabezado
  - \renewcommand{\headrulewidth}{0.4pt}

  # Tabla de contenidos en español
  - \renewcommand{\contentsname}{Tabla de Contenidos}
  - \renewcommand{\listfigurename}{Lista de Figuras}
  - \renewcommand{\listtablename}{Lista de Tablas}
  - \renewcommand{\figurename}{Figura}
  - \renewcommand{\tablename}{Tabla}

  # Bloques de código con fondo gris claro
  - \usepackage{fvextra}
  - \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,commandchars=\\\{\}}

  # Tablas longas (para tablas que ocupan más de una página)
  - \usepackage{longtable}
  - \usepackage{booktabs}

  # Soporte para caracteres especiales en bloques de código
  - \usepackage{pmboxdraw}
---
```

---

## 3. Comandos de Compilación

### 3.1 Compilar el informe completo (todos los capítulos)

Ejecuta desde el directorio `docs/informe-final/`:

```bash
pandoc \
  metadata.yaml \
  capitulo-1-introduccion.md \
  capitulo-2-marco-referencia.md \
  capitulo-3-analisis-diseno.md \
  capitulo-4-desarrollo.md \
  capitulo-5-resultados.md \
  capitulo-6-conclusiones.md \
  referencias.md \
  anexo-a-manual-usuario.md \
  anexo-b-manual-despliegue.md \
  anexo-c-documentacion-tecnica.md \
  -o ../informe-final.pdf \
  --pdf-engine=xelatex \
  --from=markdown+smart+pipe_tables \
  --highlight-style=tango \
  --number-sections \
  --toc \
  --toc-depth=3 \
  --top-level-division=chapter
```

**Explicación de cada flag:**
| Flag | Propósito |
|------|-----------|
| `metadata.yaml` | Primer argumento: carga la configuración tipográfica |
| `--pdf-engine=xelatex` | Motor LaTeX que soporta fuentes del sistema y UTF-8 nativo |
| `--from=markdown+smart+pipe_tables` | `smart` convierte `--` en em-dash; `pipe_tables` para tablas `\|col\|col\|` |
| `--highlight-style=tango` | Estilo de coloreado de código (alternativas: `pygments`, `kate`, `monochrome`) |
| `--number-sections` | Numera encabezados: `1.`, `1.1`, `1.1.1` |
| `--toc` | Genera tabla de contenidos |
| `--toc-depth=3` | Incluye hasta subsecciones en el TOC |
| `--top-level-division=chapter` | Los `#` de nivel 1 se convierten en `\chapter{}` (clase `report`) |

### 3.2 Script de compilación automático (recomendado)

Crea el archivo `docs/compile.ps1` (PowerShell para Windows):

```powershell
# compile.ps1 — Compila el informe de grado con Pandoc
# Uso: cd docs && .\compile.ps1

$ErrorActionPreference = "Stop"

$output = "informe-final.pdf"
$inputDir = "informe-final"

Write-Host "Compilando $output..." -ForegroundColor Cyan

pandoc `
  "$inputDir\metadata.yaml" `
  "$inputDir\capitulo-1-introduccion.md" `
  "$inputDir\capitulo-2-marco-referencia.md" `
  "$inputDir\capitulo-3-analisis-diseno.md" `
  "$inputDir\capitulo-4-desarrollo.md" `
  "$inputDir\capitulo-5-resultados.md" `
  "$inputDir\capitulo-6-conclusiones.md" `
  "$inputDir\referencias.md" `
  "$inputDir\anexo-a-manual-usuario.md" `
  "$inputDir\anexo-b-manual-despliegue.md" `
  "$inputDir\anexo-c-documentacion-tecnica.md" `
  -o $output `
  --pdf-engine=xelatex `
  --from="markdown+smart+pipe_tables" `
  --highlight-style=tango `
  --number-sections `
  --toc `
  --toc-depth=3 `
  --top-level-division=chapter

if ($LASTEXITCODE -eq 0) {
  Write-Host "✓ PDF generado: $output" -ForegroundColor Green
  # Abre el PDF automáticamente
  Start-Process $output
} else {
  Write-Host "✗ Error al compilar. Revisa los mensajes de xelatex." -ForegroundColor Red
}
```

Ejecución:
```powershell
cd docs
.\compile.ps1
```

---

## 4. Separadores de Capítulos en los Archivos .md

Para que Pandoc sepa dónde empieza cada capítulo (especialmente los Anexos, que no forman parte de la numeración principal), agrega este bloque al inicio de cada archivo de anexo:

```markdown
\appendix

# Anexo A — Manual de Usuario
```

El `\appendix` le indica a LaTeX que los capítulos siguientes se numeran con letras (A, B, C...) en lugar de números.

**Estructura recomendada para el bloque final del informe:**
```markdown
# Referencias  ← al inicio de referencias.md (sin \appendix, es parte del cuerpo)

\appendix     ← al inicio de anexo-a-manual-usuario.md

# Anexo A — Manual de Usuario
```

---

## 5. Ajustes para Problemas Comunes

### 5.1 Caracteres especiales en español (tildes, ñ)

Si aparecen caracteres como `?` o cuadros negros en lugar de `á`, `é`, `ñ`:

- **Causa**: xelatex no está cargando las fuentes con soporte UTF-8.
- **Solución**: asegúrate de que `mainfont` esté configurado en `metadata.yaml`. La combinación `--pdf-engine=xelatex` + `mainfont` definido resuelve este problema definitivamente.
- Si el problema persiste, agrega a `header-includes`:
  ```yaml
  - \usepackage[spanish]{babel}
  ```

### 5.2 Tablas que se desbordan del margen

Las tablas con muchas columnas o celdas largas frecuentemente se salen del margen en LaTeX.

**Opción A — Reducir el tamaño de fuente de la tabla** añadiendo HTML en el Markdown:
```markdown
\small
| Col1 | Col2 | Col3 | Col4 |
|------|------|------|------|
| ... | ... | ... | ... |
\normalsize
```

**Opción B — Forzar saltos de línea en celdas largas** con `longtable` (ya incluido en `header-includes`). Antepon `\tiny` a las tablas más densas.

**Opción C — Cambiar orientación de página para tablas grandes** (landscape):
```markdown
\begin{landscape}

| Columna muy larga 1 | Columna muy larga 2 | ... |
|---------------------|---------------------|-----|
| ...                 | ...                 | ... |

\end{landscape}
```
Requiere agregar `- \usepackage{pdflscape}` en `header-includes`.

### 5.3 Bloques de código que se desbordan

Si el código en los bloques ` ``` ` se sale del margen:

Agrega en `header-includes`:
```yaml
- \usepackage{fvextra}
- \DefineVerbatimEnvironment{Highlighting}{Verbatim}{breaklines,breakanywhere,commandchars=\\\{\}}
```

`breaklines` fuerza el quiebre de líneas largas en bloques de código. Si no es suficiente, usa `breakanywhere=true`.

### 5.4 Tabla de contenidos no muestra los Anexos

Si los anexos no aparecen en el TOC:

Verifica que estés usando `\appendix` seguido de `# Título del Anexo` (no `## Título`). El nivel `#` con `--top-level-division=chapter` genera `\chapter{}`, que sí aparece en el TOC.

### 5.5 El PDF no genera portada formal

Pandoc no genera automáticamente una página de portada académica con formato institucional. Tienes dos opciones:

**Opción A** (más simple): crear la portada en Word/Canva y combinar los PDFs al final con:
```powershell
# Combinar portada.pdf + informe-final.pdf
# Requiere tener instalado pdftk o similar
pdftk portada.pdf informe-final.pdf cat output informe-completo.pdf
```

**Opción B** (LaTeX puro): agrega en `header-includes`:
```yaml
- |
  \AtBeginDocument{
    \begin{titlepage}
      \centering
      \vspace*{2cm}
      {\Large\bfseries Universidad Nombre\par}
      \vspace{0.5cm}
      {\large Facultad de Ingeniería\par}
      \vspace{3cm}
      {\Huge\bfseries OrbitEngine\par}
      \vspace{1cm}
      {\large Plataforma SaaS para la Gestión Integral de Pymes\par}
      \vspace{2cm}
      {\large Nombre Apellido 1\par Nombre Apellido 2\par Nombre Apellido 3\par}
      \vspace{1cm}
      {\large Asesor: Nombre del Asesor\par}
      \vfill
      {\large Abril 2026\par}
    \end{titlepage}
  }
```

### 5.6 Error `! LaTeX Error: File 'fvextra.sty' not found`

Significa que el paquete LaTeX no está instalado. Instálalo con:

```powershell
# En Windows con MiKTeX (gestor de paquetes)
miktex-console   # Abre la interfaz y busca "fvextra"

# O desde consola con tlmgr (TeX Live)
tlmgr install fvextra
tlmgr install booktabs
tlmgr install longtable
```

---

## 6. Instalación de Fuentes para XeLaTeX en Windows

XeLaTeX puede usar cualquier fuente instalada en el sistema Windows. Las opciones más comunes:

### Fuentes ya instaladas en Windows (sin instalar nada adicional)
```yaml
mainfont: "Times New Roman"    # Clásico académico
sansfont: "Arial"
monofont: "Consolas"
```

### Fuentes LaTeX de alta calidad (recomendadas)
Si tienes TeX Live o MiKTeX instalado, estas fuentes ya están disponibles:
```yaml
mainfont: "TeX Gyre Termes"    # Equivalente a Times New Roman, pero mejor
sansfont: "TeX Gyre Heros"     # Equivalente a Helvetica
monofont: "TeX Gyre Cursor"    # Equivalente a Courier
```

### Palatino (elegante, común en tesis)
```yaml
mainfont: "Palatino Linotype"  # Disponible en Windows
```

---

## 7. Verificar la Instalación de Pandoc y XeLaTeX

Antes de compilar, verifica que tienes todo instalado:

```powershell
# Verificar Pandoc
pandoc --version

# Verificar XeLaTeX (parte de MiKTeX o TeX Live)
xelatex --version

# Si xelatex no está disponible, instala MiKTeX desde:
# https://miktex.org/download
# O TeX Live desde:
# https://tug.org/texlive/
```

**Versiones mínimas recomendadas:**
- Pandoc: 3.0+
- XeLaTeX: incluido en MiKTeX 23+ o TeX Live 2023+

---

## 8. Producir un Documento Word (.docx) Alternativo

Si necesitas entregar también en formato Word (para revisiones del asesor):

```bash
pandoc \
  metadata.yaml \
  capitulo-1-introduccion.md \
  ... \
  -o informe-final.docx \
  --from=markdown+smart+pipe_tables \
  --number-sections \
  --toc \
  --top-level-division=chapter \
  --reference-doc=plantilla-universidad.docx
```

Con `--reference-doc`, Pandoc aplica los estilos del documento Word de referencia (plantilla) al contenido generado. Si no tienes una plantilla, omite ese flag y ajusta estilos manualmente en Word.

Para crear una plantilla base:
```bash
pandoc --print-default-data-file reference.docx > plantilla-base.docx
```
Luego abre `plantilla-base.docx`, modifica los estilos (Heading 1, Heading 2, Normal, Code, etc.) y úsala como `--reference-doc`.

---

## 9. Resumen Rápido (TL;DR)

1. Crea `docs/informe-final/metadata.yaml` con el contenido de la sección 2.1.
2. Crea `docs/compile.ps1` con el script de la sección 3.2.
3. Ejecuta: `cd docs && .\compile.ps1`
4. Si hay errores, consulta la sección 5 según el tipo de error.

**El comando final reemplaza por completo tu comando anterior.** No uses más `-V geometry:margin=0.5in` ni `-V fontsize=8pt` inline — toda esa configuración ya está en `metadata.yaml`.
