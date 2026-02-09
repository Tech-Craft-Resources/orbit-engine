import { useQuery } from "@tanstack/react-query"
import { Eye } from "lucide-react"
import { useState } from "react"
import { type SalePublic, SalesService } from "@/client"
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

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

interface SaleDetailProps {
  sale: SalePublic
}

const SaleDetail = ({ sale }: SaleDetailProps) => {
  const [isOpen, setIsOpen] = useState(false)

  const { data: fullSale, isLoading } = useQuery({
    queryKey: ["sale", sale.id],
    queryFn: () => SalesService.readSale({ saleId: sale.id }),
    enabled: isOpen,
  })

  const displaySale = fullSale ?? sale

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => setIsOpen(true)}
      >
        <Eye />
        View Details
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Sale {displaySale.invoice_number}</DialogTitle>
          <DialogDescription>
            {new Date(displaySale.sale_date).toLocaleDateString("en-US", {
              weekday: "long",
              year: "numeric",
              month: "long",
              day: "numeric",
              hour: "2-digit",
              minute: "2-digit",
            })}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-4">
          <div className="flex items-center gap-2">
            <Badge
              variant={
                displaySale.status === "completed" ? "default" : "destructive"
              }
              className="capitalize"
            >
              {displaySale.status}
            </Badge>
            <Badge variant="secondary" className="capitalize">
              {displaySale.payment_method}
            </Badge>
          </div>

          {displaySale.cancellation_reason && (
            <div className="rounded-md bg-destructive/10 p-3 text-sm text-destructive">
              <strong>Cancellation reason:</strong>{" "}
              {displaySale.cancellation_reason}
            </div>
          )}

          {isLoading ? (
            <div className="space-y-2">
              {Array.from({ length: 3 }).map((_, i) => (
                <Skeleton key={i} className="h-8 w-full" />
              ))}
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Product</TableHead>
                  <TableHead className="text-right">Qty</TableHead>
                  <TableHead className="text-right">Unit Price</TableHead>
                  <TableHead className="text-right">Subtotal</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {displaySale.items?.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <div>
                        <span className="font-medium">{item.product_name}</span>
                        <span className="ml-2 text-xs text-muted-foreground font-mono">
                          {item.product_sku}
                        </span>
                      </div>
                    </TableCell>
                    <TableCell className="text-right">
                      {item.quantity}
                    </TableCell>
                    <TableCell className="text-right">
                      {formatCurrency(item.unit_price)}
                    </TableCell>
                    <TableCell className="text-right font-medium">
                      {formatCurrency(item.subtotal)}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}

          <div className="space-y-1 border-t pt-3 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Subtotal</span>
              <span>{formatCurrency(displaySale.subtotal)}</span>
            </div>
            {Number(displaySale.discount) > 0 && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Discount</span>
                <span className="text-destructive">
                  -{formatCurrency(displaySale.discount)}
                </span>
              </div>
            )}
            {Number(displaySale.tax) > 0 && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Tax</span>
                <span>{formatCurrency(displaySale.tax)}</span>
              </div>
            )}
            <div className="flex justify-between font-semibold text-base border-t pt-2">
              <span>Total</span>
              <span>{formatCurrency(displaySale.total)}</span>
            </div>
          </div>

          {displaySale.notes && (
            <div className="text-sm text-muted-foreground">
              <strong>Notes:</strong> {displaySale.notes}
            </div>
          )}
        </div>

        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default SaleDetail
