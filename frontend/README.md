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

### Component Library

The application includes a base component library following React best practices with TypeScript and Tailwind CSS.

#### Button Component

The `Button` component is a flexible, reusable button with multiple variants and features:

**Features:**

- **5 Variants**: `primary`, `secondary`, `outline`, `ghost`, `danger`
- **3 Sizes**: `sm`, `md`, `lg`
- **Loading State**: Built-in spinner with automatic disabling
- **Icons Support**: `leftIcon` and `rightIcon` props for icons
- **Full Width**: Optional `fullWidth` prop for responsive layouts
- **Accessibility**: Proper ARIA attributes and keyboard navigation
- **TypeScript**: Fully typed with intellisense support
- **Extends HTML Button**: Inherits all native button attributes

**Usage Examples:**

```typescript
import { Button } from '@/components';

// Basic usage
<Button variant="primary" size="md">
  Click Me
</Button>

// With loading state
<Button variant="primary" isLoading>
  Saving...
</Button>

// With icons
<Button
  variant="secondary"
  leftIcon={<PlusIcon />}
  onClick={handleAdd}
>
  Add Item
</Button>

// Full width (responsive)
<Button fullWidth>
  Submit Form
</Button>

// All native button props work
<Button
  type="submit"
  disabled={!isValid}
  onClick={handleSubmit}
>
  Submit
</Button>
```

**Component Structure:**

```
components/common/Button/
├── Button.tsx           # Component implementation
├── Button.types.ts      # TypeScript interfaces
└── index.ts             # Exports
```

**Available Props:**

| Prop        | Type                 | Default     | Description                  |
| ----------- | -------------------- | ----------- | ---------------------------- |
| `variant`   | ButtonVariant        | `'primary'` | Visual style variant         |
| `size`      | ButtonSize           | `'md'`      | Button size                  |
| `fullWidth` | boolean              | `false`     | Take full width of container |
| `isLoading` | boolean              | `false`     | Show loading spinner         |
| `leftIcon`  | ReactNode            | -           | Icon before text             |
| `rightIcon` | ReactNode            | -           | Icon after text              |
| `children`  | ReactNode            | required    | Button content               |
| `...rest`   | ButtonHTMLAttributes | -           | All native button attributes |

**Testing the Component:**

Visit the home page (`/`) to see a comprehensive showcase of all Button variants, sizes, and states.

#### Component Best Practices

The Button component demonstrates best practices for creating reusable components:

1. **TypeScript First**: Proper typing with interfaces and type exports
2. **Composition**: Using `forwardRef` for ref forwarding
3. **Accessibility**: Semantic HTML with proper ARIA attributes
4. **Flexibility**: Extensible through props and native attributes
5. **Documentation**: JSDoc comments for IntelliSense
6. **Styling**: Tailwind CSS with variant-based styling
7. **Testing**: Visual showcase on home page

#### Adding New Components

To add new components to the library:

1. Create a new directory in `components/common/`
2. Add three files:
   - `ComponentName.tsx` - Component implementation
   - `ComponentName.types.ts` - TypeScript interfaces
   - `index.ts` - Exports
3. Export from `components/common/index.ts`
4. Component is automatically available through `components/index.ts`

#### RegistrationForm Component

The `RegistrationForm` component is a comprehensive, production-ready registration form with advanced features:

**Features:**

- **Form Fields**: Email, password, and confirm password inputs
- **Password Strength Indicator**: Real-time password strength analysis using zxcvbn
- **Form Validation**: React Hook Form integration with real-time validation
- **Debounced Validation**: 300ms debounce for improved performance
- **Loading States**: Built-in loading state with spinner animation
- **Accessibility**: Full ARIA attributes and keyboard navigation support
- **Show/Hide Password**: Toggle visibility for password fields
- **Error Messages**: Clear, user-friendly error messages for all validation failures
- **Password Requirements**: Visual display of password rules
- **TypeScript**: Fully typed with comprehensive interfaces
- **Responsive Design**: Mobile-first design with Tailwind CSS

**Component Structure:**

```
components/features/auth/
├── RegistrationForm.tsx          # Component implementation
├── RegistrationForm.types.ts     # TypeScript interfaces
└── index.ts                       # Exports
```

**Usage Example:**

```typescript
import { RegistrationForm } from '@/components/features/auth';
import type { RegistrationFormData } from '@/components/features/auth/RegistrationForm.types';

const RegisterPage = () => {
  const handleRegistration = async (data: RegistrationFormData) => {
    // Call your API here
    await registerUser({
      email: data.email,
      password: data.password,
    });
  };

  return (
    <div className="container">
      <RegistrationForm
        onSubmit={handleRegistration}
        isLoading={false}
      />
    </div>
  );
};
```

**Available Props:**

