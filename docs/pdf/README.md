# Informe en formato Universidad Sergio Arboleda (LaTeX)

Convierte el informe en Markdown (`docs/informe-final/`) a la plantilla institucional
LaTeX `Orbit_Engine/` (clase `MIA-USA.cls`), lista para compilar en Overleaf.

## Estructura

- `Orbit_Engine/main.tex` — informe (Cap. 1–7 + Referencias)
- `Orbit_Engine/anexos.tex` — Anexos A, B, C
- `Orbit_Engine/pandoc-preamble.tex` — paquetes/macros que necesita la salida de Pandoc
- `build-latex.sh` — regenera los `.tex` desde el Markdown

## Regenerar tras editar el Markdown

Requiere [Pandoc](https://pandoc.org). Desde esta carpeta (`docs/pdf/`):

```bash
bash build-latex.sh
```

Esto reescribe los capítulos/anexos en `Orbit_Engine/`. Hace tres cosas por archivo:
1. **Quita la numeración manual** de los títulos (la plantilla numera sola).
2. **Pandoc** convierte Markdown → LaTeX (`#`→`\chapter`, tablas→`booktabs`, código→resaltado).
3. **Corrige las rutas de imagen** a `Images/informe/`.

> El front matter (Resumen/Abstract) y las Referencias APA se ajustaron a mano una vez en
> `Orbit_Engine/FrontMatter/` y `Orbit_Engine/BackMatter/`; no los pisa el script.

## Compilar a PDF

**Overleaf:** sube la carpeta `Orbit_Engine/`, motor **pdfLaTeX**, compila `main.tex` y `anexos.tex`.

**Local (MiKTeX/TeX Live):** dos pasadas para el índice:

```bash
cd Orbit_Engine
pdflatex main.tex && pdflatex main.tex
pdflatex anexos.tex && pdflatex anexos.tex
```
