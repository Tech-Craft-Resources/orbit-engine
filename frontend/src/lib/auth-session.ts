import { type QueryClient, queryOptions } from "@tanstack/react-query"

import {
  ApiError,
  type OrganizationPublic,
  OrganizationsService,
  type UserPublic,
  UsersService,
} from "@/client"

export const ACCESS_TOKEN_STORAGE_KEY = "access_token"

export type SessionStatus = "unknown" | "authenticated" | "unauthenticated"
export type UnauthenticatedReason = "missing-token" | "invalid-identity"

export const AUTH_QUERY_KEYS = {
  root: ["auth"] as const,
  currentUser: ["auth", "currentUser"] as const,
  currentOrganization: ["auth", "currentOrganization"] as const,
}

type AuthSessionState =
  | {
      status: "authenticated"
      user: UserPublic
    }
  | {
      status: "unauthenticated"
      reason: UnauthenticatedReason
    }

function isCurrentUserEndpoint(url: string): boolean {
  return url.endsWith("/api/v1/users/me")
}

export function getAccessToken(): string | null {
  return localStorage.getItem(ACCESS_TOKEN_STORAGE_KEY)
}

export function hasAccessToken(): boolean {
  return getAccessToken() !== null
}

export function setAccessToken(token: string): void {
  localStorage.setItem(ACCESS_TOKEN_STORAGE_KEY, token)
}

export function clearAccessToken(): void {
  localStorage.removeItem(ACCESS_TOKEN_STORAGE_KEY)
}

export function isSessionInvalidError(error: unknown): boolean {
  if (!(error instanceof ApiError)) {
    return false
  }

  if (![401, 403, 404].includes(error.status)) {
    return false
  }

  return (
    isCurrentUserEndpoint(error.request.url) || isCurrentUserEndpoint(error.url)
  )
}

export function isUnauthorizedError(error: unknown): boolean {
  return error instanceof ApiError && [401, 403].includes(error.status)
}

export function currentUserQueryOptions() {
  return queryOptions<UserPublic>({
    queryKey: AUTH_QUERY_KEYS.currentUser,
    queryFn: UsersService.readUserMe,
    retry: false,
    staleTime: 60_000,
  })
}

export function currentOrganizationQueryOptions() {
  return queryOptions<OrganizationPublic>({
    queryKey: AUTH_QUERY_KEYS.currentOrganization,
    queryFn: OrganizationsService.getMyOrganization,
    retry: false,
    staleTime: 60_000,
  })
}

export function clearAuthCache(queryClient: QueryClient): void {
  queryClient.removeQueries({ queryKey: AUTH_QUERY_KEYS.root })
}

export async function resolveAuthSession(
  queryClient: QueryClient,
): Promise<AuthSessionState> {
  if (!hasAccessToken()) {
    return {
      status: "unauthenticated",
      reason: "missing-token",
    }
  }

  try {
    const user = await queryClient.ensureQueryData(currentUserQueryOptions())
    return {
      status: "authenticated",
      user,
    }
  } catch (error) {
    if (!isSessionInvalidError(error)) {
      throw error
    }

    clearAccessToken()
    clearAuthCache(queryClient)

    return {
      status: "unauthenticated",
      reason: "invalid-identity",
    }
  }
}
