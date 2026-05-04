$ErrorActionPreference = "Stop"

$dir = "$PSScriptRoot\informe-final"

# =========================
# 1. Documento principal
# =========================
$outputMain = "informe-final.pdf"

Write-Host "Compilando documento principal..." -ForegroundColor Cyan

pandoc `
  "$dir\metadata.yaml" `
  "$dir\capitulo-1-introduccion.md" `
  "$dir\capitulo-2-marco-referencia.md" `
  "$dir\capitulo-3-analisis-diseno.md" `
  "$dir\capitulo-4-desarrollo.md" `
  "$dir\capitulo-5-resultados-tecnicos.md" `
  "$dir\capitulo-6-resultados-usuarios.md" `
  "$dir\capitulo-7-conclusiones.md" `
  "$dir\referencias.md" `
  -o "$PSScriptRoot\$outputMain" `
  --pdf-engine=xelatex `
  --from="markdown+smart+pipe_tables" `
  --syntax-highlighting=tango `
  --resource-path="$dir" `
  --top-level-division=chapter

# =========================
# 2. Anexos
# =========================
$outputAnexos = "anexos.pdf"

Write-Host "Compilando anexos..." -ForegroundColor Cyan

pandoc `
  "$dir\metadata.yaml" `
  "$dir\anexo-a-manual-usuario.md" `
  "$dir\anexo-b-manual-despliegue.md" `
  "$dir\anexo-c-documentacion-tecnica.md" `
  -o "$PSScriptRoot\$outputAnexos" `
  --pdf-engine=xelatex `
  --from="markdown+smart+pipe_tables" `
  --syntax-highlighting=tango `
  --resource-path="$dir" `
  --top-level-division=chapter

# =========================
# Resultado
# =========================
if ($LASTEXITCODE -eq 0) {
    Write-Host "PDFs generados:" -ForegroundColor Green
    Write-Host " - docs\$outputMain"
    Write-Host " - docs\$outputAnexos"

    Start-Process "$PSScriptRoot\$outputMain"
    Start-Process "$PSScriptRoot\$outputAnexos"
} else {
    Write-Host "Error al compilar. Revisa los mensajes de xelatex." -ForegroundColor Red
    exit 1
}