| Prop        | Type                                            | Default  | Description                          |
| ----------- | ----------------------------------------------- | -------- | ------------------------------------ |
| `onSubmit`  | `(data: RegistrationFormData) => Promise<void>` | required | Async handler for form submission    |
| `isLoading` | `boolean`                                       | `false`  | Controls loading state of submit btn |

**Form Data Interface:**

```typescript
interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
}
```

**Password Validation Rules:**

The form enforces the following password requirements:

- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number
- At least 1 special character (@$!%\*?&)

**Password Strength Levels:**

- **Too weak** (score 0): Red indicator
- **Weak** (score 1): Orange indicator
- **Fair** (score 2): Yellow indicator
- **Good** (score 3): Blue indicator
- **Strong** (score 4): Green indicator

**Accessibility Features:**

- Proper ARIA labels and descriptions for all form fields
- ARIA live regions for real-time validation feedback
- Keyboard navigation support
- Screen reader friendly error messages
- Semantic HTML with proper form structure
- Focus management and visible focus indicators

**Dependencies:**

- `react-hook-form@7.64.0` - Form state management and validation
- `zxcvbn@4.6.0` - Password strength calculation
- `@types/zxcvbn@4.4.5` - TypeScript types for zxcvbn
- `zod@latest` - Schema validation library
- `@hookform/resolvers@latest` - React Hook Form resolvers for Zod

**Testing the Component:**

Visit the registration page (`/register`) to see the form in action with:

- Real-time email validation
- Dynamic password strength indicator
- Instant validation feedback
- Loading state simulation
- Accessible form interactions

### Form Validation Schema

The frontend uses **Zod** for type-safe form validation that matches backend requirements exactly.

#### Validation Architecture

The validation system is centralized in `src/utils/validation/` for consistency and maintainability:

```
src/utils/validation/
├── auth.validation.ts    # Authentication form schemas
└── index.ts              # Exports
```

#### Backend Consistency

All validation rules are designed to match backend validators exactly:

| Frontend Schema     | Backend Validator              | File Path                                 |
| ------------------- | ------------------------------ | ----------------------------------------- |
| `emailSchema`       | `EmailValidator`               | `backend/app/services/email_validator.py` |
| `passwordSchema`    | `PasswordValidator`            | `backend/app/services/password_validator.py` |
| `registrationSchema`| Combined email + password validation | Used by `UserService.register_user()` |

#### Email Validation

Matches backend `EmailValidator` requirements:

```typescript
import { emailSchema } from '@/utils/validation';

// Backend requirements:
// - Cannot be empty → "Email address cannot be empty"
// - Must be RFC-compliant → "Email address is not valid"

const result = emailSchema.safeParse('user@example.com');
if (!result.success) {
  console.error(result.error.errors);
}
```

**Validation Rules:**
- ✅ Non-empty email address required
- ✅ RFC-compliant email format
- ✅ Case-insensitive (normalized to lowercase on backend)

#### Password Validation

Matches backend `PasswordValidator` requirements **exactly**:

```typescript
import { passwordSchema, PASSWORD_REQUIREMENTS, checkPasswordRequirements } from '@/utils/validation';

// Backend requirements (exact match):
// - MIN_LENGTH = 8
// - UPPERCASE_PATTERN = r'[A-Z]'
// - NUMBER_PATTERN = r'[0-9]'
// - SPECIAL_CHAR_PATTERN = r'[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]'

const result = passwordSchema.safeParse('MyPass123!');
```

**Validation Rules (Backend-Aligned):**
- ✅ Minimum 8 characters → "Password must be at least 8 characters long"
- ✅ At least 1 uppercase letter → "Password must contain at least 1 uppercase letter"
- ✅ At least 1 number → "Password must contain at least 1 number"
- ✅ At least 1 special character → "Password must contain at least 1 special character (!@#$%^&*(),.?\":{}|<>_-+=[]\\\/;~`)"

**Special Characters (Backend-Aligned):**
```
! @ # $ % ^ & * ( ) , . ? " : { } | < > _ - + = [ ] \ / ; ~ `
```

**Helper Function for UI Feedback:**

```typescript
import { checkPasswordRequirements } from '@/utils/validation';

const requirements = checkPasswordRequirements('MyPass123!');
// Returns:
// {
//   minLength: true,
//   hasUppercase: true,
//   hasLowercase: true,
//   hasNumber: true,
//   hasSpecialChar: true
// }
```

#### Registration Form Schema

Complete schema for user registration:

```typescript
import { registrationSchema } from '@/utils/validation';
import type { RegistrationFormData } from '@/utils/validation';

// Type-safe form data
const data: RegistrationFormData = {
  email: 'user@example.com',
  password: 'SecurePass123!',
  confirmPassword: 'SecurePass123!'
};

