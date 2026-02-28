import React from 'react';

export interface TableProps {
  children: React.ReactNode;
}

export const Table: React.FC<TableProps> = ({ children }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">{children}</table>
    </div>
  );
};

export const TableHeader: React.FC<TableProps> = ({ children }) => {
  return <thead className="bg-gray-50">{children}</thead>;
};

export const TableBody: React.FC<TableProps> = ({ children }) => {
  return <tbody className="divide-y divide-gray-200 bg-white">{children}</tbody>;
};

export const TableRow: React.FC<TableProps> = ({ children }) => {
  return <tr className="hover:bg-gray-50">{children}</tr>;
};

export interface TableHeaderCellProps {
  children: React.ReactNode;
  className?: string;
}

export const TableHeaderCell: React.FC<TableHeaderCellProps> = ({
  children,
  className = '',
}) => {
  return (
    <th
      scope="col"
      className={`px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500 ${className}`}
    >
      {children}
    </th>
  );
};

export interface TableCellProps {
  children: React.ReactNode;
  className?: string;
}

export const TableCell: React.FC<TableCellProps> = ({ children, className = '' }) => {
  return <td className={`whitespace-nowrap px-6 py-4 text-sm text-gray-900 ${className}`}>{children}</td>;
};

export default Table;
