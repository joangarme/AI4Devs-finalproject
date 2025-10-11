# Personal Finance Tracker - Frontend

Frontend application for the Personal Finance Tracker built with React, TypeScript, and Vite.

## Development Environment Setup

### Prerequisites

- Node.js 20.19+ or 22.12+ (required by Vite)
- npm or yarn package manager
- Git

### Quick Start

1. **Clone the repository** (if not already done):

   ```bash
   git clone <repository-url>
   cd finalproject-JAGM/frontend
   ```

2. **Verify Node.js version**:

   ```bash
   node --version
   # Should show Node.js 20.19+ or 22.12+
   ```

3. **Install dependencies**:

   ```bash
   npm install
   ```

4. **Start the development server**:

   ```bash
   npm run dev
   ```

   The application will start on `http://localhost:5173` with:
   - Hot Module Replacement (HMR) for instant updates
   - TypeScript compilation
   - ESLint integration
   - Fast build times with Vite

### Project Structure

```
frontend/
├── node_modules/           # Dependencies (not tracked in git)
├── public/                # Static assets
│   └── vite.svg
├── src/                   # Source code
│   ├── assets/           # Images and static files
│   │   └── react.svg
│   ├── components/       # React components
│   │   ├── App.tsx       # Main application component
│   │   ├── App.css       # Application styles
│   │   ├── common/       # Reusable common components
│   │   │   └── index.ts
│   │   ├── features/    # Feature-specific components
│   │   │   └── index.ts
│   │   └── index.ts      # Component exports
│   ├── pages/           # Page components
│   │   └── index.ts
│   ├── hooks/           # Custom React hooks
│   │   └── index.ts
│   ├── services/        # API services and external integrations
│   │   └── index.ts
│   ├── types/           # TypeScript type definitions
│   │   └── index.ts
│   ├── utils/           # Utility functions
│   │   └── index.ts
│   ├── index.css        # Global styles
│   └── main.tsx         # Application entry point
├── dist/                # Build output (not tracked in git)
├── package.json         # Dependencies and scripts
├── package-lock.json    # Lock file for reproducible installs
├── tsconfig.json        # TypeScript configuration
├── tsconfig.app.json    # TypeScript app configuration
├── tsconfig.node.json   # TypeScript node configuration
├── vite.config.ts       # Vite configuration
├── eslint.config.js     # ESLint configuration
├── tailwind.config.js   # Tailwind CSS configuration
├── postcss.config.js    # PostCSS configuration
└── README.md            # This file
```

### Dependencies

The following core dependencies are installed and configured:

#### Core Framework

- **React 19.1.1** - Modern UI library with hooks and concurrent features
- **TypeScript 5.9.3** - Type-safe JavaScript with static type checking
- **Vite 7.1.7** - Fast build tool and development server
- **@vitejs/plugin-react 5.0.4** - React plugin for Vite with Fast Refresh

#### Essential Libraries (MVP)

- **react-router-dom 6.30.1** - Client-side routing for single-page applications
- **@tanstack/react-query 5.90.2** - Powerful data synchronization for React
- **react-hook-form 7.64.0** - Performant, flexible forms with easy validation
- **axios 1.12.2** - Promise-based HTTP client for API calls

### Routing Structure

The application uses React Router DOM for client-side routing with the following setup:

#### Route Configuration

- **`/`** - Home/Landing page
- **`/login`** - User login page
- **`/register`** - User registration page
- **`/dashboard`** - Main dashboard (authenticated users)
- **`/transactions`** - Transaction management
- **`/settings`** - User settings and preferences
- **`*`** - 404 Not Found page for unknown routes

#### Navigation Component

A responsive navigation component is included for testing routes:

- Active route highlighting
- Mobile-friendly design
- Clean navigation structure
- TypeScript support

#### Router Setup

The routing is configured in:

- **`main.tsx`** - BrowserRouter wrapper around the entire app
- **`components/AppRoutes.tsx`** - Route definitions and component mapping
- **`components/Navigation.tsx`** - Navigation component for route testing
- **`pages/`** - Individual page components for each route

#### Testing Routes

To test the routing functionality:

