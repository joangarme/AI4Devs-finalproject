import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation } from '@tanstack/react-query';
import { RegistrationForm } from '../components/features/auth';
import type { RegistrationFormData } from '../utils/validation';
import { authService, getErrorMessage, getFieldErrors } from '../services';

/**
 * Register Page Component
 *
 * Complete registration flow with:
 * - Registration form integration
 * - API submission with React Query
 * - Success message display
 * - Auto-login after successful registration
 * - Redirect to dashboard on success
 * - API error display handling
 * - Loading states
 */
const Register: React.FC = () => {
  const navigate = useNavigate();
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [generalError, setGeneralError] = useState<string | null>(null);

  // Registration mutation with React Query
  const registrationMutation = useMutation({
    mutationFn: async (data: RegistrationFormData) => {
      // Call registration API
      const response = await authService.register({
        email: data.email,
        password: data.password,
      });
      return response;
    },
    onSuccess: (data) => {
      // Clear any previous errors
      setGeneralError(null);

      // Show success message
      setSuccessMessage(`Account created successfully! Welcome, ${data.email}`);

      // Auto-login: Store auth token and user data
      authService.setAuthToken(data.access_token);
      authService.setUser({
        id: data.id,
        email: data.email,
        is_active: data.is_active,
      });

      // Redirect to dashboard after a short delay (let user see success message)
      setTimeout(() => {
        navigate('/dashboard');
      }, 1500);
    },
    onError: (error: unknown) => {
      // Clear success message if there was one
      setSuccessMessage(null);

      // Extract and display error message
      const errorMessage = getErrorMessage(error);
      setGeneralError(errorMessage);

      // Check for field-specific errors
      const fieldErrors = getFieldErrors(error);
      if (fieldErrors) {
        // Field errors are already displayed by the form validation
        console.error('Field validation errors:', fieldErrors);
      }
    },
  });

  // Handle form submission
  const handleRegistration = async (data: RegistrationFormData) => {
    // Clear previous messages
    setSuccessMessage(null);
    setGeneralError(null);

    // Submit registration
    await registrationMutation.mutateAsync(data);
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="mb-2 text-4xl font-bold text-gray-900">
            Create Account
          </h1>
          <p className="text-lg text-gray-600">
            Join us to start tracking your finances
          </p>
        </div>

        <div className="rounded-lg bg-white p-8 shadow-lg">
          {/* Success Message */}
          {successMessage && (
            <div
              className="mb-6 rounded-md border border-green-200 bg-green-50 p-4"
              role="alert"
              aria-live="polite"
            >
              <div className="flex items-center">
                <svg
                  className="mr-3 h-5 w-5 text-green-600"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <p className="text-sm font-medium text-green-800">
                  {successMessage}
                </p>
              </div>
            </div>
          )}

          {/* General Error Message */}
          {generalError && (
            <div
              className="mb-6 rounded-md border border-red-200 bg-red-50 p-4"
              role="alert"
              aria-live="assertive"
            >
              <div className="flex items-center">
                <svg
                  className="mr-3 h-5 w-5 text-red-600"
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                  aria-hidden="true"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
                <p className="text-sm font-medium text-red-800">{generalError}</p>
              </div>
            </div>
          )}

          {/* Registration Form */}
          <RegistrationForm
            onSubmit={handleRegistration}
            isLoading={registrationMutation.isPending}
          />
        </div>

        <div className="mt-6 text-center">
          <p className="text-sm text-gray-600">
            Already have an account?{' '}
            <a
              href="/login"
              className="font-medium text-blue-600 hover:text-blue-500 focus:underline focus:outline-none"
            >
              Sign in
            </a>
          </p>
        </div>

        {/* Loading overlay when redirecting */}
        {successMessage && (
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">
              Redirecting to dashboard...
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Register;
