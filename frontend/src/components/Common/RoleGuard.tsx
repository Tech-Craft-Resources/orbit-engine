import type { ReactNode } from "react"
import useAuth, { type RoleName } from "@/hooks/useAuth"

interface RoleGuardProps {
  /** Roles that are allowed to see the children */
  roles: RoleName[]
  /** Content to render when the user has an allowed role */
  children: ReactNode
  /** Optional content to render when the user does NOT have an allowed role */
  fallback?: ReactNode
}

/**
 * Conditionally renders children based on the current user's role.
 *
 * Usage:
 * ```tsx
 * <RoleGuard roles={["admin", "seller"]}>
 *   <Button>Create Sale</Button>
 * </RoleGuard>
 * ```
 */
export function RoleGuard({
  roles,
  children,
  fallback = null,
}: RoleGuardProps) {
  const { hasRole } = useAuth()

  if (!hasRole(roles)) {
    return <>{fallback}</>
  }

  return <>{children}</>
}
