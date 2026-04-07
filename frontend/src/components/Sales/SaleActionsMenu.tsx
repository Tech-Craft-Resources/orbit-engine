import { Link } from "@tanstack/react-router"
import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { SalePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import CancelSale from "./CancelSale"

interface SaleActionsMenuProps {
  sale: SalePublic
}

export const SaleActionsMenu = ({ sale }: SaleActionsMenuProps) => {
  const [open, setOpen] = useState(false)
  const { hasRole } = useAuth()

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem asChild>
          <Link to="/dashboard/sales/$saleId" params={{ saleId: sale.id }}>
            Ver detalles
          </Link>
        </DropdownMenuItem>
        {sale.status === "completed" && hasRole(["admin"]) && (
          <>
            <DropdownMenuSeparator />
            <CancelSale sale={sale} onSuccess={() => setOpen(false)} />
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
