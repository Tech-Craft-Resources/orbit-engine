import type { ColumnDef } from "@tanstack/react-table"

import type { SalePublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { SaleActionsMenu } from "./SaleActionsMenu"

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

function formatDate(value: string): string {
  return new Date(value).toLocaleDateString("es-ES", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

const statusConfig: Record<string, { label: string; color: string }> = {
  completed: { label: "Completada", color: "bg-green-500" },
  cancelled: { label: "Cancelada", color: "bg-red-500" },
  pending: { label: "Pendiente", color: "bg-yellow-500" },
}

const paymentMethodLabels: Record<string, string> = {
  cash: "Efectivo",
  card: "Tarjeta",
  transfer: "Transferencia",
  other: "Otro",
}

export const saleColumns: ColumnDef<SalePublic>[] = [
  {
    accessorKey: "invoice_number",
    header: "Factura #",
    enableSorting: true,
    cell: ({ row }) => (
      <span className="font-mono text-sm">{row.original.invoice_number}</span>
    ),
  },
  {
    accessorKey: "sale_date",
    header: "Fecha",
    enableSorting: true,
    sortingFn: "datetime",
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {formatDate(row.original.sale_date)}
      </span>
    ),
  },
  {
    id: "items_count",
    header: "Productos",
    enableSorting: false,
    cell: ({ row }) => <span>{row.original.items?.length ?? 0}</span>,
  },
  {
    accessorKey: "total",
    header: "Total",
    enableSorting: true,
    sortingFn: "alphanumeric",
    cell: ({ row }) => (
      <span className="font-semibold">
        {formatCurrency(row.original.total)}
      </span>
    ),
  },
  {
    accessorKey: "payment_method",
    header: "Pago",
    enableSorting: false,
    filterFn: (row, _columnId, filterValue) =>
      row.original.payment_method === filterValue,
    cell: ({ row }) => (
      <Badge variant="secondary" className="capitalize">
        {paymentMethodLabels[row.original.payment_method] ??
          row.original.payment_method}
      </Badge>
    ),
  },
  {
    accessorKey: "status",
    header: "Estado",
    enableSorting: false,
    filterFn: (row, _columnId, filterValue) =>
      row.original.status === filterValue,
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
    header: () => <span className="sr-only">Acciones</span>,
    enableSorting: false,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <SaleActionsMenu sale={row.original} />
      </div>
    ),
  },
]
