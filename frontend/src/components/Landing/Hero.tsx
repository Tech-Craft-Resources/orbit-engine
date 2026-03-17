import { Link as RouterLink } from "@tanstack/react-router"
import { ArrowRight, ChevronRight } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

export function Hero() {
  const { ref, isVisible } = useScrollAnimation({ threshold: 0.1 })

  return (
    <section className="relative overflow-hidden border-b border-border/70 py-20 md:py-24 lg:py-28">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 -z-10 bg-[linear-gradient(180deg,transparent_0%,rgba(15,23,42,0.02)_100%)] dark:bg-[linear-gradient(180deg,transparent_0%,rgba(148,163,184,0.07)_100%)]"
      />
      <div
        ref={ref}
        className="mx-auto grid max-w-6xl gap-10 px-6 lg:grid-cols-[minmax(0,1fr)_420px] lg:items-center"
      >
        <div
          className={cn(
            "max-w-3xl scroll-hidden",
            isVisible && "animate-fade-in-up",
          )}
        >
          <Badge
            variant="secondary"
            className="mb-5 rounded-md border border-border/70"
          >
            Operations Intelligence for SME Teams
          </Badge>
          <h1 className="text-balance text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
            Build a Clear Operating System for Your Business
          </h1>
          <p
            className={cn(
              "mt-6 max-w-2xl text-pretty text-base leading-7 text-muted-foreground sm:text-lg scroll-hidden",
              isVisible && "animate-fade-in stagger-2",
            )}
          >
            OrbitEngine centralizes inventory, sales, customers, and forecasting
            into one deliberate workspace. Your team works faster, with fewer
            handoffs, better visibility, and AI-backed next actions.
          </p>
          <div
            className={cn(
              "mt-9 flex flex-col gap-3 sm:flex-row sm:items-center scroll-hidden",
              isVisible && "animate-fade-in-up stagger-3",
            )}
          >
            <Button size="lg" asChild className="touch-manipulation">
              <RouterLink to="/signup-org">
                Start Free
                <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
              </RouterLink>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <a href="#features">
                Explore Modules
                <ChevronRight className="ml-1 h-4 w-4" aria-hidden="true" />
              </a>
            </Button>
          </div>
          <div className="mt-10 flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted-foreground">
            <p>
              <span className="font-mono tabular-nums text-foreground">
                99.95%
              </span>{" "}
              Uptime
            </p>
            <p>
              <span className="font-mono tabular-nums text-foreground">
                3.8x
              </span>{" "}
              Faster Monthly Close
            </p>
            <p>
              <span className="font-mono tabular-nums text-foreground">
                24/7
              </span>{" "}
              Audit Trail
            </p>
          </div>
        </div>

        <Card
          className={cn(
            "relative border-border/80 bg-card/95 shadow-sm scroll-hidden",
            isVisible && "animate-scale-in stagger-2",
          )}
        >
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-x-0 top-0 h-1 rounded-t-lg bg-linear-to-r from-sky-500/70 via-cyan-400/80 to-emerald-400/80"
          />
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium uppercase tracking-[0.12em] text-muted-foreground">
              Live Operations Snapshot
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-md border border-border/70 bg-muted/40 p-3">
                <p className="text-xs text-muted-foreground">Open Orders</p>
                <p className="mt-2 font-mono text-2xl font-semibold tabular-nums">
                  128
                </p>
              </div>
              <div className="rounded-md border border-border/70 bg-muted/40 p-3">
                <p className="text-xs text-muted-foreground">Low Stock SKUs</p>
                <p className="mt-2 font-mono text-2xl font-semibold tabular-nums text-sky-700 dark:text-sky-300">
                  09
                </p>
              </div>
            </div>
            <div className="rounded-md border border-border/70 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-muted-foreground">
                Forecast Engine
              </p>
              <p className="mt-2 font-mono text-sm text-foreground">
                model://demand-weekly-v3
              </p>
              <p className="mt-3 text-sm text-muted-foreground">
                Next recommendation: Reorder{" "}
                <span className="font-medium text-foreground">42</span> units of
                "Premium Beans" by Friday.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
