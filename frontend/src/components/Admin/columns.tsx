import type { ColumnDef } from "@tanstack/react-table"

import type { UserPublic } from "@/client"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { UserActionsMenu } from "./UserActionsMenu"

export type UserTableData = UserPublic & {
  isCurrentUser: boolean
}

export const columns: ColumnDef<UserTableData>[] = [
  {
    accessorKey: "first_name",
    header: "Nombre",
    cell: ({ row }) => {
      const firstName = row.original.first_name
      const lastName = row.original.last_name
      const fullName = `${firstName} ${lastName}`.trim()
      return (
        <div className="flex items-center gap-2">
          <span className={cn("font-medium")}>
            {fullName || "No disponible"}
          </span>
          {row.original.isCurrentUser && (
            <Badge variant="outline" className="text-xs">
              Tu
            </Badge>
          )}
        </div>
      )
    },
  },
  {
    accessorKey: "email",
    header: "Correo electronico",
    cell: ({ row }) => (
      <span className="text-muted-foreground">{row.original.email}</span>
    ),
  },
  {
    accessorKey: "role_id",
    header: "Rol",
    cell: ({ row }) => {
      const roleNames = {
        1: "Administrador",
        2: "Vendedor",
        3: "Consulta",
      } as const
      const roleId = row.original.role_id as 1 | 2 | 3
      const roleName = roleNames[roleId] || "Desconocido"
      return (
        <Badge variant={roleId === 1 ? "default" : "secondary"}>
          {roleName}
        </Badge>
      )
    },
  },
  {
    accessorKey: "is_active",
    header: "Estado",
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
    cell: ({ row }) => (
      <div className="flex justify-end">
        <UserActionsMenu user={row.original} />
      </div>
    ),
  },
]
