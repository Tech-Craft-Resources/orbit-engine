import type { LucideIcon } from "lucide-react"
import {
  BarChart3,
  Bot,
  Package,
  ShieldCheck,
  ShoppingCart,
  Users,
} from "lucide-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

interface Feature {
  icon: LucideIcon
  title: string
  detail: string
  dataPoint: string
}

const features: Feature[] = [
  {
    icon: Package,
    title: "Inventory Control",
    detail:
      "Track SKU movement, low-stock thresholds, and replenishment windows from one ledger.",
    dataPoint: "Stock Drift: -41%",
  },
  {
    icon: ShoppingCart,
    title: "Sales Workspace",
    detail:
      "Create invoices, monitor pending orders, and map revenue trends without switching tools.",
    dataPoint: "Checkout Time: 58s",
  },
  {
    icon: Users,
    title: "Customer Registry",
    detail:
      "Maintain complete profiles with order history, segmentation, and lifecycle signals.",
    dataPoint: "Retention Lift: +18%",
  },
  {
    icon: BarChart3,
    title: "Operational Analytics",
    detail:
      "See margin, volume, and conversion in a shared source of truth for every role.",
    dataPoint: "Report Prep: 1.4h",
  },
  {
    icon: Bot,
    title: "Forecast Automation",
    detail:
      "Use built-in demand modeling to prioritize purchase timing and reduce overstock.",
    dataPoint: "Forecast Confidence: 94.2%",
  },
  {
    icon: ShieldCheck,
    title: "Role Guardrails",
    detail:
      "Apply precise access controls so operators, managers, and finance teams only see what they need.",
    dataPoint: "Policy Coverage: 100%",
  },
]

const staggerClass = [
  "stagger-1",
  "stagger-2",
  "stagger-3",
  "stagger-4",
  "stagger-5",
  "stagger-6",
]

export function Features() {
  const header = useScrollAnimation()
  const grid = useScrollAnimation({ threshold: 0.1 })

  return (
    <section id="features" className="scroll-mt-24 py-20 md:py-24">
      <div className="mx-auto max-w-6xl px-6">
        <div
          ref={header.ref}
          className={cn(
            "mx-auto max-w-3xl text-center scroll-hidden",
            header.isVisible && "animate-fade-in-up",
          )}
        >
          <Badge variant="outline" className="mb-4 rounded-full border-primary/25 bg-primary/8 text-primary font-medium px-3">
            Product Surface
          </Badge>
          <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
            Every Core Workflow, Composed Into One Operating Layer
          </h2>
          <p className="mt-4 text-pretty text-muted-foreground">
            OrbitEngine keeps teams aligned by combining critical modules under
            a shared model, shared data, and shared accountability.
          </p>
        </div>

        <div
          ref={grid.ref}
          className="mt-12 grid gap-3 sm:grid-cols-2 xl:grid-cols-3"
        >
          {features.map((feature, index) => (
            <Card
              key={feature.title}
              className={cn(
                "relative overflow-hidden border-border/75 bg-card/95 transition-all hover:border-primary/40 hover:shadow-md scroll-hidden",
                grid.isVisible && `animate-scale-in ${staggerClass[index]}`,
              )}
            >
              <div
                aria-hidden="true"
                className="pointer-events-none absolute left-0 top-0 h-full w-0.5 bg-linear-to-b from-primary/80 via-primary/50 to-emerald-500/70"
              />
              <CardHeader className="pb-3 pl-5 pr-5 pt-5">
                <div className="mb-2 flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20 dark:bg-primary/15">
                  <feature.icon className="h-4 w-4" aria-hidden="true" />
                </div>
                <CardTitle className="text-base font-semibold tracking-tight">
                  {feature.title}
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4 pl-5 pr-5 pb-5">
                <CardDescription className="text-sm leading-6 text-muted-foreground">
                  {feature.detail}
                </CardDescription>
                <p className="rounded-md bg-primary/8 px-2.5 py-1.5 font-mono text-xs tabular-nums text-primary">
                  {feature.dataPoint}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
