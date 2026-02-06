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
    <div className="min-h-svh bg-background text-foreground">
      <LandingNav />
      <Hero />
      <Stats />
      <Features />
      <Benefits />
      <CTA />
      <LandingFooter />
    </div>
  )
}
