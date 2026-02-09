import { useMutation, useQuery } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"

import {
  type Body_login_login_access_token as AccessToken,
  LoginService,
  type OrganizationPublic,
  OrganizationsService,
  type UserPublic,
  UsersService,
} from "@/client"
import { handleError } from "@/utils"
import useCustomToast from "./useCustomToast"

/** Well-known role IDs matching backend seed data */
export const ROLE_IDS = {
  admin: 1,
  seller: 2,
  viewer: 3,
} as const

export type RoleName = keyof typeof ROLE_IDS

const ROLE_NAMES: Record<number, RoleName> = {
  [ROLE_IDS.admin]: "admin",
  [ROLE_IDS.seller]: "seller",
  [ROLE_IDS.viewer]: "viewer",
}

const isLoggedIn = () => {
  return localStorage.getItem("access_token") !== null
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
  const { showErrorToast } = useCustomToast()

  const { data: user, isLoading } = useQuery<UserPublic | null, Error>({
    queryKey: ["currentUser"],
    queryFn: UsersService.readUserMe,
    enabled: isLoggedIn(),
  })

  const { data: organization } = useQuery<OrganizationPublic | null, Error>({
    queryKey: ["currentOrganization"],
    queryFn: OrganizationsService.getMyOrganization,
    enabled: isLoggedIn(),
  })

  const login = async (data: AccessToken) => {
    const response = await LoginService.loginAccessToken({
      formData: data,
    })
    localStorage.setItem("access_token", response.access_token)
  }

  const loginMutation = useMutation({
    mutationFn: login,
    onSuccess: () => {
      navigate({ to: "/dashboard" })
    },
    onError: handleError.bind(showErrorToast),
  })

  const logout = () => {
    localStorage.removeItem("access_token")
    navigate({ to: "/login" })
  }

  const roleName = getRoleName(user)

  return {
    loginMutation,
    logout,
    user,
    organization,
    isLoading,
    roleName,
    /** Check if the current user has any of the given roles */
    hasRole: (roles: RoleName[]) => hasRole(user, roles),
  }
}

export { isLoggedIn }
export default useAuth
