import React from 'react';
import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid';
import clsx from 'clsx';
import Card from './Card';

export interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  changeLabel?: string;
  icon?: React.ComponentType<{ className?: string }>;
  trend?: 'up' | 'down' | 'neutral';
  subtitle?: string;
  loading?: boolean;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  change,
  changeLabel,
  icon: Icon,
  trend,
  subtitle,
  loading = false,
}) => {
  const getTrendColor = () => {
    if (!trend) return '';
    return trend === 'up' ? 'text-green-600' : trend === 'down' ? 'text-red-600' : 'text-gray-600';
  };

  const getTrendBgColor = () => {
    if (!trend) return '';
    return trend === 'up' ? 'bg-green-50' : trend === 'down' ? 'bg-red-50' : 'bg-gray-50';
  };

  return (
    <Card className="relative overflow-hidden" hover>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          {loading ? (
            <div className="mt-2 h-8 w-24 animate-pulse rounded bg-gray-200" />
          ) : (
            <p className="mt-2 text-3xl font-bold text-gray-900">{value}</p>
          )}
          {subtitle && <p className="mt-1 text-xs text-gray-500">{subtitle}</p>}
        </div>
        {Icon && (
          <div className="flex h-12 w-12 items-center justify-center rounded-lg bg-indigo-50">
            <Icon className="h-6 w-6 text-indigo-600" aria-hidden="true" />
          </div>
        )}
      </div>
      {change !== undefined && !loading && (
        <div className="mt-4 flex items-center">
          <span
            className={clsx(
              'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
              getTrendBgColor(),
              getTrendColor()
            )}
          >
            {trend === 'up' && <ArrowUpIcon className="mr-1 h-3 w-3" aria-hidden="true" />}
            {trend === 'down' && <ArrowDownIcon className="mr-1 h-3 w-3" aria-hidden="true" />}
            {change > 0 ? '+' : ''}
            {change}%
          </span>
          {changeLabel && <span className="ml-2 text-sm text-gray-500">{changeLabel}</span>}
        </div>
      )}
    </Card>
  );
};

export default MetricCard;
