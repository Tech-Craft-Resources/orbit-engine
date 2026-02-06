import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

interface Stat {
  value: string
  label: string
}

const stats: Stat[] = [
  { value: "40%", label: "Fewer administrative errors" },
  { value: "30%", label: "Time saved on manual tasks" },
  { value: "70%+", label: "Demand prediction accuracy" },
  { value: "3", label: "Clicks max for any action" },
]

const staggerClass = ["stagger-1", "stagger-2", "stagger-3", "stagger-4"]

export function Stats() {
  const { ref, isVisible } = useScrollAnimation({ threshold: 0.2 })

  return (
    <section id="stats" className="border-y bg-muted/50">
      <div
        ref={ref}
        className="mx-auto grid max-w-6xl grid-cols-2 gap-8 px-6 py-16 md:grid-cols-4"
      >
        {stats.map((stat, i) => (
          <div
            key={stat.label}
            className={cn(
              "text-center scroll-hidden",
              isVisible && `animate-fade-in-up ${staggerClass[i]}`,
            )}
          >
            <div className="text-3xl font-bold tracking-tight text-primary sm:text-4xl">
              {stat.value}
            </div>
            <p className="mt-1 text-sm text-muted-foreground">{stat.label}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
