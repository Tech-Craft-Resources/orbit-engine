import { expect, test } from "@playwright/test"

test.describe("Customers page", () => {
  test("Customers page is accessible and shows correct title", async ({
    page,
  }) => {
    await page.goto("/dashboard/customers")

    await expect(page.getByRole("heading", { name: "Customers" })).toBeVisible()
    await expect(page.getByText("Manage your customer database")).toBeVisible()
  })

  test("Add Customer button is visible", async ({ page }) => {
    await page.goto("/dashboard/customers")

    await expect(
      page.getByRole("button", { name: "Add Customer" }),
    ).toBeVisible()
  })
})

test.describe("Customer CRUD", () => {
  const uniqueSuffix = () => Math.random().toString(36).substring(7)

  test("Create a new customer successfully", async ({ page }) => {
    await page.goto("/dashboard/customers")

    const firstName = `Test${uniqueSuffix()}`
    const lastName = `Customer${uniqueSuffix()}`
    const docNumber = `DOC-${uniqueSuffix()}`

    await page.getByRole("button", { name: "Add Customer" }).click()

    await page.getByPlaceholder("Document number").fill(docNumber)
    await page.getByPlaceholder("First name").fill(firstName)
    await page.getByPlaceholder("Last name").fill(lastName)
    await page
      .getByPlaceholder("email@example.com")
      .fill(`${firstName}@test.com`)
    await page.getByPlaceholder("+1234567890").fill("+1234567890")

    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Customer created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Verify customer appears in the table
    await expect(
      page.getByRole("row").filter({ hasText: docNumber }),
    ).toBeVisible()
  })

  test("Document number is required", async ({ page }) => {
    await page.goto("/dashboard/customers")

    await page.getByRole("button", { name: "Add Customer" }).click()

    await page.getByPlaceholder("First name").fill("John")
    await page.getByPlaceholder("Last name").fill("Doe")
    // Leave document number empty
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Document number is required")).toBeVisible()
  })

  test("First name is required", async ({ page }) => {
    await page.goto("/dashboard/customers")

    await page.getByRole("button", { name: "Add Customer" }).click()

    await page.getByPlaceholder("Document number").fill("123456")
    await page.getByPlaceholder("Last name").fill("Doe")
    // Leave first name empty
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("First name is required")).toBeVisible()
  })

  test("Last name is required", async ({ page }) => {
    await page.goto("/dashboard/customers")

    await page.getByRole("button", { name: "Add Customer" }).click()

    await page.getByPlaceholder("Document number").fill("123456")
    await page.getByPlaceholder("First name").fill("John")
    // Leave last name empty
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Last name is required")).toBeVisible()
  })

  test("Cancel customer creation", async ({ page }) => {
    await page.goto("/dashboard/customers")

    await page.getByRole("button", { name: "Add Customer" }).click()
    await page.getByPlaceholder("First name").fill("To be cancelled")
    await page.getByRole("button", { name: "Cancel" }).click()

    await expect(page.getByRole("dialog")).not.toBeVisible()
  })

  test("Edit a customer successfully", async ({ page }) => {
    await page.goto("/dashboard/customers")

    const firstName = `Edit${uniqueSuffix()}`
    const lastName = `Cust${uniqueSuffix()}`
    const docNumber = `DOC-${uniqueSuffix()}`
    const updatedFirstName = `Updated${uniqueSuffix()}`

    // Create customer first
    await page.getByRole("button", { name: "Add Customer" }).click()
    await page.getByPlaceholder("Document number").fill(docNumber)
    await page.getByPlaceholder("First name").fill(firstName)
    await page.getByPlaceholder("Last name").fill(lastName)
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Customer created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Edit the customer
    const customerRow = page.getByRole("row").filter({ hasText: docNumber })
    await customerRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "Edit" }).click()

    await page.getByLabel("First Name").fill(updatedFirstName)
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Customer updated successfully")).toBeVisible()
    await expect(page.getByText(updatedFirstName)).toBeVisible()
  })

  test("Delete a customer successfully", async ({ page }) => {
    await page.goto("/dashboard/customers")

    const firstName = `Del${uniqueSuffix()}`
    const lastName = `Cust${uniqueSuffix()}`
    const docNumber = `DOC-${uniqueSuffix()}`

    // Create customer first
    await page.getByRole("button", { name: "Add Customer" }).click()
    await page.getByPlaceholder("Document number").fill(docNumber)
    await page.getByPlaceholder("First name").fill(firstName)
    await page.getByPlaceholder("Last name").fill(lastName)
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Customer created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Delete
    const customerRow = page.getByRole("row").filter({ hasText: docNumber })
    await customerRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "Delete" }).click()
    await page.getByRole("button", { name: "Delete" }).click()

    await expect(page.getByText("Customer deleted successfully")).toBeVisible()

    await expect(
      page.getByRole("row").filter({ hasText: docNumber }),
    ).not.toBeVisible()
  })
})

test.describe("Customer purchase history", () => {
  const uniqueSuffix = () => Math.random().toString(36).substring(7)

  test("View purchase history for a customer", async ({ page }) => {
    await page.goto("/dashboard/customers")

    const firstName = `History${uniqueSuffix()}`
    const lastName = `Cust${uniqueSuffix()}`
    const docNumber = `DOC-${uniqueSuffix()}`

    // Create customer
    await page.getByRole("button", { name: "Add Customer" }).click()
    await page.getByPlaceholder("Document number").fill(docNumber)
    await page.getByPlaceholder("First name").fill(firstName)
    await page.getByPlaceholder("Last name").fill(lastName)
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Customer created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Open purchase history
    const customerRow = page.getByRole("row").filter({ hasText: docNumber })
    await customerRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "Purchase History" }).click()

    // Verify the dialog shows
    await expect(page.getByText("Purchase History")).toBeVisible()
  })
})
