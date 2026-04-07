import { Link as RouterLink } from "@tanstack/react-router"
import { ChevronsUpDown, LogOut, Settings } from "lucide-react"
import { useEffect, useState } from "react"

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
import { cn } from "@/lib/utils"
import { getInitials } from "@/utils"
import { landingNavLinks } from "./landingNavLinks"

export function LandingNav() {
  const { user, logout } = useAuth()
  const [activeHref, setActiveHref] = useState<`#${string}` | "">("")

  const fullName = user ? `${user.first_name} ${user.last_name}` : ""

  useEffect(() => {
    const trackedSections = landingNavLinks
      .map((link) => document.getElementById(link.sectionId))
      .filter((section): section is HTMLElement => section !== null)

    if (!trackedSections.length) {
      return
    }

    const sectionEntries = new Map<string, IntersectionObserverEntry>()

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          sectionEntries.set(entry.target.id, entry)
        }

        const visibleEntries = Array.from(sectionEntries.values())
          .filter(
            (entry): entry is IntersectionObserverEntry => entry.isIntersecting,
          )
          .sort(
            (a, b) =>
              Math.abs(a.boundingClientRect.top) -
              Math.abs(b.boundingClientRect.top),
          )

        const activeSectionId = visibleEntries[0]?.target.id
        if (!activeSectionId) {
          setActiveHref("")
          return
        }

        const activeLink = landingNavLinks.find(
          (link) => link.sectionId === activeSectionId,
        )

        if (activeLink) {
          setActiveHref(activeLink.href)
          return
        }

        setActiveHref("")
      },
      {
        root: null,
        rootMargin: "-80px 0px -55% 0px",
        threshold: [0.2, 0.35, 0.5, 0.65],
      },
    )

    trackedSections.forEach((section) => {
      observer.observe(section)
    })

    return () => {
      observer.disconnect()
    }
  }, [])

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
        <nav
          className="hidden items-center gap-1 md:flex"
          aria-label="Principal"
        >
          {landingNavLinks.map((link) => {
            const isActive = activeHref === link.href

            return (
              <a
                key={link.href}
                href={link.href}
                aria-current={isActive ? "location" : undefined}
                className={cn(
                  "rounded-md px-3 py-2 text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60",
                  isActive
                    ? "font-semibold text-primary"
                    : "text-muted-foreground hover:text-foreground",
                )}
              >
                {link.label}
              </a>
            )
          })}
        </nav>
        <div className="flex items-center gap-2">
          <Appearance />
          {user ? (
            <>
              <Button size="sm" asChild className="touch-manipulation">
                <RouterLink to="/dashboard">Ingresar</RouterLink>
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="gap-2"
                    aria-label="Abrir menú de usuario"
                  >
                    <Avatar className="size-6">
                      <AvatarFallback className="bg-muted text-muted-foreground border border-sidebar text-xs">
                        {getInitials(fullName || "Usuario")}
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
                      Configuración
                    </RouterLink>
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={logout}>
                    <LogOut aria-hidden="true" />
                    Cerrar sesión
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <>
              <Button variant="ghost" size="sm" asChild>
                <RouterLink to="/login">Iniciar sesión</RouterLink>
              </Button>
              <Button size="sm" asChild className="touch-manipulation">
                <RouterLink to="/signup">Comenzar</RouterLink>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
