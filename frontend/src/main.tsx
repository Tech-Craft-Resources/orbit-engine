import { QueryClientProvider } from "@tanstack/react-query"
import { createRouter, RouterProvider } from "@tanstack/react-router"
import { StrictMode } from "react"
import ReactDOM from "react-dom/client"
import { OpenAPI } from "./client"
import { ThemeProvider } from "./components/theme-provider"
import { Toaster } from "./components/ui/sonner"
import "./index.css"
import { getAccessToken } from "./lib/auth-session"
import { queryClient, registerAuthFailureHandler } from "./lib/queryClient"
import { routeTree } from "./routeTree.gen"

OpenAPI.BASE = import.meta.env.VITE_API_URL
OpenAPI.TOKEN = async () => {
  return getAccessToken() || ""
}

const router = createRouter({ routeTree })

registerAuthFailureHandler((reason) => {
  const currentPath = router.state.location.pathname
  const authPaths = new Set([
    "/login",
    "/signup",
    "/signup-org",
    "/recover-password",
    "/reset-password",
  ])

  if (authPaths.has(currentPath)) {
    return
  }

  router.navigate({
    to: "/login",
    search: { reason },
  })
})

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <QueryClientProvider client={queryClient}>
        <RouterProvider router={router} />
        <Toaster richColors closeButton />
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>,
)
