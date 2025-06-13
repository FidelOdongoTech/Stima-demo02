/**
 * Financial overview component for dashboard
 */

import React from "react";

export const FinancialOverview = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Outstanding Amounts</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Total Outstanding</span>
            <span className="text-xl font-semibold text-gray-900">
              KES {(stats?.total_outstanding_amount / 1000000).toFixed(1)}M
            </span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Total Arrears</span>
            <span className="text-xl font-semibold text-red-600">
              KES {(stats?.total_arrears_amount / 1000000).toFixed(1)}M
            </span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Today's Activity</h3>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Calls Made</span>
            <span className="text-xl font-semibold text-blue-600">{stats?.calls_today}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Promises Due</span>
            <span className="text-xl font-semibold text-yellow-600">{stats?.promises_due_today}</span>
          </div>
          <div className="flex justify-between items-center">
            <span className="text-gray-600">Escalations Pending</span>
            <span className="text-xl font-semibold text-red-600">{stats?.escalations_pending}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

