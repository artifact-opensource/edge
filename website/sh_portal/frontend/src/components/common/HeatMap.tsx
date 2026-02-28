import React from 'react';
import Card, { CardHeader, CardTitle, CardDescription } from './Card';

export interface HeatMapProps {
  data: {
    x: string;
    y: string;
    value: number;
  }[];
  title?: string;
  description?: string;
  colorScale?: {
    min: string;
    mid: string;
    max: string;
  };
  height?: number;
  loading?: boolean;
}

const HeatMap: React.FC<HeatMapProps> = ({
  data,
  title,
  description,
  colorScale = {
    min: '#dbeafe',
    mid: '#60a5fa',
    max: '#1e40af',
  },
  height = 400,
  loading = false,
}) => {
  const xLabels = Array.from(new Set(data.map((d) => d.x)));
  const yLabels = Array.from(new Set(data.map((d) => d.y)));

  const getColorForValue = (value: number, min: number, max: number) => {
    const normalized = (value - min) / (max - min);
    
    if (normalized < 0.5) {
      const ratio = normalized * 2;
      return interpolateColor(colorScale.min, colorScale.mid, ratio);
    } else {
      const ratio = (normalized - 0.5) * 2;
      return interpolateColor(colorScale.mid, colorScale.max, ratio);
    }
  };

  const interpolateColor = (color1: string, color2: string, ratio: number) => {
    const hex = (color: string) => {
      const c = color.replace('#', '');
      return {
        r: parseInt(c.substring(0, 2), 16),
        g: parseInt(c.substring(2, 4), 16),
        b: parseInt(c.substring(4, 6), 16),
      };
    };

    const c1 = hex(color1);
    const c2 = hex(color2);

    const r = Math.round(c1.r + (c2.r - c1.r) * ratio);
    const g = Math.round(c1.g + (c2.g - c1.g) * ratio);
    const b = Math.round(c1.b + (c2.b - c1.b) * ratio);

    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
  };

  const values = data.map((d) => d.value);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);

  const getCellValue = (x: string, y: string) => {
    const cell = data.find((d) => d.x === x && d.y === y);
    return cell?.value ?? 0;
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
      <div className="overflow-x-auto">
        <div className="inline-block min-w-full">
          <table className="min-w-full border-collapse">
            <thead>
              <tr>
                <th className="border border-gray-200 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700"></th>
                {xLabels.map((label) => (
                  <th
                    key={label}
                    className="border border-gray-200 bg-gray-50 px-4 py-2 text-center text-sm font-medium text-gray-700"
                  >
                    {label}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {yLabels.map((yLabel) => (
                <tr key={yLabel}>
                  <td className="border border-gray-200 bg-gray-50 px-4 py-2 text-sm font-medium text-gray-700">
                    {yLabel}
                  </td>
                  {xLabels.map((xLabel) => {
                    const value = getCellValue(xLabel, yLabel);
                    const color = getColorForValue(value, minValue, maxValue);
                    return (
                      <td
                        key={`${xLabel}-${yLabel}`}
                        className="group relative border border-gray-200 p-0 transition-all hover:ring-2 hover:ring-indigo-500"
                        style={{ backgroundColor: color }}
                      >
                        <div className="flex h-16 items-center justify-center">
                          <span className="text-sm font-semibold text-gray-800">
                            {value.toFixed(1)}
                          </span>
                        </div>
                        <div className="invisible absolute left-1/2 top-full z-10 mt-2 -translate-x-1/2 whitespace-nowrap rounded-md bg-gray-900 px-3 py-1.5 text-xs text-white shadow-lg group-hover:visible">
                          {xLabel} / {yLabel}: {value.toFixed(2)}
                        </div>
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
      {/* Legend */}
      <div className="mt-6 flex items-center justify-center gap-4">
        <span className="text-sm text-gray-600">Low</span>
        <div className="flex h-4 w-48 overflow-hidden rounded">
          {[...Array(20)].map((_, i) => {
            const ratio = i / 19;
            const color = ratio < 0.5
              ? interpolateColor(colorScale.min, colorScale.mid, ratio * 2)
              : interpolateColor(colorScale.mid, colorScale.max, (ratio - 0.5) * 2);
            return (
              <div
                key={i}
                className="flex-1"
                style={{ backgroundColor: color }}
              />
            );
          })}
        </div>
        <span className="text-sm text-gray-600">High</span>
      </div>
    </Card>
  );
};

export default HeatMap;
