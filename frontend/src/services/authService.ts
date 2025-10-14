/**
 * Authentication Service
 * Handles user registration, login, and authentication state
 */

import { apiClient } from './apiClient';

// Request/Response Types
export interface RegisterRequest {
  email: string;
  password: string;
}

export interface RegisterResponse {
  id: number;
  email: string;
  created_at: string;
  is_active: boolean;
  access_token: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: {
    id: number;
    email: string;
    is_active: boolean;
  };
}

export interface User {
  id: number;
  email: string;
  is_active: boolean;
}

/**
 * Auth Service
 */
export const authService = {
  /**
   * Register a new user
   */
  register: async (data: RegisterRequest): Promise<RegisterResponse> => {
    const response = await apiClient.post<RegisterResponse>(
      '/auth/register',
      data
    );
    return response.data;
  },

  /**
   * Login user
   */
  login: async (data: LoginRequest): Promise<LoginResponse> => {
    const response = await apiClient.post<LoginResponse>('/auth/login', data);
    return response.data;
  },

  /**
   * Logout user
   */
  logout: (): void => {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user');
  },

  /**
   * Store auth token
   */
  setAuthToken: (token: string): void => {
    localStorage.setItem('auth_token', token);
  },

  /**
   * Get stored auth token
   */
  getAuthToken: (): string | null => {
    return localStorage.getItem('auth_token');
  },

  /**
   * Store user data
   */
  setUser: (user: User): void => {
    localStorage.setItem('user', JSON.stringify(user));
  },

  /**
   * Get stored user data
   */
  getUser: (): User | null => {
    const userStr = localStorage.getItem('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated: (): boolean => {
    return !!authService.getAuthToken();
  },
};
