import { useMutation } from "@tanstack/react-query"
import { Download } from "lucide-react"

import { Button } from "@/components/ui/button"
import useCustomToast from "@/hooks/useCustomToast"
import { downloadDashboardExport } from "@/lib/dashboard-export"
import { handleError } from "@/utils"

type Props = {
  search?: string
}

export default function ExportInventoryButton({ search }: Props) {
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const mutation = useMutation({
    mutationFn: async () => {
      const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC"
      await downloadDashboardExport({
        dataset: "inventory",
        timezone,
        search: search || undefined,
      })
    },
    onSuccess: () => showSuccessToast("Inventario exportado"),
    onError: handleError.bind(showErrorToast),
  })

  return (
    <Button
      variant="outline"
      className="gap-2"
      onClick={() => mutation.mutate()}
      disabled={mutation.isPending}
    >
      <Download className="size-4" />
      {mutation.isPending ? "Exportando..." : "Exportar Excel"}
    </Button>
  )
}
