# compile.ps1 — Compila el informe de grado con Pandoc
# Ejecutar desde la raiz del proyecto: .\docs\compile.ps1
# O desde la carpeta docs:             .\compile.ps1

$ErrorActionPreference = "Stop"

$output  = "informe-final.pdf"
$dir     = "$PSScriptRoot\informe-final"

Write-Host "Compilando $output..." -ForegroundColor Cyan

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
  "$dir\anexo-a-manual-usuario.md" `
  "$dir\anexo-b-manual-despliegue.md" `
  "$dir\anexo-c-documentacion-tecnica.md" `
  -o "$PSScriptRoot\$output" `
  --pdf-engine=xelatex `
  --from="markdown+smart+pipe_tables" `
  --syntax-highlighting=tango `
  --resource-path="$dir" `
  --top-level-division=chapter

if ($LASTEXITCODE -eq 0) {
    Write-Host "PDF generado: docs\$output" -ForegroundColor Green
    Start-Process "$PSScriptRoot\$output"
} else {
    Write-Host "Error al compilar. Revisa los mensajes de xelatex." -ForegroundColor Red
    exit 1
}
