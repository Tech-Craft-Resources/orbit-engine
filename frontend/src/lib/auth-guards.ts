import type { QueryClient } from "@tanstack/react-query"
import { redirect } from "@tanstack/react-router"

import { hasRole, type RoleName } from "@/hooks/useAuth"
import { resolveAuthSession } from "@/lib/auth-session"

function getLoginReason(reason: "missing-token" | "invalid-identity") {
  return reason === "invalid-identity" ? "session-invalid" : "auth-required"
}

export async function redirectIfAuthenticated(
  queryClient: QueryClient,
): Promise<void> {
  const session = await resolveAuthSession(queryClient)

  if (session.status === "authenticated") {
    throw redirect({ to: "/dashboard" })
  }
}

export async function requireAuthenticatedUser(queryClient: QueryClient) {
  const session = await resolveAuthSession(queryClient)

  if (session.status === "unauthenticated") {
    throw redirect({
      to: "/login",
      search: { reason: getLoginReason(session.reason) },
    })
  }

  return session.user
}

export async function requireUserWithRoles(
  queryClient: QueryClient,
  roles: RoleName[],
) {
  const user = await requireAuthenticatedUser(queryClient)

  if (!hasRole(user, roles)) {
    throw redirect({ to: "/dashboard" })
  }

  return user
}
