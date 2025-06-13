/**
 * Authentication logo component
 */

import React from "react";

export const AuthLogo = () => {
  return (
    <div className="text-center mb-8">
      <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            strokeWidth="2" 
            d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"
          />
        </svg>
      </div>
      <h1 className="text-2xl font-bold text-gray-900">Stima Sacco</h1>
      <p className="text-gray-600">Debt Management System</p>
    </div>
  );
};

