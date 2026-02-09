import { useQuery } from "@tanstack/react-query"
import { ArrowDownUp } from "lucide-react"
import { useState } from "react"
import { type ProductPublic, ProductsService } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { DropdownMenuItem } from "@/components/ui/dropdown-menu"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

const movementTypeStyles: Record<
  string,
  {
    label: string
    variant: "default" | "secondary" | "destructive" | "outline"
  }
> = {
  sale: { label: "Sale", variant: "destructive" },
  purchase: { label: "Purchase", variant: "default" },
  adjustment: { label: "Adjustment", variant: "secondary" },
  return: { label: "Return", variant: "outline" },
}

interface MovementHistoryProps {
  product: ProductPublic
}

const MovementHistory = ({ product }: MovementHistoryProps) => {
  const [isOpen, setIsOpen] = useState(false)

  const { data: movements, isLoading } = useQuery({
    queryKey: ["product-movements", product.id],
    queryFn: () =>
      ProductsService.readProductMovements({
        productId: product.id,
        skip: 0,
        limit: 100,
      }),
    enabled: isOpen,
  })

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => setIsOpen(true)}
      >
        <ArrowDownUp />
        Movement History
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Movement History</DialogTitle>
          <DialogDescription>
            Stock movements for <strong>{product.name}</strong>
          </DialogDescription>
        </DialogHeader>

        <div className="max-h-80 overflow-y-auto">
          {isLoading ? (
            <div className="space-y-2">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={i} className="h-8 w-full" />
              ))}
            </div>
          ) : movements?.data && movements.data.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Date</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead className="text-right">Qty</TableHead>
                  <TableHead className="text-right">Stock</TableHead>
                  <TableHead>Reason</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {movements.data.map((movement) => {
                  const style = movementTypeStyles[movement.movement_type] ?? {
                    label: movement.movement_type,
                    variant: "secondary" as const,
                  }
                  return (
                    <TableRow key={movement.id}>
                      <TableCell className="text-xs text-muted-foreground whitespace-nowrap">
                        {new Date(movement.created_at).toLocaleDateString(
                          "en-US",
                          {
                            month: "short",
                            day: "numeric",
                            hour: "2-digit",
                            minute: "2-digit",
                          },
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={style.variant}
                          className="capitalize text-xs"
                        >
                          {style.label}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-right font-mono">
                        <span
                          className={
                            movement.quantity > 0
                              ? "text-green-600"
                              : "text-destructive"
                          }
                        >
                          {movement.quantity > 0 ? "+" : ""}
                          {movement.quantity}
                        </span>
                      </TableCell>
                      <TableCell className="text-right text-xs text-muted-foreground">
                        {movement.previous_stock} → {movement.new_stock}
                      </TableCell>
                      <TableCell className="text-xs max-w-[120px] truncate">
                        {movement.reason ?? "—"}
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          ) : (
            <p className="text-sm text-muted-foreground text-center py-8">
              No movements recorded for this product
            </p>
          )}
        </div>

        {movements?.count != null && movements.count > 0 && (
          <p className="text-xs text-muted-foreground text-right">
            Showing {movements.data.length} of {movements.count} movements
          </p>
        )}

        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default MovementHistory
