import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"

import {
  type Body_login_login_access_token as AccessToken,
  LoginService,
  type UserPublic,
} from "@/client"
import {
  AUTH_QUERY_KEYS,
  clearAccessToken,
  clearAuthCache,
  currentOrganizationQueryOptions,
  currentUserQueryOptions,
  hasAccessToken,
  type SessionStatus,
  setAccessToken,
} from "@/lib/auth-session"
import { handleError } from "@/utils"
import useCustomToast from "./useCustomToast"

/** Well-known role IDs matching backend seed data */
export const ROLE_IDS = {
  admin: 1,
  seller: 2,
  viewer: 3,
  contador: 4,
} as const

export type RoleName = keyof typeof ROLE_IDS

const ROLE_NAMES: Record<number, RoleName> = {
  [ROLE_IDS.admin]: "admin",
  [ROLE_IDS.seller]: "seller",
  [ROLE_IDS.viewer]: "viewer",
  [ROLE_IDS.contador]: "contador",
}

const isLoggedIn = () => {
  return hasAccessToken()
}

/**
 * Check whether a user's role matches any of the given role names.
 * Returns false if the user is undefined.
 */
export function hasRole(
  user: UserPublic | null | undefined,
  roles: RoleName[],
): boolean {
  if (!user) return false
  return roles.some((r) => ROLE_IDS[r] === user.role_id)
}

/**
 * Get the human-readable role name for a user.
 */
export function getRoleName(
  user: UserPublic | null | undefined,
): RoleName | undefined {
  if (!user) return undefined
  return ROLE_NAMES[user.role_id]
}

const useAuth = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const { showErrorToast } = useCustomToast()
  const hasToken = hasAccessToken()

  const {
    data: user,
    isPending: isUserPending,
    isFetching: isUserFetching,
  } = useQuery({
    ...currentUserQueryOptions(),
    enabled: hasToken,
  })

  const { data: organization } = useQuery({
    ...currentOrganizationQueryOptions(),
    enabled: hasToken && Boolean(user),
  })

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    setAccessToken(response.access_token)
  }

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: AUTH_QUERY_KEYS.root })
      navigate({ to: "/dashboard" })
    },
    onError: handleError.bind(showErrorToast),
  })

  const logout = () => {
    clearAccessToken()
    clearAuthCache(queryClient)
    navigate({ to: "/login" })
  }

  const sessionStatus: SessionStatus = !hasToken
    ? "unauthenticated"
    : isUserPending || (isUserFetching && !user)
      ? "unknown"
      : user
        ? "authenticated"
        : "unauthenticated"

  const roleName = getRoleName(user)

  return {
    loginMutation,
    logout,
    sessionStatus,
    user,
    organization,
    isLoading: sessionStatus === "unknown",
    roleName,
    /** Check if the current user has any of the given roles */
    hasRole: (roles: RoleName[]) => hasRole(user, roles),
  }
}

export { isLoggedIn }
export default useAuth
