import { useQuery } from "@tanstack/react-query"
import { createFileRoute, Link } from "@tanstack/react-router"
import {
  AlertTriangle,
  ArrowUpRight,
  DollarSign,
  PackageSearch,
  Receipt,
  ShoppingCart,
  TrendingUp,
} from "lucide-react"
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  XAxis,
  YAxis,
} from "recharts"

import { DashboardService } from "@/client"
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import { Skeleton } from "@/components/ui/skeleton"
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

function formatCurrency(value: string | number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(Number(value))
}

function formatCompact(value: string | number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(Number(value))
}

function formatCount(value: number): string {
  return new Intl.NumberFormat("en-US").format(value)
}

const CHART_COLORS = [
  "var(--chart-1)",
  "var(--chart-2)",
  "var(--chart-3)",
  "var(--chart-4)",
  "var(--chart-5)",
]

const salesChartConfig = {
  total: {
    label: "Revenue",
    color: "var(--chart-1)",
  },
  count: {
    label: "Transactions",
    color: "var(--chart-2)",
  },
} satisfies ChartConfig

const productsChartConfig = {
  revenue: {
    label: "Revenue",
    color: "var(--chart-1)",
  },
} satisfies ChartConfig

function KPICardSkeleton() {
  return (
    <Card>
      <CardHeader className="pb-2">
        <Skeleton className="h-4 w-28" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-8 w-32 mb-2" />
        <Skeleton className="h-3 w-20" />
      </CardContent>
    </Card>
  )
}

