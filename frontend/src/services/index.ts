// API services and external integrations
export { apiClient, getErrorMessage, getFieldErrors } from './apiClient';
export type { ApiError } from './apiClient';
export { authService } from './authService';
export type {
  RegisterRequest,
  RegisterResponse,
  LoginRequest,
  LoginResponse,
  User,
} from './authService';
