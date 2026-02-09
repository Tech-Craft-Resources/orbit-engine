import { useSuspenseQuery } from "@tanstack/react-query";
import { createFileRoute, redirect } from "@tanstack/react-router";
import { Suspense, useMemo } from "react";

import { CategoriesService, ProductsService, UsersService } from "@/client";
import { DataTable } from "@/components/Common/DataTable";
import AddCategory from "@/components/Inventory/AddCategory";
import AddProduct from "@/components/Inventory/AddProduct";
import { categoryColumns } from "@/components/Inventory/categoryColumns";
import { buildProductColumns } from "@/components/Inventory/columns";
import PendingCategories from "@/components/Inventory/PendingCategories";
import PendingProducts from "@/components/Inventory/PendingProducts";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { hasRole } from "@/hooks/useAuth";

function getProductsQueryOptions() {
  return {
    queryFn: () => ProductsService.readProducts({ skip: 0, limit: 100 }),
    queryKey: ["products"],
  };
}

function getCategoriesQueryOptions() {
  return {
    queryFn: () => CategoriesService.readCategories({ skip: 0, limit: 100 }),
    queryKey: ["categories"],
  };
}

function getLowStockQueryOptions() {
  return {
    queryFn: () =>
      ProductsService.readLowStockProducts({ skip: 0, limit: 100 }),
    queryKey: ["low-stock-products"],
  };
}

export const Route = createFileRoute("/dashboard/inventory")({
  component: Inventory,
  beforeLoad: async () => {
    const user = await UsersService.readUserMe();
    if (!hasRole(user, ["admin", "seller"])) {
      throw redirect({
        to: "/",
      });
    }
  },
  head: () => ({
    meta: [
      {
        title: "Inventory - OrbitEngine",
      },
    ],
  }),
});

function ProductsTableContent() {
  const { data: products } = useSuspenseQuery(getProductsQueryOptions());
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions());

  const columns = useMemo(
    () => buildProductColumns(categories.data),
    [categories.data],
  );

  return <DataTable columns={columns} data={products.data} />;
}

function ProductsTable() {
  return (
    <Suspense fallback={<PendingProducts />}>
      <ProductsTableContent />
    </Suspense>
  );
}

function CategoriesTableContent() {
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions());
  return <DataTable columns={categoryColumns} data={categories.data} />;
}

function CategoriesTable() {
  return (
    <Suspense fallback={<PendingCategories />}>
      <CategoriesTableContent />
    </Suspense>
  );
}

function LowStockTableContent() {
  const { data: lowStock } = useSuspenseQuery(getLowStockQueryOptions());
  const { data: categories } = useSuspenseQuery(getCategoriesQueryOptions());

  const columns = useMemo(
    () => buildProductColumns(categories.data),
    [categories.data],
  );

  return <DataTable columns={columns} data={lowStock.data} />;
}

function LowStockTable() {
  return (
    <Suspense fallback={<PendingProducts />}>
      <LowStockTableContent />
    </Suspense>
  );
}

function LowStockBadge() {
  const { data: lowStock } = useSuspenseQuery(getLowStockQueryOptions());
  if (lowStock.count === 0) return null;
  return (
    <Badge variant="destructive" className="ml-1.5 text-xs px-1.5 py-0">
      {lowStock.count}
    </Badge>
  );
}

function Inventory() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight">Inventory</h1>
        <p className="text-muted-foreground">
          Manage your product catalog and categories
        </p>
      </div>
      <Tabs defaultValue="products">
        <div className="flex items-center justify-between">
          <TabsList>
            <TabsTrigger value="products">Products</TabsTrigger>
            <TabsTrigger value="categories">Categories</TabsTrigger>
            <TabsTrigger value="low-stock" className="gap-1">
              Low Stock
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
          <ProductsTable />
        </TabsContent>
        <TabsContent value="categories">
          <CategoriesTable />
        </TabsContent>
        <TabsContent value="low-stock">
          <LowStockTable />
        </TabsContent>
      </Tabs>
    </div>
  );
}
