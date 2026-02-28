import React from 'react';
import clsx from 'clsx';

export interface AvatarProps {
  src?: string;
  alt?: string;
  name?: string;
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
  className?: string;
}

const Avatar: React.FC<AvatarProps> = ({
  src,
  alt,
  name,
  size = 'md',
  className,
}) => {
  const sizes = {
    xs: 'h-6 w-6 text-xs',
    sm: 'h-8 w-8 text-sm',
    md: 'h-10 w-10 text-base',
    lg: 'h-12 w-12 text-lg',
    xl: 'h-16 w-16 text-2xl',
  };

  const getInitials = (name: string) => {
    const parts = name.trim().split(' ');
    if (parts.length >= 2) {
      return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
    }
    return name.substring(0, 2).toUpperCase();
  };

  return (
    <div
      className={clsx(
        'inline-flex items-center justify-center rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white font-medium',
        sizes[size],
        className
      )}
    >
      {src ? (
        <img
          src={src}
          alt={alt || name || 'Avatar'}
          className="h-full w-full rounded-full object-cover"
        />
      ) : (
        <span>{name ? getInitials(name) : '?'}</span>
      )}
    </div>
  );
};

export default Avatar;
