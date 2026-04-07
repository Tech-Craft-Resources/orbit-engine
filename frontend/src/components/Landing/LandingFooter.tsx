import { Link as RouterLink } from "@tanstack/react-router"
import { FaGithub } from "react-icons/fa"

import { Separator } from "@/components/ui/separator"
import { landingNavLinks } from "./landingNavLinks"

interface FooterLink {
  label: string
  href: string
  external?: boolean
}

interface FooterSection {
  title: string
  links: FooterLink[]
}

const footerSections: FooterSection[] = [
  {
    title: "Producto",
    links: [
      ...landingNavLinks.map(({ href, label }) => ({ href, label })),
      { label: "Comenzar prueba gratis", href: "/signup" },
    ],
  },
  {
    title: "Empresa",
    links: [
      {
        label: "Repositorio",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine",
        external: true,
      },
      {
        label: "Documentación",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine#readme",
        external: true,
      },
      {
        label: "Licencia",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/LICENSE",
        external: true,
      },
      {
        label: "Soporte",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/issues",
        external: true,
      },
    ],
  },
  {
    title: "Acceso",
    links: [
      { label: "Iniciar sesión", href: "/login" },
      { label: "Crear cuenta", href: "/signup" },
      {
        label: "Notas del proyecto",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/README.md",
        external: true,
      },
    ],
  },
]

const legalLinks: FooterLink[] = [
  {
    label: "Privacidad",
    href: "/privacidad",
  },
  {
    label: "Términos",
    href: "/terminos",
  },
]

function FooterLinkItem({ link }: { link: FooterLink }) {
  if (link.external) {
    return (
      <a
        href={link.href}
        target="_blank"
        rel="noopener noreferrer"
        className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60"
      >
        {link.label}
      </a>
    )
  }

  if (link.href.startsWith("#")) {
    return (
      <a
        href={link.href}
        className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60"
      >
        {link.label}
      </a>
    )
  }

  return (
    <a
      href={link.href}
      className="text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60"
    >
      {link.label}
    </a>
  )
}

export function LandingFooter() {
  return (
    <footer className="border-t border-border/70 bg-muted/15">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="grid gap-10 md:grid-cols-2 lg:grid-cols-5">
          <div className="lg:col-span-2">
            <RouterLink to="/" className="flex items-center gap-3">
              <img
                src="/assets/images/orbit-engine-logo.png"
                alt="OrbitEngine"
                width={28}
                height={28}
                className="h-7 dark:hidden"
              />
              <img
                src="/assets/images/orbit-engine-logo-dark.png"
                alt="OrbitEngine"
                width={28}
                height={28}
                className="hidden h-7 dark:block"
              />
              <span className="text-base tracking-tight">
                <span className="font-semibold">Orbit</span>Engine
              </span>
            </RouterLink>
            <p className="mt-4 max-w-sm text-sm leading-6 text-muted-foreground">
              Centraliza inventario, ventas y control operativo en un solo lugar
              para crecer con procesos ordenados.
            </p>
            <a
              href="https://github.com/Tech-Craft-Resources/orbit-engine"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Abrir repositorio de OrbitEngine en GitHub"
              className="mt-5 inline-flex items-center gap-2 text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring/60"
            >
              <FaGithub className="h-4 w-4" aria-hidden="true" />
              <span className="text-sm">GitHub</span>
            </a>
          </div>

          {footerSections.map((section) => (
            <div key={section.title}>
              <h3 className="mb-4 text-xs font-medium uppercase tracking-[0.08em] text-muted-foreground">
                {section.title}
              </h3>
              <ul className="space-y-3 text-sm">
                {section.links.map((link) => (
                  <li key={link.label}>
                    <FooterLinkItem link={link} />
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <Separator className="my-8" />
        <div className="flex flex-col gap-3 text-sm text-muted-foreground sm:flex-row sm:items-center sm:justify-between">
          <p>
            Copyright {new Date().getFullYear()} OrbitEngine. Todos los derechos
            reservados.
          </p>
          <div className="flex items-center gap-6">
            {legalLinks.map((link) => (
              <FooterLinkItem key={link.label} link={link} />
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
