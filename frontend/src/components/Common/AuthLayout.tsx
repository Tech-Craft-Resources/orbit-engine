import { Appearance } from "@/components/Common/Appearance"
import { Footer } from "./Footer"

interface AuthLayoutProps {
  children: React.ReactNode
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div className="grid min-h-svh lg:grid-cols-2">
      <div className="bg-muted relative hidden lg:flex lg:flex-col lg:items-center lg:justify-center">
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
      <div className="flex flex-col gap-4 p-6 md:p-10">
        <div className="flex justify-between">
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
          <Appearance />
        </div>
        <div className="flex flex-1 items-center justify-center">
          <div className="w-full max-w-xs">{children}</div>
        </div>
        <Footer />
      </div>
    </div>
  )
}
