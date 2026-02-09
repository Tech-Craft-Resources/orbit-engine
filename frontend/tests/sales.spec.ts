import { expect, test } from "@playwright/test"

test.describe("Sales page", () => {
  test("Sales page is accessible and shows correct title", async ({ page }) => {
    await page.goto("/dashboard/sales")

    await expect(page.getByRole("heading", { name: "Sales" })).toBeVisible()
    await expect(
      page.getByText("Manage sales and process transactions"),
    ).toBeVisible()
  })

  test("New Sale button is visible", async ({ page }) => {
    await page.goto("/dashboard/sales")

    await expect(page.getByRole("button", { name: "New Sale" })).toBeVisible()
  })
})

test.describe("Create sale", () => {
  const uniqueSuffix = () => Math.random().toString(36).substring(7)

  test("Create a sale with a product in the cart", async ({ page }) => {
    // First, ensure we have a product in inventory
    await page.goto("/dashboard/inventory")

    const productName = `Sale Product ${uniqueSuffix()}`
    const sku = `SKU-SALE-${uniqueSuffix()}`

    await page.getByRole("button", { name: "Add Product" }).click()
    await page.getByPlaceholder("Product name").fill(productName)
    await page.getByPlaceholder("SKU-001").fill(sku)
    await page.getByLabel("Sale Price").fill("50.00")
    await page.getByLabel("Initial Stock").fill("20")
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Product created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Navigate to sales page
    await page.goto("/dashboard/sales")

    // Open the New Sale dialog
    await page.getByRole("button", { name: "New Sale" }).click()

    // Search for the product
    await page
      .getByPlaceholder("Search by name, SKU, or barcode")
      .fill(productName)

    // Click on the product in search results to add to cart
    await page.getByText(productName).first().click()

    // Verify cart shows the product
    await expect(page.getByText("Cart (1 items)")).toBeVisible()

    // Complete the sale
    await page.getByRole("button", { name: "Complete Sale" }).click()

    await expect(page.getByText("Sale created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()
  })

  test("Cannot complete sale with empty cart", async ({ page }) => {
    await page.goto("/dashboard/sales")

    await page.getByRole("button", { name: "New Sale" }).click()

    // Try to submit with empty cart - button should be disabled
    const completeButton = page.getByRole("button", { name: "Complete Sale" })
    await expect(completeButton).toBeDisabled()
  })

  test("Cancel sale creation", async ({ page }) => {
    await page.goto("/dashboard/sales")

    await page.getByRole("button", { name: "New Sale" }).click()
    await page.getByRole("button", { name: "Cancel" }).click()

    await expect(page.getByRole("dialog")).not.toBeVisible()
  })
})

test.describe("Sale actions", () => {
  const uniqueSuffix = () => Math.random().toString(36).substring(7)

  test("View sale details", async ({ page }) => {
    // Create a product and a sale first
    await page.goto("/dashboard/inventory")

    const productName = `Detail Product ${uniqueSuffix()}`
    const sku = `SKU-DET-${uniqueSuffix()}`

    await page.getByRole("button", { name: "Add Product" }).click()
    await page.getByPlaceholder("Product name").fill(productName)
    await page.getByPlaceholder("SKU-001").fill(sku)
    await page.getByLabel("Sale Price").fill("30.00")
    await page.getByLabel("Initial Stock").fill("50")
    await page.getByRole("button", { name: "Save" }).click()

    await expect(page.getByText("Product created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // Create sale
    await page.goto("/dashboard/sales")
    await page.getByRole("button", { name: "New Sale" }).click()
    await page
      .getByPlaceholder("Search by name, SKU, or barcode")
      .fill(productName)
    await page.getByText(productName).first().click()
    await page.getByRole("button", { name: "Complete Sale" }).click()

    await expect(page.getByText("Sale created successfully")).toBeVisible()
    await expect(page.getByRole("dialog")).not.toBeVisible()

    // View details of the most recent sale
    const saleRow = page.getByRole("row").filter({ hasText: "$30.00" }).first()
    await saleRow.getByRole("button").click()
    await page.getByRole("menuitem", { name: "View Details" }).click()

    // Verify the detail dialog shows
    await expect(page.getByText("Sale Details")).toBeVisible()
  })
})
