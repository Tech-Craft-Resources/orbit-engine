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
        title: "OrbitEngine - Smart Business Management for SMEs",
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
    <div className="relative min-h-svh overflow-x-hidden bg-background text-foreground">
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-md focus:border focus:bg-background focus:px-3 focus:py-2 focus:text-sm"
      >
        Skip to Main Content
      </a>
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-x-0 top-0 -z-10 h-[520px] bg-[radial-gradient(circle_at_15%_15%,rgba(14,165,233,0.14),transparent_38%),radial-gradient(circle_at_85%_0%,rgba(16,185,129,0.13),transparent_34%)]"
      />
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
