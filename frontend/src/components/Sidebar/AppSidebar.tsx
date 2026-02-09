import { Home, Package, ShoppingCart, Users, UsersRound } from "lucide-react"

import { SidebarAppearance } from "@/components/Common/Appearance"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth, { type RoleName } from "@/hooks/useAuth"
import { Separator } from "../ui/separator"
import { type Item, Main } from "./Main"
import { User } from "./User"

type NavItem = Item & {
  /** If set, only users with one of these roles will see this item */
  roles?: RoleName[]
}

const navItems: NavItem[] = [
  { icon: Home, title: "Dashboard", path: "/dashboard" },
  {
    icon: Package,
    title: "Inventory",
    path: "/dashboard/inventory",
    roles: ["admin", "seller"],
  },
  {
    icon: ShoppingCart,
    title: "Sales",
    path: "/dashboard/sales",
    roles: ["admin", "seller"],
  },
  {
    icon: UsersRound,
    title: "Customers",
    path: "/dashboard/customers",
    roles: ["admin", "seller"],
  },
  { icon: Users, title: "Admin", path: "/dashboard/admin", roles: ["admin"] },
]

export function AppSidebar() {
  const { user: currentUser, organization, hasRole } = useAuth()

  const items = navItems.filter((item) => !item.roles || hasRole(item.roles))

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 items-center group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <img
          src="/assets/images/orbit-engine-logo-dark.png"
          alt="OrbitEngine"
          className="size-10"
        />
        {organization && (
          <span className="text-md font-semibold truncate group-data-[collapsible=icon]:hidden">
            {organization.name}
          </span>
        )}
        <Separator className="group-data-[collapsible=icon]:hidden" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
