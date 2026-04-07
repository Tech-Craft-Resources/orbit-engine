import { useQuery } from "@tanstack/react-query"
import { createFileRoute, Link } from "@tanstack/react-router"
import { ArrowLeft } from "lucide-react"

import { SalesService } from "@/client"
import SaleDetailContent from "@/components/Sales/SaleDetailContent"
import { Button } from "@/components/ui/button"
import { requireUserWithRoles } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

function getSaleQueryOptions(saleId: string) {
  return {
    queryKey: ["sale", saleId],
    queryFn: () => SalesService.readSale({ saleId }),
  }
}

export const Route = createFileRoute("/dashboard/sales/$saleId")({
  component: SaleDetailPage,
  beforeLoad: async () => {
    await requireUserWithRoles(queryClient, ["admin", "seller", "contador"])
  },
  loader: ({ params }) =>
    queryClient.ensureQueryData(getSaleQueryOptions(params.saleId)),
  head: () => ({
    meta: [
      {
        title: "Detalle de venta - OrbitEngine",
      },
    ],
  }),
})

function SaleDetailPage() {
  const { saleId } = Route.useParams()

  const { data: sale, isLoading } = useQuery(getSaleQueryOptions(saleId))

  if (!sale && isLoading) {
    return (
      <div className="flex flex-col gap-4">
        <Button variant="ghost" className="w-fit" asChild>
          <Link to="/dashboard/sales">
            <ArrowLeft />
            Volver a ventas
          </Link>
        </Button>
        <div className="rounded-lg border bg-card p-5">
          <p className="text-sm text-muted-foreground">
            Cargando detalle de venta...
          </p>
        </div>
      </div>
    )
  }

  if (!sale) {
    return (
      <div className="flex flex-col gap-4">
        <Button variant="ghost" className="w-fit" asChild>
          <Link to="/dashboard/sales">
            <ArrowLeft />
            Volver a ventas
          </Link>
        </Button>
        <div className="rounded-lg border bg-card p-5">
          <p className="text-sm text-muted-foreground">
            No se pudo cargar la venta solicitada.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <Button variant="ghost" className="w-fit" asChild>
          <Link to="/dashboard/sales">
            <ArrowLeft />
            Volver a ventas
          </Link>
        </Button>
        <div className="flex flex-col gap-1">
          <h1 className="text-2xl font-bold tracking-tight">
            Venta {sale.invoice_number}
          </h1>
          <p className="text-muted-foreground">
            Revisa los productos, montos y estado de la transaccion.
          </p>
        </div>
      </div>
      <SaleDetailContent sale={sale} isLoading={isLoading} />
    </div>
  )
}