1. Start the development server: `npm run dev`
2. Navigate to `http://localhost:5173`
3. Use the navigation bar to test each route
4. Verify 404 page by visiting unknown URLs
5. Test browser back/forward buttons

#### Styling

- **tailwindcss 3.4.17** - Utility-first CSS framework for rapid UI development
- **postcss 8.4.49** - CSS post-processor for Tailwind CSS
- **autoprefixer 10.4.20** - Automatic vendor prefixing for CSS
- **@tailwindcss/postcss 0.0.1** - PostCSS plugin for Tailwind CSS

#### Development Tools

- **ESLint 9.36.0** - Code linting and quality enforcement
- **@types/react 19.1.16** - TypeScript definitions for React
- **@types/react-dom 19.1.9** - TypeScript definitions for React DOM

All dependencies are pinned to specific versions in `package.json` for reproducible builds.

#### Verifying Installation

After installing dependencies, you can verify the installation:

```bash
# Check installed packages
npm list

# Test React imports
npm run build
# Should complete without errors

# Check TypeScript compilation
npx tsc --noEmit
# Should complete without type errors
```

### Available Scripts

```bash
# Development
npm run dev          # Start development server with HMR
npm run build        # Build for production
npm run preview      # Preview production build locally

# Code Quality
npm run lint         # Run ESLint
npm run lint:fix     # Fix ESLint issues automatically
npm run format       # Format code with Prettier
npm run format:check # Check if code is formatted correctly

# Type Checking
npx tsc --noEmit     # Check TypeScript types without emitting files
```

### Development Workflow

1. Always run `npm install` after pulling changes
2. Use `npm run dev` for development with hot reloading
3. Run `npm run lint` and `npm run format:check` before committing changes
4. Use `npm run build` to test production builds
5. Follow the established project structure for new components

### Project Architecture

The frontend follows a modular architecture with clear separation of concerns:

#### Component Organization

- **`components/common/`** - Reusable UI components (buttons, inputs, modals)
- **`components/features/`** - Feature-specific components (user profile, financial charts)
- **`pages/`** - Top-level page components that compose features
- **`hooks/`** - Custom React hooks for shared logic
- **`services/`** - API clients and external service integrations
- **`types/`** - TypeScript interfaces and type definitions
- **`utils/`** - Pure utility functions and helpers

#### Import Strategy

Each directory includes an `index.ts` file for clean imports:

```typescript
// Clean imports from organized structure
import { Button } from '@/components/common';
import { UserProfile } from '@/components/features';
import { useAuth } from '@/hooks';
import { apiClient } from '@/services';
import type { User } from '@/types';
```

### Configuration Management

The application uses modern tooling with optimized configurations:

#### TypeScript Configuration

- **Strict mode enabled** for maximum type safety
- **Path mapping** for clean imports (`@/` maps to `src/`)
- **Separate configs** for app and build tools
- **Modern target** (ES2020) with React JSX support

#### Vite Configuration

- **Fast HMR** with React Fast Refresh
- **Optimized builds** with code splitting
- **Asset handling** for images and static files
- **Development server** with proxy support for API calls

#### ESLint Configuration

- **TypeScript-aware** linting rules
- **React-specific** rules for hooks and components
- **Import organization** and unused variable detection
- **Code quality** enforcement with consistent formatting
- **Prettier integration** to avoid formatting conflicts

#### Prettier Configuration

- **Code formatting** with consistent style across the project
- **Tailwind CSS class sorting** for organized utility classes
- **Editor integration** with format-on-save support
- **Team consistency** with shared formatting rules

#### Tailwind CSS Configuration

- **Utility-first** approach for rapid UI development
- **PostCSS integration** with autoprefixer for vendor prefixes
- **Content scanning** for purging unused CSS in production
- **Default configuration** optimized for React components
- **Responsive design** utilities for mobile-first development

### Environment Variables

The application uses Vite's built-in environment variable handling for configuration management.

#### Setup

1. **Copy the example file**:

   ```bash
   cp .env.example .env.local
   ```

2. **Edit `.env.local`** with your configuration:

   ```bash
   # .env.local is ignored by git (*.local in .gitignore)
   # Modify values as needed for your local environment
   ```

#### Available Variables

All environment variables must be prefixed with `VITE_` to be exposed to the client:

