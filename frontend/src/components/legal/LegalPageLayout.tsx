import { type ReactNode, useEffect, useState } from "react"

import { LandingFooter } from "@/components/Landing/LandingFooter"
import { LandingNav } from "@/components/Landing/LandingNav"
import { cn } from "@/lib/utils"

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
  const [activeSectionId, setActiveSectionId] = useState(sections[0]?.id ?? "")

  useEffect(() => {
    if (sections.length === 0) {
      return
    }

    const sectionElements = sections
      .map((section) => document.getElementById(section.id))
      .filter((element): element is HTMLElement => element !== null)

    if (sectionElements.length === 0) {
      return
    }

    const sectionIds = new Set(sections.map((section) => section.id))

    const updateFromHash = () => {
      const hashId = decodeURIComponent(window.location.hash.replace("#", ""))
      if (hashId && sectionIds.has(hashId)) {
        setActiveSectionId(hashId)
      }
    }

    const updateFromScrollPosition = () => {
      const activationLine = window.innerHeight * 0.35
      let nextActiveId = sectionElements[0]?.id ?? sections[0].id

      for (const sectionElement of sectionElements) {
        if (sectionElement.getBoundingClientRect().top <= activationLine) {
          nextActiveId = sectionElement.id
          continue
        }
        break
      }

      const isNearPageBottom =
        window.innerHeight + window.scrollY >=
        document.documentElement.scrollHeight - 4

      if (isNearPageBottom) {
        nextActiveId = sectionElements[sectionElements.length - 1].id
      }

      setActiveSectionId(nextActiveId)
    }

    updateFromHash()
    updateFromScrollPosition()

    const observer =
      "IntersectionObserver" in window
        ? new IntersectionObserver(
            () => {
              updateFromScrollPosition()
            },
            {
              rootMargin: "-18% 0px -60% 0px",
              threshold: [0, 0.2, 0.4, 0.65, 1],
            },
          )
        : null

    if (observer) {
      for (const sectionElement of sectionElements) {
        observer.observe(sectionElement)
      }
    } else {
      window.addEventListener("scroll", updateFromScrollPosition, {
        passive: true,
      })
      window.addEventListener("resize", updateFromScrollPosition)
    }

    window.addEventListener("hashchange", updateFromHash)

    return () => {
      window.removeEventListener("hashchange", updateFromHash)
      window.removeEventListener("scroll", updateFromScrollPosition)
      window.removeEventListener("resize", updateFromScrollPosition)
      observer?.disconnect()
    }
  }, [sections])

  const getTocLinkClassName = (sectionId: string) =>
    cn(
      "block rounded-sm text-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 focus-visible:ring-offset-background",
      activeSectionId === sectionId
        ? "font-semibold text-primary"
        : "text-foreground/80 hover:text-foreground",
    )

  return (
    <div className="relative min-h-svh bg-background text-foreground landing-bg">
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
                        aria-current={
                          activeSectionId === section.id
                            ? "location"
                            : undefined
                        }
                        className={getTocLinkClassName(section.id)}
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

          <aside className="hidden self-start lg:sticky lg:top-20 lg:block">
            <nav
              aria-label="Indice de contenidos"
              className="max-h-[calc(100svh-5.5rem)] overflow-y-auto rounded-xl border border-border/70 bg-background/95 p-4 shadow-sm backdrop-blur"
            >
              <h2 className="text-sm font-semibold text-foreground">
                Índice de contenidos
              </h2>
              <ol className="mt-3 space-y-2">
                {sections.map((section) => (
                  <li key={section.id}>
                    <a
                      href={`#${section.id}`}
                      aria-current={
                        activeSectionId === section.id ? "location" : undefined
                      }
                      className={cn(
                        getTocLinkClassName(section.id),
                        "leading-6",
                      )}
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
