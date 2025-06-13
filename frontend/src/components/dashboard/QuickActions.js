/**
 * Quick actions component for dashboard
 */

import React from "react";
import { Link } from "react-router-dom";

export const QuickActions = () => {
  const actions = [
    { to: "/call-center", icon: "📞", label: "Call Center", color: "blue" },
    { to: "/loans", icon: "💰", label: "NPL Loans", color: "green" },
    { to: "/promises", icon: "🤝", label: "Promises", color: "yellow" },
    { to: "/partners", icon: "🏢", label: "Partners", color: "purple" },
    { to: "/reports", icon: "📊", label: "Reports", color: "indigo" },
    { to: "/notifications", icon: "🔔", label: "Notifications", color: "red" }
  ];

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
      <div className="grid grid-cols-2 md:grid-cols-6 gap-4">
        {actions.map((action, index) => (
          <Link 
            key={index}
            to={action.to} 
            className={`bg-${action.color}-50 hover:bg-${action.color}-100 p-4 rounded-lg text-center transition-colors`}
          >
            <div className={`text-${action.color}-600 mb-2`}>{action.icon}</div>
            <div className={`text-sm font-medium text-${action.color}-600`}>{action.label}</div>
          </Link>
        ))}
      </div>
    </div>
  );
};

