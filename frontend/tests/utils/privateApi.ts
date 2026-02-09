// Note: the `PrivateService` is only available when generating the client
// for local environments
import {
  LoginService,
  OpenAPI,
  OrganizationsService,
  PrivateService,
} from "../../src/client"

OpenAPI.BASE = `${process.env.VITE_API_URL}`

let cachedOrgId: string | null = null

/**
 * Get the default organization ID by logging in as the first superuser
 * and fetching their organization.
 */
async function getDefaultOrgId(): Promise<string> {
  if (cachedOrgId) return cachedOrgId

  const loginResponse = await LoginService.loginAccessToken({
    formData: {
      username: process.env.FIRST_SUPERUSER!,
      password: process.env.FIRST_SUPERUSER_PASSWORD!,
    },
  })

  const previousToken = OpenAPI.TOKEN
  OpenAPI.TOKEN = loginResponse.access_token

  const org = await OrganizationsService.getMyOrganization()
  cachedOrgId = org.id

  // Restore previous token state
  OpenAPI.TOKEN = previousToken

  return cachedOrgId
}

export const createUser = async ({
  email,
  password,
  firstName = "Test",
  lastName = "User",
  organizationId,
  roleId = 3,
}: {
  email: string
  password: string
  firstName?: string
  lastName?: string
  organizationId?: string
  roleId?: number
}) => {
  const orgId = organizationId ?? (await getDefaultOrgId())

  return await PrivateService.createUser({
    requestBody: {
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      organization_id: orgId,
      role_id: roleId,
      is_verified: true,
    },
  })
}
