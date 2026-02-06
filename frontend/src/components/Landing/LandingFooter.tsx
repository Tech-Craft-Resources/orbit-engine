import { Link as RouterLink } from "@tanstack/react-router"
import { FaGithub } from "react-icons/fa"

import { Separator } from "@/components/ui/separator"

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
    title: "Product",
    links: [
      { label: "Features", href: "#features" },
      { label: "Benefits", href: "#benefits" },
      { label: "Results", href: "#stats" },
      { label: "Pricing", href: "/signup" },
    ],
  },
  {
    title: "Company",
    links: [
      {
        label: "About Us",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine",
        external: true,
      },
      {
        label: "Documentation",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine#readme",
        external: true,
      },
      {
        label: "License",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/LICENSE",
        external: true,
      },
      {
        label: "Contact",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/issues",
        external: true,
      },
    ],
  },
  {
    title: "Resources",
    links: [
      { label: "Log In", href: "/login" },
      { label: "Sign Up", href: "/signup" },
      {
        label: "GitHub",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine",
        external: true,
      },
      {
        label: "API Docs",
        href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/README.md",
        external: true,
      },
    ],
  },
]

const legalLinks: FooterLink[] = [
  {
    label: "Privacy",
    href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/LICENSE",
    external: true,
  },
  {
    label: "Terms",
    href: "https://github.com/Tech-Craft-Resources/orbit-engine/blob/main/LICENSE",
    external: true,
  },
  {
    label: "Support",
    href: "https://github.com/Tech-Craft-Resources/orbit-engine/issues",
    external: true,
  },
]

export function LandingFooter() {
  return (
    <footer className="border-t bg-muted/30">
      <div className="mx-auto max-w-6xl px-6 py-12 md:py-16">
        <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-5">
          {/* Brand Section */}
          <div className="lg:col-span-2">
            <RouterLink to="/" className="flex items-center gap-2">
              <img
                src="/assets/images/orbit-engine-logo.png"
                alt="OrbitEngine"
                className="h-8"
              />
              <span className="text-xl font-semibold">
                <span className="font-bold">Orbit</span>Engine
              </span>
            </RouterLink>
            <p className="mt-4 text-sm text-muted-foreground">
              Smart business management platform for SMEs. Digitalize your
              operations, automate routine tasks, and make data-driven decisions
              with AI.
            </p>
            <div className="mt-6 flex items-center gap-4">
              <a
                href="https://github.com/Tech-Craft-Resources/orbit-engine"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="GitHub"
                className="text-muted-foreground transition-colors hover:text-foreground"
              >
                <FaGithub className="h-5 w-5" />
              </a>
            </div>
          </div>

          {/* Link Sections */}
          {footerSections.map((section) => (
            <div key={section.title}>
              <h3 className="mb-4 text-sm font-semibold">{section.title}</h3>
              <ul className="space-y-3 text-sm">
                {section.links.map((link) =>
                  link.external ? (
                    <li key={link.label}>
                      <a
                        href={link.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-muted-foreground transition-colors hover:text-foreground"
                      >
                        {link.label}
                      </a>
                    </li>
                  ) : (
                    <li key={link.label}>
                      {link.href.startsWith("#") ? (
                        <a
                          href={link.href}
                          className="text-muted-foreground transition-colors hover:text-foreground"
                        >
                          {link.label}
                        </a>
                      ) : (
                        <RouterLink
                          to={link.href}
                          className="text-muted-foreground transition-colors hover:text-foreground"
                        >
                          {link.label}
                        </RouterLink>
                      )}
                    </li>
                  ),
                )}
              </ul>
            </div>
          ))}
        </div>

        {/* Bottom Bar */}
        <Separator className="my-8" />
        <div className="flex flex-col items-center justify-between gap-4 text-sm text-muted-foreground sm:flex-row">
          <p>© {new Date().getFullYear()} OrbitEngine. All rights reserved.</p>
          <div className="flex gap-6">
            {legalLinks.map((link) => (
              <a
                key={link.label}
                href={link.href}
                target="_blank"
                rel="noopener noreferrer"
                className="transition-colors hover:text-foreground"
              >
                {link.label}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  )
}
