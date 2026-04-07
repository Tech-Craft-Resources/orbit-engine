import { useQuery } from "@tanstack/react-query"
import { ShoppingCart } from "lucide-react"
import { useState } from "react"
import { type CustomerPublic, CustomersService } from "@/client"
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

const statusStyles: Record<
  string,
  { variant: "default" | "destructive" | "secondary"; label: string }
> = {
  completed: { variant: "default", label: "Completada" },
  cancelled: { variant: "destructive", label: "Cancelada" },
  pending: { variant: "secondary", label: "Pendiente" },
}

interface CustomerSalesHistoryProps {
  customer: CustomerPublic
}

const CustomerSalesHistory = ({ customer }: CustomerSalesHistoryProps) => {
  const [isOpen, setIsOpen] = useState(false)

  const { data: sales, isLoading } = useQuery({
    queryKey: ["customer-sales", customer.id],
    queryFn: () =>
      CustomersService.readCustomerSales({
        customerId: customer.id,
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
        <ShoppingCart />
        Historial de compras
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle>Historial de compras</DialogTitle>
          <DialogDescription>
            Ventas de{" "}
            <strong>
              {customer.first_name} {customer.last_name}
            </strong>
          </DialogDescription>
        </DialogHeader>

        <div className="max-h-80 overflow-y-auto">
          {isLoading ? (
            <div className="space-y-2">
              {Array.from({ length: 5 }).map((_, i) => (
                <Skeleton key={i} className="h-8 w-full" />
              ))}
            </div>
          ) : sales?.data && sales.data.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Factura #</TableHead>
                  <TableHead>Fecha</TableHead>
                  <TableHead className="text-right">Productos</TableHead>
                  <TableHead className="text-right">Total</TableHead>
                  <TableHead>Estado</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {sales.data.map((sale) => {
                  const style = statusStyles[sale.status] ?? {
                    variant: "secondary" as const,
                    label: sale.status,
                  }
                  return (
                    <TableRow key={sale.id}>
                      <TableCell className="font-mono text-xs">
                        {sale.invoice_number}
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground whitespace-nowrap">
                        {new Date(sale.sale_date).toLocaleDateString("es-ES", {
                          month: "short",
                          day: "numeric",
                          year: "numeric",
                        })}
                      </TableCell>
                      <TableCell className="text-right">
                        {sale.items?.length ?? "—"}
                      </TableCell>
                      <TableCell className="text-right font-medium">
                        {formatCurrency(sale.total)}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={style.variant}
                          className="capitalize text-xs"
                        >
                          {style.label}
                        </Badge>
                      </TableCell>
                    </TableRow>
                  )
                })}
              </TableBody>
            </Table>
          ) : (
            <p className="text-sm text-muted-foreground text-center py-8">
              Este cliente no tiene compras registradas
            </p>
          )}
        </div>

        {sales?.count != null && sales.count > 0 && (
          <p className="text-xs text-muted-foreground text-right">
            Mostrando {sales.data.length} de {sales.count} compras
          </p>
        )}

        <DialogFooter>
          <DialogClose asChild>
            <Button variant="outline">Cerrar</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default CustomerSalesHistory
