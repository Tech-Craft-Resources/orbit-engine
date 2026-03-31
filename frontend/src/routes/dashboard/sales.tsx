import { useQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { Suspense, useState } from "react"

import { SalesService, UsersService } from "@/client"
import { DataTable, type FilterableColumn } from "@/components/Common/DataTable"
import AddSale from "@/components/Sales/AddSale"
import { saleColumns } from "@/components/Sales/columns"
import PendingSales from "@/components/Sales/PendingSales"
import { hasRole } from "@/hooks/useAuth"
import { useDebounce } from "@/hooks/useDebounce"

const SALES_FILTER_COLUMNS: FilterableColumn[] = [
  {
    id: "status",
    label: "Status",
    options: [
      { label: "Completed", value: "completed" },
      { label: "Cancelled", value: "cancelled" },
      { label: "Pending", value: "pending" },
    ],
  },
  {
    id: "payment_method",
    label: "Payment",
    options: [
      { label: "Cash", value: "cash" },
      { label: "Card", value: "card" },
      { label: "Transfer", value: "transfer" },
      { label: "Other", value: "other" },
    ],
  },
]

export const Route = createFileRoute("/dashboard/sales")({
  component: Sales,
  beforeLoad: async () => {
    const user = await UsersService.readUserMe()
    if (!hasRole(user, ["admin", "seller"])) {
      throw redirect({
        to: "/",
      })
    }
  },
  head: () => ({
    meta: [
      {
        title: "Sales - OrbitEngine",
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
  })

  if (isLoading) return <PendingSales />

  return (
    <DataTable
      columns={saleColumns}
      data={sales?.data ?? []}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Search by invoice number…"
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
          <h1 className="text-2xl font-bold tracking-tight">Sales</h1>
          <p className="text-muted-foreground">
            Manage sales and process transactions
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
