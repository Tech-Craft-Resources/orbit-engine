import { expect, test } from "@playwright/test"
import { createUser } from "./utils/privateApi.ts"
import { randomEmail, randomPassword } from "./utils/random.ts"
import { logInUser } from "./utils/user.ts"

const uniqueSuffix = () => Math.random().toString(36).substring(7)

test.describe("Role selector in user management", () => {
  test("Role selector is visible when adding a user", async ({ page }) => {
    await page.goto("/dashboard/admin")
    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await expect(page.getByRole("combobox")).toBeVisible()
  })

  test("Role selector shows all available roles", async ({ page }) => {
    await page.goto("/dashboard/admin")
    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByRole("combobox").click()
    await expect(page.getByRole("option", { name: "Admin" })).toBeVisible()
    await expect(page.getByRole("option", { name: "Seller" })).toBeVisible()
    await expect(page.getByRole("option", { name: "Viewer" })).toBeVisible()
    await expect(page.getByRole("option", { name: "Contador" })).toBeVisible()
  })

  test("Create user with seller role shows Vendedor badge", async ({ page }) => {
    await page.goto("/dashboard/admin")

    const email = randomEmail()
    const password = randomPassword()

    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByPlaceholder("correo@empresa.com").fill(email)
    await page.getByPlaceholder("Nombre").fill("Test")
    await page.getByPlaceholder("Apellido").fill(`Seller${uniqueSuffix()}`)
    await page.getByRole("combobox").click()
    await page.getByRole("option", { name: "Seller" }).click()
    await page.getByPlaceholder("Contrasena", { exact: true }).fill(password)
    await page.getByPlaceholder("Confirmar contrasena").fill(password)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(page.getByText("Usuario creado correctamente")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    const userRow = page.getByRole("row").filter({ hasText: email })
    await expect(userRow.getByText("Vendedor")).toBeVisible()
  })

  test("Create user with admin role shows Administrador badge", async ({
    page,
  }) => {
    await page.goto("/dashboard/admin")

    const email = randomEmail()
    const password = randomPassword()

    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByPlaceholder("correo@empresa.com").fill(email)
    await page.getByPlaceholder("Nombre").fill("Test")
    await page.getByPlaceholder("Apellido").fill(`Admin${uniqueSuffix()}`)
    await page.getByRole("combobox").click()
    await page.getByRole("option", { name: "Admin" }).click()
    await page.getByPlaceholder("Contrasena", { exact: true }).fill(password)
    await page.getByPlaceholder("Confirmar contrasena").fill(password)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(page.getByText("Usuario creado correctamente")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    const userRow = page.getByRole("row").filter({ hasText: email })
    await expect(userRow.getByText("Administrador")).toBeVisible()
  })

  test("Create user with viewer role shows Consulta badge", async ({ page }) => {
    await page.goto("/dashboard/admin")

    const email = randomEmail()
    const password = randomPassword()

    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByPlaceholder("correo@empresa.com").fill(email)
    await page.getByPlaceholder("Nombre").fill("Test")
    await page.getByPlaceholder("Apellido").fill(`Viewer${uniqueSuffix()}`)
    await page.getByRole("combobox").click()
    await page.getByRole("option", { name: "Viewer" }).click()
    await page.getByPlaceholder("Contrasena", { exact: true }).fill(password)
    await page.getByPlaceholder("Confirmar contrasena").fill(password)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(page.getByText("Usuario creado correctamente")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    const userRow = page.getByRole("row").filter({ hasText: email })
    await expect(userRow.getByText("Consulta")).toBeVisible()
  })

  test("Edit user role from Consulta to Administrador", async ({ page }) => {
    await page.goto("/dashboard/admin")

    const email = randomEmail()
    const password = randomPassword()

    // Create a viewer user
    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByPlaceholder("correo@empresa.com").fill(email)
    await page.getByPlaceholder("Nombre").fill("Role")
    await page.getByPlaceholder("Apellido").fill(`Edit${uniqueSuffix()}`)
    await page.getByRole("combobox").click()
    await page.getByRole("option", { name: "Viewer" }).click()
    await page.getByPlaceholder("Contrasena", { exact: true }).fill(password)
    await page.getByPlaceholder("Confirmar contrasena").fill(password)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(page.getByText("Usuario creado correctamente")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Change role to admin
    const userRow = page.getByRole("row").filter({ hasText: email })
    await userRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "Editar usuario" }).click()

    await page.getByRole("combobox").click()
    await page.getByRole("option", { name: "Admin" }).click()
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(
      page.getByText("Usuario actualizado correctamente"),
    ).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    await expect(userRow.getByText("Administrador")).toBeVisible()
  })

  test("Role selector is visible when editing a user", async ({ page }) => {
    await page.goto("/dashboard/admin")

    const email = randomEmail()
    const password = randomPassword()

    // Create a user to edit
    await page.getByRole("button", { name: "Agregar usuario" }).click()
    await page.getByPlaceholder("correo@empresa.com").fill(email)
    await page.getByPlaceholder("Nombre").fill("Test")
    await page.getByPlaceholder("Apellido").fill(`Edit${uniqueSuffix()}`)
    await page.getByPlaceholder("Contrasena", { exact: true }).fill(password)
    await page.getByPlaceholder("Confirmar contrasena").fill(password)
    await page.getByRole("button", { name: "Guardar" }).click()

    await expect(page.getByText("Usuario creado correctamente")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    const userRow = page.getByRole("row").filter({ hasText: email })
    await userRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "Editar usuario" }).click()

    await expect(page.getByRole("combobox")).toBeVisible()
  })
})

test.describe("Role-based access control", () => {
  test.use({ storageState: { cookies: [], origins: [] } })

  test("Admin user can access admin page", async ({ page }) => {
    const email = randomEmail()
    const password = randomPassword()
    await createUser({ email, password, roleId: 1 })
    await logInUser(page, email, password)
    await page.goto("/dashboard/admin")
    await expect(
      page.getByRole("heading", { name: "Usuarios" }),
    ).toBeVisible()
  })

  test("Viewer user cannot access admin page", async ({ page }) => {
    const email = randomEmail()
    const password = randomPassword()
    await createUser({ email, password, roleId: 3 })
    await logInUser(page, email, password)
    await page.goto("/dashboard/admin")
    await expect(
      page.getByRole("heading", { name: "Usuarios" }),
    ).not.toBeVisible()
    await expect(page).not.toHaveURL(/\/dashboard\/admin/)
  })

  test("Seller user cannot access admin page", async ({ page }) => {
    const email = randomEmail()
    const password = randomPassword()
    await createUser({ email, password, roleId: 2 })
    await logInUser(page, email, password)
    await page.goto("/dashboard/admin")
    await expect(
      page.getByRole("heading", { name: "Usuarios" }),
    ).not.toBeVisible()
    await expect(page).not.toHaveURL(/\/dashboard\/admin/)
  })
})
