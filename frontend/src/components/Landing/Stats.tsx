import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

interface Stat {
  metric: string
  label: string
  context: string
}

const stats: Stat[] = [
  {
    metric: "-32%",
    label: "Admin Rework",
    context: "Fewer back-office corrections after process rollout",
  },
  {
    metric: "+47%",
    label: "Order Throughput",
    context: "More completed orders per operator per day",
  },
  {
    metric: "94.2%",
    label: "Forecast Precision",
    context: "Average demand signal quality across active catalogs",
  },
  {
    metric: "4.6 d",
    label: "Onboarding Time",
    context: "Median days to team-level adoption",
  },
]

const staggerClass = ["stagger-1", "stagger-2", "stagger-3", "stagger-4"]

export function Stats() {
  const { ref, isVisible } = useScrollAnimation({ threshold: 0.2 })

  return (
    <section
      id="stats"
      className="scroll-mt-24 border-b border-border/70 py-14 md:py-16"
    >
      <div className="mx-auto max-w-6xl px-6">
        <h2 className="sr-only">Performance Proof</h2>
        <div ref={ref} className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {stats.map((stat, index) => (
            <article
              key={stat.label}
              className={cn(
                "rounded-lg border border-border/75 bg-card p-5 shadow-sm transition-shadow hover:shadow-md hover:border-primary/30 scroll-hidden",
                isVisible && `animate-fade-in-up ${staggerClass[index]}`,
              )}
            >
              <p className="font-mono text-2xl font-bold tabular-nums tracking-tight text-primary">
                {stat.metric}
              </p>
              <p className="mt-2 text-sm font-semibold text-foreground">
                {stat.label}
              </p>
              <p className="mt-1 text-xs leading-5 text-muted-foreground">
                {stat.context}
              </p>
            </article>
          ))}
        </div>
      </div>
    </section>
  )
}
