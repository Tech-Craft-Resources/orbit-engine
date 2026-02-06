import { Link as RouterLink } from "@tanstack/react-router"

import { Appearance } from "@/components/Common/Appearance"
import { Button } from "@/components/ui/button"

const navLinks = [
  { href: "#features", label: "Features" },
  { href: "#benefits", label: "Benefits" },
  { href: "#stats", label: "Results" },
]

export function LandingNav() {
  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur-sm">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
        <RouterLink to="/" className="flex items-center gap-2">
          <img
            src="/assets/images/orbit-engine-logo.png"
            alt="OrbitEngine"
            className="h-8"
          />
          <span className="text-xl">
            <span className="font-bold">Orbit</span>Engine
          </span>
        </RouterLink>
        <nav className="hidden items-center gap-6 md:flex">
          {navLinks.map((link) => (
            <a
              key={link.href}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </a>
          ))}
        </nav>
        <div className="flex items-center gap-3">
          <Appearance />
          <Button variant="ghost" size="sm" asChild>
            <RouterLink to="/login">Log In</RouterLink>
          </Button>
          <Button size="sm" asChild>
            <RouterLink to="/signup">Get Started</RouterLink>
          </Button>
        </div>
      </div>
    </header>
  )
}
