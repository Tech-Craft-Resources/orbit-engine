import { Link as RouterLink } from "@tanstack/react-router"
import { ArrowLeft } from "lucide-react"
import { Button } from "@/components/ui/button"

// import { Appearance } from "@/components/Common/Appearance";
import { Footer } from "./Footer"

interface AuthLayoutProps {
  children: React.ReactNode
  showHomeLink?: boolean
}

export function AuthLayout({
  children,
  showHomeLink = false,
}: AuthLayoutProps) {
  return (
    <div className="grid min-h-svh lg:h-svh lg:grid-cols-2">
      <div className="bg-muted relative hidden lg:flex lg:flex-col lg:items-center lg:justify-center lg:overflow-hidden">
        <img
          src="/assets/images/orbit-engine-logo.png"
          alt="OrbitEngine"
          className="h-40 dark:hidden"
        />
        <img
          src="/assets/images/orbit-engine-logo-dark.png"
          alt="OrbitEngine"
          className="h-40 hidden dark:block"
        />
        <h1 className="text-5xl">
          <span className="font-bold">Orbit</span>Engine
        </h1>
      </div>
      <div className="flex flex-col gap-4 p-6 md:p-10 lg:overflow-y-scroll auth-panel-scroll">
        <div className="sticky top-0 z-10 flex justify-between bg-background/95 py-2 backdrop-blur supports-[backdrop-filter]:bg-background/80">
          <div className="flex items-center gap-3">
            {showHomeLink ? (
              <Button
                variant="ghost"
                asChild
                className="min-h-11 px-3 touch-manipulation"
              >
                <RouterLink to="/" aria-label="Volver a la pagina principal">
                  <ArrowLeft className="size-4" aria-hidden="true" />
                  Volver al inicio
                </RouterLink>
              </Button>
            ) : null}

            <div className="text-2xl lg:hidden flex items-center gap-2">
              <img
                src="/assets/images/orbit-engine-logo.png"
                alt="OrbitEngine"
                className="h-8 dark:hidden"
              />
              <img
                src="/assets/images/orbit-engine-logo-dark.png"
                alt="OrbitEngine"
                className="h-8 hidden dark:block"
              />
              <h2>
                <span className="font-bold">Orbit</span>Engine
              </h2>
            </div>
          </div>
          {/* <Appearance /> */}
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">{children}</div>
        </div>
        <Footer />
      </div>
    </div>
  )
}
