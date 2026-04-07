export interface LandingNavLink {
  href: `#${string}`
  sectionId: string
  label: string
}

export const landingNavLinks: LandingNavLink[] = [
  { href: "#stats", sectionId: "stats", label: "Beneficios" },
  { href: "#features", sectionId: "features", label: "Cómo funciona" },
  {
    href: "#benefits",
    sectionId: "benefits",
    label: "Equipos",
  },
]
