import React from 'react';
import clsx from 'clsx';

export interface SkeletonProps {
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  className?: string;
}

const Skeleton: React.FC<SkeletonProps> = ({
  variant = 'text',
  width,
  height,
  className,
}) => {
  const baseStyles = 'animate-pulse bg-gray-200';

  const variants = {
    text: 'rounded h-4',
    circular: 'rounded-full',
    rectangular: 'rounded',
  };

  const style: React.CSSProperties = {};
  if (width) style.width = typeof width === 'number' ? `${width}px` : width;
  if (height) style.height = typeof height === 'number' ? `${height}px` : height;

  return (
    <div
      className={clsx(baseStyles, variants[variant], className)}
      style={style}
    />
  );
};

export const SkeletonCard: React.FC = () => {
  return (
    <div className="rounded-lg bg-white p-6 shadow-sm border border-gray-200">
      <div className="flex items-center space-x-4">
        <Skeleton variant="circular" width={40} height={40} />
        <div className="flex-1 space-y-2">
          <Skeleton width="60%" />
          <Skeleton width="40%" />
        </div>
      </div>
      <div className="mt-4 space-y-2">
        <Skeleton />
        <Skeleton />
        <Skeleton width="80%" />
      </div>
    </div>
  );
};

export const SkeletonTable: React.FC<{ rows?: number }> = ({ rows = 5 }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center space-x-4">
          <Skeleton variant="circular" width={32} height={32} />
          <Skeleton className="flex-1" />
          <Skeleton width={100} />
          <Skeleton width={80} />
        </div>
      ))}
    </div>
  );
};

export default Skeleton;
