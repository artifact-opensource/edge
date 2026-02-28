import React from 'react';
import clsx from 'clsx';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  InformationCircleIcon,
  XCircleIcon,
} from '@heroicons/react/24/outline';

export interface AlertProps {
  variant?: 'info' | 'success' | 'warning' | 'danger';
  title?: string;
  children: React.ReactNode;
  onClose?: () => void;
}

const Alert: React.FC<AlertProps> = ({
  variant = 'info',
  title,
  children,
  onClose,
}) => {
  const variants = {
    info: {
      container: 'bg-blue-50 border-blue-200',
      icon: 'text-blue-400',
      title: 'text-blue-800',
      text: 'text-blue-700',
      Icon: InformationCircleIcon,
    },
    success: {
      container: 'bg-success-50 border-success-200',
      icon: 'text-success-400',
      title: 'text-success-800',
      text: 'text-success-700',
      Icon: CheckCircleIcon,
    },
    warning: {
      container: 'bg-warning-50 border-warning-200',
      icon: 'text-warning-400',
      title: 'text-warning-800',
      text: 'text-warning-700',
      Icon: ExclamationTriangleIcon,
    },
    danger: {
      container: 'bg-danger-50 border-danger-200',
      icon: 'text-danger-400',
      title: 'text-danger-800',
      text: 'text-danger-700',
      Icon: XCircleIcon,
    },
  };

  const { container, icon, title: titleColor, text, Icon } = variants[variant];

  return (
    <div className={clsx('rounded-lg border p-4', container)}>
      <div className="flex">
        <div className="flex-shrink-0">
          <Icon className={clsx('h-5 w-5', icon)} aria-hidden="true" />
        </div>
        <div className="ml-3 flex-1">
          {title && (
            <h3 className={clsx('text-sm font-medium', titleColor)}>{title}</h3>
          )}
          <div className={clsx('text-sm', title ? 'mt-2' : '', text)}>
            {children}
          </div>
        </div>
        {onClose && (
          <div className="ml-auto pl-3">
            <button
              type="button"
              className={clsx('inline-flex rounded-md p-1.5 focus:outline-none focus:ring-2 focus:ring-offset-2', text)}
              onClick={onClose}
            >
              <span className="sr-only">Dismiss</span>
              <XCircleIcon className="h-5 w-5" aria-hidden="true" />
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Alert;
