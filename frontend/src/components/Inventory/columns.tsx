import type { ColumnDef } from "@tanstack/react-table"

import type { CategoryPublic, ProductPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { ProductActionsMenu } from "./ProductActionsMenu"

export type ProductTableData = ProductPublic & {
  categoryName?: string
}

export function buildProductColumns(
  categories: CategoryPublic[],
): ColumnDef<ProductTableData>[] {
  const categoryMap = new Map(categories.map((c) => [c.id, c.name]))

  return [
    {
      accessorKey: "sku",
      header: "SKU",
      cell: ({ row }) => (
        <span className="font-mono text-sm">{row.original.sku}</span>
      ),
    },
    {
      accessorKey: "name",
      header: "Name",
      cell: ({ row }) => (
        <span className="font-medium">{row.original.name}</span>
      ),
    },
    {
      accessorKey: "category_id",
      header: "Category",
      cell: ({ row }) => {
        const catId = row.original.category_id
        const catName = catId ? categoryMap.get(catId) : null
        return <span className="text-muted-foreground">{catName ?? "—"}</span>
      },
    },
    {
      accessorKey: "stock_quantity",
      header: "Stock",
      cell: ({ row }) => {
        const qty = row.original.stock_quantity ?? 0
        const min = row.original.stock_min ?? 0
        const isLow = qty <= min
        return (
          <div className="flex items-center gap-2">
            <span className={cn(isLow && "text-destructive font-medium")}>
              {qty}
            </span>
            {isLow && (
              <Badge variant="destructive" className="text-xs">
                Low
              </Badge>
            )}
          </div>
        )
      },
    },
    {
      accessorKey: "sale_price",
      header: "Sale Price",
      cell: ({ row }) => {
        const price = row.original.sale_price
        return (
          <span className="text-muted-foreground">
            {price ? `$${Number(price).toFixed(2)}` : "—"}
          </span>
        )
      },
    },
    {
      accessorKey: "is_active",
      header: "Status",
      cell: ({ row }) => (
        <div className="flex items-center gap-2">
          <span
            className={cn(
              "size-2 rounded-full",
              row.original.is_active ? "bg-green-500" : "bg-gray-400",
            )}
          />
          <span
            className={row.original.is_active ? "" : "text-muted-foreground"}
          >
            {row.original.is_active ? "Active" : "Inactive"}
          </span>
        </div>
      ),
    },
    {
      id: "actions",
      header: () => <span className="sr-only">Actions</span>,
      cell: ({ row }) => (
        <div className="flex justify-end">
          <ProductActionsMenu product={row.original} />
        </div>
      ),
    },
  ]
}
