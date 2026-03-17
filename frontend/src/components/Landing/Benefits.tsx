import type { LucideIcon } from "lucide-react"
import { Globe, Layers, TrendingUp, Zap } from "lucide-react"

import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

interface Benefit {
  icon: LucideIcon
  title: string
  description: string
}

const benefits: Benefit[] = [
  {
    icon: Zap,
    title: "Fast Team Adoption",
    description:
      "Interface patterns stay simple enough for non-technical operators and robust enough for managers.",
  },
  {
    icon: Layers,
    title: "Composable By Design",
    description:
      "Start with essential modules, then expand as your operation adds complexity.",
  },
  {
    icon: Globe,
    title: "Cloud-Ready Access",
    description:
      "Run workflows from desktop or mobile with consistent access and control.",
  },
  {
    icon: TrendingUp,
    title: "Decision-Grade Signals",
    description:
      "Move from static reports to prediction-supported planning and prioritization.",
  },
]

const rolloutSteps = [
  {
    step: "01",
    title: "Map Current Flow",
    detail: "Capture current inventory, sales, and customer touchpoints.",
  },
  {
    step: "02",
    title: "Activate Shared Modules",
    detail: "Launch a common workspace for operators and decision-makers.",
  },
  {
    step: "03",
    title: "Scale With Confidence",
    detail: "Use forecasting and analytics to guide monthly planning.",
  },
]

const staggerClass = ["stagger-1", "stagger-2", "stagger-3", "stagger-4"]

export function Benefits() {
  const left = useScrollAnimation()
  const right = useScrollAnimation()

  return (
    <section
      id="benefits"
      className="scroll-mt-24 border-y border-border/70 bg-muted/20 py-20 md:py-24"
    >
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-start">
          <div
            ref={left.ref}
            className={cn(
              "scroll-hidden",
              left.isVisible && "animate-fade-in-left",
            )}
          >
            <Badge
              variant="outline"
              className="mb-4 rounded-md border-border/70"
            >
              Why OrbitEngine
            </Badge>
            <h2 className="text-balance text-3xl font-semibold tracking-tight sm:text-4xl">
              Minimal Surface, High Operational Depth
            </h2>
            <p className="mt-4 max-w-2xl text-pretty text-muted-foreground">
              You get a clean interface that still supports dense workflows,
              role-based control, and measurable process discipline.
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {benefits.map((benefit, index) => (
                <article
                  key={benefit.title}
                  className={cn(
                    "rounded-md border border-border/75 bg-card p-4 shadow-sm scroll-hidden",
                    left.isVisible &&
                      `animate-fade-in-up ${staggerClass[index]}`,
                  )}
                >
                  <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-md bg-sky-100 text-sky-700 dark:bg-sky-950/70 dark:text-sky-300">
                    <benefit.icon className="h-4 w-4" aria-hidden="true" />
                  </div>
                  <h3 className="text-sm font-medium text-foreground">
                    {benefit.title}
                  </h3>
                  <p className="mt-1 text-sm leading-6 text-muted-foreground">
                    {benefit.description}
                  </p>
                </article>
              ))}
            </div>
          </div>

          <aside
            ref={right.ref}
            className={cn(
              "rounded-md border border-border/75 bg-card p-6 shadow-sm scroll-hidden",
              right.isVisible && "animate-fade-in-right",
            )}
            aria-label="Implementation Path"
          >
            <h3 className="text-base font-medium">Implementation Path</h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Roll out in short cycles while keeping governance and reporting
              intact.
            </p>
            <Separator className="my-5" />
            <div className="space-y-5">
              {rolloutSteps.map((item, index) => (
                <div
                  key={item.step}
                  className={cn(
                    "rounded-sm border border-border/65 p-3 scroll-hidden",
                    right.isVisible &&
                      `animate-fade-in-up ${staggerClass[index]}`,
                  )}
                >
                  <p className="font-mono text-xs tabular-nums text-sky-700 dark:text-sky-300">
                    Step {item.step}
                  </p>
                  <p className="mt-1 text-sm font-medium text-foreground">
                    {item.title}
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    {item.detail}
                  </p>
                </div>
              ))}
            </div>
          </aside>
        </div>
      </div>
    </section>
  )
}
