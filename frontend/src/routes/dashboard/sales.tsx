import { createFileRoute, Outlet } from "@tanstack/react-router"

import { requireUserWithRoles } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

export const Route = createFileRoute("/dashboard/sales")({
  component: SalesLayout,
  beforeLoad: async () => {
    await requireUserWithRoles(queryClient, ["admin", "seller", "contador"])
  },
})

function SalesLayout() {
  return <Outlet />
}
