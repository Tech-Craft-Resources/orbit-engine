import { useQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense, useState } from "react"

import { SalesService } from "@/client"
import { DataTable, type FilterableColumn } from "@/components/Common/DataTable"
import AddSale from "@/components/Sales/AddSale"
import { saleColumns } from "@/components/Sales/columns"
import PendingSales from "@/components/Sales/PendingSales"
import { useDebounce } from "@/hooks/useDebounce"
import { requireUserWithRoles } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

const SALES_FILTER_COLUMNS: FilterableColumn[] = [
  {
    id: "status",
    label: "Estado",
    options: [
      { label: "Completada", value: "completed" },
      { label: "Cancelada", value: "cancelled" },
      { label: "Pendiente", value: "pending" },
    ],
  },
  {
    id: "payment_method",
    label: "Pago",
    options: [
      { label: "Efectivo", value: "cash" },
      { label: "Tarjeta", value: "card" },
      { label: "Transferencia", value: "transfer" },
      { label: "Otro", value: "other" },
    ],
  },
]

export const Route = createFileRoute("/dashboard/sales")({
  component: Sales,
  beforeLoad: async () => {
    await requireUserWithRoles(queryClient, ["admin", "seller"])
  },
  head: () => ({
    meta: [
      {
        title: "Ventas - OrbitEngine",
      },
    ],
  }),
})

function SalesTableContent({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  const debouncedSearch = useDebounce(search, 300)

  const { data: sales, isLoading } = useQuery({
    queryFn: () =>
      SalesService.readSales({
        skip: 0,
        limit: 100,
        search: debouncedSearch || undefined,
      }),
    queryKey: ["sales", debouncedSearch],
    placeholderData: (previousData) => previousData,
  })

  if (!sales && isLoading) return <PendingSales />

  return (
    <DataTable
      columns={saleColumns}
      data={sales?.data ?? []}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Buscar por numero de factura..."
      filterableColumns={SALES_FILTER_COLUMNS}
    />
  )
}

function Sales() {
  const [search, setSearch] = useState("")

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Ventas</h1>
          <p className="text-muted-foreground">
            Gestiona ventas y procesa transacciones
          </p>
        </div>
        <AddSale />
      </div>
      <Suspense fallback={<PendingSales />}>
        <SalesTableContent search={search} onSearchChange={setSearch} />
      </Suspense>
    </div>
  )
}
