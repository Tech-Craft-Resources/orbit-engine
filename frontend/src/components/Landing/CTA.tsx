import { Link as RouterLink } from "@tanstack/react-router"
import { ArrowRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

export function CTA() {
  const { ref, isVisible } = useScrollAnimation()

  return (
    <section className="py-20 md:py-24">
      <div className="mx-auto max-w-6xl px-6">
        <div
          ref={ref}
          className={cn(
            "relative overflow-hidden rounded-lg border border-border/80 bg-card px-6 py-10 shadow-sm md:px-10 md:py-12 scroll-hidden",
            isVisible && "animate-scale-in",
          )}
        >
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-20 -top-20 h-56 w-56 rounded-full bg-sky-400/10 blur-3xl"
          />
          <h2
            className={cn(
              "max-w-3xl text-balance text-3xl font-semibold tracking-tight sm:text-4xl scroll-hidden",
              isVisible && "animate-fade-in-up stagger-1",
            )}
          >
            Replace Fragmented Tools With One Reliable Control Surface
          </h2>
          <p
            className={cn(
              "mt-4 max-w-2xl text-pretty text-muted-foreground scroll-hidden",
              isVisible && "animate-fade-in stagger-2",
            )}
          >
            Launch with your current team, preserve process clarity, and give
            every role the same trusted source of operational truth.
          </p>
          <div
            className={cn(
              "mt-8 flex flex-col gap-3 sm:flex-row sm:items-center scroll-hidden",
              isVisible && "animate-fade-in-up stagger-3",
            )}
          >
            <Button size="lg" asChild className="touch-manipulation">
              <RouterLink to="/signup">
                Create Your Workspace
                <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
              </RouterLink>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <RouterLink to="/login">Open Existing Account</RouterLink>
            </Button>
          </div>
          <p className="mt-5 font-mono text-xs tabular-nums text-muted-foreground">
            setup_time=15m | migration_mode=incremental | support_window=24x5
          </p>
        </div>
      </div>
    </section>
  )
}
