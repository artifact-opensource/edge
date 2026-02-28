import React from 'react';
import {
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from 'recharts';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface PieChartProps {
  data: any[];
  dataKey: string;
  nameKey: string;
  title?: string;
  description?: string;
  height?: number;
  showLegend?: boolean;
  donut?: boolean;
  colors?: string[];
  loading?: boolean;
}

const PieChart: React.FC<PieChartProps> = ({
  data,
  dataKey,
  nameKey,
  title,
  description,
  height = 400,
  showLegend = true,
  donut = false,
  colors,
  loading = false,
}) => {
  const defaultColors = [
    '#6366f1',
    '#10b981',
    '#f59e0b',
    '#ef4444',
    '#8b5cf6',
    '#ec4899',
    '#14b8a6',
    '#f97316',
    '#06b6d4',
    '#84cc16',
  ];

  const chartColors = colors || defaultColors;

  const renderCustomLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: any) => {
    const RADIAN = Math.PI / 180;
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5;
    const x = cx + radius * Math.cos(-midAngle * RADIAN);
    const y = cy + radius * Math.sin(-midAngle * RADIAN);

    if (percent < 0.05) return null;

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
        className="text-xs font-semibold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    );
  };

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
        <RechartsPieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomLabel}
            outerRadius={donut ? 120 : 140}
            innerRadius={donut ? 80 : 0}
            fill="#8884d8"
            dataKey={dataKey}
            nameKey={nameKey}
          >
            {data.map((_item, index) => (
              <Cell
                key={`cell-${index}`}
                fill={chartColors[index % chartColors.length]}
              />
            ))}
          </Pie>
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
              verticalAlign="bottom"
              height={36}
              iconType="circle"
            />
          )}
        </RechartsPieChart>
      </ResponsiveContainer>
    </Card>
  );
};

export default PieChart;