function ChartSkeleton() {
  return (
    <div className="space-y-3">
      <div className="flex items-end gap-2 h-48">
        {Array.from({ length: 7 }).map((_, i) => (
          <Skeleton
            key={i}
            className="flex-1 rounded"
            style={{ height: `${30 + Math.random() * 70}%` }}
          />
        ))}
      </div>
      <div className="flex justify-between">
        {Array.from({ length: 7 }).map((_, i) => (
          <Skeleton key={i} className="h-3 w-8" />
        ))}
      </div>
    </div>
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

  const salesByDayData =
    stats?.sales_by_day.map((d) => ({
      date: d.date,
      label: new Date(`${d.date}T00:00:00`).toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
      }),
      shortLabel: new Date(`${d.date}T00:00:00`).toLocaleDateString("en-US", {
        weekday: "short",
      }),
      total: Number(d.total),
      count: d.count,
    })) ?? []

  const topProductsData =
    stats?.top_products.map((p) => ({
      name: p.product_name,
      revenue: Number(p.revenue),
      quantity_sold: p.quantity_sold,
    })) ?? []

  const maxRevenue = Math.max(...topProductsData.map((p) => p.revenue), 1)

  const hasLowStock = (stats?.low_stock_count ?? 0) > 0

  return (
    <div className="flex flex-col gap-6">
      {/* Header */}
      <div className="flex flex-col gap-1">
        <h1 className="text-2xl font-bold tracking-tight">Hi, {displayName}</h1>
        <p className="text-muted-foreground text-sm">
          Here&apos;s an overview of your business today
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
          {/* Today's Sales */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardDescription className="text-sm font-medium">
                Today&apos;s Sales
              </CardDescription>
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-blue-50 dark:bg-blue-950">
                <ShoppingCart className="size-4 text-blue-600 dark:text-blue-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold tabular-nums">
                {formatCurrency(stats.sales_today.total)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {formatCount(stats.sales_today.count)} transactions today
              </p>
            </CardContent>
          </Card>

          {/* Monthly Sales */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardDescription className="text-sm font-medium">
                Monthly Sales
              </CardDescription>
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-emerald-50 dark:bg-emerald-950">
                <DollarSign className="size-4 text-emerald-600 dark:text-emerald-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold tabular-nums">
                {formatCurrency(stats.sales_month.total)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {formatCount(stats.sales_month.count)} transactions this month
              </p>
            </CardContent>
          </Card>

          {/* Average Ticket */}
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardDescription className="text-sm font-medium">
                Average Ticket
              </CardDescription>
              <div className="flex h-8 w-8 items-center justify-center rounded-md bg-amber-50 dark:bg-amber-950">
                <TrendingUp className="size-4 text-amber-600 dark:text-amber-400" />
              </div>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold tabular-nums">
                {formatCurrency(stats.average_ticket)}
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                Per transaction average
              </p>
            </CardContent>
          </Card>

          {/* Low Stock */}
          <Link
            to="/dashboard/inventory"
            className="block transition-opacity hover:opacity-80 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring rounded-xl"
          >
            <Card
              className={
                hasLowStock ? "border-orange-200 dark:border-orange-900" : ""
              }
            >
              <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
                <CardDescription className="text-sm font-medium">
                  Low Stock
                </CardDescription>
                <div
                  className={`flex h-8 w-8 items-center justify-center rounded-md ${
                    hasLowStock ? "bg-orange-50 dark:bg-orange-950" : "bg-muted"
                  }`}
                >
                  <AlertTriangle
                    className={`size-4 ${hasLowStock ? "text-orange-500" : "text-muted-foreground"}`}
                  />
                </div>
              </CardHeader>
              <CardContent>
                <div
                  className={`text-2xl font-bold tabular-nums ${hasLowStock ? "text-orange-600 dark:text-orange-400" : ""}`}
                >
                  {formatCount(stats.low_stock_count)}
                </div>
                <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
                  Products below minimum
                  <ArrowUpRight className="size-3" />
                </p>
              </CardContent>
            </Card>
          </Link>
        </div>
      ) : null}

      {/* Sales This Week Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Receipt className="size-4" />
            Sales This Week
          </CardTitle>
          <CardDescription>
            Daily revenue — Mon to Sun this week, hover to see details
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <ChartSkeleton />
          ) : salesByDayData.length > 0 ? (
            <ChartContainer config={salesChartConfig} className="h-56 w-full">
              <LineChart
                data={salesByDayData}
                margin={{ top: 8, right: 8, left: 4, bottom: 0 }}
              >
                <CartesianGrid
                  vertical={false}
                  strokeDasharray="3 3"
                  className="stroke-border"
                />
                <XAxis
                  dataKey="shortLabel"
                  tickLine={false}
                  axisLine={false}
                  tick={{ fontSize: 12 }}
                  className="fill-muted-foreground"
                />
                <YAxis
                  tickLine={false}
                  axisLine={false}
                  tick={{ fontSize: 11 }}
                  tickFormatter={(v: number) => formatCompact(v)}
                  width={56}
                  className="fill-muted-foreground"
                />
                <ChartTooltip
                  cursor={{ stroke: "var(--border)", strokeWidth: 1 }}
                  content={({ content: _c, ...props }) => (
                    <ChartTooltipContent
                      {...props}
                      formatter={(value, name) => {
                        if (name === "total") {
                          return (
                            <span className="font-medium tabular-nums">
                              {formatCurrency(value as number)}
                            </span>
                          )
                        }
                        return (
                          <span className="tabular-nums">
                            {formatCount(value as number)} sales
                          </span>
                        )
                      }}
                      labelFormatter={(_, payload) => {
                        const item = payload?.[0]?.payload
                        return item ? (
                          <span className="font-medium">{item.label}</span>
                        ) : null
                      }}
                    />
                  )}
                />
                <Line
                  type="monotone"
                  dataKey="total"
                  name="total"
                  stroke="var(--color-total)"
                  strokeWidth={2}
                  dot={{ fill: "var(--color-total)", r: 4, strokeWidth: 0 }}
                  activeDot={{ r: 6, strokeWidth: 0 }}
                />
              </LineChart>
            </ChartContainer>
          ) : (
            <div className="flex h-56 flex-col items-center justify-center gap-2 text-muted-foreground">
              <TrendingUp className="size-8 opacity-30" />
              <p className="text-sm">No sales data for this week yet</p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Bottom section: Top Products */}
      <div className="grid gap-6 lg:grid-cols-2">
        {/* Top Products Table */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PackageSearch className="size-4" />
              Top Products
            </CardTitle>
            <CardDescription>Best selling products this month</CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="space-y-4">
                {Array.from({ length: 5 }).map((_, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <Skeleton className="h-4 flex-1" />
                    <Skeleton className="h-4 w-12" />
                    <Skeleton className="h-4 w-20" />
                  </div>
                ))}
              </div>
            ) : topProductsData.length > 0 ? (
              <div className="space-y-3">
                {topProductsData.map((product, idx) => (
                  <div key={product.name} className="space-y-1.5">
                    <div className="flex items-center justify-between gap-2 text-sm">
                      <div className="flex items-center gap-2 min-w-0">
                        <span className="text-xs font-mono text-muted-foreground w-4 shrink-0">
                          {idx + 1}
                        </span>
                        <span className="font-medium truncate">
                          {product.name}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 shrink-0">
                        <span className="text-xs text-muted-foreground">
                          {formatCount(product.quantity_sold)} units
                        </span>
                        <span className="font-semibold tabular-nums">
                          {formatCurrency(product.revenue)}
                        </span>
                      </div>
                    </div>
                    <div className="h-1.5 rounded-full bg-muted overflow-hidden">
                      <div
                        className="h-full rounded-full transition-all duration-500"
                        style={{
                          width: `${(product.revenue / maxRevenue) * 100}%`,
                          backgroundColor:
                            CHART_COLORS[idx % CHART_COLORS.length],
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center gap-2 py-8 text-muted-foreground">
                <PackageSearch className="size-8 opacity-30" />
                <p className="text-sm">No sales data yet</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Revenue by Product Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <DollarSign className="size-4" />
              Revenue by Product
            </CardTitle>
            <CardDescription>
              Comparative revenue — hover bars for details
            </CardDescription>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <ChartSkeleton />
            ) : topProductsData.length > 0 ? (
              <ChartContainer
                config={productsChartConfig}
                className="h-56 w-full"
              >
                <BarChart
                  data={topProductsData}
                  layout="vertical"
                  margin={{ top: 0, right: 8, left: 8, bottom: 0 }}
                  barCategoryGap="25%"
                >
                  <CartesianGrid
                    horizontal={false}
                    strokeDasharray="3 3"
                    className="stroke-border"
                  />
                  <XAxis
                    type="number"
                    tickLine={false}
                    axisLine={false}
                    tick={{ fontSize: 11 }}
                    tickFormatter={(v: number) => formatCompact(v)}
                  />
                  <YAxis
                    type="category"
                    dataKey="name"
                    tickLine={false}
                    axisLine={false}
                    tick={{ fontSize: 11 }}
                    width={90}
                    tickFormatter={(v: string) =>
                      v.length > 12 ? `${v.slice(0, 12)}…` : v
                    }
                  />
                  <ChartTooltip
                    cursor={{ fill: "var(--muted)", radius: 4 }}
                    content={({ content: _c, ...props }) => (
                      <ChartTooltipContent
                        {...props}
                        formatter={(value) => (
                          <span className="font-medium tabular-nums">
                            {formatCurrency(value as number)}
                          </span>
                        )}
                      />
                    )}
                  />
                  <Bar
                    dataKey="revenue"
                    name="revenue"
                    radius={[0, 4, 4, 0]}
                    maxBarSize={32}
                  >
                    {topProductsData.map((_, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={CHART_COLORS[index % CHART_COLORS.length]}
                      />
                    ))}
                  </Bar>
                </BarChart>
              </ChartContainer>
            ) : (
              <div className="flex h-56 flex-col items-center justify-center gap-2 text-muted-foreground">
                <DollarSign className="size-8 opacity-30" />
                <p className="text-sm">No product revenue data yet</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
