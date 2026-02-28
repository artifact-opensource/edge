import React from 'react';
import {
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface BarChartProps {
  data: any[];
  bars: {
    dataKey: string;
    fill?: string;
    name?: string;
    stackId?: string;
  }[];
  xAxisKey: string;
  title?: string;
  description?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  horizontal?: boolean;
  stacked?: boolean;
  loading?: boolean;
}

const BarChart: React.FC<BarChartProps> = ({
  data,
  bars,
  xAxisKey,
  title,
  description,
  height = 400,
  showGrid = true,
  showLegend = true,
  horizontal = false,
  stacked = false,
  loading = false,
}) => {
  const colors = [
    '#6366f1',
    '#10b981',
    '#f59e0b',
    '#ef4444',
    '#8b5cf6',
    '#ec4899',
    '#14b8a6',
  ];

  if (loading) {
    return (
      <Card>
        {(title || description) && (
          <CardHeader>
            {title && <CardTitle>{title}</CardTitle>}
            {description && <CardDescription>{description}</CardDescription>}
          </CardHeader>
        )}
        <div className="flex items-center justify-center" style={{ height }}>
          <div className="h-12 w-12 animate-spin rounded-full border-b-2 border-indigo-600" />
        </div>
      </Card>
    );
  }

  return (
    <Card>
      {(title || description) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <RechartsBarChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
          layout={horizontal ? 'vertical' : 'horizontal'}
        >
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />}
          {horizontal ? (
            <>
              <XAxis
                type="number"
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: '#e5e7eb' }}
              />
              <YAxis
                type="category"
                dataKey={xAxisKey}
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: '#e5e7eb' }}
              />
            </>
          ) : (
            <>
              <XAxis
                dataKey={xAxisKey}
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: '#e5e7eb' }}
              />
              <YAxis
                stroke="#6b7280"
                fontSize={12}
                tickLine={false}
                axisLine={{ stroke: '#e5e7eb' }}
              />
            </>
          )}
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
              boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
            }}
            labelStyle={{ color: '#374151', fontWeight: 600 }}
            cursor={{ fill: 'rgba(99, 102, 241, 0.1)' }}
          />
          {showLegend && (
            <Legend
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="rect"
            />
          )}
          {bars.map((bar, index) => {
            const color = bar.fill || colors[index % colors.length];
            return (
              <Bar
                key={bar.dataKey}
                dataKey={bar.dataKey}
                fill={color}
                name={bar.name || bar.dataKey}
                stackId={stacked ? (bar.stackId || 'stack') : undefined}
                radius={stacked ? undefined : [4, 4, 0, 0]}
              />
            );
          })}
        </RechartsBarChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default BarChart;
