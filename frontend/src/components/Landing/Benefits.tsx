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
    title: "Built for Simplicity",
    description:
      "Designed for non-technical users. Your team can get started in minutes, not weeks.",
  },
  {
    icon: Layers,
    title: "Modular & Scalable",
    description:
      "Start with what you need today and add modules as your business grows. Pay for what you use.",
  },
  {
    icon: Globe,
    title: "Cloud-Native",
    description:
      "Access your business data from anywhere, on any device. No hardware or installation required.",
  },
  {
    icon: TrendingUp,
    title: "AI-Powered Insights",
    description:
      "Go beyond data entry. Get predictions, trends, and actionable recommendations automatically.",
  },
]

interface Role {
  letter: string
  title: string
  description: string
}

const roles: Role[] = [
  {
    letter: "A",
    title: "Administrator",
    description:
      "Full control over inventory, sales, customers, and reports. Manage your team and make strategic decisions with AI insights.",
  },
  {
    letter: "S",
    title: "Seller",
    description:
      "Register sales quickly, check stock in real time, and access customer history for better service.",
  },
  {
    letter: "V",
    title: "Viewer",
    description:
      "Read-only access to reports and analytics. Perfect for external accountants and business advisors.",
  },
]

const staggerClass = ["stagger-1", "stagger-2", "stagger-3", "stagger-4"]

export function Benefits() {
  const left = useScrollAnimation()
  const right = useScrollAnimation()

  return (
    <section id="benefits" className="border-y bg-muted/30 py-24 md:py-32">
      <div className="mx-auto max-w-6xl px-6">
        <div className="grid gap-12 lg:grid-cols-2 lg:items-center">
          <div
            ref={left.ref}
            className={cn(
              "scroll-hidden",
              left.isVisible && "animate-fade-in-left",
            )}
          >
            <Badge variant="outline" className="mb-4">
              Why OrbitEngine
            </Badge>
            <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Designed for the reality of small businesses
            </h2>
            <p className="mt-4 text-muted-foreground">
              Enterprise tools are too complex and expensive. Spreadsheets don't
              scale. OrbitEngine bridges the gap with a platform that's powerful
              yet accessible.
            </p>
            <div className="mt-8 grid gap-6 sm:grid-cols-2">
              {benefits.map((benefit, i) => (
                <div
                  key={benefit.title}
                  className={cn(
                    "flex gap-3 scroll-hidden",
                    left.isVisible &&
                      `animate-fade-in-up ${staggerClass[i + 1]}`,
                  )}
                >
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-primary">
                    <benefit.icon className="h-4 w-4" />
                  </div>
                  <div>
                    <h3 className="font-semibold">{benefit.title}</h3>
                    <p className="mt-1 text-sm text-muted-foreground">
                      {benefit.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div
            ref={right.ref}
            className={cn(
              "rounded-xl border bg-card p-8 shadow-sm scroll-hidden",
              right.isVisible && "animate-fade-in-right",
            )}
          >
            <h3 className="text-lg font-semibold">Built for three key roles</h3>
            <Separator className="my-4" />
            <div className="space-y-6">
              {roles.map((role, i) => (
                <div
                  key={role.letter}
                  className={cn(
                    "flex gap-4 scroll-hidden",
                    right.isVisible &&
                      `animate-fade-in-up ${staggerClass[i + 1]}`,
                  )}
                >
                  <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-primary/10 text-sm font-bold text-primary">
                    {role.letter}
                  </div>
                  <div>
                    <p className="font-medium">{role.title}</p>
                    <p className="text-sm text-muted-foreground">
                      {role.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
