#!/usr/bin/env bash
# ============================================================================
# build-latex.sh
# Convierte los archivos Markdown del informe final (docs/informe-final/) a
# fragmentos LaTeX dentro de la plantilla Orbit_Engine, listos para compilar
# con pdfLaTeX (Overleaf / MiKTeX).
#
# - Numeración AUTOMÁTICA: se eliminan los números manuales de los encabezados.
# - '#'  -> \chapter, '##' -> \section, '###' -> \subsection (top-level=chapter)
# - Imágenes movidas a Images/informe/ y rutas corregidas.
# ============================================================================
set -euo pipefail

SRC="../informe-final"                       # relativo a docs/pdf/
DST="Orbit_Engine"
TMP="_tmp"
mkdir -p "$TMP"
mkdir -p "$DST/MainMatter/Cap1" "$DST/MainMatter/Cap2" "$DST/MainMatter/Cap3" \
         "$DST/MainMatter/Cap4" "$DST/MainMatter/Cap5" "$DST/MainMatter/Cap6" \
         "$DST/MainMatter/Cap7" "$DST/BackMatter" "$DST/FrontMatter" \
         "$DST/Images/informe"

# --- Limpieza de encabezados: quita numeración manual -----------------------
# Quita "Capítulo N — ", "Anexo X — " y prefijos "N.N…", "X.N.N…".
strip_headings() {
  perl -CSD -Mutf8 -pe '
    if (/^\s*#/) {
      s/^(\#+\s+)(Cap[ií]tulo\s+\d+\s*[—–-]\s*)/$1/;
      s/^(\#+\s+)(Anexo\s+[A-Z]\s*[—–-]\s*)/$1/;
      s/^(\#+\s+)([A-Z]?\.?\d+(?:\.\d+)*\s+)/$1/;
    }
  ' "$1"
}

# --- Conversión de un .md a fragmento .tex ----------------------------------
convert() {
  local src="$1" out="$2"
  strip_headings "$SRC/$src" > "$TMP/clean.md"
  pandoc "$TMP/clean.md" -f markdown -t latex \
         --top-level-division=chapter --wrap=preserve \
         -o "$TMP/raw.tex"
  # Corrige rutas de imagen: images/Foo%20Bar.png -> informe/Foo Bar.png
  perl -CSD -pe '
    if (/\\includegraphics/) {
      s/\{images\//\{informe\//g;
      while (/%([0-9A-Fa-f]{2})/) { s/%([0-9A-Fa-f]{2})/chr(hex($1))/e; }
    }
  ' "$TMP/raw.tex" > "$DST/$out"
  echo "  $src -> $out"
}

echo "== Capítulos =="
convert "capitulo-1-introduccion.md"        "MainMatter/Cap1/C1-Introduccion.tex"
convert "capitulo-2-marco-referencia.md"    "MainMatter/Cap2/C2-MarcoReferencia.tex"
convert "capitulo-3-analisis-diseno.md"     "MainMatter/Cap3/C3-AnalisisDiseno.tex"
convert "capitulo-4-desarrollo.md"          "MainMatter/Cap4/C4-Desarrollo.tex"
convert "capitulo-5-resultados-tecnicos.md" "MainMatter/Cap5/C5-ResultadosTecnicos.tex"
convert "capitulo-6-resultados-usuarios.md" "MainMatter/Cap6/C6-ResultadosUsuarios.tex"
convert "capitulo-7-conclusiones.md"        "MainMatter/Cap7/C7-Conclusiones.tex"

echo "== Anexos =="
convert "anexo-a-manual-usuario.md"     "BackMatter/AnexoA-ManualUsuario.tex"
convert "anexo-b-manual-despliegue.md"  "BackMatter/AnexoB-Despliegue.tex"
convert "anexo-c-documentacion-tecnica.md" "BackMatter/AnexoC-DocTecnica.tex"

echo "== Imágenes =="
cp "$SRC/images/OrbitEngine_DER.drawio.png" "$DST/Images/informe/"
cp "$SRC/images/Vista de Componentes de Alto Nivel.png" "$DST/Images/informe/"
echo "  2 imágenes copiadas a Images/informe/"

echo "Listo."
