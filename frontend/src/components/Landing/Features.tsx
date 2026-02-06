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
  description: string
}

const features: Feature[] = [
  {
    icon: Package,
    title: "Inventory Management",
    description:
      "Full product catalog with stock control, low-stock alerts, and movement history. Never lose track of your inventory again.",
  },
  {
    icon: ShoppingCart,
    title: "Sales Management",
    description:
      "Register sales, generate invoices automatically, and track your transaction history with a real-time sales dashboard.",
  },
  {
    icon: Users,
    title: "Customer Management",
    description:
      "Maintain a complete customer database with purchase history, contact info, and segmentation for targeted service.",
  },
  {
    icon: BarChart3,
    title: "Reports & Analytics",
    description:
      "KPI dashboards with interactive charts. Export daily, weekly, and monthly reports in PDF and Excel formats.",
  },
  {
    icon: Bot,
    title: "AI Demand Prediction",
    description:
      "Powered by Meta's Prophet, get smart restocking recommendations with quantity, urgency, and suggested order dates.",
  },
  {
    icon: ShieldCheck,
    title: "Roles & Security",
    description:
      "Multi-tenant architecture with role-based access. Administrators, sellers, and viewers each see what they need.",
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
    <section id="features" className="py-24 md:py-32">
      <div className="mx-auto max-w-6xl px-6">
        <div
          ref={header.ref}
          className={cn(
            "mx-auto max-w-2xl text-center scroll-hidden",
            header.isVisible && "animate-fade-in-up",
          )}
        >
          <Badge variant="outline" className="mb-4">
            Core Modules
          </Badge>
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Everything your business needs, in one place
          </h2>
          <p className="mt-4 text-muted-foreground">
            Six integrated modules designed to cover every aspect of your daily
            operations, from inventory to AI-powered forecasting.
          </p>
        </div>
        <div
          ref={grid.ref}
          className="mt-16 grid gap-6 sm:grid-cols-2 lg:grid-cols-3"
        >
          {features.map((feature, i) => (
            <Card
              key={feature.title}
              className={cn(
                "group transition-colors hover:border-primary/50 scroll-hidden",
                grid.isVisible && `animate-scale-in ${staggerClass[i]}`,
              )}
            >
              <CardHeader>
                <div className="mb-2 flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 text-primary transition-colors group-hover:bg-primary group-hover:text-primary-foreground">
                  <feature.icon className="h-5 w-5" />
                </div>
                <CardTitle className="text-lg">{feature.title}</CardTitle>
              </CardHeader>
              <CardContent>
                <CardDescription className="text-sm leading-relaxed">
                  {feature.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
