import React from 'react';

const Home: React.FC = () => {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="mx-auto max-w-md text-center">
        <h1 className="mb-4 text-4xl font-bold text-gray-900">
          Welcome to LiDR
        </h1>
        <p className="mb-8 text-lg text-gray-600">
          Your personal finance management solution
        </p>
        <div className="space-y-4">
          <p className="text-gray-500">
            This is the home/landing page placeholder.
          </p>
          <p className="text-sm text-gray-400">Route: / (home/landing)</p>
        </div>
      </div>
    </div>
  );
};

export default Home;
