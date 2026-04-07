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
    title: "Administrador de pyme",
    description:
      "Control total de inventario, ventas y operación en una sola vista.",
  },
  {
    icon: Layers,
    title: "Vendedor",
    description:
      "Ventas más rápidas con información clave al momento y mejor atención.",
  },
  {
    icon: Globe,
    title: "Contador / visualizador",
    description:
      "Reportes y exportaciones para seguimiento financiero y control documental.",
  },
  {
    icon: TrendingUp,
    title: "Escalabilidad real",
    description:
      "Agrega usuarios y volumen sin perder trazabilidad ni visibilidad.",
  },
]

const rolloutSteps = [
  {
    step: "01",
    title: "Empieza con lo que ya tienes",
    detail: "Ordena tus procesos actuales sin frenar la operación.",
  },
  {
    step: "02",
    title: "Conecta áreas y equipos",
    detail: "Comparte información en tiempo real entre roles clave.",
  },
  {
    step: "03",
    title: "Escala con control",
    detail: "Mantiene control operativo y reportes claros al crecer.",
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
              className="mb-4 rounded-full border-primary/25 bg-primary/8 text-primary font-medium px-3"
            >
              Valor por rol
            </Badge>
            <h2 className="text-balance text-3xl font-bold tracking-tight sm:text-4xl">
              Una plataforma pensada para pymes en crecimiento
            </h2>
            <p className="mt-4 max-w-2xl text-pretty text-muted-foreground">
              Cada rol ve lo que necesita para ejecutar rápido, colaborar mejor
              y decidir con datos confiables.
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              {benefits.map((benefit, index) => (
                <article
                  key={benefit.title}
                  className={cn(
                    "rounded-lg border border-border/75 bg-card p-4 shadow-sm transition-all hover:border-primary/30 hover:shadow-md scroll-hidden",
                    left.isVisible &&
                      `animate-fade-in-up ${staggerClass[index]}`,
                  )}
                >
                  <div className="mb-3 flex h-8 w-8 items-center justify-center rounded-lg bg-primary/10 text-primary ring-1 ring-primary/20 dark:bg-primary/15">
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
              "rounded-xl border border-border/75 bg-card p-6 shadow-sm scroll-hidden",
              right.isVisible && "animate-fade-in-right",
            )}
            aria-label="Ruta de implementación"
          >
            <h3 className="text-base font-semibold tracking-tight">
              Implementación por etapas
            </h3>
            <p className="mt-2 text-sm text-muted-foreground">
              Activa OrbitEngine en ciclos cortos y mantén el control desde el
              primer día.
            </p>
            <Separator className="my-5" />
            <div className="space-y-5">
              {rolloutSteps.map((item, index) => (
                <div
                  key={item.step}
                  className={cn(
                    "rounded-lg border border-border/65 bg-muted/20 p-3 scroll-hidden",
                    right.isVisible &&
                      `animate-fade-in-up ${staggerClass[index]}`,
                  )}
                >
                  <p className="font-mono text-xs tabular-nums font-semibold text-primary">
                    Paso {item.step}
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
