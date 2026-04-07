import { createFileRoute } from "@tanstack/react-router"
import { useEffect } from "react"

import { Benefits } from "@/components/Landing/Benefits"
import { CTA } from "@/components/Landing/CTA"
import { Features } from "@/components/Landing/Features"
import { Hero } from "@/components/Landing/Hero"
import { LandingFooter } from "@/components/Landing/LandingFooter"
import { LandingNav } from "@/components/Landing/LandingNav"
import { Stats } from "@/components/Landing/Stats"

export const Route = createFileRoute("/")({
  component: LandingPage,
  head: () => ({
    meta: [
      {
        title:
          "OrbitEngine | Digitaliza y automatiza procesos internos de tu pyme",
      },
      {
        name: "description",
        content:
          "Centraliza inventario, ventas y control operativo en un solo lugar. OrbitEngine te ayuda a tomar decisiones con reportes claros y crecer con procesos ordenados. Prueba gratis por 1 mes con acceso completo al plan Pro.",
      },
    ],
  }),
})

function LandingPage() {
  // Handle smooth scroll to hash on page load
  useEffect(() => {
    const hash = window.location.hash
    if (hash) {
      setTimeout(() => {
        const element = document.querySelector(hash)
        if (element) {
          element.scrollIntoView({ behavior: "smooth", block: "start" })
        }
      }, 100)
    }
  }, [])

  return (
    <div className="relative min-h-svh overflow-x-hidden bg-background text-foreground landing-bg">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-100 focus:rounded-md focus:border focus:bg-background focus:px-3 focus:py-2 focus:text-sm"
      >
        Ir al contenido principal
      </a>
      <LandingNav />
      <main id="main-content" className="pt-16">
        <Hero />
        <Stats />
        <Features />
        <Benefits />
        <CTA />
      </main>
      <LandingFooter />
    </div>
  )
}
