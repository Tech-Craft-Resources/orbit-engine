import { zodResolver } from "@hookform/resolvers/zod"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Pencil } from "lucide-react"
import { useState } from "react"
import { useForm } from "react-hook-form"
import { z } from "zod"

import {
  CategoriesService,
  type ProductPublic,
  ProductsService,
} from "@/client"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"
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
import useCustomToast from "@/hooks/useCustomToast"
import { handleError } from "@/utils"

const formSchema = z.object({
  name: z.string().min(1, { message: "Name is required" }),
  sku: z.string().min(1, { message: "SKU is required" }),
  description: z.string().optional(),
  category_id: z.string().optional(),
  cost_price: z.string().optional(),
  sale_price: z.string().optional(),
  stock_min: z.string().optional(),
  stock_max: z.string().optional(),
  unit: z.string().optional(),
  barcode: z.string().optional(),
  is_active: z.boolean(),
})

type FormData = z.infer<typeof formSchema>

interface EditProductProps {
  product: ProductPublic
  onSuccess: () => void
}

const EditProduct = ({ product, onSuccess }: EditProductProps) => {
  const [isOpen, setIsOpen] = useState(false)
  const queryClient = useQueryClient()
  const { showSuccessToast, showErrorToast } = useCustomToast()

  const { data: categoriesData } = useQuery({
    queryKey: ["categories"],
    queryFn: () => CategoriesService.readCategories({ skip: 0, limit: 100 }),
  })

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    mode: "onBlur",
    criteriaMode: "all",
    defaultValues: {
      name: product.name,
      sku: product.sku,
      description: product.description ?? "",
      category_id: product.category_id ?? undefined,
      cost_price: product.cost_price ?? "",
      sale_price: product.sale_price ?? "",
      stock_min: product.stock_min?.toString() ?? "",
      stock_max: product.stock_max?.toString() ?? "",
      unit: product.unit ?? "",
      barcode: product.barcode ?? "",
      is_active: product.is_active ?? true,
    },
  })

  const mutation = useMutation({
    mutationFn: (data: FormData) => {
      const requestBody = {
        name: data.name,
        sku: data.sku,
        description: data.description || null,
        category_id: data.category_id || null,
        cost_price: data.cost_price ? Number(data.cost_price) : null,
        sale_price: data.sale_price ? Number(data.sale_price) : null,
        stock_min: data.stock_min ? Number(data.stock_min) : null,
        stock_max: data.stock_max ? Number(data.stock_max) : null,
        unit: data.unit || null,
        barcode: data.barcode || null,
        is_active: data.is_active,
      }
      return ProductsService.updateProduct({
        productId: product.id,
        requestBody,
      })
    },
    onSuccess: () => {
      showSuccessToast("Product updated successfully")
      setIsOpen(false)
      onSuccess()
    },
    onError: handleError.bind(showErrorToast),
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ["products"] })
    },
  })

  const onSubmit = (data: FormData) => {
    mutation.mutate(data)
  }

  return (
    <Dialog open={isOpen} onOpenChange={setIsOpen}>
      <DropdownMenuItem
        onSelect={(e) => e.preventDefault()}
        onClick={() => setIsOpen(true)}
      >
        <Pencil />
        Edit Product
      </DropdownMenuItem>
      <DialogContent className="sm:max-w-lg max-h-[90vh] overflow-y-auto">
        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)}>
            <DialogHeader>
              <DialogTitle>Edit Product</DialogTitle>
              <DialogDescription>
                Update the product details below.
              </DialogDescription>
            </DialogHeader>
            <div className="grid gap-4 py-4">
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="name"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        Name <span className="text-destructive">*</span>
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="Product name" {...field} required />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="sku"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>
                        SKU <span className="text-destructive">*</span>
                      </FormLabel>
                      <FormControl>
                        <Input placeholder="SKU-001" {...field} required />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Input placeholder="Product description" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="category_id"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Category</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value ?? ""}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select a category" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {categoriesData?.data.map((cat) => (
                          <SelectItem key={cat.id} value={cat.id}>
                            {cat.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="cost_price"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Cost Price</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          step="0.01"
                          min="0"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="sale_price"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Sale Price</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0.00"
                          type="number"
                          step="0.01"
                          min="0"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="stock_min"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Min Stock</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0"
                          type="number"
                          min="0"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="stock_max"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Max Stock</FormLabel>
                      <FormControl>
                        <Input
                          placeholder="0"
                          type="number"
                          min="0"
                          {...field}
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="unit"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Unit</FormLabel>
                      <FormControl>
                        <Input placeholder="pcs, kg, etc." {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="barcode"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Barcode</FormLabel>
                      <FormControl>
                        <Input placeholder="Barcode" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <FormField
                control={form.control}
                name="is_active"
                render={({ field }) => (
                  <FormItem className="flex items-center gap-3 space-y-0">
                    <FormControl>
                      <Checkbox
                        checked={field.value}
                        onCheckedChange={field.onChange}
                      />
                    </FormControl>
                    <FormLabel className="font-normal">Is active?</FormLabel>
                  </FormItem>
                )}
              />
            </div>

            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline" disabled={mutation.isPending}>
                  Cancel
                </Button>
              </DialogClose>
              <LoadingButton type="submit" loading={mutation.isPending}>
                Save
              </LoadingButton>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

export default EditProduct
