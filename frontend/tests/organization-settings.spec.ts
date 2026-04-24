import { expect, test } from "@playwright/test"
import { createUser } from "./utils/privateApi.ts"
import { randomEmail, randomPassword } from "./utils/random.ts"
import { logInUser } from "./utils/user.ts"

const uniqueSuffix = () => Math.random().toString(36).substring(7)

test.describe("Organization tab visibility", () => {
  test("Organization tab is visible for admin users", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await expect(
      page.getByRole("tab", { name: "Organización" }),
    ).toBeVisible()
  })

  test.describe("Non-admin users", () => {
    test.use({ storageState: { cookies: [], origins: [] } })

    test("Organization tab is not visible for viewer users", async ({
      page,
    }) => {
      const email = randomEmail()
      const password = randomPassword()
      await createUser({ email, password, roleId: 3 })
      await logInUser(page, email, password)
      await page.goto("/dashboard/settings")
      await expect(
        page.getByRole("tab", { name: "Organización" }),
      ).not.toBeVisible()
    })

    test("Organization tab is not visible for seller users", async ({
      page,
    }) => {
      const email = randomEmail()
      const password = randomPassword()
      await createUser({ email, password, roleId: 2 })
      await logInUser(page, email, password)
      await page.goto("/dashboard/settings")
      await expect(
        page.getByRole("tab", { name: "Organización" }),
      ).not.toBeVisible()
    })
  })
})

test.describe("Organization settings content", () => {
  test("Organization settings heading is visible", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await expect(
      page.getByText("Configuracion de organizacion"),
    ).toBeVisible()
  })

  test("Edit button is visible in view mode", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await expect(page.getByRole("button", { name: "Editar" })).toBeVisible()
  })

  test("Edit mode shows Guardar and Cancelar buttons", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()
    await expect(page.getByRole("button", { name: "Guardar" })).toBeVisible()
    await expect(page.getByRole("button", { name: "Cancelar" })).toBeVisible()
  })

  test("Cancel edit restores view mode", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()
    await page.getByRole("button", { name: "Cancelar" }).click()
    await expect(page.getByRole("button", { name: "Editar" })).toBeVisible()
    await expect(
      page.getByRole("button", { name: "Guardar" }),
    ).not.toBeVisible()
  })
})

test.describe("Update organization", () => {
  test("Update organization name successfully", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()

    const newName = `Org Test ${uniqueSuffix()}`
    await page.getByLabel("Nombre de la organizacion").fill(newName)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(
      page.getByText("Organizacion actualizada correctamente"),
    ).toBeVisible()
  })

  test("Update organization description successfully", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()

    const description = `Descripcion de prueba ${uniqueSuffix()}`
    await page
      .getByPlaceholder("Breve descripcion de tu organizacion")
      .fill(description)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(
      page.getByText("Organizacion actualizada correctamente"),
    ).toBeVisible()
  })

  test("Update logo URL successfully", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()

    await page
      .getByPlaceholder("https://example.com/logo.png")
      .fill("https://example.com/logo-test.png")
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(
      page.getByText("Organizacion actualizada correctamente"),
    ).toBeVisible()
  })
})

test.describe("Organization settings validation", () => {
  test("Organization name cannot be empty", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()

    await page.getByLabel("Nombre de la organizacion").fill("")
    await page.getByLabel("Nombre de la organizacion").blur()

    await expect(
      page.getByText("El nombre de la organizacion es obligatorio"),
    ).toBeVisible()
  })

  test("Invalid logo URL shows validation error", async ({ page }) => {
    await page.goto("/dashboard/settings")
    await page.getByRole("tab", { name: "Organización" }).click()
    await page.getByRole("button", { name: "Editar" }).click()

    await page
      .getByPlaceholder("https://example.com/logo.png")
      .fill("no-es-una-url")
    await page.getByLabel("Nombre de la organizacion").click()

    await expect(page.getByText("Ingresa una URL valida")).toBeVisible()
  })
})