const result = registrationSchema.safeParse(data);
```

**Validation Rules:**
- ✅ Email must pass email validation
- ✅ Password must pass password validation
- ✅ Confirm password must match password → "Passwords do not match"

#### Integration with React Hook Form

The validation schemas integrate seamlessly with React Hook Form using `zodResolver`:

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { registrationSchema, type RegistrationFormData } from '@/utils/validation';

const MyForm = () => {
  const { register, handleSubmit, formState: { errors } } = useForm<RegistrationFormData>({
    resolver: zodResolver(registrationSchema),
    mode: 'onChange', // Real-time validation
  });

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      
      <input type="password" {...register('password')} />
      {errors.password && <span>{errors.password.message}</span>}
      
      <button type="submit">Register</button>
    </form>
  );
};
```

#### Error Messages

All error messages match backend validators exactly for consistent user experience:

| Field | Error Condition | Frontend Message | Backend Message |
|-------|----------------|------------------|-----------------|
| Email | Empty | "Email address cannot be empty" | "Email address cannot be empty" |
| Email | Invalid format | "Email address is not valid" | "Email address is not valid" |
| Password | Too short | "Password must be at least 8 characters long" | "Password must be at least 8 characters long" |
| Password | No uppercase | "Password must contain at least 1 uppercase letter" | "Password must contain at least 1 uppercase letter" |
| Password | No number | "Password must contain at least 1 number" | "Password must contain at least 1 number" |
| Password | No special char | "Password must contain at least 1 special character (!@#$%^&*(),.?\":{}|<>_-+=[]\\\/;~`)" | "Password must contain at least 1 special character (!@#$%^&*(),.?\":{}|<>_-+=[]\\\/;~`)" |
| Confirm Password | Empty | "Please confirm your password" | N/A (frontend only) |
| Confirm Password | Mismatch | "Passwords do not match" | N/A (frontend only) |

#### Benefits of Zod Validation

1. **Type Safety**: TypeScript types inferred from schemas
2. **Backend Consistency**: Validation rules match backend exactly
3. **Clear Error Messages**: User-friendly, specific error messages
4. **Maintainability**: Centralized validation logic
5. **Composability**: Schemas can be combined and reused
6. **Integration**: Works seamlessly with React Hook Form

#### Validation Best Practices

1. **Always validate on both frontend and backend**
   - Frontend: Better UX with immediate feedback
   - Backend: Security and data integrity

2. **Keep validation rules synchronized**
   - Frontend schemas match backend validators
   - Error messages are identical
   - Special character sets are aligned

3. **Use TypeScript types from schemas**
   ```typescript
   import type { RegistrationFormData } from '@/utils/validation';
   // Type is automatically inferred from Zod schema
   ```

4. **Leverage Zod's composition**
   ```typescript
   // Reuse schemas in multiple forms
   const loginSchema = z.object({
     email: emailSchema,
     password: z.string().min(1, 'Password is required')
   });
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

### VS Code Recommended Extensions

This project includes a `.vscode/extensions.json` file that will prompt you to install recommended extensions when you open the project in VS Code.

#### Essential Extensions

1. **ESLint** (`dbaeumer.vscode-eslint`)
   - Real-time linting and error detection
   - Automatic fixing on save
   - Installation: VS Code will prompt you, or install from Extensions panel

2. **Prettier** (`esbenp.prettier-vscode`)
   - Code formatting on save
   - Consistent code style across team
   - Works seamlessly with ESLint

3. **Tailwind CSS IntelliSense** (`bradlc.vscode-tailwindcss`)
   - Autocomplete for Tailwind classes
   - Syntax highlighting for class names
   - CSS preview on hover

4. **Jest Runner** (`firsttris.vscode-jest-runner`)
   - Run individual tests from the editor
   - Quick test debugging
   - Useful when tests are added

5. **Jest** (`orta.vscode-jest`)
   - Inline test results
   - Automatic test running
   - Test coverage visualization

#### VS Code Settings

Create or update `.vscode/settings.json` in your workspace with:

```json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "javascriptreact",
    "typescript",
    "typescriptreact"
  ],
  "tailwindCSS.experimental.classRegex": [
    ["clsx\\(([^)]*)\\)", "(?:'|\"|`)([^']*)(?:'|\"|`)"]
  ]
}
```

### Troubleshooting

#### Node.js Version Issues

**Problem:** Errors during `npm install` or `npm run dev` related to Node.js version

**Symptoms:**

- "Node.js version not supported"
- "Unsupported engine" errors
- Build failures with version warnings

**Solution:**

1. Check your current Node.js version:

   ```bash
   node --version
   ```

2. Install/use Node.js 20.19+ or 22.12+:

   ```bash
   # Install nvm if not already installed
   curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

   # Install and use Node.js 20
   nvm install 20
   nvm use 20
   nvm alias default 20
   ```

3. Reinstall dependencies:
   ```bash
   rm -rf node_modules package-lock.json
   npm install
   ```

#### Build Failures

**Problem:** `npm run build` fails with errors

**Common Causes & Solutions:**

1. **TypeScript errors:**

   ```bash
   # Check for type errors
   npm run type-check

   # Fix common issues:
   # - Missing imports
   # - Incorrect prop types
   # - Unused variables
   ```

2. **Dependency conflicts:**

   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm cache clean --force
   npm install
   ```

