import React from 'react';
import {
  AreaChart as RechartsAreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface AreaChartProps {
  data: any[];
  areas: {
    dataKey: string;
    fill?: string;
    stroke?: string;
    name?: string;
    stackId?: string;
  }[];
  xAxisKey: string;
  title?: string;
  description?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  stacked?: boolean;
  loading?: boolean;
}

const AreaChart: React.FC<AreaChartProps> = ({
  data,
  areas,
  xAxisKey,
  title,
  description,
  height = 400,
  showGrid = true,
  showLegend = true,
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
        <RechartsAreaChart
          data={data}
          margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
        >
          {showGrid && <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />}
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
          <Tooltip
            contentStyle={{
              backgroundColor: '#fff',
              border: '1px solid #e5e7eb',
              borderRadius: '0.5rem',
              boxShadow: '0 1px 3px 0 rgb(0 0 0 / 0.1)',
            }}
            labelStyle={{ color: '#374151', fontWeight: 600 }}
          />
          {showLegend && (
            <Legend
              wrapperStyle={{ paddingTop: '20px' }}
              iconType="rect"
            />
          )}
          {areas.map((area, index) => {
            const color = area.fill || colors[index % colors.length];
            return (
              <Area
                key={area.dataKey}
                type="monotone"
                dataKey={area.dataKey}
                stackId={stacked ? (area.stackId || 'stack') : undefined}
                stroke={area.stroke || color}
                fill={color}
                fillOpacity={0.6}
                name={area.name || area.dataKey}
              />
            );
          })}
        </RechartsAreaChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default AreaChart;
