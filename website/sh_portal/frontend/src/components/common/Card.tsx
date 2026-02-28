import { forwardRef } from 'react';
import type { HTMLAttributes } from 'react';
import clsx from 'clsx';

export interface CardProps extends HTMLAttributes<HTMLDivElement> {
  padding?: 'none' | 'sm' | 'md' | 'lg';
  hover?: boolean;
}

const Card = forwardRef<HTMLDivElement, CardProps>(
  ({ children, padding = 'md', hover = false, className, ...props }, ref) => {
    const paddings = {
      none: '',
      sm: 'p-4',
      md: 'p-6',
      lg: 'p-8',
    };

    return (
      <div
        ref={ref}
        className={clsx(
          'rounded-lg bg-white shadow-sm border border-gray-200',
          paddings[padding],
          hover && 'transition-shadow hover:shadow-md',
          className
        )}
        {...props}
      >
        {children}
      </div>
    );
  }
);

Card.displayName = 'Card';

export const CardHeader = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ children, className, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={clsx('mb-4 border-b border-gray-200 pb-4', className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);

CardHeader.displayName = 'CardHeader';

export const CardTitle = forwardRef<HTMLHeadingElement, HTMLAttributes<HTMLHeadingElement>>(
  ({ children, className, ...props }, ref) => {
    return (
      <h3
        ref={ref}
        className={clsx('text-lg font-semibold text-gray-900', className)}
        {...props}
      >
        {children}
      </h3>
    );
  }
);

CardTitle.displayName = 'CardTitle';

export const CardDescription = forwardRef<HTMLParagraphElement, HTMLAttributes<HTMLParagraphElement>>(
  ({ children, className, ...props }, ref) => {
    return (
      <p
        ref={ref}
        className={clsx('text-sm text-gray-500', className)}
        {...props}
      >
        {children}
      </p>
    );
  }
);

CardDescription.displayName = 'CardDescription';

export default Card;
