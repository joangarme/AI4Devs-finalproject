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

# Type Checking
npx tsc --noEmit     # Check TypeScript types without emitting files
```

### Development Workflow

1. Always run `npm install` after pulling changes
2. Use `npm run dev` for development with hot reloading
3. Run `npm run lint` before committing changes
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
import { Button } from "@/components/common";
import { UserProfile } from "@/components/features";
import { useAuth } from "@/hooks";
import { apiClient } from "@/services";
import type { User } from "@/types";
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

#### Tailwind CSS Configuration

- **Utility-first** approach for rapid UI development
- **PostCSS integration** with autoprefixer for vendor prefixes
- **Content scanning** for purging unused CSS in production
- **Default configuration** optimized for React components
- **Responsive design** utilities for mobile-first development

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
- ✅ Component architecture with clean imports
- ✅ Development environment configuration

**Upcoming tasks:**

- ESLint and Prettier configuration (US0.3-T5)
- Basic routing structure (US0.3-T6)
- Environment variables setup (US0.3-T7)
- Base component library (US0.3-T8)
- Development scripts and documentation (US0.3-T9)

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.3-frontend-development-environment-setup-tasks.md`
