/**
 * Refactored App.js with improved structure and separation of concerns
 */

import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import "./App.css";

// Import components
import { Login, ProtectedRoute } from "./components/auth";
import { Dashboard } from "./components/dashboard";
import Reports from "./components/Reports";
import Notifications from "./components/Notifications";

// Authentication Context
const AuthContext = React.createContext();

const App = () => {
  const [auth, setAuth] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing authentication on app load
    const storedAuth = localStorage.getItem("auth");
    if (storedAuth) {
      try {
        const authData = JSON.parse(storedAuth);
        setAuth(authData);
      } catch (error) {
        console.error("Error parsing stored auth data:", error);
        localStorage.removeItem("auth");
      }
    }
    setLoading(false);
  }, []);

  const handleLogin = (authData) => {
    setAuth(authData);
  };

  const handleLogout = () => {
    localStorage.removeItem("auth");
    setAuth(null);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <AuthContext.Provider value={{ auth, login: handleLogin, logout: handleLogout }}>
      <BrowserRouter>
        <Routes>
          <Route 
            path="/login" 
            element={
              auth ? <Navigate to="/" replace /> : <Login onLogin={handleLogin} />
            } 
          />
          
          <Route 
            path="/" 
            element={
              <ProtectedRoute auth={auth}>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/reports" 
            element={
              <ProtectedRoute auth={auth}>
                <Reports />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/notifications" 
            element={
              <ProtectedRoute auth={auth}>
                <Notifications />
              </ProtectedRoute>
            } 
          />
          
          {/* Redirect any unknown routes to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthContext.Provider>
  );
};

export default App;
export { AuthContext };

