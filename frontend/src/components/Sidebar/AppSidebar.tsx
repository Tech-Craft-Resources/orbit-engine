import {
  Home,
  Package,
  PanelLeft,
  Settings,
  ShoppingCart,
  Users,
  UsersRound,
} from "lucide-react"

import { SidebarAppearance } from "@/components/Common/Appearance"
import { useTheme } from "@/components/theme-provider"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  useSidebar,
} from "@/components/ui/sidebar"
import useAuth, { type RoleName } from "@/hooks/useAuth"
import { type Item, Main } from "./Main"
import { User } from "./User"

type NavItem = Item & {
  /** If set, only users with one of these roles will see this item */
  roles?: RoleName[]
}

const navItems: NavItem[] = [
  { icon: Home, title: "Panel", path: "/dashboard" },
  {
    icon: Package,
    title: "Inventario",
    path: "/dashboard/inventory",
    roles: ["admin", "seller"],
  },
  {
    icon: ShoppingCart,
    title: "Ventas",
    path: "/dashboard/sales",
    roles: ["admin", "seller"],
  },
  {
    icon: UsersRound,
    title: "Clientes",
    path: "/dashboard/customers",
    roles: ["admin", "seller"],
  },
  {
    icon: Users,
    title: "Administración",
    path: "/dashboard/admin",
    roles: ["admin"],
  },
  {
    icon: Settings,
    title: "Configuración",
    path: "/dashboard/settings",
    roles: ["admin"],
  },
]

export function AppSidebar() {
  const { user: currentUser, organization, hasRole } = useAuth()
  const { resolvedTheme } = useTheme()
  const { toggleSidebar } = useSidebar()

  const items = navItems.filter((item) => !item.roles || hasRole(item.roles))

  const logoSrc =
    resolvedTheme === "dark"
      ? "/assets/images/orbit-engine-logo-dark.png"
      : "/assets/images/orbit-engine-logo.png"

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-3 py-3 group-data-[collapsible=icon]:px-2">
        {/* Expanded: logo + org name + collapse button */}
        <div className="flex items-center gap-2.5 group-data-[collapsible=icon]:hidden">
          <img src={logoSrc} alt="OrbitEngine" className="size-8 shrink-0" />
          <span className="text-sm font-bold tracking-tight truncate flex-1">
            {organization?.name ?? "OrbitEngine"}
          </span>
          <button
            type="button"
            onClick={toggleSidebar}
            className="flex size-7 shrink-0 items-center justify-center rounded-md text-sidebar-foreground/50 hover:bg-sidebar-accent hover:text-sidebar-accent-foreground transition-colors duration-150"
            aria-label="Colapsar barra lateral"
          >
            <PanelLeft className="size-4" />
          </button>
        </div>

        {/* Collapsed: logo as expand trigger */}
        <button
          type="button"
          onClick={toggleSidebar}
          className="hidden group-data-[collapsible=icon]:flex items-center justify-center rounded-md p-0.5 hover:bg-sidebar-accent transition-colors duration-150"
          aria-label="Abrir barra lateral"
        >
          <img
            src={logoSrc}
            alt="OrbitEngine"
            className="size-8 shrink-0 aspect-square object-contain"
          />
        </button>

        <div className="mt-2.5 h-px bg-linear-to-r from-transparent via-sidebar-border to-transparent group-data-[collapsible=icon]:hidden" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <div className="h-px bg-linear-to-r from-transparent via-sidebar-border to-transparent mb-1" />
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
