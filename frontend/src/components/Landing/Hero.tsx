import { Link as RouterLink } from "@tanstack/react-router"
import { ArrowRight, Bot, ChevronRight } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

export function Hero() {
  const { ref, isVisible } = useScrollAnimation({ threshold: 0.1 })

  return (
    <section className="relative overflow-hidden">
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-background to-background" />
      <div ref={ref} className="mx-auto max-w-6xl px-6 py-24 md:py-32 lg:py-40">
        <div
          className={cn(
            "mx-auto max-w-3xl text-center scroll-hidden",
            isVisible && "animate-fade-in-up",
          )}
        >
          <Badge variant="secondary" className="mb-6">
            <Bot className="mr-1 h-3 w-3" />
            AI-Powered Business Management
          </Badge>
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Run your business smarter,{" "}
            <span className="text-primary">not harder</span>
          </h1>
          <p
            className={cn(
              "mt-6 text-lg text-muted-foreground sm:text-xl scroll-hidden",
              isVisible && "animate-fade-in stagger-2",
            )}
          >
            OrbitEngine is the all-in-one platform that helps small and
            medium-sized businesses digitalize operations, automate routine
            tasks, and make data-driven decisions with AI.
          </p>
          <div
            className={cn(
              "mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center scroll-hidden",
              isVisible && "animate-fade-in-up stagger-3",
            )}
          >
            <Button size="lg" asChild>
              <RouterLink to="/signup">
                Start Free
                <ArrowRight className="ml-2 h-4 w-4" />
              </RouterLink>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <a href="#features">
                See Features
                <ChevronRight className="ml-1 h-4 w-4" />
              </a>
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
