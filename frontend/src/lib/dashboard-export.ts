import { OpenAPI } from "@/client"
import { getAccessToken } from "@/lib/auth-session"

type Dataset = "inventory" | "sales" | "customers"

type ExportPayload = {
  dataset: Dataset
  timezone: string
  search?: string
  status?: string
  payment_method?: string
  is_active?: boolean
  category_id?: string
  date_from?: string
  date_to?: string
}

function readFilename(disposition: string | null, fallback: string): string {
  if (!disposition) return fallback
  const match = disposition.match(/filename="?([^"]+)"?/i)
  return match?.[1] ?? fallback
}

export async function downloadDashboardExport(payload: ExportPayload) {
  const token = getAccessToken()
  if (!token) {
    throw new Error("No hay sesión activa")
  }

  const response = await fetch(
    `${OpenAPI.BASE}/api/v1/dashboard/export-excel`,
    {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    },
  )

  if (!response.ok) {
    throw new Error("No se pudo exportar el archivo")
  }

  const blob = await response.blob()
  const defaultName = `${payload.dataset}-export.xlsx`
  const filename = readFilename(
    response.headers.get("content-disposition"),
    defaultName,
  )

  const url = window.URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = filename
  document.body.append(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}
