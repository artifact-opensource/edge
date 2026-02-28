import React from 'react';
import Card, { CardHeader, CardTitle } from '../../components/common/Card';
import Badge from '../../components/common/Badge';
import { ArrowUpIcon, ArrowDownIcon, UsersIcon, DocumentIcon } from '@heroicons/react/24/outline';

const DashboardPage: React.FC = () => {
  const metrics = [
    { name: 'Total Users', value: '2,847', change: '+12.5%', trend: 'up', icon: UsersIcon },
    { name: 'Active Documents', value: '1,234', change: '+8.2%', trend: 'up', icon: DocumentIcon },
    { name: 'Monthly Revenue', value: '$45.2K', change: '-2.4%', trend: 'down', icon: ArrowUpIcon },
    { name: 'Stakeholders', value: '156', change: '+5.1%', trend: 'up', icon: UsersIcon },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-700">Welcome back! Here's what's happening with your stakeholder portal.</p>
      </div>
      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <Card key={metric.name} padding="md" hover>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600">{metric.name}</p>
                <p className="mt-2 text-3xl font-semibold text-gray-900">{metric.value}</p>
                <div className="mt-2 flex items-center gap-2">
                  <Badge variant={metric.trend === 'up' ? 'success' : 'danger'} size="sm">
                    <span className="flex items-center gap-1">
                      {metric.trend === 'up' ? <ArrowUpIcon className="h-3 w-3" /> : <ArrowDownIcon className="h-3 w-3" />}
                      {metric.change}
                    </span>
                  </Badge>
                  <span className="text-xs text-gray-500">vs last month</span>
                </div>
              </div>
              <div className="rounded-full bg-primary-50 p-3">
                <metric.icon className="h-6 w-6 text-primary-600" />
              </div>
            </div>
          </Card>
        ))}
      </div>
      <div className="grid gap-6 lg:grid-cols-2">
        <Card><CardHeader><CardTitle>Recent Activity</CardTitle></CardHeader><div className="space-y-4"><p className="text-sm text-gray-500">No recent activity to display.</p></div></Card>
        <Card><CardHeader><CardTitle>Quick Actions</CardTitle></CardHeader><div className="space-y-4"><p className="text-sm text-gray-500">Quick action buttons will appear here.</p></div></Card>
      </div>
    </div>
  );
};

export default DashboardPage;
