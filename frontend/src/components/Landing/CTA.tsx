import { Link as RouterLink } from "@tanstack/react-router"
import { ArrowRight } from "lucide-react"

import { Button } from "@/components/ui/button"
import { useScrollAnimation } from "@/hooks/useScrollAnimation"
import { cn } from "@/lib/utils"

export function CTA() {
  const { ref, isVisible } = useScrollAnimation()

  return (
    <section className="py-24 md:py-32">
      <div className="mx-auto max-w-6xl px-6">
        <div
          ref={ref}
          className={cn(
            "rounded-2xl border bg-card p-8 text-center shadow-sm md:p-16 scroll-hidden",
            isVisible && "animate-scale-in",
          )}
        >
          <h2
            className={cn(
              "text-3xl font-bold tracking-tight sm:text-4xl scroll-hidden",
              isVisible && "animate-fade-in-up stagger-1",
            )}
          >
            Ready to take control of your business?
          </h2>
          <p
            className={cn(
              "mx-auto mt-4 max-w-xl text-muted-foreground scroll-hidden",
              isVisible && "animate-fade-in stagger-2",
            )}
          >
            Stop losing time on spreadsheets and manual processes. OrbitEngine
            gives you the tools and intelligence to grow with confidence.
          </p>
          <div
            className={cn(
              "mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center scroll-hidden",
              isVisible && "animate-fade-in-up stagger-3",
            )}
          >
            <Button size="lg" asChild>
              <RouterLink to="/signup">
                Get Started Now
                <ArrowRight className="ml-2 h-4 w-4" />
              </RouterLink>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <RouterLink to="/login">Log In to Your Account</RouterLink>
            </Button>
          </div>
        </div>
      </div>
    </section>
  )
}
