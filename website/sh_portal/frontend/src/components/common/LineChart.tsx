import React from 'react';
import {
  LineChart as RechartsLineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Brush,
  Area,
  AreaChart as RechartsAreaChart,
} from 'recharts';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface LineChartProps {
  data: any[];
  lines: {
    dataKey: string;
    stroke?: string;
    name?: string;
    strokeWidth?: number;
  }[];
  xAxisKey: string;
  title?: string;
  description?: string;
  height?: number;
  showGrid?: boolean;
  showLegend?: boolean;
  showBrush?: boolean;
  curved?: boolean;
  filled?: boolean;
  loading?: boolean;
}

const LineChart: React.FC<LineChartProps> = ({
  data,
  lines,
  xAxisKey,
  title,
  description,
  height = 400,
  showGrid = true,
  showLegend = true,
  showBrush = false,
  curved = true,
  filled = false,
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

  const ChartComponent = filled ? RechartsAreaChart : RechartsLineChart;

  return (
    <Card>
      {(title || description) && (
        <CardHeader>
          {title && <CardTitle>{title}</CardTitle>}
          {description && <CardDescription>{description}</CardDescription>}
        </CardHeader>
      )}
      <ResponsiveContainer width="100%" height={height}>
        <ChartComponent
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
              iconType="line"
            />
          )}
          {lines.map((line, index) => {
            const color = line.stroke || colors[index % colors.length];
            if (filled) {
              return (
                <Area
                  key={line.dataKey}
                  type={curved ? 'monotone' : 'linear'}
                  dataKey={line.dataKey}
                  stroke={color}
                  fill={color}
                  fillOpacity={0.2}
                  strokeWidth={line.strokeWidth || 2}
                  name={line.name || line.dataKey}
                  activeDot={{ r: 6 }}
                />
              );
            }
            return (
              <Line
                key={line.dataKey}
                type={curved ? 'monotone' : 'linear'}
                dataKey={line.dataKey}
                stroke={color}
                strokeWidth={line.strokeWidth || 2}
                name={line.name || line.dataKey}
                activeDot={{ r: 6 }}
                dot={{ r: 3 }}
              />
            );
          })}
          {showBrush && (
            <Brush
              dataKey={xAxisKey}
              height={30}
              stroke="#6366f1"
              fill="#f3f4f6"
            />
          )}
        </ChartComponent>
      </ResponsiveContainer>
    </Card>
  );
};

export default LineChart;
