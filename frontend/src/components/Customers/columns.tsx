import type { ColumnDef } from "@tanstack/react-table"

import type { CustomerPublic } from "@/client"
import { cn } from "@/lib/utils"
import { CustomerActionsMenu } from "./CustomerActionsMenu"

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

export const customerColumns: ColumnDef<CustomerPublic>[] = [
  {
    accessorKey: "first_name",
    header: "Nombre",
    enableSorting: true,
    cell: ({ row }) => {
      const { first_name, last_name } = row.original
      return (
        <span className="font-medium">
          {first_name} {last_name}
        </span>
      )
    },
  },
  {
    accessorKey: "document_number",
    header: "Documento",
    enableSorting: true,
    cell: ({ row }) => (
      <div>
        <span className="text-xs text-muted-foreground uppercase">
          {row.original.document_type}
        </span>{" "}
        <span className="font-mono text-sm">
          {row.original.document_number}
        </span>
      </div>
    ),
  },
  {
    accessorKey: "email",
    header: "Contacto",
    enableSorting: false,
    cell: ({ row }) => (
      <div className="text-sm">
        {row.original.email && (
          <div className="text-muted-foreground">{row.original.email}</div>
        )}
        {row.original.phone && (
          <div className="text-muted-foreground">{row.original.phone}</div>
        )}
        {!row.original.email && !row.original.phone && (
          <span className="text-muted-foreground">-</span>
        )}
      </div>
    ),
  },
  {
    accessorKey: "purchases_count",
    header: "Compras",
    enableSorting: true,
    sortingFn: "alphanumeric",
    cell: ({ row }) => <span>{row.original.purchases_count}</span>,
  },
  {
    accessorKey: "total_purchases",
    header: "Total comprado",
    enableSorting: true,
    sortingFn: "alphanumeric",
    cell: ({ row }) => (
      <span className="font-medium">
        {formatCurrency(row.original.total_purchases)}
      </span>
    ),
  },
  {
    accessorKey: "is_active",
    header: "Estado",
    enableSorting: false,
    filterFn: (row, _columnId, filterValue) =>
      String(row.original.is_active) === filterValue,
    cell: ({ row }) => (
      <div className="flex items-center gap-2">
        <span
          className={cn(
            "size-2 rounded-full",
            row.original.is_active ? "bg-green-500" : "bg-gray-400",
          )}
        />
        <span className={row.original.is_active ? "" : "text-muted-foreground"}>
          {row.original.is_active ? "Activo" : "Inactivo"}
        </span>
      </div>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Acciones</span>,
    enableSorting: false,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <CustomerActionsMenu customer={row.original} />
      </div>
    ),
  },
]
