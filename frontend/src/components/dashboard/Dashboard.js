/**
 * Main dashboard component
 */

import React, { useState, useEffect } from "react";
import { DashboardHeader } from "./DashboardHeader";
import { MetricsCards } from "./MetricsCards";
import { FinancialOverview } from "./FinancialOverview";
import { QuickActions } from "./QuickActions";
import { LoadingSpinner } from "../common/LoadingSpinner";
import { apiService } from "../../services/apiService";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await apiService.getDashboardStats();
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching dashboard stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="p-6">
      <DashboardHeader />
      <MetricsCards stats={stats} />
      <FinancialOverview stats={stats} />
      <QuickActions />
    </div>
  );
};

export default Dashboard;

