import type { ColumnDef } from "@tanstack/react-table"

import type { CategoryPublic } from "@/client"
import { cn } from "@/lib/utils"
import { CategoryActionsMenu } from "./CategoryActionsMenu"

export const categoryColumns: ColumnDef<CategoryPublic>[] = [
  {
    accessorKey: "name",
    header: "Nombre",
    enableSorting: true,
    cell: ({ row }) => <span className="font-medium">{row.original.name}</span>,
  },
  {
    accessorKey: "description",
    header: "Descripción",
    enableSorting: false,
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {row.original.description || "—"}
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
    accessorKey: "created_at",
    header: "Creado",
    enableSorting: true,
    sortingFn: "datetime",
    cell: ({ row }) => (
      <span className="text-muted-foreground">
        {new Date(row.original.created_at).toLocaleDateString()}
      </span>
    ),
  },
  {
    id: "actions",
    header: () => <span className="sr-only">Acciones</span>,
    enableSorting: false,
    cell: ({ row }) => (
      <div className="flex justify-end">
        <CategoryActionsMenu category={row.original} />
      </div>
    ),
  },
]
