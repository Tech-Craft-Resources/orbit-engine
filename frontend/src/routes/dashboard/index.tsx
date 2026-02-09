import { useQuery } from "@tanstack/react-query"
import { createFileRoute, Link } from "@tanstack/react-router"
import {
  AlertTriangle,
  DollarSign,
  Receipt,
  ShoppingCart,
  TrendingUp,
} from "lucide-react"

import { DashboardService } from "@/client"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
import useAuth from "@/hooks/useAuth"

export const Route = createFileRoute("/dashboard/")({
  component: Dashboard,
  head: () => ({
    meta: [
      {
        title: "Dashboard - OrbitEngine",
      },
    ],
  }),
})

function formatCurrency(value: string): string {
  return `$${Number(value).toFixed(2)}`
}

function KPICardSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-4 w-24" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-32" />
        <Skeleton className="mt-2 h-3 w-20" />
      </CardContent>
    </Card>
  )
}

function Dashboard() {
  const { user: currentUser } = useAuth()

  const { data: stats, isLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: DashboardService.readDashboardStats,
  })

  const displayName = currentUser?.first_name
    ? `${currentUser.first_name} ${currentUser.last_name}`.trim()
    : currentUser?.email

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-bold tracking-tight truncate max-w-sm">
          Hi, {displayName}
        </h1>
        <p className="text-muted-foreground">
          Here&apos;s an overview of your business
        </p>
      </div>

      {/* KPI Cards */}
      {isLoading ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <KPICardSkeleton key={i} />
          ))}
        </div>
      ) : stats ? (
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader>
              <CardDescription className="flex items-center gap-2">
                <ShoppingCart className="size-4" />
                Today&apos;s Sales
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(stats.sales_today.total)}
              </div>
              <p className="text-xs text-muted-foreground">
                {stats.sales_today.count} transactions
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardDescription className="flex items-center gap-2">
                <DollarSign className="size-4" />
                Monthly Sales
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(stats.sales_month.total)}
              </div>
              <p className="text-xs text-muted-foreground">
                {stats.sales_month.count} transactions
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardDescription className="flex items-center gap-2">
                <TrendingUp className="size-4" />
                Average Ticket
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {formatCurrency(stats.average_ticket)}
              </div>
              <p className="text-xs text-muted-foreground">Per transaction</p>
            </CardContent>
          </Card>

          <Link
            to="/dashboard/inventory"
            className="block transition-opacity hover:opacity-80"
          >
            <Card>
              <CardHeader>
                <CardDescription className="flex items-center gap-2">
                  <AlertTriangle className="size-4" />
                  Low Stock
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">
                  {stats.low_stock_count}
                </div>
                <p className="text-xs text-muted-foreground">
                  Products below minimum
                </p>
              </CardContent>
            </Card>
          </Link>
        </div>
      ) : null}

      {/* Bottom section: Top Products + Sales by Day */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Top Products */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Receipt className="size-4" />
              Top Products
            </CardTitle>
            <CardDescription>Best selling products this month</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {Array.from({ length: 5 }).map((_, i) => (
                  <Skeleton key={i} className="h-6 w-full" />
                ))}
              </div>
            ) : stats?.top_products && stats.top_products.length > 0 ? (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Product</TableHead>
                    <TableHead className="text-right">Sold</TableHead>
                    <TableHead className="text-right">Revenue</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {stats.top_products.map((product) => (
                    <TableRow key={product.product_id}>
                      <TableCell className="font-medium">
                        {product.product_name}
                      </TableCell>
                      <TableCell className="text-right">
                        {product.quantity_sold}
                      </TableCell>
                      <TableCell className="text-right">
                        {formatCurrency(product.revenue)}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">
                No sales data yet
              </p>
            )}
          </CardContent>
        </Card>

        {/* Sales by Day */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="size-4" />
              Sales This Week
            </CardTitle>
            <CardDescription>Daily sales breakdown</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-3">
                {Array.from({ length: 7 }).map((_, i) => (
                  <Skeleton key={i} className="h-6 w-full" />
                ))}
              </div>
            ) : stats?.sales_by_day && stats.sales_by_day.length > 0 ? (
              <div className="space-y-3">
                {stats.sales_by_day.map((day) => {
                  const maxTotal = Math.max(
                    ...stats.sales_by_day.map((d) => Number(d.total)),
                  )
                  const percentage =
                    maxTotal > 0 ? (Number(day.total) / maxTotal) * 100 : 0
                  return (
                    <div key={day.date} className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <span className="text-muted-foreground">
                          {new Date(`${day.date}T00:00:00`).toLocaleDateString(
                            "en-US",
                            {
                              weekday: "short",
                              month: "short",
                              day: "numeric",
                            },
                          )}
                        </span>
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-muted-foreground">
                            {day.count} sales
                          </span>
                          <span className="font-medium">
                            {formatCurrency(day.total)}
                          </span>
                        </div>
                      </div>
                      <div className="h-2 rounded-full bg-muted">
                        <div
                          className="h-2 rounded-full bg-primary transition-all"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-4">
                No sales data yet
              </p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
