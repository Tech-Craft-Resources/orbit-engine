import type { ReactNode } from "react"

import { LandingFooter } from "@/components/Landing/LandingFooter"
import { LandingNav } from "@/components/Landing/LandingNav"

type LegalPageLayoutProps = {
  title: string
  lastUpdated: string
  sections: LegalTocItem[]
  children: ReactNode
}

type LegalTocItem = {
  id: string
  title: string
}

type LegalSectionProps = {
  id: string
  title: string
  children: ReactNode
}

export function LegalPageLayout({
  title,
  lastUpdated,
  sections,
  children,
}: LegalPageLayoutProps) {
  return (
    <div className="relative min-h-svh overflow-x-hidden bg-background text-foreground landing-bg">
      <LandingNav />
      <main className="mx-auto w-full max-w-6xl px-4 pb-16 pt-24 sm:px-6 lg:px-8">
        <div className="grid items-start gap-8 lg:grid-cols-[minmax(0,1fr)_16rem] lg:gap-10">
          <article className="max-w-3xl">
            <header className="border-b border-border/70 pb-6 sm:pb-8">
              <h1 className="text-balance text-2xl font-bold tracking-tight sm:text-3xl">
                {title}
              </h1>
              <p className="mt-3 text-sm text-muted-foreground">
                Última actualización: {lastUpdated}
              </p>
            </header>
            <details className="mt-6 rounded-xl border border-border/70 bg-muted/30 p-4 lg:hidden">
              <summary className="cursor-pointer text-sm font-semibold text-foreground">
                Índice de contenidos
              </summary>
              <nav aria-label="Indice de contenidos" className="mt-3">
                <ol className="space-y-2">
                  {sections.map((section) => (
                    <li key={section.id}>
                      <a
                        href={`#${section.id}`}
                        className="text-sm text-foreground/80 transition-colors hover:text-foreground focus-visible:rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                      >
                        {section.title}
                      </a>
                    </li>
                  ))}
                </ol>
              </nav>
            </details>
            <div className="mt-8 space-y-8">{children}</div>
          </article>

          <aside className="hidden self-start lg:block">
            <nav
              aria-label="Indice de contenidos"
              className="sticky top-24 max-h-[calc(100svh-7rem)] overflow-y-auto rounded-xl border border-border/70 bg-background/95 p-4 shadow-sm backdrop-blur"
            >
              <h2 className="text-sm font-semibold text-foreground">
                Índice de contenidos
              </h2>
              <ol className="mt-3 space-y-2">
                {sections.map((section) => (
                  <li key={section.id}>
                    <a
                      href={`#${section.id}`}
                      className="text-sm leading-6 text-foreground/80 transition-colors hover:text-foreground focus-visible:rounded-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
                    >
                      {section.title}
                    </a>
                  </li>
                ))}
              </ol>
            </nav>
          </aside>
        </div>
      </main>
      <LandingFooter />
    </div>
  )
}

export function LegalSection({ id, title, children }: LegalSectionProps) {
  return (
    <section id={id} aria-labelledby={`${id}-title`} className="scroll-mt-28">
      <h2
        id={`${id}-title`}
        className="text-lg font-semibold tracking-tight text-foreground sm:text-xl"
      >
        {title}
      </h2>
      <div className="mt-3 space-y-3 text-pretty text-[0.95rem] leading-7 text-foreground/90">
        {children}
      </div>
    </section>
  )
}

export function LegalLink({
  href,
  children,
}: {
  href: string
  children: ReactNode
}) {
  return (
    <a
      href={href}
      className="font-medium text-primary underline underline-offset-4 transition-colors hover:text-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background"
    >
      {children}
    </a>
  )
}
