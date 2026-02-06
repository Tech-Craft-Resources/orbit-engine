import { createFileRoute } from "@tanstack/react-router"

import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/dashboard/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard - FastAPI Cloud",
      },
    ],
  }),
})

function Dashboard() {
  const { user: currentUser } = useAuth()

  const displayName = currentUser?.first_name
    ? `${currentUser.first_name} ${currentUser.last_name}`.trim()
    : currentUser?.email

  return (
    <div>
      <div>
        <h1 className="text-2xl truncate max-w-sm">Hi, {displayName} 👋</h1>
        <p className="text-muted-foreground">
          Welcome back, nice to see you again!!!
        </p>
      </div>
    </div>
  )
}
