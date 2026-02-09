import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Minus, Plus, ShoppingCart, X } from "lucide-react"
import { useCallback, useMemo, useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import {
  CustomersService,
  type ProductPublic,
  ProductsService,
  SalesService,
} from "@/client"
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
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { LoadingButton } from "@/components/ui/loading-button"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Separator } from "@/components/ui/separator"
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

interface CartItem {
  product: ProductPublic
  quantity: number
}

const formSchema = z.object({
  customer_id: z.string().optional(),
  payment_method: z.string().min(1, { message: "Payment method is required" }),
  discount: z.string().optional(),
  tax: z.string().optional(),
  notes: z.string().optional(),
})

type FormData = z.infer<typeof formSchema>

const AddSale = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [cart, setCart] = useState<CartItem[]>([])
  const [search, setSearch] = useState("")
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const { data: productsData } = useQuery({
    queryKey: ["products"],
    queryFn: () => ProductsService.readProducts({ skip: 0, limit: 100 }),
    enabled: isOpen,
  })

  const { data: customersData } = useQuery({
    queryKey: ["customers"],
    queryFn: () => CustomersService.readCustomers({ skip: 0, limit: 100 }),
    enabled: isOpen,
  })

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      customer_id: "",
      payment_method: "cash",
      discount: "0",
      tax: "0",
      notes: "",
    },
  })

  const filteredProducts = useMemo(() => {
    if (!productsData?.data) return []
    const activeProducts = productsData.data.filter((p) => p.is_active)
    if (!search.trim()) return activeProducts
    const term = search.toLowerCase()
    return activeProducts.filter(
      (p) =>
        p.name.toLowerCase().includes(term) ||
        p.sku.toLowerCase().includes(term) ||
        p.barcode?.toLowerCase().includes(term),
    )
  }, [productsData?.data, search])

  const addToCart = useCallback((product: ProductPublic) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id)
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item,
        )
      }
      return [...prev, { product, quantity: 1 }]
    })
    setSearch("")
  }, [])

  const updateQuantity = useCallback((productId: string, delta: number) => {
    setCart((prev) =>
      prev
        .map((item) =>
          item.product.id === productId
            ? { ...item, quantity: item.quantity + delta }
            : item,
        )
        .filter((item) => item.quantity > 0),
    )
  }, [])

  const removeFromCart = useCallback((productId: string) => {
    setCart((prev) => prev.filter((item) => item.product.id !== productId))
  }, [])

  const subtotal = useMemo(
    () =>
      cart.reduce(
        (sum, item) => sum + item.quantity * Number(item.product.sale_price),
        0,
      ),
    [cart],
  )

  const discountValue = Number(form.watch("discount") || 0)
  const taxValue = Number(form.watch("tax") || 0)
  const total = subtotal - discountValue + taxValue

  const mutation = useMutation({
    mutationFn: SalesService.createSale,
    onSuccess: () => {
      showSuccessToast("Sale created successfully")
      form.reset()
      setCart([])
      setSearch("")
      setIsOpen(false)
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["sales"] })
      queryClient.invalidateQueries({ queryKey: ["products"] })
    },
  })

  const onSubmit = (data: FormData) => {
    if (cart.length === 0) {
      showErrorToast("Add at least one product to the cart")
      return
    }

    mutation.mutate({
      requestBody: {
        customer_id: data.customer_id || null,
        payment_method: data.payment_method,
        discount: Number(data.discount || 0),
        tax: Number(data.tax || 0),
        notes: data.notes || null,
        items: cart.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
      },
    })
  }

  const handleOpenChange = (open: boolean) => {
    setIsOpen(open)
    if (!open) {
      setCart([])
      setSearch("")
      form.reset()
    }
  }

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>
        <Button>
          <Plus className="mr-2" />
          New Sale
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>New Sale</DialogTitle>
          <DialogDescription>
            Search and add products, then complete the sale.
          </DialogDescription>
        </DialogHeader>
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <div className="space-y-4 py-4">
              {/* Product Search */}
              <div className="space-y-2">
                <FormLabel>Add Products</FormLabel>
                <Input
                  placeholder="Search by name, SKU, or barcode..."
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
                {search.trim() && filteredProducts.length > 0 && (
                  <div className="max-h-40 overflow-y-auto rounded-md border">
                    {filteredProducts.slice(0, 8).map((product) => (
                      <button
                        key={product.id}
                        type="button"
                        className="flex w-full items-center justify-between p-2 text-sm hover:bg-muted transition-colors"
                        onClick={() => addToCart(product)}
                      >
                        <div className="flex items-center gap-2">
                          <span className="font-medium">{product.name}</span>
                          <span className="text-xs text-muted-foreground font-mono">
                            {product.sku}
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-muted-foreground">
                            ${Number(product.sale_price).toFixed(2)}
                          </span>
                          <Badge
                            variant={
                              (product.stock_quantity ?? 0) > 0
                                ? "secondary"
                                : "destructive"
                            }
                            className="text-xs"
                          >
                            Stock: {product.stock_quantity ?? 0}
                          </Badge>
                        </div>
                      </button>
                    ))}
                  </div>
                )}
                {search.trim() && filteredProducts.length === 0 && (
                  <p className="text-sm text-muted-foreground p-2">
                    No products found
                  </p>
                )}
              </div>

              {/* Cart */}
              {cart.length > 0 && (
                <div className="space-y-2">
                  <FormLabel className="flex items-center gap-2">
                    <ShoppingCart className="size-4" />
                    Cart ({cart.length} items)
                  </FormLabel>
                  <div className="rounded-md border divide-y">
                    {cart.map((item) => (
                      <div
                        key={item.product.id}
                        className="flex items-center justify-between p-2 text-sm"
                      >
                        <div className="flex-1 min-w-0">
                          <span className="font-medium truncate block">
                            {item.product.name}
                          </span>
                          <span className="text-xs text-muted-foreground">
                            ${Number(item.product.sale_price).toFixed(2)} each
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <Button
                            type="button"
                            variant="outline"
                            size="icon"
                            className="size-7"
                            onClick={() => updateQuantity(item.product.id, -1)}
                          >
                            <Minus className="size-3" />
                          </Button>
                          <span className="w-8 text-center font-medium">
                            {item.quantity}
                          </span>
                          <Button
                            type="button"
                            variant="outline"
                            size="icon"
                            className="size-7"
                            onClick={() => updateQuantity(item.product.id, 1)}
                          >
                            <Plus className="size-3" />
                          </Button>
                          <span className="w-20 text-right font-medium">
                            $
                            {(
                              item.quantity * Number(item.product.sale_price)
                            ).toFixed(2)}
                          </span>
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="size-7 text-destructive"
                            onClick={() => removeFromCart(item.product.id)}
                          >
                            <X className="size-3" />
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <Separator />

              {/* Sale Details */}
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="customer_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Customer</FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        value={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Walk-in customer" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {customersData?.data.map((customer) => (
                            <SelectItem key={customer.id} value={customer.id}>
                              {customer.first_name} {customer.last_name}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="payment_method"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Payment Method{" "}
                        <span className="text-destructive">*</span>
                      </FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select method" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="cash">Cash</SelectItem>
                          <SelectItem value="card">Card</SelectItem>
                          <SelectItem value="transfer">Transfer</SelectItem>
                          <SelectItem value="other">Other</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="discount"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Discount ($)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          min={0}
                          step="0.01"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="tax"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Tax ($)</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          min={0}
                          step="0.01"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="notes"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Notes</FormLabel>
                    <FormControl>
                      <Input placeholder="Optional notes" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Totals */}
              <div className="space-y-1 rounded-md bg-muted/50 p-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Subtotal</span>
                  <span>${subtotal.toFixed(2)}</span>
                </div>
                {discountValue > 0 && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Discount</span>
                    <span className="text-destructive">
                      -${discountValue.toFixed(2)}
                    </span>
                  </div>
                )}
                {taxValue > 0 && (
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Tax</span>
                    <span>${taxValue.toFixed(2)}</span>
                  </div>
                )}
                <Separator />
                <div className="flex justify-between font-semibold text-base">
                  <span>Total</span>
                  <span>${total.toFixed(2)}</span>
                </div>
              </div>
            </div>

            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline" disabled={mutation.isPending}>
                  Cancel
                </Button>
              </DialogClose>
              <LoadingButton
                type="submit"
                loading={mutation.isPending}
                disabled={cart.length === 0}
              >
                Complete Sale
              </LoadingButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default AddSale
