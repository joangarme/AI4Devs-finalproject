# Task Breakdown: US1.1 - Account Registration

## User Story

**As a** Sarah (Budget-Conscious Partner),  
**I want** to create a secure account with my email and password,  
**So that** I can start tracking my finances privately and securely.

**MVP Scope Note**: This implementation focuses on basic authentication only. Email verification has been deferred to post-MVP to accelerate delivery of core finance tracking features.

**Acceptance Criteria (MVP):**

- Email validation with proper format checking
- Password requirements: minimum 8 characters, 1 uppercase, 1 number, 1 special character
- Clear error messages for validation failures
- Success confirmation and automatic login
- Duplicate email prevention

**Post-MVP Features:**

- Email verification sent upon registration
- Email service provider configuration
- Email verification page and workflow

## Task Breakdown

### Development Sequence

---

### Task ID: US1.1-T1

**Type**: [Database]  
**Title**: Create users table schema  
**Story Points**: 0.5  
**Dependencies**: None

#### Description

**What**: Create the users table with fields for authentication  
**Input**: Data model specification for user entity  
**Output**: Migration script for users table  
**Boundary**: Only base table structure, no indexes or verification tables

#### Acceptance Criteria

- [ ] Table includes: id, email, password_hash, created_at, updated_at, is_active
- [ ] Email field has unique constraint
- [ ] Migration script is reversible
- [ ] Appropriate data types used (VARCHAR for email, TEXT for password_hash)
- [ ] All users created are active by default (MVP: no email verification)

#### Testing Requirements

- [ ] Test migration up and down functionality
- [ ] Verify all columns created with correct types
- [ ] Test unique constraint on email
- [ ] Verify default values are set correctly

#### Technical Notes

- Use Alembic for migration management
- Password_hash field should accommodate bcrypt output (60 chars)
- Consider adding fields for future OAuth integration
- **MVP**: Removed `is_verified` field - all users are active upon registration

---

### Task ID: US1.1-T2

**Type**: [Backend]  
**Title**: Create user authentication Pydantic models  
**Story Points**: 0.5  
**Dependencies**: None

#### Description

**What**: Define request/response models for user registration  
**Input**: API specification for authentication endpoints  
**Output**: Pydantic model classes in schemas/auth.py  
**Boundary**: Only data models, no validation logic beyond basic types

#### Acceptance Criteria

- [ ] UserRegisterRequest model with email and password fields
- [ ] UserRegisterResponse model with user info (excluding password)
- [ ] UserLoginRequest model with email and password fields
- [ ] Proper typing for all fields

#### Testing Requirements

- [ ] Test model instantiation with valid data
- [ ] Test basic field type validation
- [ ] Test serialization/deserialization
- [ ] Verify password field is excluded from response

#### Technical Notes

- Use Pydantic v2 syntax
- Email field should use EmailStr type
- Password should be SecretStr in request model

---

### Task ID: US1.1-T3

**Type**: [Backend]  
**Title**: Implement password validation service  
**Story Points**: 0.5  
**Dependencies**: None

#### Description

**What**: Create service to validate password requirements  
**Input**: Password string  
**Output**: services/password_validator.py  
**Boundary**: Only validation logic, no hashing or storage

#### Acceptance Criteria

- [ ] Validates minimum 8 characters
- [ ] Checks for at least 1 uppercase letter
- [ ] Checks for at least 1 number
- [ ] Checks for at least 1 special character
- [ ] Returns specific error messages for each failed requirement

#### Testing Requirements

- [ ] Test each validation rule independently
- [ ] Test valid passwords pass all checks
- [ ] Test boundary cases (exactly 8 chars, etc.)
- [ ] Test error message accuracy
- [ ] 100% code coverage

#### Technical Notes

- Use regex for pattern matching
- Return list of validation errors, not just boolean
- Consider making requirements configurable

---

### Task ID: US1.1-T4

**Type**: [Backend]  
**Title**: Implement email validation service  
**Story Points**: 0.5  
**Dependencies**: None

#### Description

**What**: Create service to validate email format and check duplicates  
**Input**: Email string and database connection  
**Output**: services/email_validator.py  
**Boundary**: Format validation and duplicate check only, no email sending

#### Acceptance Criteria

- [ ] Validates email format using RFC-compliant regex
- [ ] Checks for existing email in database
- [ ] Returns clear error messages
- [ ] Case-insensitive duplicate checking

#### Testing Requirements

- [ ] Test valid email formats
- [ ] Test invalid email formats
- [ ] Test duplicate detection
- [ ] Test case-insensitive matching
- [ ] Test SQL injection prevention

#### Technical Notes

- Use email-validator library for RFC compliance
- Normalize emails to lowercase before storage
- Consider checking MX records in future iteration

---

### Task ID: US1.1-T5

**Type**: [Backend]  
**Title**: Create user registration service  
**Story Points**: 1  
**Dependencies**: US1.1-T3, US1.1-T4

#### Description

**What**: Implement core registration logic with password hashing  
**Input**: Validated email and password  
**Output**: services/user_service.py with register method  
**Boundary**: User creation only, no email sending

#### Acceptance Criteria

- [ ] Hashes password using bcrypt
- [ ] Creates user record in database
- [ ] Sets user as active by default (MVP: no verification required)
- [ ] Handles database errors gracefully
- [ ] Returns created user (without password)

#### Testing Requirements

- [ ] Test successful user creation
- [ ] Test password is properly hashed
- [ ] Test user is created as active by default
- [ ] Test transaction rollback on errors
- [ ] Test duplicate email handling
- [ ] Integration test with real database

#### Technical Notes

- Use bcrypt with cost factor of 12
- Wrap in database transaction
- **MVP**: No verification token generation needed

---

### Task ID: US1.1-T6

