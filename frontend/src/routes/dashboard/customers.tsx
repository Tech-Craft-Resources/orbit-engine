import { useQuery } from "@tanstack/react-query"
import { createFileRoute, redirect } from "@tanstack/react-router"
import { Suspense, useState } from "react"

import { CustomersService, UsersService } from "@/client"
import { DataTable, type FilterableColumn } from "@/components/Common/DataTable"
import AddCustomer from "@/components/Customers/AddCustomer"
import { customerColumns } from "@/components/Customers/columns"
import PendingCustomers from "@/components/Customers/PendingCustomers"
import { hasRole } from "@/hooks/useAuth"
import { useDebounce } from "@/hooks/useDebounce"

const CUSTOMERS_FILTER_COLUMNS: FilterableColumn[] = [
  {
    id: "is_active",
    label: "Status",
    options: [
      { label: "Active", value: "true" },
      { label: "Inactive", value: "false" },
    ],
  },
]

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

function CustomersTableContent({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  const debouncedSearch = useDebounce(search, 300)

  const { data: customers, isLoading } = useQuery({
    queryFn: () =>
      CustomersService.readCustomers({
        skip: 0,
        limit: 100,
        search: debouncedSearch || undefined,
      }),
    queryKey: ["customers", debouncedSearch],
  })

  if (isLoading) return <PendingCustomers />

  return (
    <DataTable
      columns={customerColumns}
      data={customers?.data ?? []}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Search by name, email, document…"
      filterableColumns={CUSTOMERS_FILTER_COLUMNS}
    />
  )
}

function Customers() {
  const [search, setSearch] = useState("")

  return (
    <div className="flex flex-col gap-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Customers</h1>
          <p className="text-muted-foreground">Manage your customer database</p>
        </div>
        <AddCustomer />
      </div>
      <Suspense fallback={<PendingCustomers />}>
        <CustomersTableContent search={search} onSearchChange={setSearch} />
      </Suspense>
    </div>
  )
}
