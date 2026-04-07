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
        className="pointer-events-none absolute inset-0 -z-10 bg-[linear-gradient(180deg,transparent_0%,rgba(15,23,42,0.02)_100%)] dark:bg-[linear-gradient(180deg,transparent_0%,rgba(37,99,235,0.04)_100%)]"
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
            className="mb-5 rounded-full border border-primary/20 bg-primary/8 text-primary font-medium px-3"
          >
            1 mes gratis con acceso completo al plan Pro
          </Badge>
          <h1 className="text-balance text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Controla inventario, ventas y operación de tu pyme desde un solo
            lugar.
          </h1>
          <p
            className={cn(
              "mt-6 max-w-2xl text-pretty text-base leading-7 text-muted-foreground sm:text-lg scroll-hidden",
              isVisible && "animate-fade-in stagger-2",
            )}
          >
            OrbitEngine digitaliza y automatiza tus procesos internos para que
            tu equipo trabaje con orden, rapidez y métricas confiables desde el
            primer día.
          </p>
          <div
            className={cn(
              "mt-9 flex flex-col gap-3 sm:flex-row sm:items-center scroll-hidden",
              isVisible && "animate-fade-in-up stagger-3",
            )}
          >
            <Button size="lg" asChild className="touch-manipulation">
              <RouterLink to="/signup-org">
                Comenzar prueba gratis
                <ArrowRight className="ml-2 h-4 w-4" aria-hidden="true" />
              </RouterLink>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <a href="#features">
                Ver cómo funciona
                <ChevronRight className="ml-1 h-4 w-4" aria-hidden="true" />
              </a>
            </Button>
          </div>
          <div className="mt-10 flex flex-wrap gap-x-6 gap-y-2 text-sm text-muted-foreground">
            <p>
              <span className="font-mono tabular-nums font-semibold text-primary">
                99.95%
              </span>{" "}
              Operación estable
            </p>
            <p>
              <span className="font-mono tabular-nums font-semibold text-primary">
                3.8x
              </span>{" "}
              Menos tareas manuales
            </p>
            <p>
              <span className="font-mono tabular-nums font-semibold text-primary">
                24/7
              </span>{" "}
              Trazabilidad operativa
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
            className="pointer-events-none absolute inset-x-0 top-0 h-0.5 rounded-t-lg bg-linear-to-r from-primary/90 via-primary/70 to-emerald-500/80"
          />
          <CardHeader className="pb-3">
            <CardTitle className="text-xs font-semibold uppercase tracking-[0.12em] text-muted-foreground">
              Estado operativo en tiempo real
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-5">
            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-lg border border-border/70 bg-muted/40 p-3">
                <p className="text-xs text-muted-foreground">
                  Ordenes abiertas
                </p>
                <p className="mt-2 font-mono text-2xl font-bold tabular-nums tracking-tight">
                  128
                </p>
              </div>
              <div className="rounded-lg border border-primary/20 bg-primary/5 p-3">
                <p className="text-xs text-muted-foreground">
                  SKU con stock bajo
                </p>
                <p className="mt-2 font-mono text-2xl font-bold tabular-nums tracking-tight text-primary">
                  09
                </p>
              </div>
            </div>
            <div className="rounded-lg border border-border/70 bg-muted/20 p-4">
              <p className="text-xs uppercase tracking-[0.08em] text-muted-foreground">
                Recomendación operativa
              </p>
              <p className="mt-2 font-mono text-sm text-primary">
                seguimiento://inventario-semanal
              </p>
              <p className="mt-3 text-sm text-muted-foreground">
                Siguiente acción sugerida: reponer{" "}
                <span className="font-semibold text-foreground">42</span>{" "}
                unidades de "Café Premium" antes del viernes.
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </section>
  )
}