3. **Out of memory:**
   ```bash
   # Increase Node memory limit
   export NODE_OPTIONS="--max-old-space-size=4096"
   npm run build
   ```

#### Import Path Issues

**Problem:** Module not found errors or incorrect imports

**Solutions:**

1. **Verify path aliases in `tsconfig.json`:**

   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./src/*"]
       }
     }
   }
   ```

2. **Check index.ts files exist:**

   ```bash
   # Each directory should have an index.ts
   ls src/components/index.ts
   ls src/hooks/index.ts
   ls src/utils/index.ts
   ```

3. **Restart TypeScript server in VS Code:**
   - Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
   - Type "TypeScript: Restart TS Server"
   - Press Enter

#### ESLint/Prettier Conflicts

**Problem:** Code formatting keeps changing back and forth

**Solution:**

1. Ensure both ESLint and Prettier extensions are installed
2. Check that `eslint-config-prettier` is in devDependencies
3. Verify ESLint config includes Prettier:
   ```bash
   # Should be in package.json
   "eslint-config-prettier": "^10.1.8"
   ```
4. Restart VS Code

#### Hot Module Replacement (HMR) Not Working

**Problem:** Changes don't reflect automatically during development

**Solutions:**

1. **Check dev server is running:**

   ```bash
   npm run dev
   ```

2. **Clear browser cache:**
   - Hard refresh: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)

3. **Restart dev server:**

   ```bash
   # Stop server (Ctrl+C) and restart
   npm run dev
   ```

4. **Check for console errors:**
   - Open browser DevTools (F12)
   - Look for errors in Console tab

#### Port Already in Use

**Problem:** "Port 5173 is already in use"

**Solution:**

1. **Find and kill the process:**

   ```bash
   # macOS/Linux
   lsof -ti:5173 | xargs kill -9

   # Windows
   netstat -ano | findstr :5173
   taskkill /PID <PID> /F
   ```

2. **Use a different port:**
   ```bash
   # Vite will automatically use next available port
   # Or specify port manually:
   npm run dev -- --port 5174
   ```

#### Environment Variables Not Loading

**Problem:** `import.meta.env.VITE_*` is undefined

**Solutions:**

1. **Verify file naming:**
   - File must be named `.env` or `.env.local`
   - Must be in `frontend/` directory (not root)

2. **Check variable prefix:**
   - All variables must start with `VITE_`
   - Example: `VITE_API_BASE_URL=http://localhost:8000`

3. **Restart dev server:**
   - Environment variables are loaded at startup
   - Changes require server restart

4. **Verify TypeScript types:**
   - Check `src/env.d.ts` includes your variables

#### Slow Build Times

**Problem:** `npm run build` takes too long

**Solutions:**

1. **Clear dist folder:**

   ```bash
   rm -rf dist
   npm run build
   ```

2. **Update dependencies:**

   ```bash
   npm update
   ```

3. **Check for large dependencies:**
   ```bash
   npx vite-bundle-visualizer
   ```

#### Additional Help

If you encounter issues not covered here:

1. **Check the browser console** for runtime errors
2. **Check the terminal** for build-time errors
3. **Review Vite documentation**: https://vite.dev/
4. **Review React documentation**: https://react.dev/
5. **Search GitHub issues** in the project repository

### Next Steps

**Completed:**

- ✅ React + TypeScript + Vite setup (US0.3-T1)
- ✅ Organized project structure (US0.3-T2)
- ✅ Essential dependencies installed (US0.3-T3)
- ✅ Tailwind CSS configured for styling (US0.3-T4)
- ✅ ESLint and Prettier configuration (US0.3-T5)
- ✅ Basic routing structure with React Router (US0.3-T6)
- ✅ Environment variables setup (US0.3-T7)
- ✅ Base component library structure with Button component (US0.3-T8)
- ✅ Component architecture with clean imports
- ✅ Development environment configuration

**Upcoming tasks:**

- Development scripts and documentation (US0.3-T9)

For detailed task breakdown, see: `../backlog/Epic 0: Development Environment & Project Scaffolding/US0.3-frontend-development-environment-setup-tasks.md`
