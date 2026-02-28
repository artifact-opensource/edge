import React from 'react';
import Card from '../../components/common/Card';
import Avatar from '../../components/common/Avatar';
import Badge from '../../components/common/Badge';

const ProfilePage: React.FC = () => {
  const user = { name: 'John Doe', email: 'john@example.com', tier: 'Executive', company: 'Artifact Virtual', joinedAt: 'January 2024' };
  return (
    <div className="space-y-6">
      <div><h1 className="text-3xl font-bold text-gray-900">Profile</h1><p className="mt-2 text-sm text-gray-700">Manage your account information</p></div>
      <Card padding="lg">
        <div className="flex items-center gap-6">
          <Avatar name={user.name} size="xl" />
          <div className="flex-1">
            <h2 className="text-2xl font-bold text-gray-900">{user.name}</h2>
            <p className="text-gray-600">{user.email}</p>
            <div className="mt-2 flex gap-2"><Badge variant="primary">{user.tier} Tier</Badge><Badge variant="default">{user.company}</Badge></div>
          </div>
        </div>
        <div className="mt-8 space-y-4"><div><h3 className="text-sm font-medium text-gray-500">Member Since</h3><p className="mt-1 text-sm text-gray-900">{user.joinedAt}</p></div></div>
      </Card>
    </div>
  );
};

export default ProfilePage;
