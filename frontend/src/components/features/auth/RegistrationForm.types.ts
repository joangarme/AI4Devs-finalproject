/**
 * Form data interface for registration
 */
export interface RegistrationFormData {
  email: string;
  password: string;
  confirmPassword: string;
}

/**
 * Password strength levels
 */
export interface PasswordStrength {
  score: number;
  label: string;
  color: string;
  bgColor: string;
}

/**
 * Component props for RegistrationForm
 */
export interface RegistrationFormProps {
  onSubmit: (data: RegistrationFormData) => Promise<void>;
  isLoading?: boolean;
}
