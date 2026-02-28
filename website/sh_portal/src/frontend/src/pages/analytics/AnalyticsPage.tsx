import React, { useState } from 'react';
import type { ColumnDef } from '@tanstack/react-table';
import {
  CurrencyDollarIcon,
  UsersIcon,
  ShoppingCartIcon,
  StarIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline';
import {
  MetricCard,
  DataTable,
  LineChart,
  BarChart,
  PieChart,
  AreaChart,
  HeatMap,
  DataExplorer,
  QueryBuilder,
  Card,
  Badge,
} from '../../components/common';
import type { CustomerSegment } from '../../data/sampleAnalyticsData';
import {
  generateTimeSeriesData,
  revenueByCategory,
  usersByPlatform,
  regionalPerformance,
  monthlyComparison,
  productPerformance,
  userActivityHeatmap,
  customerSegments,
  keyMetrics,
} from '../../data/sampleAnalyticsData';

const AnalyticsPage: React.FC = () => {
  const [timeSeriesData] = useState(generateTimeSeriesData(30));
  const [selectedTab, setSelectedTab] = useState<'overview' | 'products' | 'query'>('overview');

  // Product performance table columns
  const productColumns: ColumnDef<typeof productPerformance[0]>[] = [
    {
      accessorKey: 'product',
      header: 'Product',
      cell: ({ row }) => (
        <div className="font-medium text-gray-900">{row.original.product}</div>
      ),
    },
    {
      accessorKey: 'category',
      header: 'Category',
      cell: ({ row }) => (
        <Badge variant={row.original.category === 'Enterprise' ? 'primary' : 'default'}>
          {row.original.category}
        </Badge>
      ),
    },
    {
      accessorKey: 'revenue',
      header: 'Revenue',
      cell: ({ row }) => (
        <span className="font-semibold text-gray-900">
          ${row.original.revenue.toLocaleString()}
        </span>
      ),
    },
    {
      accessorKey: 'units',
      header: 'Units Sold',
      cell: ({ row }) => <span>{row.original.units.toLocaleString()}</span>,
    },
    {
      accessorKey: 'growth',
      header: 'Growth',
      cell: ({ row }) => {
        const growth = row.original.growth;
        return (
          <span className={growth >= 0 ? 'text-green-600' : 'text-red-600'}>
            {growth > 0 ? '+' : ''}
            {growth.toFixed(1)}%
          </span>
        );
      },
    },
    {
      accessorKey: 'rating',
      header: 'Rating',
      cell: ({ row }) => (
        <div className="flex items-center gap-1">
          <StarIcon className="h-4 w-4 text-yellow-400" />
          <span className="font-medium">{row.original.rating}</span>
        </div>
      ),
    },
    {
      accessorKey: 'status',
      header: 'Status',
      cell: ({ row }) => (
        <Badge variant={row.original.status === 'Active' ? 'success' : 'warning'}>
          {row.original.status}
        </Badge>
      ),
    },
  ];

  const queryFields = [
    { name: 'product', label: 'Product Name', type: 'text' as const },
    { name: 'category', label: 'Category', type: 'text' as const },
    { name: 'revenue', label: 'Revenue', type: 'number' as const },
    { name: 'units', label: 'Units Sold', type: 'number' as const },
    { name: 'growth', label: 'Growth Rate', type: 'number' as const },
    { name: 'rating', label: 'Rating', type: 'number' as const },
  ];

  const explorerFields = [
    { name: 'region', label: 'Region', type: 'text' as const },
    {
      name: 'category',
      label: 'Category',
      type: 'select' as const,
      options: [
        { label: 'Enterprise', value: 'enterprise' },
        { label: 'Professional', value: 'professional' },
        { label: 'Starter', value: 'starter' },
      ],
    },
    { name: 'revenue', label: 'Revenue', type: 'number' as const },
    { name: 'date', label: 'Date', type: 'date' as const },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">
          Comprehensive insights and data visualization
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          {[
            { id: 'overview' as const, label: 'Overview' },
            { id: 'products' as const, label: 'Product Analysis' },
            { id: 'query' as const, label: 'Query Builder' },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setSelectedTab(tab.id)}
              className={`
                whitespace-nowrap border-b-2 px-1 py-4 text-sm font-medium transition-colors
                ${
                  selectedTab === tab.id
                    ? 'border-indigo-500 text-indigo-600'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }
              `}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Overview Tab */}
      {selectedTab === 'overview' && (
        <DataExplorer fields={explorerFields}>
          {/* Key Metrics */}
          <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
            <MetricCard
              title="Total Revenue"
              value={keyMetrics.totalRevenue.value}
              change={keyMetrics.totalRevenue.change}
              changeLabel={keyMetrics.totalRevenue.label}
              icon={CurrencyDollarIcon}
              trend={keyMetrics.totalRevenue.trend}
            />
            <MetricCard
              title="Active Users"
              value={keyMetrics.activeUsers.value}
              change={keyMetrics.activeUsers.change}
              changeLabel={keyMetrics.activeUsers.label}
              icon={UsersIcon}
              trend={keyMetrics.activeUsers.trend}
            />
            <MetricCard
              title="Conversion Rate"
              value={keyMetrics.conversionRate.value}
              change={keyMetrics.conversionRate.change}
              changeLabel={keyMetrics.conversionRate.label}
              icon={ShoppingCartIcon}
              trend={keyMetrics.conversionRate.trend}
            />
            <MetricCard
              title="Avg Order Value"
              value={keyMetrics.avgOrderValue.value}
              change={keyMetrics.avgOrderValue.change}
              changeLabel={keyMetrics.avgOrderValue.label}
              icon={CurrencyDollarIcon}
              trend={keyMetrics.avgOrderValue.trend}
            />
            <MetricCard
              title="Customer Satisfaction"
              value={keyMetrics.customerSatisfaction.value}
              change={keyMetrics.customerSatisfaction.change}
              changeLabel={keyMetrics.customerSatisfaction.label}
              icon={StarIcon}
              trend={keyMetrics.customerSatisfaction.trend}
            />
            <MetricCard
              title="Churn Rate"
              value={keyMetrics.churnRate.value}
              change={keyMetrics.churnRate.change}
              changeLabel={keyMetrics.churnRate.label}
              icon={ArrowTrendingUpIcon}
              trend={keyMetrics.churnRate.trend}
            />
          </div>

          {/* Revenue Trends */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <LineChart
              data={timeSeriesData}
              lines={[
                { dataKey: 'revenue', name: 'Revenue', stroke: '#6366f1' },
                { dataKey: 'expenses', name: 'Expenses', stroke: '#ef4444' },
                { dataKey: 'profit', name: 'Profit', stroke: '#10b981' },
              ]}
              xAxisKey="date"
              title="Revenue vs Expenses"
              description="30-day trend analysis"
              showBrush
            />

            <AreaChart
              data={monthlyComparison}
              areas={[
                { dataKey: 'thisYear', name: '2024', fill: '#6366f1' },
                { dataKey: 'lastYear', name: '2023', fill: '#94a3b8' },
              ]}
              xAxisKey="month"
              title="Year-over-Year Comparison"
              description="Monthly revenue comparison"
            />
          </div>

          {/* Performance by Category */}
          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <PieChart
              data={revenueByCategory}
              dataKey="value"
              nameKey="name"
              title="Revenue by Category"
              description="Distribution across product categories"
              donut
            />

            <PieChart
              data={usersByPlatform}
              dataKey="value"
              nameKey="name"
              title="Users by Platform"
              description="Platform distribution"
            />
          </div>

          {/* Regional Performance */}
          <BarChart
            data={regionalPerformance}
            bars={[
              { dataKey: 'revenue', name: 'Revenue', fill: '#6366f1' },
              { dataKey: 'users', name: 'Users', fill: '#10b981' },
            ]}
            xAxisKey="region"
            title="Regional Performance"
            description="Revenue and user distribution by region"
          />

          {/* User Activity Heatmap */}
          <HeatMap
            data={userActivityHeatmap}
            title="User Activity Heatmap"
            description="Peak usage times by day and hour"
          />

          {/* Customer Segments Table */}
          <Card>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Customer Segments</h3>
              <p className="text-sm text-gray-500">Breakdown by customer value</p>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Segment
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Customers
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Revenue
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500">
                      Avg Spend
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {customerSegments.map((segment: CustomerSegment) => (
                    <tr key={segment.segment} className="hover:bg-gray-50">
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
                        {segment.segment}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">
                        {segment.count.toLocaleString()}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm font-semibold text-gray-900">
                        ${segment.revenue.toLocaleString()}
                      </td>
                      <td className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">
                        ${segment.avgSpend}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        </DataExplorer>
      )}

      {/* Products Tab */}
      {selectedTab === 'products' && (
        <div className="space-y-6">
          <DataTable
            data={productPerformance}
            columns={productColumns}
            searchPlaceholder="Search products..."
            exportFileName="product-performance"
          />

          <div className="grid grid-cols-1 gap-6 lg:grid-cols-2">
            <BarChart
              data={productPerformance.slice(0, 6)}
              bars={[{ dataKey: 'revenue', name: 'Revenue', fill: '#6366f1' }]}
              xAxisKey="product"
              title="Top Products by Revenue"
              description="Revenue comparison across products"
            />

            <BarChart
              data={productPerformance.slice(0, 6)}
              bars={[{ dataKey: 'units', name: 'Units Sold', fill: '#10b981' }]}
              xAxisKey="product"
              title="Top Products by Units"
              description="Sales volume comparison"
              horizontal
            />
          </div>
        </div>
      )}

      {/* Query Builder Tab */}
      {selectedTab === 'query' && (
        <div className="space-y-6">
          <QueryBuilder
            fields={queryFields}
            onExecuteQuery={(conditions) => {
              console.log('Executing query with conditions:', conditions);
              // In a real app, this would filter the data based on conditions
            }}
          />

          <Card>
            <div className="mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Query Results</h3>
              <p className="text-sm text-gray-500">
                Results will appear here after executing a query
              </p>
            </div>
            <DataTable
              data={productPerformance}
              columns={productColumns}
              searchPlaceholder="Search results..."
              exportFileName="query-results"
              pageSize={5}
            />
          </Card>
        </div>
      )}
    </div>
  );
};

export default AnalyticsPage;
