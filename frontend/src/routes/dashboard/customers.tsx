import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { Suspense } from "react"

import { CustomersService, UsersService } from "@/client"
import { DataTable } from "@/components/Common/DataTable"
import AddCustomer from "@/components/Customers/AddCustomer"
import { customerColumns } from "@/components/Customers/columns"
import PendingCustomers from "@/components/Customers/PendingCustomers"
import { hasRole } from "@/hooks/useAuth"

function getCustomersQueryOptions() {
  return {
    queryFn: () => CustomersService.readCustomers({ skip: 0, limit: 100 }),
    queryKey: ["customers"],
  }
}

export const Route = createFileRoute("/dashboard/customers")({
  component: Customers,
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
        title: "Customers - OrbitEngine",
      },
    ],
  }),
})

function CustomersTableContent() {
  const { data: customers } = useSuspenseQuery(getCustomersQueryOptions())
  return <DataTable columns={customerColumns} data={customers.data} />
}

function CustomersTable() {
  return (
    <Suspense fallback={<PendingCustomers />}>
      <CustomersTableContent />
    </Suspense>
  )
}

function Customers() {
  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Customers</h1>
          <p className="text-muted-foreground">Manage your customer database</p>
        </div>
        <AddCustomer />
      </div>
      <CustomersTable />
    </div>
  )
}
