import { useState } from 'react';
import reactLogo from '../assets/react.svg';
import viteLogo from '/vite.svg';
import './App.css';

function App() {
  const [count, setCount] = useState(0);

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-gray-100 p-8">
      <div className="mb-8 flex gap-8">
        <a
          href="https://vite.dev"
          target="_blank"
          className="transition-transform hover:scale-110"
        >
          <img src={viteLogo} className="h-24 w-24" alt="Vite logo" />
        </a>
        <a
          href="https://react.dev"
          target="_blank"
          className="transition-transform hover:scale-110"
        >
          <img
            src={reactLogo}
            className="h-24 w-24 animate-spin"
            alt="React logo"
          />
        </a>
      </div>
      <h1 className="mb-8 text-4xl font-bold text-gray-800">
        Vite + React + Tailwind
      </h1>
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-lg">
        <button
          onClick={() => setCount((count) => count + 1)}
          className="mb-4 w-full rounded-lg bg-blue-500 px-6 py-3 font-semibold text-white transition-colors duration-200 hover:bg-blue-600"
        >
          count is {count}
        </button>
        <p className="text-center text-gray-600">
          Edit{' '}
          <code className="rounded bg-gray-100 px-2 py-1 text-sm">
            src/App.tsx
          </code>{' '}
          and save to test HMR
        </p>
      </div>
      <p className="mt-8 max-w-md text-center text-gray-500">
        Click on the Vite and React logos to learn more. Tailwind CSS is now
        configured!
      </p>
    </div>
  );
}

export default App;
