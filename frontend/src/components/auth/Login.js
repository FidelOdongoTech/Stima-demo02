/**
 * Login component for user authentication
 */

import React, { useState } from "react";
import { AuthLogo } from "./AuthLogo";
import { DemoCredentials } from "./DemoCredentials";

const Login = ({ onLogin }) => {
  const [credentials, setCredentials] = useState({ username: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    // Simulate authentication (in real system, this would call an API)
    setTimeout(() => {
      if (credentials.username && credentials.password) {
        // Demo credentials - in real system, validate against backend
        const validCredentials = [
          { username: "admin", password: "admin123", role: "admin", name: "System Administrator" },
          { username: "agent", password: "agent123", role: "agent", name: "Collection Agent" },
          { username: "manager", password: "manager123", role: "manager", name: "Branch Manager" }
        ];

        const user = validCredentials.find(
          u => u.username === credentials.username && u.password === credentials.password
        );

        if (user) {
          const authData = {
            user: { 
              id: user.username + "_id",
              username: user.username,
              name: user.name,
              role: user.role
            },
            token: "mock_jwt_token_" + Date.now()
          };
          localStorage.setItem("auth", JSON.stringify(authData));
          onLogin(authData);
        } else {
          setError("Invalid username or password");
        }
      } else {
        setError("Please enter both username and password");
      }
      setLoading(false);
    }, 1000);
  };

  const handleInputChange = (field, value) => {
    setCredentials(prev => ({ ...prev, [field]: value }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-700 to-indigo-800 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-2xl p-8 w-full max-w-md">
        <AuthLogo />

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              type="text"
              value={credentials.username}
              onChange={(e) => handleInputChange("username", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your username"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              type="password"
              value={credentials.password}
              onChange={(e) => handleInputChange("password", e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your password"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white py-2 px-4 rounded-lg font-medium transition-colors"
          >
            {loading ? "Signing In..." : "Sign In"}
          </button>
        </form>

        <DemoCredentials />
      </div>
    </div>
  );
};

export default Login;

