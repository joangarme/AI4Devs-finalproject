import { useState, useCallback, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import zxcvbn from 'zxcvbn';

// Form data interface
interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

// Password strength levels
type PasswordStrength = {
  score: number;
  label: string;
  color: string;
  bgColor: string;
};

// Component props
interface RegistrationFormProps {
  onSubmit: (data: RegistrationFormData) => Promise<void>;
  isLoading?: boolean;
}

/**
 * RegistrationForm Component
 *
 * A comprehensive registration form with:
 * - Email and password input fields
 * - Real-time password strength indicator
 * - Form validation with React Hook Form
 * - Loading states
 * - Accessible form with proper labels and ARIA attributes
 * - Debounced validation
 */
export const RegistrationForm = ({
  onSubmit,
  isLoading = false,
}: RegistrationFormProps) => {
  const [passwordStrength, setPasswordStrength] = useState<PasswordStrength>({
    score: 0,
    label: 'Too weak',
    color: 'text-red-600',
    bgColor: 'bg-red-500',
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [validationTimer, setValidationTimer] = useState<number | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors, isValid, isDirty },
    setError,
    clearErrors,
  } = useForm<RegistrationFormData>({
    mode: 'onChange',
    defaultValues: {
      email: '',
      password: '',
      confirmPassword: '',
    },
  });

  const password = watch('password');
  const confirmPassword = watch('confirmPassword');

  // Password strength mapping
  const getPasswordStrength = (score: number): PasswordStrength => {
    const strengthMap: Record<number, PasswordStrength> = {
      0: {
        score: 0,
        label: 'Too weak',
        color: 'text-red-600',
        bgColor: 'bg-red-500',
      },
      1: {
        score: 1,
        label: 'Weak',
        color: 'text-orange-600',
        bgColor: 'bg-orange-500',
      },
      2: {
        score: 2,
        label: 'Fair',
        color: 'text-yellow-600',
        bgColor: 'bg-yellow-500',
      },
      3: {
        score: 3,
        label: 'Good',
        color: 'text-blue-600',
        bgColor: 'bg-blue-500',
      },
      4: {
        score: 4,
        label: 'Strong',
        color: 'text-green-600',
        bgColor: 'bg-green-500',
      },
    };
    return strengthMap[score] || strengthMap[0];
  };

  // Debounced password strength calculation
  useEffect(() => {
    if (validationTimer) {
      window.clearTimeout(validationTimer);
    }

    const timer = window.setTimeout(() => {
      if (password && password.length > 0) {
        const result = zxcvbn(password);
        setPasswordStrength(getPasswordStrength(result.score));
      } else {
        setPasswordStrength(getPasswordStrength(0));
      }
    }, 300); // 300ms debounce

    setValidationTimer(timer);

    return () => {
      if (timer) window.clearTimeout(timer);
    };
  }, [password]);

  // Password confirmation validation (debounced)
  useEffect(() => {
    if (validationTimer) {
      window.clearTimeout(validationTimer);
    }

    const timer = window.setTimeout(() => {
      if (confirmPassword && password !== confirmPassword) {
        setError('confirmPassword', {
          type: 'manual',
          message: 'Passwords do not match',
        });
      } else {
        clearErrors('confirmPassword');
      }
    }, 300); // 300ms debounce

    setValidationTimer(timer);

    return () => {
      if (timer) window.clearTimeout(timer);
    };
  }, [password, confirmPassword, setError, clearErrors]);

  // Handle form submission
  const handleFormSubmit = useCallback(
    async (data: RegistrationFormData) => {
      if (data.password !== data.confirmPassword) {
        setError('confirmPassword', {
          type: 'manual',
          message: 'Passwords do not match',
        });
        return;
      }

      try {
        await onSubmit(data);
      } catch (error) {
        console.error('Registration error:', error);
      }
    },
    [onSubmit, setError]
  );

  return (
    <form
      onSubmit={handleSubmit(handleFormSubmit)}
      className="w-full max-w-md space-y-6"
      noValidate
      aria-label="Registration form"
    >
      {/* Email Field */}
      <div className="space-y-2">
        <label
          htmlFor="email"
          className="block text-sm font-medium text-gray-700"
        >
          Email Address
          <span className="text-red-500" aria-label="required">
            *
          </span>
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          disabled={isLoading}
          aria-required="true"
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
          className={`w-full rounded-md border px-4 py-2 text-gray-900 shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500 ${
            errors.email
              ? 'border-red-500 focus:ring-red-500'
              : 'border-gray-300'
          }`}
          {...register('email', {
            required: 'Email is required',
            pattern: {
              value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
              message: 'Invalid email address',
            },
          })}
        />
        {errors.email && (
          <p
            id="email-error"
            className="text-sm text-red-600"
            role="alert"
            aria-live="polite"
          >
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password Field */}
      <div className="space-y-2">
        <label
          htmlFor="password"
          className="block text-sm font-medium text-gray-700"
        >
          Password
          <span className="text-red-500" aria-label="required">
            *
          </span>
        </label>
        <div className="relative">
          <input
            id="password"
            type={showPassword ? 'text' : 'password'}
            autoComplete="new-password"
            disabled={isLoading}
            aria-required="true"
            aria-invalid={errors.password ? 'true' : 'false'}
            aria-describedby={
              errors.password
                ? 'password-error'
                : password
                  ? 'password-strength'
                  : undefined
            }
            className={`w-full rounded-md border px-4 py-2 pr-10 text-gray-900 shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500 ${
              errors.password
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300'
            }`}
            {...register('password', {
              required: 'Password is required',
              minLength: {
                value: 8,
                message: 'Password must be at least 8 characters',
              },
              pattern: {
                value:
                  /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
                message:
                  'Password must contain uppercase, lowercase, number, and special character',
              },
            })}
          />
          <button
            type="button"
            onClick={() => setShowPassword(!showPassword)}
            disabled={isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded px-2 py-1 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:text-gray-400"
            aria-label={showPassword ? 'Hide password' : 'Show password'}
          >
            {showPassword ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            )}
          </button>
        </div>

        {/* Password Strength Indicator */}
        {password && password.length > 0 && (
          <div
            id="password-strength"
            className="space-y-2"
            role="status"
            aria-live="polite"
          >
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-600">Password strength:</span>
              <span className={`text-xs font-medium ${passwordStrength.color}`}>
                {passwordStrength.label}
              </span>
            </div>
            <div className="h-2 w-full overflow-hidden rounded-full bg-gray-200">
              <div
                className={`h-full transition-all duration-300 ${passwordStrength.bgColor}`}
                style={{
                  width: `${(passwordStrength.score / 4) * 100}%`,
                }}
                role="progressbar"
                aria-valuenow={passwordStrength.score}
                aria-valuemin={0}
                aria-valuemax={4}
                aria-label={`Password strength: ${passwordStrength.label}`}
              />
            </div>
          </div>
        )}

        {errors.password && (
          <p
            id="password-error"
            className="text-sm text-red-600"
            role="alert"
            aria-live="polite"
          >
            {errors.password.message}
          </p>
        )}

        {/* Password Requirements */}
        <div className="text-xs text-gray-600">
          <p>Password must contain:</p>
          <ul className="ml-4 mt-1 list-disc space-y-1">
            <li>At least 8 characters</li>
            <li>One uppercase letter</li>
            <li>One lowercase letter</li>
            <li>One number</li>
            <li>One special character (@$!%*?&)</li>
          </ul>
        </div>
      </div>

      {/* Confirm Password Field */}
      <div className="space-y-2">
        <label
          htmlFor="confirmPassword"
          className="block text-sm font-medium text-gray-700"
        >
          Confirm Password
          <span className="text-red-500" aria-label="required">
            *
          </span>
        </label>
        <div className="relative">
          <input
            id="confirmPassword"
            type={showConfirmPassword ? 'text' : 'password'}
            autoComplete="new-password"
            disabled={isLoading}
            aria-required="true"
            aria-invalid={errors.confirmPassword ? 'true' : 'false'}
            aria-describedby={
              errors.confirmPassword ? 'confirm-password-error' : undefined
            }
            className={`w-full rounded-md border px-4 py-2 pr-10 text-gray-900 shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500 ${
              errors.confirmPassword
                ? 'border-red-500 focus:ring-red-500'
                : 'border-gray-300'
            }`}
            {...register('confirmPassword', {
              required: 'Please confirm your password',
            })}
          />
          <button
            type="button"
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            disabled={isLoading}
            className="absolute right-2 top-1/2 -translate-y-1/2 rounded px-2 py-1 text-sm text-gray-600 hover:text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:text-gray-400"
            aria-label={
              showConfirmPassword ? 'Hide password' : 'Show password'
            }
          >
            {showConfirmPassword ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
                />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
                strokeWidth={1.5}
                stroke="currentColor"
                className="h-5 w-5"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
            )}
          </button>
        </div>
        {errors.confirmPassword && (
          <p
            id="confirm-password-error"
            className="text-sm text-red-600"
            role="alert"
            aria-live="polite"
          >
            {errors.confirmPassword.message}
          </p>
        )}
      </div>

      {/* Submit Button */}
      <button
        type="submit"
        disabled={isLoading || !isValid || !isDirty}
        className="w-full rounded-md bg-blue-600 px-4 py-2 text-white font-medium shadow-sm transition-all hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400 disabled:hover:bg-gray-400"
        aria-label="Create account"
      >
        {isLoading ? (
          <span className="flex items-center justify-center">
            <svg
              className="-ml-1 mr-3 h-5 w-5 animate-spin text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              ></circle>
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            <span>Creating account...</span>
          </span>
        ) : (
          'Create Account'
        )}
      </button>
    </form>
  );
};

export default RegistrationForm;

