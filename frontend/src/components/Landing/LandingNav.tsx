import { Link as RouterLink } from "@tanstack/react-router"
import { ChevronsUpDown, LogOut, Settings } from "lucide-react"

import { Appearance } from "@/components/Common/Appearance"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import { getInitials } from "@/utils"

const navLinks = [
  { href: "#features", label: "Modules" },
  { href: "#benefits", label: "Approach" },
  { href: "#stats", label: "Proof" },
]

export function LandingNav() {
  const { user, logout } = useAuth()

  const fullName = user ? `${user.first_name} ${user.last_name}` : ""

  return (
    <header className="fixed inset-x-0 top-0 z-50 w-full border-b border-border/70 bg-background/95 backdrop-blur-md supports-[backdrop-filter]:bg-background/75">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <RouterLink to="/" className="group flex items-center gap-3">
          <img
            src="/assets/images/orbit-engine-logo.png"
            alt="OrbitEngine"
            width={28}
            height={28}
            className="h-7 dark:hidden"
          />
          <img
            src="/assets/images/orbit-engine-logo-dark.png"
            alt="OrbitEngine"
            width={28}
            height={28}
            className="hidden h-7 dark:block"
          />
          <span className="text-base tracking-tight">
            <span className="font-semibold">Orbit</span>Engine
          </span>
          <span
            aria-hidden="true"
            className="hidden h-2 w-2 rounded-full bg-primary md:block"
          />
        </RouterLink>
        <nav className="hidden items-center gap-1 md:flex" aria-label="Primary">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60"
            >
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-2">
          <Appearance />
          {user ? (
            <>
              <Button size="sm" asChild className="touch-manipulation">
                <RouterLink to="/dashboard">Go to Dashboard</RouterLink>
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-2"
                    aria-label="Open User Menu"
                  >
                    <Avatar className="size-6">
                      <AvatarFallback className="bg-muted text-muted-foreground border border-sidebar text-xs">
                        {getInitials(fullName || "User")}
                      </AvatarFallback>
                    </Avatar>
                    <ChevronsUpDown className="size-4" aria-hidden="true" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" className="w-56">
                  <DropdownMenuLabel>
                    <div className="flex flex-col space-y-1">
                      <p className="text-sm font-medium">{fullName}</p>
                      <p className="text-xs text-muted-foreground">
                        {user.email}
                      </p>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem asChild>
                    <RouterLink to="/dashboard/settings">
                      <Settings aria-hidden="true" />
                      User Settings
                    </RouterLink>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={logout}>
                    <LogOut aria-hidden="true" />
                    Log Out
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <>
              <Button variant="ghost" size="sm" asChild>
                <RouterLink to="/login">Log In</RouterLink>
              </Button>
              <Button size="sm" asChild className="touch-manipulation">
                <RouterLink to="/signup">Get Started</RouterLink>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