| Variable            | Description          | Default                    |
| ------------------- | -------------------- | -------------------------- |
| `VITE_API_BASE_URL` | Backend API base URL | `http://localhost:8000`    |
| `VITE_API_VERSION`  | API version prefix   | `v1`                       |
| `VITE_NODE_ENV`     | Environment mode     | `development`              |
| `VITE_APP_NAME`     | Application name     | `Personal Finance Manager` |
| `VITE_APP_VERSION`  | Application version  | `1.0.0`                    |
| `VITE_ENABLE_DEBUG` | Enable debug mode    | `false`                    |

#### Usage in Code

The application provides a type-safe utility for accessing environment variables:

```typescript
import { env, getApiUrl, isDevelopment } from '@/utils';

// Access environment variables with TypeScript autocomplete
const apiBaseUrl = env.apiBaseUrl;
const isDebug = env.enableDebug;

// Build full API URLs
const endpoint = getApiUrl('users'); // http://localhost:8000/api/v1/users

// Check environment
if (isDevelopment()) {
  console.log('Running in development mode');
}
```

#### TypeScript Support

Environment variables are fully typed in `src/env.d.ts`:

```typescript
interface ImportMetaEnv {
  readonly VITE_API_BASE_URL: string;
  readonly VITE_API_VERSION: string;
  readonly VITE_NODE_ENV: 'development' | 'production' | 'test';
  readonly VITE_APP_NAME: string;
  readonly VITE_APP_VERSION: string;
  readonly VITE_ENABLE_DEBUG: string;
}
```

This enables:

- **IntelliSense** in your editor
- **Type checking** at compile time
- **Auto-completion** for environment variable names

#### Environment Precedence

Vite loads environment variables in the following order (later overrides earlier):

1. `.env` - Shared defaults (tracked in git, no secrets)
2. `.env.local` - Local overrides (ignored by git)
3. `.env.[mode]` - Mode-specific (e.g., `.env.production`)
4. `.env.[mode].local` - Mode-specific local overrides

#### Security Notes

- **Never commit** `.env.local` or files with secrets
- **Only add** non-sensitive defaults to `.env.example`
- **Always prefix** client-exposed variables with `VITE_`
- **Backend secrets** should NEVER be in frontend env files

#### Verification

Test environment variables are loaded correctly:

```bash
# Build should succeed with env vars
npm run build

# Check TypeScript recognizes env types
npx tsc --noEmit
```

### API Integration

The frontend is designed to integrate with the backend API:

- **Base URL**: Configured to connect to backend API
- **CORS**: Properly configured for cross-origin requests
- **Error Handling**: Centralized error handling for API responses
- **Type Safety**: TypeScript interfaces matching backend schemas

### Build and Deployment

#### Production Build

```bash
npm run build
```

Creates optimized production build in `dist/` directory with:

- Minified JavaScript and CSS
- Tree-shaking for smaller bundle sizes
- Asset optimization and compression
- Source maps for debugging

#### Development vs Production

- **Development**: Fast HMR, detailed error messages, source maps
- **Production**: Optimized bundles, minified code, performance optimizations

### Troubleshooting

**Node.js version issues:**

- Ensure Node.js 20.19+ or 22.12+ is installed
- Use `nvm` to manage Node.js versions: `nvm use 20`

**Build failures:**

- Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`
- Check TypeScript errors: `npx tsc --noEmit`

**Import path issues:**

- Verify `tsconfig.json` path mapping configuration
- Check that `index.ts` files exist in each directory

### Next Steps

**Completed:**

- ✅ React + TypeScript + Vite setup (US0.3-T1)
- ✅ Organized project structure (US0.3-T2)
- ✅ Essential dependencies installed (US0.3-T3)
- ✅ Tailwind CSS configured for styling (US0.3-T4)
- ✅ ESLint and Prettier configuration (US0.3-T5)
- ✅ Basic routing structure with React Router (US0.3-T6)
- ✅ Environment variables setup (US0.3-T7)
- ✅ Component architecture with clean imports
- ✅ Development environment configuration

**Upcoming tasks:**

- Base component library (US0.3-T8)
- Development scripts and documentation (US0.3-T9)

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.3-frontend-development-environment-setup-tasks.md`
