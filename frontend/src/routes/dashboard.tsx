import { createFileRoute, Outlet } from "@tanstack/react-router"

import { Footer } from "@/components/Common/Footer"
import AppSidebar from "@/components/Sidebar/AppSidebar"
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar"
import { requireAuthenticatedUser } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

export const Route = createFileRoute("/dashboard")({
  component: Layout,
  beforeLoad: async () => {
    await requireAuthenticatedUser(queryClient)
  },
})

function Layout() {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <main className="flex-1 p-6 md:p-8 dashboard-bg">
          <div className="mx-auto max-w-7xl">
            <Outlet />
          </div>
        </main>
        <Footer />
      </SidebarInset>
    </SidebarProvider>
  )
}

export default Layout
