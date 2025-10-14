/**
 * API Client Configuration
 * Central axios instance for all API calls
 */

import axios, { AxiosInstance, AxiosError } from 'axios';
import { getApiUrl } from '../utils/env';

// Create axios instance with default configuration
export const apiClient: AxiosInstance = axios.create({
  baseURL: getApiUrl(),
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add auth token to requests
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor - Handle common errors
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle 401 Unauthorized - clear token and redirect to login
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      localStorage.removeItem('user');
      // Only redirect if not already on login/register pages
      if (!window.location.pathname.match(/^\/(login|register)/)) {
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

/**
 * API Error type for structured error handling
 */
export interface ApiError {
  message: string;
  field?: string;
  code?: string;
}

/**
 * Extract error message from axios error
 */
export const getErrorMessage = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    // Backend validation error with field-specific messages
    if (error.response?.data?.detail) {
      const detail = error.response.data.detail;
      if (typeof detail === 'string') {
        return detail;
      }
      if (Array.isArray(detail) && detail.length > 0) {
        return detail[0].msg || detail[0].message || 'Validation error';
      }
    }

    // Generic backend error
    if (error.response?.data?.message) {
      return error.response.data.message;
    }

    // Network errors
    if (error.code === 'ECONNABORTED') {
      return 'Request timeout. Please try again.';
    }

    if (!error.response) {
      return 'Network error. Please check your connection.';
    }

    // HTTP status errors
    switch (error.response.status) {
      case 400:
        return 'Invalid request. Please check your input.';
      case 401:
        return 'Unauthorized. Please log in again.';
      case 403:
        return 'Access forbidden.';
      case 404:
        return 'Resource not found.';
      case 409:
        return 'This resource already exists.';
      case 422:
        return 'Validation error. Please check your input.';
      case 500:
        return 'Server error. Please try again later.';
      default:
        return `Error: ${error.response.status}`;
    }
  }

  if (error instanceof Error) {
    return error.message;
  }

  return 'An unexpected error occurred.';
};

/**
 * Validation error detail structure
 */
interface ValidationErrorDetail {
  loc: string[];
  msg?: string;
  message?: string;
}

/**
 * Extract field-specific errors from axios error
 */
export const getFieldErrors = (
  error: unknown
): Record<string, string> | null => {
  if (axios.isAxiosError(error)) {
    if (
      error.response?.data?.detail &&
      Array.isArray(error.response.data.detail)
    ) {
      const fieldErrors: Record<string, string> = {};
      error.response.data.detail.forEach((err: ValidationErrorDetail) => {
        if (err.loc && err.loc.length > 1) {
          const field = err.loc[err.loc.length - 1];
          fieldErrors[field] = err.msg || err.message || 'Invalid value';
        }
      });
      return Object.keys(fieldErrors).length > 0 ? fieldErrors : null;
    }
  }
  return null;
};
