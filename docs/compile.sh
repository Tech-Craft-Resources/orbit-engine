#!/usr/bin/env bash
set -e

DIR="$(dirname "$0")/informe-final"
OUTPUT_MAIN="informe-final.pdf"
OUTPUT_ANEXOS="anexos.pdf"
OUT_DIR="$(dirname "$0")"

echo "Compilando documento principal..."

pandoc \
  "$DIR/metadata.yaml" \
  "$DIR/capitulo-1-introduccion.md" \
  "$DIR/capitulo-2-marco-referencia.md" \
  "$DIR/capitulo-3-analisis-diseno.md" \
  "$DIR/capitulo-4-desarrollo.md" \
  "$DIR/capitulo-5-resultados-tecnicos.md" \
  "$DIR/capitulo-6-resultados-usuarios.md" \
  "$DIR/capitulo-7-conclusiones.md" \
  "$DIR/referencias.md" \
  -o "$OUT_DIR/$OUTPUT_MAIN" \
  --pdf-engine=xelatex \
  --from="markdown+smart+pipe_tables" \
  --syntax-highlighting=tango \
  --resource-path="$DIR" \
  --top-level-division=chapter

# echo "Compilando anexos..."

# pandoc \
#   "$DIR/metadata.yaml" \
#   "$DIR/anexo-a-manual-usuario.md" \
#   "$DIR/anexo-b-manual-despliegue.md" \
#   "$DIR/anexo-c-documentacion-tecnica.md" \
#   -o "$OUT_DIR/$OUTPUT_ANEXOS" \
#   --pdf-engine=xelatex \
#   --from="markdown+smart+pipe_tables" \
#   --syntax-highlighting=tango \
#   --resource-path="$DIR" \
#   --top-level-division=chapter

echo "PDFs generados:"
echo " - docs/$OUTPUT_MAIN"
# echo " - docs/$OUTPUT_ANEXOS"

if command -v open &>/dev/null; then
  open "$OUT_DIR/$OUTPUT_MAIN"
  # open "$OUT_DIR/$OUTPUT_ANEXOS"
fi
