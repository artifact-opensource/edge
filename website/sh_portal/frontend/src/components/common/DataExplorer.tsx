import React, { useState } from 'react';
import {
  FunnelIcon,
  XMarkIcon,
  CalendarIcon,
} from '@heroicons/react/24/outline';
import Button from './Button';
import Input from './Input';
import Select from './Select';
import Card from './Card';
import { subDays, subMonths, subYears } from 'date-fns';

export interface Filter {
  id: string;
  field: string;
  operator: 'equals' | 'contains' | 'greaterThan' | 'lessThan' | 'between' | 'in';
  value: any;
}

export interface DataExplorerProps {
  fields: {
    name: string;
    label: string;
    type: 'text' | 'number' | 'date' | 'select';
    options?: { label: string; value: string }[];
  }[];
  dateRanges?: {
    label: string;
    value: string;
    start: Date;
    end: Date;
  }[];
  onFiltersChange?: (filters: Filter[]) => void;
  onDateRangeChange?: (start: Date, end: Date) => void;
  children?: React.ReactNode;
}

const DataExplorer: React.FC<DataExplorerProps> = ({
  fields,
  dateRanges: customDateRanges,
  onFiltersChange,
  onDateRangeChange,
  children,
}) => {
  const [filters, setFilters] = useState<Filter[]>([]);
  const [showFilters, setShowFilters] = useState(false);
  const [selectedDateRange, setSelectedDateRange] = useState('last30days');

  const defaultDateRanges = [
    { label: 'Last 7 Days', value: 'last7days', start: subDays(new Date(), 7), end: new Date() },
    { label: 'Last 30 Days', value: 'last30days', start: subDays(new Date(), 30), end: new Date() },
    { label: 'Last 90 Days', value: 'last90days', start: subDays(new Date(), 90), end: new Date() },
    { label: 'Last 6 Months', value: 'last6months', start: subMonths(new Date(), 6), end: new Date() },
    { label: 'Last Year', value: 'lastyear', start: subYears(new Date(), 1), end: new Date() },
  ];

  const dateRanges = customDateRanges || defaultDateRanges;

  const addFilter = () => {
    const newFilter: Filter = {
      id: `filter-${Date.now()}`,
      field: fields[0]?.name || '',
      operator: 'equals',
      value: '',
    };
    const updatedFilters = [...filters, newFilter];
    setFilters(updatedFilters);
    onFiltersChange?.(updatedFilters);
  };

  const removeFilter = (id: string) => {
    const updatedFilters = filters.filter((f) => f.id !== id);
    setFilters(updatedFilters);
    onFiltersChange?.(updatedFilters);
  };

  const updateFilter = (id: string, updates: Partial<Filter>) => {
    const updatedFilters = filters.map((f) =>
      f.id === id ? { ...f, ...updates } : f
    );
    setFilters(updatedFilters);
    onFiltersChange?.(updatedFilters);
  };

  const handleDateRangeChange = (value: string) => {
    setSelectedDateRange(value);
    const range = dateRanges.find((r) => r.value === value);
    if (range) {
      onDateRangeChange?.(range.start, range.end);
    }
  };

  const operatorOptions = [
    { label: 'Equals', value: 'equals' },
    { label: 'Contains', value: 'contains' },
    { label: 'Greater Than', value: 'greaterThan' },
    { label: 'Less Than', value: 'lessThan' },
    { label: 'Between', value: 'between' },
    { label: 'In', value: 'in' },
  ];

  return (
    <div className="space-y-6">
      {/* Toolbar */}
      <Card>
        <div className="flex flex-wrap items-center gap-4">
          {/* Date Range Selector */}
          <div className="flex items-center gap-2">
            <CalendarIcon className="h-5 w-5 text-gray-400" />
            <Select
              value={selectedDateRange}
              onChange={(e) => handleDateRangeChange(e.target.value)}
              className="w-48"
            >
              {dateRanges.map((range) => (
                <option key={range.value} value={range.value}>
                  {range.label}
                </option>
              ))}
            </Select>
          </div>

          {/* Filter Toggle */}
          <Button
            variant="secondary"
            size="sm"
            onClick={() => setShowFilters(!showFilters)}
            leftIcon={<FunnelIcon className="h-4 w-4" />}
          >
            Filters {filters.length > 0 && `(${filters.length})`}
          </Button>

          {filters.length > 0 && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => {
                setFilters([]);
                onFiltersChange?.([]);
              }}
            >
              Clear All
            </Button>
          )}
        </div>

        {/* Filter Panel */}
        {showFilters && (
          <div className="mt-4 space-y-3 border-t border-gray-200 pt-4">
            {filters.map((filter) => {
              const field = fields.find((f) => f.name === filter.field);
              return (
                <div key={filter.id} className="flex items-center gap-2">
                  <Select
                    value={filter.field}
                    onChange={(e) => updateFilter(filter.id, { field: e.target.value })}
                    className="flex-1"
                  >
                    {fields.map((f) => (
                      <option key={f.name} value={f.name}>
                        {f.label}
                      </option>
                    ))}
                  </Select>

                  <Select
                    value={filter.operator}
                    onChange={(e) =>
                      updateFilter(filter.id, { operator: e.target.value as any })
                    }
                    className="flex-1"
                  >
                    {operatorOptions.map((op) => (
                      <option key={op.value} value={op.value}>
                        {op.label}
                      </option>
                    ))}
                  </Select>

                  {field?.type === 'select' && field.options ? (
                    <Select
                      value={filter.value}
                      onChange={(e) => updateFilter(filter.id, { value: e.target.value })}
                      className="flex-1"
                    >
                      <option value="">Select...</option>
                      {field.options.map((opt) => (
                        <option key={opt.value} value={opt.value}>
                          {opt.label}
                        </option>
                      ))}
                    </Select>
                  ) : (
                    <Input
                      type={field?.type === 'number' ? 'number' : field?.type === 'date' ? 'date' : 'text'}
                      value={filter.value}
                      onChange={(e) => updateFilter(filter.id, { value: e.target.value })}
                      placeholder="Value..."
                      className="flex-1"
                    />
                  )}

                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeFilter(filter.id)}
                    aria-label="Remove filter"
                  >
                    <XMarkIcon className="h-5 w-5" />
                  </Button>
                </div>
              );
            })}

            <Button variant="secondary" size="sm" onClick={addFilter}>
              Add Filter
            </Button>
          </div>
        )}
      </Card>

      {/* Content */}
      {children}
    </div>
  );
};

export default DataExplorer;
