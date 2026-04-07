import { createFileRoute, redirect } from "@tanstack/react-router"
import { redirectIfAuthenticated } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

export const Route = createFileRoute("/signup")({
  component: () => null,
  beforeLoad: async () => {
    await redirectIfAuthenticated(queryClient)
    // Redirect to organization signup
    throw redirect({ to: "/signup-org" })
  },
})

export default function SignUp() {
  return null
}
