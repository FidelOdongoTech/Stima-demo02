/**
 * API service for handling HTTP requests
 */

import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE_URL = `${BACKEND_URL}/api`;

class ApiService {
  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });

    // Add request interceptor for authentication
    this.client.interceptors.request.use(
      (config) => {
        const auth = localStorage.getItem("auth");
        if (auth) {
          const { token } = JSON.parse(auth);
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized access
          localStorage.removeItem("auth");
          window.location.href = "/login";
        }
        return Promise.reject(error);
      }
    );
  }

  // Dashboard endpoints
  getDashboardStats() {
    return this.client.get("/dashboard/stats");
  }

  // Member endpoints
  getMembers(params = {}) {
    return this.client.get("/members", { params });
  }

  getMember(memberId) {
    return this.client.get(`/members/${memberId}`);
  }

  createMember(memberData) {
    return this.client.post("/members", memberData);
  }

  // Loan endpoints
  getLoans(params = {}) {
    return this.client.get("/loans", { params });
  }

  getLoan(loanId) {
    return this.client.get(`/loans/${loanId}`);
  }

  getMemberLoans(memberId) {
    return this.client.get(`/loans/member/${memberId}`);
  }

  createLoan(loanData) {
    return this.client.post("/loans", loanData);
  }
}

export const apiService = new ApiService();

