/**
 * Metrics cards component for dashboard
 */

import React from "react";
import { MetricCard } from "../common/MetricCard";

export const MetricsCards = ({ stats }) => {
  const metrics = [
    {
      title: "Total Members",
      value: stats?.total_members?.toLocaleString(),
      icon: "users",
      color: "blue"
    },
    {
      title: "Total Loans", 
      value: stats?.total_loans?.toLocaleString(),
      icon: "money",
      color: "green"
    },
    {
      title: "NPL Loans",
      value: stats?.total_npl_loans?.toLocaleString(),
      icon: "warning",
      color: "red"
    },
    {
      title: "Recovery Rate",
      value: `${stats?.recovery_rate_percent?.toFixed(1)}%`,
      icon: "chart",
      color: "yellow"
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {metrics.map((metric, index) => (
        <MetricCard key={index} {...metric} />
      ))}
    </div>
  );
};

