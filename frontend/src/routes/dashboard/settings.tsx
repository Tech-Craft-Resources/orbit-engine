import { createFileRoute } from "@tanstack/react-router"
import { type ComponentType, useMemo } from "react"

import ChangePassword from "@/components/UserSettings/ChangePassword"
import DeleteAccount from "@/components/UserSettings/DeleteAccount"
import OrganizationSettings from "@/components/UserSettings/OrganizationSettings"
import UserInformation from "@/components/UserSettings/UserInformation"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import useAuth, { type RoleName } from "@/hooks/useAuth"

interface TabConfig {
  value: string
  title: string
  component: ComponentType
  roles?: RoleName[]
}

const tabsConfig: TabConfig[] = [
  { value: "my-profile", title: "My profile", component: UserInformation },
  { value: "password", title: "Password", component: ChangePassword },
  {
    value: "organization",
    title: "Organization",
    component: OrganizationSettings,
    roles: ["admin"],
  },
  { value: "danger-zone", title: "Danger zone", component: DeleteAccount },
]

export const Route = createFileRoute("/dashboard/settings")({
  component: UserSettings,
  head: () => ({
    meta: [
      {
        title: "Settings - FastAPI Cloud",
      },
    ],
  }),
})

function UserSettings() {
  const { user: currentUser, hasRole } = useAuth()

  const finalTabs = useMemo(
    () => tabsConfig.filter((tab) => !tab.roles || hasRole(tab.roles)),
    [hasRole],
  )

  if (!currentUser) {
    return null
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">User Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences
        </p>
      </div>

      <Tabs defaultValue="my-profile">
        <TabsList>
          {finalTabs.map((tab) => (
            <TabsTrigger key={tab.value} value={tab.value}>
              {tab.title}
            </TabsTrigger>
          ))}
        </TabsList>
        {finalTabs.map((tab) => (
          <TabsContent key={tab.value} value={tab.value}>
            <tab.component />
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}
