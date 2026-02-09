import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { Suspense } from "react"

import { SalesService, UsersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddSale from "@/components/Sales/AddSale"
import { saleColumns } from "@/components/Sales/columns"
import PendingSales from "@/components/Sales/PendingSales"
import { hasRole } from "@/hooks/useAuth"

function getSalesQueryOptions() {
  return {
    queryFn: () => SalesService.readSales({ skip: 0, limit: 100 }),
    queryKey: ["sales"],
  }
}

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

function SalesTableContent() {
  const { data: sales } = useSuspenseQuery(getSalesQueryOptions())
  return <DataTable columns={saleColumns} data={sales.data} />
}

function SalesTable() {
  return (
    <Suspense fallback={<PendingSales />}>
      <SalesTableContent />
    </Suspense>
  )
}

function Sales() {
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
      <SalesTable />
    </div>
  )
}
