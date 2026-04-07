import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query"

import { ApiError } from "@/client"
import {
  clearAccessToken,
  clearAuthCache,
  isSessionInvalidError,
  isUnauthorizedError,
} from "@/lib/auth-session"

type AuthFailureReason = "auth-required" | "session-invalid"

let authFailureHandler: ((reason: AuthFailureReason) => void) | null = null

export function registerAuthFailureHandler(
  handler: (reason: AuthFailureReason) => void,
): void {
  authFailureHandler = handler
}

const queryClient = new QueryClient({
  queryCache: new QueryCache({
    onError: handleApiError,
  }),
  mutationCache: new MutationCache({
    onError: handleApiError,
  }),
})

function handleApiError(error: Error): void {
  if (!(error instanceof ApiError)) {
    return
  }

  const unauthorized = isUnauthorizedError(error)
  const invalidSession = isSessionInvalidError(error)
  if (!unauthorized && !invalidSession) {
    return
  }

  clearAccessToken()
  clearAuthCache(queryClient)

  if (!authFailureHandler) {
    return
  }

  const reason: AuthFailureReason = invalidSession
    ? "session-invalid"
    : "auth-required"

  authFailureHandler(reason)
}

export { queryClient }
