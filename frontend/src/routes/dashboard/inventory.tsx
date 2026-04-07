import { useQuery, useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense, useMemo, useState } from "react"

import { CategoriesService, ProductsService } from "@/client"
import { DataTable, type FilterableColumn } from "@/components/Common/DataTable"
import AddCategory from "@/components/Inventory/AddCategory"
import AddProduct from "@/components/Inventory/AddProduct"
import { categoryColumns } from "@/components/Inventory/categoryColumns"
import { buildProductColumns } from "@/components/Inventory/columns"
import PendingCategories from "@/components/Inventory/PendingCategories"
import PendingProducts from "@/components/Inventory/PendingProducts"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useDebounce } from "@/hooks/useDebounce"
import { requireUserWithRoles } from "@/lib/auth-guards"
import { queryClient } from "@/lib/queryClient"

const STATUS_FILTER: FilterableColumn = {
  id: "is_active",
  label: "Estado",
  options: [
    { label: "Activo", value: "true" },
    { label: "Inactivo", value: "false" },
  ],
}

function getCategoriesQueryOptions() {
  return {
    queryFn: () => CategoriesService.readCategories({ skip: 0, limit: 100 }),
    queryKey: ["categories"],
  }
}

function getLowStockQueryOptions() {
  return {
    queryFn: () =>
      ProductsService.readLowStockProducts({ skip: 0, limit: 100 }),
    queryKey: ["low-stock-products"],
  }
}

export const Route = createFileRoute("/dashboard/inventory")({
  component: Inventory,
  beforeLoad: async () => {
    await requireUserWithRoles(queryClient, ["admin", "seller"])
  },
  head: () => ({
    meta: [
      {
        title: "Inventario - OrbitEngine",
      },
    ],
  }),
})

function ProductsTableContent({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  const debouncedSearch = useDebounce(search, 300)
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions())

  const { data: products, isLoading } = useQuery({
    queryFn: () =>
      ProductsService.readProducts({
        skip: 0,
        limit: 100,
        search: debouncedSearch || undefined,
      }),
    queryKey: ["products", debouncedSearch],
    placeholderData: (previousData) => previousData,
  })

  const columns = useMemo(
    () => buildProductColumns(categories.data),
    [categories.data],
  )

  const categoryFilterOptions = useMemo(
    () =>
      categories.data.map((c) => ({
        label: c.name,
        value: c.id,
      })),
    [categories.data],
  )

  const filterableColumns: FilterableColumn[] = useMemo(
    () => [
      {
        id: "category_id",
        label: "Categoría",
        options: categoryFilterOptions,
      },
      STATUS_FILTER,
    ],
    [categoryFilterOptions],
  )

  if (!products && isLoading) return <PendingProducts />

  return (
    <DataTable
      columns={columns}
      data={products?.data ?? []}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Buscar por nombre o SKU…"
      filterableColumns={filterableColumns}
    />
  )
}

function ProductsTable({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  return (
    <Suspense fallback={<PendingProducts />}>
      <ProductsTableContent search={search} onSearchChange={onSearchChange} />
    </Suspense>
  )
}

function CategoriesTableContent({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions())

  const filtered = useMemo(() => {
    if (!search) return categories.data
    const term = search.toLowerCase()
    return categories.data.filter(
      (c) =>
        c.name.toLowerCase().includes(term) ||
        (c.description ?? "").toLowerCase().includes(term),
    )
  }, [categories.data, search])

  return (
    <DataTable
      columns={categoryColumns}
      data={filtered}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Buscar por nombre…"
      filterableColumns={[STATUS_FILTER]}
    />
  )
}

function CategoriesTable({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  return (
    <Suspense fallback={<PendingCategories />}>
      <CategoriesTableContent search={search} onSearchChange={onSearchChange} />
    </Suspense>
  )
}

function LowStockTableContent({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  const { data: lowStock } = useSuspenseQuery(getLowStockQueryOptions())
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions())

  const columns = useMemo(
    () => buildProductColumns(categories.data),
    [categories.data],
  )

  const categoryFilterOptions = useMemo(
    () =>
      categories.data.map((c) => ({
        label: c.name,
        value: c.id,
      })),
    [categories.data],
  )

  const filterableColumns: FilterableColumn[] = useMemo(
    () => [
      {
        id: "category_id",
        label: "Categoría",
        options: categoryFilterOptions,
      },
    ],
    [categoryFilterOptions],
  )

  const filtered = useMemo(() => {
    if (!search) return lowStock.data
    const term = search.toLowerCase()
    return lowStock.data.filter(
      (p) =>
        p.name.toLowerCase().includes(term) ||
        p.sku.toLowerCase().includes(term),
    )
  }, [lowStock.data, search])

  return (
    <DataTable
      columns={columns}
      data={filtered}
      searchValue={search}
      onSearchChange={onSearchChange}
      searchPlaceholder="Buscar por nombre o SKU…"
      filterableColumns={filterableColumns}
    />
  )
}

function LowStockTable({
  search,
  onSearchChange,
}: {
  search: string
  onSearchChange: (v: string) => void
}) {
  return (
    <Suspense fallback={<PendingProducts />}>
      <LowStockTableContent search={search} onSearchChange={onSearchChange} />
    </Suspense>
  )
}

function LowStockBadge() {
  const { data: lowStock } = useSuspenseQuery(getLowStockQueryOptions())
  if (lowStock.count === 0) return null
  return (
    <Badge variant="destructive" className="ml-1.5 text-xs px-1.5 py-0">
      {lowStock.count}
    </Badge>
  )
}

function Inventory() {
  const [productSearch, setProductSearch] = useState("")
  const [categorySearch, setCategorySearch] = useState("")
  const [lowStockSearch, setLowStockSearch] = useState("")

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Inventario</h1>
        <p className="text-muted-foreground">
          Gestiona tu catálogo de productos y categorías
        </p>
      </div>
      <Tabs defaultValue="products">
        <div className="flex items-center justify-between">
          <TabsList>
            <TabsTrigger value="products">Productos</TabsTrigger>
            <TabsTrigger value="categories">Categorías</TabsTrigger>
            <TabsTrigger value="low-stock" className="gap-1">
              Stock bajo
              <Suspense>
                <LowStockBadge />
              </Suspense>
            </TabsTrigger>
          </TabsList>
          <TabsContent value="products" className="mt-0 ml-4">
            <AddProduct />
          </TabsContent>
          <TabsContent value="categories" className="mt-0 ml-4">
            <AddCategory />
          </TabsContent>
        </div>
        <TabsContent value="products">
          <ProductsTable
            search={productSearch}
            onSearchChange={setProductSearch}
          />
        </TabsContent>
        <TabsContent value="categories">
          <CategoriesTable
            search={categorySearch}
            onSearchChange={setCategorySearch}
          />
        </TabsContent>
        <TabsContent value="low-stock">
          <LowStockTable
            search={lowStockSearch}
            onSearchChange={setLowStockSearch}
          />
        </TabsContent>
      </Tabs>
    </div>
  )
}
