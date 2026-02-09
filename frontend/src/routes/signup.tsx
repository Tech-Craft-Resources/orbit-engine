import { createFileRoute, redirect } from "@tanstack/react-router"
import { isLoggedIn } from "@/hooks/useAuth"

export const Route = createFileRoute("/signup")({
  component: () => null,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({ to: "/" })
    }
    // Redirect to organization signup
    throw redirect({ to: "/signup-org" })
  },
})

export default function SignUp() {
  return null
}