**Type**: [Backend]  
**Title**: Create POST /auth/register endpoint  
**Story Points**: 1  
**Dependencies**: US1.1-T2, US1.1-T5

#### Description

**What**: Implement API endpoint for user registration  
**Input**: UserRegisterRequest model  
**Output**: Working registration endpoint  
**Boundary**: HTTP handling only, delegates to services

#### Acceptance Criteria

- [ ] Accepts POST requests with email/password
- [ ] Validates input using services
- [ ] Returns 201 with user data on success
- [ ] Returns 400 with validation errors
- [ ] Returns 409 for duplicate email

#### Testing Requirements

- [ ] Test successful registration flow
- [ ] Test all validation error scenarios
- [ ] Test duplicate email response
- [ ] Test malformed request handling
- [ ] Test rate limiting (if implemented)
- [ ] API documentation auto-generated

#### Technical Notes

- Use FastAPI dependency injection
- Include request ID in logs
- Consider rate limiting for security
- **MVP**: User is immediately active and can log in after registration

---

### Task ID: US1.1-T7

**Type**: [Frontend]  
**Title**: Build registration form component  
**Story Points**: 1  
**Dependencies**: None

#### Description

**What**: Create React component for registration form  
**Input**: UI mockups and form requirements  
**Output**: RegistrationForm.tsx component  
**Boundary**: UI component only, no API integration

#### Acceptance Criteria

- [ ] Email and password input fields
- [ ] Password strength indicator
- [ ] Real-time validation feedback
- [ ] Submit button with loading state
- [ ] Accessible form with proper labels

#### Testing Requirements

- [ ] Component renders all fields
- [ ] Password strength indicator works correctly
- [ ] Form validation prevents invalid submission
- [ ] Loading states display properly
- [ ] Accessibility tests (ARIA, keyboard nav)
- [ ] Responsive design tests

#### Technical Notes

- Use React Hook Form for form management
- Consider zxcvbn for password strength
- Implement debounced validation

---

### Task ID: US1.1-T8

**Type**: [Frontend]  
**Title**: Implement client-side form validation  
**Story Points**: 0.5  
**Dependencies**: US1.1-T7

#### Description

**What**: Add validation logic matching backend requirements  
**Input**: Form component and validation rules  
**Output**: Enhanced form with validation  
**Boundary**: Client-side validation only

#### Acceptance Criteria

- [ ] Email format validation
- [ ] Password requirement checks
- [ ] Real-time validation feedback
- [ ] Clear error messages
- [ ] Validation matches backend exactly

#### Testing Requirements

- [ ] Test each validation rule
- [ ] Test error message display
- [ ] Test validation timing (onChange vs onBlur)
- [ ] Test form submission prevention
- [ ] Test edge cases

#### Technical Notes

- Use Yup or Zod for validation schema
- Ensure consistent validation with backend
- Consider i18n for error messages

---

### Task ID: US1.1-T9

**Type**: [Frontend]  
**Title**: Create registration page with API integration  
**Story Points**: 1  
**Dependencies**: US1.1-T7, US1.1-T8

#### Description

**What**: Build complete registration page with form and API calls  
**Input**: Registration form component and API client  
**Output**: RegisterPage.tsx with full functionality  
**Boundary**: Registration flow only, no email verification UI

#### Acceptance Criteria

- [ ] Integrates registration form component
- [ ] Handles API submission
- [ ] Shows success message
- [ ] Automatically logs user in after successful registration (MVP)
- [ ] Redirects to dashboard on success
- [ ] Displays API errors appropriately

#### Testing Requirements

- [ ] Test successful registration and auto-login flow
- [ ] Test API error handling
- [ ] Test network error scenarios
- [ ] Test loading states
- [ ] Test redirect to dashboard behavior
- [ ] Integration test with mock API

#### Technical Notes

- Use React Query for API state management
- Handle both field-level and general errors
- Store JWT token after successful registration for auto-login
- **MVP**: No email verification flow needed

---

## Task Summary

**Total Tasks**: 9 (MVP-focused)  
**Total Story Points**: 6.5 (13-26 hours)  
**Removed from MVP**: 6 tasks (3 story points) - Email verification functionality

### By Type:

- **Database**: 1 task (0.5 points)
- **Backend**: 5 tasks (4 points)
- **Frontend**: 3 tasks (2.5 points)

### Critical Path:

1. Database setup (T1)
2. Backend models and services (T2-T5)
3. Backend API endpoint (T6)
4. Frontend implementation (T7-T9)

### Deferred to Post-MVP:

- Email verification tokens table
- Email sending service
- Email verification endpoint
- Email verification page
- Email service provider configuration
- Email templates

These features will be implemented alongside US1.4 (Password Reset) in a future iteration.

## Verification Checklist

- [x] Every MVP acceptance criterion is addressed by at least one task
- [x] No task exceeds 1 story point
- [x] Each task includes testing requirements
- [x] Tasks follow logical build sequence
- [x] All tasks use the exact template format
- [x] Dependencies are clearly defined
- [x] Testing is integrated into each task
- [x] Email verification features clearly marked as Post-MVP
- [x] MVP focuses on basic authentication to accelerate delivery

## MVP Simplification Summary

This task breakdown has been simplified for MVP delivery (due October 15th) by removing email verification functionality. Users can now register and immediately start using the application without waiting for email confirmation.

**Key Changes:**

- Removed 6 tasks related to email verification (3 story points)
- Users are created as active by default
- Successful registration automatically logs the user in
- Duplicate email prevention still enforced via database constraint
- Email verification will be added in post-MVP alongside password reset functionality

**Benefits:**

- 27% reduction in implementation time
- No external dependencies (email service provider)
- Users can start tracking finances immediately
- Maintains security through strong password requirements and duplicate prevention
