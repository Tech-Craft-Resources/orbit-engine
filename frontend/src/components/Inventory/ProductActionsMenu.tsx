import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { ProductPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import DeleteProduct from "./DeleteProduct"
import EditProduct from "./EditProduct"
import MovementHistory from "./MovementHistory"
import StockAdjustment from "./StockAdjustment"

interface ProductActionsMenuProps {
  product: ProductPublic
}

export const ProductActionsMenu = ({ product }: ProductActionsMenuProps) => {
  const [open, setOpen] = useState(false)
  const { hasRole } = useAuth()

  const isEditor = hasRole(["admin", "seller"])

  if (!isEditor) {
    return null
  }

  return (
    <DropdownMenu open={open} onOpenChange={setOpen}>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon">
          <EllipsisVertical />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <EditProduct product={product} onSuccess={() => setOpen(false)} />
        <StockAdjustment product={product} onSuccess={() => setOpen(false)} />
        <MovementHistory product={product} />
        {hasRole(["admin"]) && (
          <>
            <DropdownMenuSeparator />
            <DeleteProduct id={product.id} onSuccess={() => setOpen(false)} />
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
