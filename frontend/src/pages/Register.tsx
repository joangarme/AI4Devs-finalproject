import React from 'react';
import { RegistrationForm } from '../components/features/auth';
import type { RegistrationFormData } from '../components/features/auth/RegistrationForm.types';

const Register: React.FC = () => {
  const handleRegistration = async (data: RegistrationFormData) => {
    // This will be replaced with actual API call in US1.1-T9
    console.log('Registration data:', {
      email: data.email,
      password: '[REDACTED]',
    });

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));

    alert(`Account created successfully for ${data.email}!`);
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
          <RegistrationForm onSubmit={handleRegistration} />
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
      </div>
    </div>
  );
};

export default Register;
