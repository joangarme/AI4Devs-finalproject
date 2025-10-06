import React from 'react';

const Login: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md mx-auto text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Login
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          Sign in to your account
        </p>
        <div className="space-y-4">
          <p className="text-gray-500">
            This is the login page placeholder.
          </p>
          <p className="text-sm text-gray-400">
            Route: /login
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
