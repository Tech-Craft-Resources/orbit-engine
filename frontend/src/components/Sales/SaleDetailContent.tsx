import { useQuery } from "@tanstack/react-query"
import type { SalePublic } from "@/client"
import { CustomersService } from "@/client"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Table,
  TableBody,
  TableCaption,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

function formatSaleDate(value: string): string {
  return new Date(value).toLocaleDateString("es-ES", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

function formatOptionalDate(value: string | null | undefined): string {
  if (!value) {
    return "No disponible"
  }

  return new Date(value).toLocaleDateString("es-ES", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

const statusLabels: Record<string, string> = {
  completed: "Completada",
  cancelled: "Cancelada",
  pending: "Pendiente",
}

const paymentMethodLabels: Record<string, string> = {
  cash: "Efectivo",
  card: "Tarjeta",
  transfer: "Transferencia",
  other: "Otro",
}

interface SaleDetailContentProps {
  sale: SalePublic
  isLoading?: boolean
}

const SaleDetailContent = ({
  sale,
  isLoading = false,
}: SaleDetailContentProps) => {
  const hasIdentifiedCustomer = Boolean(sale.customer_id)

  const { data: customer, isLoading: isLoadingCustomer } = useQuery({
    queryKey: ["customer", sale.customer_id],
    queryFn: () =>
      CustomersService.readCustomer({ customerId: sale.customer_id as string }),
    enabled: hasIdentifiedCustomer,
  })

  return (
    <div className="space-y-6">
      <div className="grid gap-6 lg:grid-cols-2">
        <section className="rounded-lg border bg-card p-5">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-muted-foreground">
            Informacion general
          </h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2">
            <div>
              <p className="text-xs text-muted-foreground">Fecha de venta</p>
              <p className="mt-1 text-sm font-medium">
                {formatSaleDate(sale.sale_date)}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Metodo de pago</p>
              <div className="mt-1">
                <Badge variant="secondary" className="capitalize">
                  {paymentMethodLabels[sale.payment_method] ??
                    sale.payment_method}
                </Badge>
              </div>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Estado</p>
              <div className="mt-1">
                <Badge
                  variant={
                    sale.status === "completed" ? "default" : "destructive"
                  }
                  className="capitalize"
                >
                  {statusLabels[sale.status] ?? sale.status}
                </Badge>
              </div>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Items</p>
              <p className="mt-1 text-sm font-medium">
                {sale.items?.length ?? 0}
              </p>
            </div>
            <div className="sm:col-span-2">
              <p className="text-xs text-muted-foreground">Cliente</p>
              {!hasIdentifiedCustomer ? (
                <div className="mt-1">
                  <Badge variant="secondary">Cliente ocasional</Badge>
                </div>
              ) : isLoadingCustomer ? (
                <p className="mt-1 text-sm text-muted-foreground">
                  Cargando informacion del cliente...
                </p>
              ) : customer ? (
                <div className="mt-1 space-y-1">
                  <p className="text-sm font-medium">
                    {customer.first_name} {customer.last_name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {customer.document_type.toUpperCase()}{" "}
                    {customer.document_number}
                    {customer.phone ? ` · ${customer.phone}` : ""}
                  </p>
                  <Dialog>
                    <DialogTrigger asChild>
                      <Button
                        type="button"
                        variant="link"
                        className="h-auto px-0 py-0 text-xs"
                      >
                        Ver informacion del cliente
                      </Button>
                    </DialogTrigger>
                    <DialogContent className="sm:max-w-md">
                      <DialogHeader>
                        <DialogTitle>
                          {customer.first_name} {customer.last_name}
                        </DialogTitle>
                        <DialogDescription>
                          Detalles de contacto y actividad del cliente asociado
                          a esta venta.
                        </DialogDescription>
                      </DialogHeader>
                      <div className="grid gap-3 text-sm">
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Documento
                          </p>
                          <p className="font-medium">
                            {customer.document_type.toUpperCase()}{" "}
                            {customer.document_number}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Correo electronico
                          </p>
                          <p className="font-medium">
                            {customer.email || "No disponible"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Telefono
                          </p>
                          <p className="font-medium">
                            {customer.phone || "No disponible"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Direccion
                          </p>
                          <p className="font-medium">
                            {customer.address || "No disponible"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Ciudad / Pais
                          </p>
                          <p className="font-medium">
                            {[customer.city, customer.country]
                              .filter(Boolean)
                              .join(" / ") || "No disponible"}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Compras registradas
                          </p>
                          <p className="font-medium">
                            {customer.purchases_count} venta(s) ·{" "}
                            {formatCurrency(customer.total_purchases)}
                          </p>
                        </div>
                        <div>
                          <p className="text-xs text-muted-foreground">
                            Ultima compra
                          </p>
                          <p className="font-medium">
                            {formatOptionalDate(customer.last_purchase_at)}
                          </p>
                        </div>
                      </div>
                    </DialogContent>
                  </Dialog>
                </div>
              ) : (
                <p className="mt-1 text-sm text-muted-foreground">
                  No se pudo cargar la informacion del cliente.
                </p>
              )}
            </div>
          </div>
        </section>

        <section className="rounded-lg border bg-card p-5">
          <h2 className="text-base font-semibold">Totales</h2>
          <div className="mt-4 space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Subtotal</span>
              <span>{formatCurrency(sale.subtotal)}</span>
            </div>
            {Number(sale.discount) > 0 && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Descuento</span>
                <span className="text-destructive">
                  -{formatCurrency(sale.discount)}
                </span>
              </div>
            )}
            {Number(sale.tax) > 0 && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Impuesto</span>
                <span>{formatCurrency(sale.tax)}</span>
              </div>
            )}
            <div className="flex justify-between border-t pt-2 text-base font-semibold">
              <span>Total</span>
              <span>{formatCurrency(sale.total)}</span>
            </div>
          </div>
        </section>
      </div>

      <section className="rounded-lg border">
        <div className="px-5 py-4">
          <h2 className="text-base font-semibold">Productos</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            {sale.items?.length ?? 0} item(s) registrados en esta venta.
          </p>
        </div>
        {isLoading ? (
          <div className="space-y-2 p-4">
            {Array.from({ length: 4 }).map((_, index) => (
              <Skeleton key={index} className="h-8 w-full" />
            ))}
          </div>
        ) : (
          <Table
            className="min-w-[680px]"
            containerClassName="rounded-none border-0"
          >
            <TableCaption className="sr-only">
              Productos incluidos en la venta {sale.invoice_number}
            </TableCaption>
            <TableHeader className="bg-transparent [&_tr]:border-0">
              <TableRow>
                <TableHead className="w-[45%]">Producto</TableHead>
                <TableHead className="w-[15%] text-right">Cant.</TableHead>
                <TableHead className="w-[20%] text-right">
                  Precio unitario
                </TableHead>
                <TableHead className="w-[20%] text-right">Subtotal</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {sale.items && sale.items.length > 0 ? (
                sale.items.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <div className="space-y-1">
                        <p className="font-medium whitespace-normal leading-tight">
                          {item.product_name}
                        </p>
                        <p className="font-mono text-xs text-muted-foreground">
                          SKU: {item.product_sku}
                        </p>
                      </div>
                    </TableCell>
                    <TableCell className="text-right font-medium tabular-nums">
                      {item.quantity}
                    </TableCell>
                    <TableCell className="text-right tabular-nums">
                      {formatCurrency(item.unit_price)}
                    </TableCell>
                    <TableCell className="text-right font-semibold tabular-nums">
                      {formatCurrency(item.subtotal)}
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell
                    colSpan={4}
                    className="h-24 text-center text-muted-foreground"
                  >
                    No hay productos registrados para esta venta.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        )}
      </section>

      <div className="space-y-6">
        {sale.cancellation_reason && (
          <section className="rounded-lg border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
            <h2 className="font-semibold">Motivo de cancelacion</h2>
            <p className="mt-1">{sale.cancellation_reason}</p>
          </section>
        )}

        {sale.notes && (
          <section className="rounded-lg border bg-card p-5">
            <h2 className="text-base font-semibold">Notas</h2>
            <p className="mt-2 text-sm text-muted-foreground">{sale.notes}</p>
          </section>
        )}
      </div>
    </div>
  )
}

export default SaleDetailContent
