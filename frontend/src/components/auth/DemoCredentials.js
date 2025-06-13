/**
 * Demo credentials display component
 */

import React from "react";

export const DemoCredentials = () => {
  return (
    <div className="mt-8 p-4 bg-gray-50 rounded-lg">
      <h3 className="text-sm font-medium text-gray-700 mb-2">Demo Credentials:</h3>
      <div className="text-xs text-gray-600 space-y-1">
        <div><strong>Admin:</strong> admin / admin123</div>
        <div><strong>Agent:</strong> agent / agent123</div>
        <div><strong>Manager:</strong> manager / manager123</div>
      </div>
    </div>
  );
};

