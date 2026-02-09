import { expect, type Page, test } from "@playwright/test"

import { randomEmail, randomPassword, randomTeamName } from "./utils/random"

test.use({ storageState: { cookies: [], origins: [] } })

const fillOrgSignupForm = async (
  page: Page,
  {
    orgName,
    orgSlug,
    orgDescription,
    firstName,
    lastName,
    email,
    password,
    confirmPassword,
  }: {
    orgName: string
    orgSlug?: string
    orgDescription?: string
    firstName: string
    lastName: string
    email: string
    password: string
    confirmPassword: string
  },
) => {
  await page.getByTestId("org-name-input").fill(orgName)
  if (orgSlug) {
    await page.getByTestId("org-slug-input").fill(orgSlug)
  }
  if (orgDescription) {
    await page.getByTestId("org-description-input").fill(orgDescription)
  }
  await page.getByTestId("first-name-input").fill(firstName)
  await page.getByTestId("last-name-input").fill(lastName)
  await page.getByTestId("email-input").fill(email)
  await page.getByTestId("password-input").fill(password)
  await page.getByTestId("confirm-password-input").fill(confirmPassword)
}

test("Organization signup page is accessible", async ({ page }) => {
  await page.goto("/signup-org")

  await expect(
    page.getByRole("heading", { name: "Create your organization" }),
  ).toBeVisible()
  await expect(
    page.getByText("Set up your organization and admin account"),
  ).toBeVisible()
})

test("Create Organization button is visible", async ({ page }) => {
  await page.goto("/signup-org")

  await expect(
    page.getByRole("button", { name: "Create Organization" }),
  ).toBeVisible()
})

test("Log in link is visible", async ({ page }) => {
  await page.goto("/signup-org")

  await expect(page.getByRole("link", { name: "Log in" })).toBeVisible()
})

test("Signup with valid organization data", async ({ page }) => {
  const orgName = randomTeamName()
  const email = randomEmail()
  const password = randomPassword()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName,
    firstName: "Test",
    lastName: "Admin",
    email,
    password,
    confirmPassword: password,
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  // Should redirect to dashboard after successful signup
  await page.waitForURL(/\/dashboard/)
  await expect(
    page.getByText("Organization created successfully"),
  ).toBeVisible()
})

test("Auto-generates slug from organization name", async ({ page }) => {
  const orgName = "My Test Company"

  await page.goto("/signup-org")

  await page.getByTestId("org-name-input").fill(orgName)

  const slugInput = page.getByTestId("org-slug-input")
  await expect(slugInput).toHaveValue("my-test-company")
})

test("Signup with missing organization name shows error", async ({ page }) => {
  const email = randomEmail()
  const password = randomPassword()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName: "",
    firstName: "Test",
    lastName: "Admin",
    email,
    password,
    confirmPassword: password,
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  await expect(
    page.getByText("Organization name must be at least 2 characters"),
  ).toBeVisible()
})

test("Signup with missing first name shows error", async ({ page }) => {
  const orgName = randomTeamName()
  const email = randomEmail()
  const password = randomPassword()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName,
    firstName: "",
    lastName: "Admin",
    email,
    password,
    confirmPassword: password,
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  await expect(page.getByText("First name is required")).toBeVisible()
})

test("Signup with invalid email shows error", async ({ page }) => {
  const orgName = randomTeamName()
  const password = randomPassword()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName,
    firstName: "Test",
    lastName: "Admin",
    email: "invalid-email",
    password,
    confirmPassword: password,
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  await expect(page.getByText("Please enter a valid email")).toBeVisible()
})

test("Signup with weak password shows error", async ({ page }) => {
  const orgName = randomTeamName()
  const email = randomEmail()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName,
    firstName: "Test",
    lastName: "Admin",
    email,
    password: "short",
    confirmPassword: "short",
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  await expect(
    page.getByText("Password must be at least 8 characters"),
  ).toBeVisible()
})

test("Signup with mismatched passwords shows error", async ({ page }) => {
  const orgName = randomTeamName()
  const email = randomEmail()

  await page.goto("/signup-org")

  await fillOrgSignupForm(page, {
    orgName,
    firstName: "Test",
    lastName: "Admin",
    email,
    password: randomPassword(),
    confirmPassword: randomPassword(),
  })

  await page.getByRole("button", { name: "Create Organization" }).click()

  await expect(page.getByText("Passwords don't match")).toBeVisible()
})

test("/signup redirects to /signup-org", async ({ page }) => {
  await page.goto("/signup")

  await page.waitForURL(/\/signup-org/)
  await expect(page).toHaveURL(/\/signup-org/)
})
