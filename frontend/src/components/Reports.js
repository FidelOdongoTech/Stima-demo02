import React, { useState, useEffect } from "react";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Reports = () => {
  const [nplSummary, setNplSummary] = useState([]);
  const [collectionPerformance, setCollectionPerformance] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeReport, setActiveReport] = useState("npl");

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      const [nplResponse, collectionResponse] = await Promise.all([
        axios.get(`${API}/reports/npl-summary`),
        axios.get(`${API}/reports/collection-performance`)
      ]);
      
      setNplSummary(nplResponse.data);
      setCollectionPerformance(collectionResponse.data);
    } catch (error) {
      console.error("Error fetching reports:", error);
    } finally {
      setLoading(false);
    }
  };

  const exportReport = (reportType) => {
    const data = reportType === "npl" ? nplSummary : collectionPerformance;
    const csv = convertToCSV(data);
    downloadCSV(csv, `${reportType}-report-${new Date().toISOString().split('T')[0]}.csv`);
  };

  const convertToCSV = (data) => {
    if (!data.length) return "";
    
    const headers = Object.keys(data[0]).join(",");
    const rows = data.map(row => Object.values(row).join(","));
    return [headers, ...rows].join("\n");
  };

  const downloadCSV = (csv, filename) => {
    const blob = new Blob([csv], { type: "text/csv" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.setAttribute("hidden", "");
    a.setAttribute("href", url);
    a.setAttribute("download", filename);
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Reports & Analytics</h1>
        
        {/* Report Type Selector */}
        <div className="border-b border-gray-200 mb-6">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveReport("npl")}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeReport === "npl"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              NPL Summary
            </button>
            <button
              onClick={() => setActiveReport("collection")}
              className={`py-2 px-1 border-b-2 font-medium text-sm ${
                activeReport === "collection"
                  ? "border-blue-500 text-blue-600"
                  : "border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300"
              }`}
            >
              Collection Performance
            </button>
          </nav>
        </div>
      </div>

      {/* NPL Summary Report */}
      {activeReport === "npl" && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-900">NPL Summary by Branch</h2>
            <button
              onClick={() => exportReport("npl")}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
            >
              Export CSV
            </button>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Branch Code
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Total NPL Loans
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Outstanding Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Arrears Amount
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Avg Days in Arrears
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {nplSummary.map((branch) => (
                  <tr key={branch._id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      Branch {branch._id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {branch.total_loans.toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      KES {(branch.total_outstanding / 1000000).toFixed(2)}M
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-red-600">
                      KES {(branch.total_arrears / 1000000).toFixed(2)}M
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {Math.round(branch.avg_days_arrears)} days
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Collection Performance Report */}
      {activeReport === "collection" && (
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 flex justify-between items-center">
            <h2 className="text-lg font-medium text-gray-900">Collection Performance (Last 30 Days)</h2>
            <button
              onClick={() => exportReport("collection")}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-medium"
            >
              Export CSV
            </button>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {collectionPerformance.map((item) => (
                <div key={item._id} className="bg-gray-50 rounded-lg p-4">
                  <div className="text-center">
                    <h3 className="text-lg font-semibold text-gray-900 capitalize">
                      {item._id.replace('_', ' ')} Promises
                    </h3>
                    <p className="text-3xl font-bold text-blue-600 mt-2">
                      {item.count}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      KES {(item.total_amount / 1000000).toFixed(2)}M
                    </p>
                  </div>
                </div>
              ))}
            </div>
            
            {/* Performance Metrics */}
            <div className="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="bg-green-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-green-800 mb-4">Success Metrics</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-green-700">Promise Kept Rate</span>
                    <span className="font-semibold text-green-800">
                      {collectionPerformance.length > 0 ? 
                        ((collectionPerformance.find(p => p._id === 'kept')?.count || 0) / 
                         collectionPerformance.reduce((sum, p) => sum + p.count, 0) * 100).toFixed(1)
                        : 0}%
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-green-700">Total Recovery Amount</span>
                    <span className="font-semibold text-green-800">
                      KES {((collectionPerformance.find(p => p._id === 'kept')?.total_amount || 0) / 1000000).toFixed(2)}M
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="bg-yellow-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-yellow-800 mb-4">Areas for Improvement</h3>
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-yellow-700">Broken Promises</span>
                    <span className="font-semibold text-yellow-800">
                      {collectionPerformance.find(p => p._id === 'broken')?.count || 0}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-yellow-700">Pending Follow-up</span>
                    <span className="font-semibold text-yellow-800">
                      {collectionPerformance.find(p => p._id === 'pending')?.count || 0}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Reports;
