import React from 'react';
import { Menu } from '@headlessui/react';
import {
  Bars3Icon,
  BellIcon,
} from '@heroicons/react/24/outline';
import { Link } from 'react-router-dom';
import clsx from 'clsx';
import Avatar from '../common/Avatar';

interface HeaderProps {
  onMenuClick: () => void;
}

const Header: React.FC<HeaderProps> = ({ onMenuClick }) => {
  // Mock user data - will be replaced with real data from auth store
  const user = {
    name: 'John Doe',
    email: 'john@example.com',
    avatar: '',
  };

  return (
    <header className="sticky top-0 z-40 bg-white shadow-sm">
      <div className="flex h-16 items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Mobile menu button */}
        <button
          type="button"
          className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
          onClick={onMenuClick}
        >
          <span className="sr-only">Open sidebar</span>
          <Bars3Icon className="h-6 w-6" aria-hidden="true" />
        </button>

        {/* Search bar - placeholder */}
        <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
          <div className="relative flex flex-1 items-center">
            {/* Search input placeholder */}
          </div>
        </div>

        {/* Right side - Notifications and Profile */}
        <div className="flex items-center gap-x-4 lg:gap-x-6">
          {/* Notifications */}
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-400 hover:text-gray-500"
          >
            <span className="sr-only">View notifications</span>
            <BellIcon className="h-6 w-6" aria-hidden="true" />
          </button>

          {/* Profile dropdown */}
          <Menu as="div" className="relative">
            <Menu.Button className="-m-1.5 flex items-center p-1.5">
              <span className="sr-only">Open user menu</span>
              <Avatar name={user.name} src={user.avatar} size="sm" />
              <span className="hidden lg:flex lg:items-center">
                <span
                  className="ml-4 text-sm font-semibold leading-6 text-gray-900"
                  aria-hidden="true"
                >
                  {user.name}
                </span>
              </span>
            </Menu.Button>
            <Menu.Items className="absolute right-0 z-10 mt-2.5 w-48 origin-top-right rounded-md bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
              <Menu.Item>
                {({ active }) => (
                  <Link
                    to="/profile"
                    className={clsx(
                      active ? 'bg-gray-50' : '',
                      'block px-3 py-1 text-sm leading-6 text-gray-900'
                    )}
                  >
                    Your profile
                  </Link>
                )}
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <Link
                    to="/settings"
                    className={clsx(
                      active ? 'bg-gray-50' : '',
                      'block px-3 py-1 text-sm leading-6 text-gray-900'
                    )}
                  >
                    Settings
                  </Link>
                )}
              </Menu.Item>
              <Menu.Item>
                {({ active }) => (
                  <button
                    className={clsx(
                      active ? 'bg-gray-50' : '',
                      'block w-full text-left px-3 py-1 text-sm leading-6 text-gray-900'
                    )}
                    onClick={() => {
                      // Handle sign out
                      console.log('Sign out');
                    }}
                  >
                    Sign out
                  </button>
                )}
              </Menu.Item>
            </Menu.Items>
          </Menu>
        </div>
      </div>
    </header>
  );
};

export default Header;
