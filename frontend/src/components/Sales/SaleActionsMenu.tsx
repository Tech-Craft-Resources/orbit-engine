import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { SalePublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import CancelSale from "./CancelSale"
import SaleDetail from "./SaleDetail"

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
        <SaleDetail sale={sale} />
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
