import { EllipsisVertical } from "lucide-react"
import { useState } from "react"

import type { CategoryPublic } from "@/client"
import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import useAuth from "@/hooks/useAuth"
import DeleteCategory from "./DeleteCategory"
import EditCategory from "./EditCategory"

interface CategoryActionsMenuProps {
  category: CategoryPublic
}

export const CategoryActionsMenu = ({ category }: CategoryActionsMenuProps) => {
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
        <EditCategory category={category} onSuccess={() => setOpen(false)} />
        {hasRole(["admin"]) && (
          <>
            <DropdownMenuSeparator />
            <DeleteCategory id={category.id} onSuccess={() => setOpen(false)} />
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  )
}
