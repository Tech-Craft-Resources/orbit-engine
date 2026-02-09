import type { ColumnDef } from "@tanstack/react-table"

import type { SalePublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { SaleActionsMenu } from "./SaleActionsMenu"

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

const statusConfig: Record<string, { label: string; color: string }> = {
  completed: { label: "Completed", color: "bg-green-500" },
  cancelled: { label: "Cancelled", color: "bg-red-500" },
  pending: { label: "Pending", color: "bg-yellow-500" },
}

export const saleColumns: ColumnDef<SalePublic>[] = [
  {
    accessorKey: "invoice_number",
    header: "Invoice #",
    cell: ({ row }) => (
      <span className="font-mono text-sm">{row.original.invoice_number}</span>
    ),
  },
  {
    accessorKey: "sale_date",
    header: "Date",
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {formatDate(row.original.sale_date)}
      </span>
    ),
  },
  {
    id: "items_count",
    header: "Items",
    cell: ({ row }) => <span>{row.original.items?.length ?? 0}</span>,
  },
  {
    accessorKey: "total",
    header: "Total",
    cell: ({ row }) => (
      <span className="font-semibold">
        {formatCurrency(row.original.total)}
      </span>
    ),
  },
  {
    accessorKey: "payment_method",
    header: "Payment",
    cell: ({ row }) => (
      <Badge variant="secondary" className="capitalize">
        {row.original.payment_method}
      </Badge>
    ),
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => {
      const status = row.original.status
      const config = statusConfig[status] ?? {
        label: status,
        color: "bg-gray-400",
      }
      return (
        <div className="flex items-center gap-2">
          <span className={cn("size-2 rounded-full", config.color)} />
          <span
            className={
              status === "cancelled" ? "text-muted-foreground" : undefined
            }
          >
            {config.label}
          </span>
        </div>
      )
    },
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Actions</span>,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <SaleActionsMenu sale={row.original} />
      </div>
    ),
  },
]
