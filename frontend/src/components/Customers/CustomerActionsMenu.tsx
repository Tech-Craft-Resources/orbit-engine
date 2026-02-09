import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { CustomerPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import CustomerSalesHistory from "./CustomerSalesHistory"
import DeleteCustomer from "./DeleteCustomer"
import EditCustomer from "./EditCustomer"

interface CustomerActionsMenuProps {
  customer: CustomerPublic
}

export const CustomerActionsMenu = ({ customer }: CustomerActionsMenuProps) => {
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
        <CustomerSalesHistory customer={customer} />
        <EditCustomer customer={customer} onSuccess={() => setOpen(false)} />
        {hasRole(["admin"]) && (
          <>
            <DropdownMenuSeparator />
            <DeleteCustomer
              id={customer.id}
              name={`${customer.first_name} ${customer.last_name}`}
              onSuccess={() => setOpen(false)}
            />
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
