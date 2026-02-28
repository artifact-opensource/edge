import React from 'react';
import Card from '../../components/common/Card';
import EmptyState from '../../components/common/EmptyState';
import { DocumentTextIcon } from '@heroicons/react/24/outline';

const DocumentsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Documents</h1>
          <p className="mt-2 text-sm text-gray-700">Access and manage your stakeholder documents</p>
        </div>
      </div>
      <Card padding="lg">
        <EmptyState icon={DocumentTextIcon} title="No documents yet" description="Documents will appear here once they are uploaded" />
      </Card>
    </div>
  );
};

export default DocumentsPage;
