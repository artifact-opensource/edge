import React from 'react';
import Card, { CardHeader, CardTitle } from '../../components/common/Card';

const SettingsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold text-gray-900">Settings</h1><p className="mt-2 text-sm text-gray-700">Manage your preferences and account settings</p></div>
      <div className="grid gap-6">
        <Card><CardHeader><CardTitle>Notifications</CardTitle></CardHeader><div className="space-y-4"><p className="text-sm text-gray-500">Notification settings will appear here</p></div></Card>
        <Card><CardHeader><CardTitle>Security</CardTitle></CardHeader><div className="space-y-4"><p className="text-sm text-gray-500">Security settings including 2FA will appear here</p></div></Card>
        <Card><CardHeader><CardTitle>Appearance</CardTitle></CardHeader><div className="space-y-4"><p className="text-sm text-gray-500">Theme and display preferences will appear here</p></div></Card>
      </div>
    </div>
  );
};

export default SettingsPage;
