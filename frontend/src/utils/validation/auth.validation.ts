/**
 * Authentication Validation Schemas
 * 
 * Provides Zod validation schemas for authentication forms that match
 * backend validation requirements exactly.
 * 
 * Backend References:
 * - EmailValidator: backend/app/services/email_validator.py
 * - PasswordValidator: backend/app/services/password_validator.py
 */

import { z } from 'zod';

/**
 * Email validation schema matching backend EmailValidator
 * 
 * Backend requirements:
 * - Cannot be empty
 * - Must be a valid RFC-compliant email format
 * - Case-insensitive (normalized to lowercase)
 * 
 * Backend error messages:
 * - "Email address cannot be empty"
 * - "Email address is not valid"
 */
export const emailSchema = z
  .string()
  .min(1, 'Email address cannot be empty')
  .email('Email address is not valid');

/**
 * Password validation schema matching backend PasswordValidator
 * 
 * Backend requirements:
 * - Minimum 8 characters (MIN_LENGTH = 8)
 * - At least 1 uppercase letter (UPPERCASE_PATTERN = r'[A-Z]')
 * - At least 1 number (NUMBER_PATTERN = r'[0-9]')
 * - At least 1 special character from: !@#$%^&*(),.?":{}|<>_-+=[]\/;~`
 * 
 * Backend error messages (exact match):
 * - "Password must be at least 8 characters long"
 * - "Password must contain at least 1 uppercase letter"
 * - "Password must contain at least 1 number"
 * - "Password must contain at least 1 special character (!@#$%^&*(),.?\":{}|<>_-+=[]\/;~`)"
 */
export const passwordSchema = z
  .string()
  .min(8, 'Password must be at least 8 characters long')
  .refine(
    (password) => /[A-Z]/.test(password),
    'Password must contain at least 1 uppercase letter'
  )
  .refine(
    (password) => /[0-9]/.test(password),
    'Password must contain at least 1 number'
  )
  .refine(
    (password) => /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]/.test(password),
    'Password must contain at least 1 special character (!@#$%^&*(),.?":{}|<>_-+=[]\\\/;~`)'
  );

/**
 * Registration form validation schema
 * 
 * Validates:
 * - email: Must be valid RFC-compliant email
 * - password: Must meet all password requirements
 * - confirmPassword: Must match password
 */
export const registrationSchema = z
  .object({
    email: emailSchema,
    password: passwordSchema,
    confirmPassword: z.string().min(1, 'Please confirm your password'),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

/**
 * Type inference for registration form data
 */
export type RegistrationFormData = z.infer<typeof registrationSchema>;

/**
 * Password requirements for UI display
 * Matches backend PasswordValidator requirements exactly
 */
export const PASSWORD_REQUIREMENTS = [
  'At least 8 characters',
  'One uppercase letter',
  'One lowercase letter',
  'One number',
  'One special character (!@#$%^&*(),.?":{}|<>_-+=[]\\\/;~`)',
] as const;

/**
 * Check individual password requirements
 * Useful for showing requirement-specific feedback in UI
 */
export const checkPasswordRequirements = (password: string) => ({
  minLength: password.length >= 8,
  hasUppercase: /[A-Z]/.test(password),
  hasLowercase: /[a-z]/.test(password),
  hasNumber: /[0-9]/.test(password),
  hasSpecialChar: /[!@#$%^&*(),.?":{}|<>_\-+=\[\]\\\/;~`]/.test(password),
});

