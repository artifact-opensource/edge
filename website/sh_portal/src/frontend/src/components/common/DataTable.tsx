import { useState } from 'react';
import type { ColumnDef, SortingState, ColumnFiltersState } from '@tanstack/react-table';
import {
  useReactTable,
  getCoreRowModel,
  getSortedRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  flexRender,
} from '@tanstack/react-table';
import {
  ChevronUpIcon,
  ChevronDownIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ArrowDownTrayIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import clsx from 'clsx';
import Button from './Button';
import Input from './Input';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export interface DataTableProps<T> {
  data: T[];
  columns: ColumnDef<T, any>[];
  searchable?: boolean;
  searchPlaceholder?: string;
  exportable?: boolean;
  exportFileName?: string;
  loading?: boolean;
  pageSize?: number;
  onRowClick?: (row: T) => void;
}

function DataTable<T>({
  data,
  columns,
  searchable = true,
  searchPlaceholder = 'Search...',
  exportable = true,
  exportFileName = 'data-export',
  loading = false,
  pageSize = 10,
  onRowClick,
}: DataTableProps<T>) {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [globalFilter, setGlobalFilter] = useState('');

  const table = useReactTable({
    data,
    columns,
    state: {
      sorting,
      columnFilters,
      globalFilter,
    },
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    initialState: {
      pagination: {
        pageSize,
      },
    },
  });

  const exportToCSV = () => {
    const rows = table.getFilteredRowModel().rows.map((row) => row.original);
    const csv = [
      columns.map((col: any) => col.header).join(','),
      ...rows.map((row: any) =>
        columns.map((col: any) => {
          const value = col.accessorKey ? (row as any)[col.accessorKey] : '';
          return typeof value === 'string' && value.includes(',') ? `"${value}"` : value;
        }).join(',')
      ),
    ].join('\n');

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);
    link.setAttribute('href', url);
    link.setAttribute('download', `${exportFileName}.csv`);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const exportToExcel = () => {
    const rows = table.getFilteredRowModel().rows.map((row) => row.original);
    const worksheet = XLSX.utils.json_to_sheet(rows);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Data');
    XLSX.writeFile(workbook, `${exportFileName}.xlsx`);
  };

  const exportToPDF = () => {
    const doc = new jsPDF();
    const rows = table.getFilteredRowModel().rows.map((row) => row.original);
    const headers = columns.map((col: any) => col.header);
    const body = rows.map((row: any) =>
      columns.map((col: any) => {
        const value = col.accessorKey ? (row as any)[col.accessorKey] : '';
        return String(value);
      })
    );

    autoTable(doc, {
      head: [headers],
      body,
      theme: 'grid',
      styles: { fontSize: 8 },
    });

    doc.save(`${exportFileName}.pdf`);
  };

  return (
    <div className="space-y-4">
      {/* Toolbar */}
      <div className="flex items-center justify-between gap-4">
        {searchable && (
          <div className="flex-1 max-w-sm">
            <Input
              type="text"
              value={globalFilter ?? ''}
              onChange={(e) => setGlobalFilter(e.target.value)}
              placeholder={searchPlaceholder}
              leftIcon={<MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />}
            />
          </div>
        )}
        {exportable && (
          <div className="flex gap-2">
            <Button
              variant="secondary"
              size="sm"
              onClick={exportToCSV}
              leftIcon={<ArrowDownTrayIcon className="h-4 w-4" />}
            >
              CSV
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={exportToExcel}
              leftIcon={<ArrowDownTrayIcon className="h-4 w-4" />}
            >
              Excel
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={exportToPDF}
              leftIcon={<ArrowDownTrayIcon className="h-4 w-4" />}
            >
              PDF
            </Button>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              {table.getHeaderGroups().map((headerGroup) => (
                <tr key={headerGroup.id}>
                  {headerGroup.headers.map((header) => (
                    <th
                      key={header.id}
                      className="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
                    >
                      {header.isPlaceholder ? null : (
                        <div
                          className={clsx(
                            'flex items-center gap-2',
                            header.column.getCanSort() && 'cursor-pointer select-none'
                          )}
                          onClick={header.column.getToggleSortingHandler()}
                        >
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {header.column.getCanSort() && (
                            <span className="text-gray-400">
                              {header.column.getIsSorted() === 'asc' ? (
                                <ChevronUpIcon className="h-4 w-4" />
                              ) : header.column.getIsSorted() === 'desc' ? (
                                <ChevronDownIcon className="h-4 w-4" />
                              ) : (
                                <div className="h-4 w-4" />
                              )}
                            </span>
                          )}
                        </div>
                      )}
                    </th>
                  ))}
                </tr>
              ))}
            </thead>
            <tbody className="divide-y divide-gray-200 bg-white">
              {loading ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center">
                    <div className="flex justify-center">
                      <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-indigo-600" />
                    </div>
                  </td>
                </tr>
              ) : table.getRowModel().rows.length === 0 ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center text-sm text-gray-500">
                    No data available
                  </td>
                </tr>
              ) : (
                table.getRowModel().rows.map((row) => (
                  <tr
                    key={row.id}
                    onClick={() => onRowClick?.(row.original)}
                    className={clsx(
                      'transition-colors',
                      onRowClick && 'cursor-pointer hover:bg-gray-50'
                    )}
                  >
                    {row.getVisibleCells().map((cell) => (
                      <td key={cell.id} className="whitespace-nowrap px-6 py-4 text-sm text-gray-900">
                        {flexRender(cell.column.columnDef.cell, cell.getContext())}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Pagination */}
      <div className="flex items-center justify-between border-t border-gray-200 bg-white px-4 py-3 sm:px-6">
        <div className="flex flex-1 justify-between sm:hidden">
          <Button
            variant="secondary"
            size="sm"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>
          <Button
            variant="secondary"
            size="sm"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
        <div className="hidden sm:flex sm:flex-1 sm:items-center sm:justify-between">
          <div>
            <p className="text-sm text-gray-700">
              Showing <span className="font-medium">{table.getState().pagination.pageIndex * table.getState().pagination.pageSize + 1}</span> to{' '}
              <span className="font-medium">
                {Math.min((table.getState().pagination.pageIndex + 1) * table.getState().pagination.pageSize, table.getFilteredRowModel().rows.length)}
              </span>{' '}
              of <span className="font-medium">{table.getFilteredRowModel().rows.length}</span> results
            </p>
          </div>
          <div>
            <nav className="isolate inline-flex -space-x-px rounded-md shadow-sm" aria-label="Pagination">
              <button
                onClick={() => table.previousPage()}
                disabled={!table.getCanPreviousPage()}
                className={clsx(
                  'relative inline-flex items-center rounded-l-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0',
                  !table.getCanPreviousPage() && 'cursor-not-allowed opacity-50'
                )}
              >
                <span className="sr-only">Previous</span>
                <ChevronLeftIcon className="h-5 w-5" aria-hidden="true" />
              </button>
              <span className="relative inline-flex items-center px-4 py-2 text-sm font-semibold text-gray-900 ring-1 ring-inset ring-gray-300">
                Page {table.getState().pagination.pageIndex + 1} of {table.getPageCount()}
              </span>
              <button
                onClick={() => table.nextPage()}
                disabled={!table.getCanNextPage()}
                className={clsx(
                  'relative inline-flex items-center rounded-r-md px-2 py-2 text-gray-400 ring-1 ring-inset ring-gray-300 hover:bg-gray-50 focus:z-20 focus:outline-offset-0',
                  !table.getCanNextPage() && 'cursor-not-allowed opacity-50'
                )}
              >
                <span className="sr-only">Next</span>
                <ChevronRightIcon className="h-5 w-5" aria-hidden="true" />
              </button>
            </nav>
          </div>
        </div>
      </div>
    </div>
  );
}

export default DataTable;
