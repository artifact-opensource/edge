import { forwardRef } from 'react';
import type { InputHTMLAttributes } from 'react';
import clsx from 'clsx';

export interface CheckboxProps extends InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
}

const Checkbox = forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, helperText, error, className, id, ...props }, ref) => {
    const checkboxId = id || `checkbox-${Math.random().toString(36).substr(2, 9)}`;

    return (
      <div className="flex items-start">
        <div className="flex h-5 items-center">
          <input
            ref={ref}
            id={checkboxId}
            type="checkbox"
            className={clsx(
              'h-4 w-4 rounded border-gray-300 text-primary-600 focus:ring-primary-500',
              className
            )}
            {...props}
          />
        </div>
        {(label || helperText || error) && (
          <div className="ml-3 text-sm">
            {label && (
              <label htmlFor={checkboxId} className="font-medium text-gray-700">
                {label}
              </label>
            )}
            {helperText && !error && (
              <p className="text-gray-500">{helperText}</p>
            )}
            {error && <p className="text-danger-600">{error}</p>}
          </div>
        )}
      </div>
    );
  }
);

Checkbox.displayName = 'Checkbox';

export default Checkbox;
