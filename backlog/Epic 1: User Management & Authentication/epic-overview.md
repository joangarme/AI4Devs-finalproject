# Epic 1: User Management & Authentication

**Jira Epic**: AI4DFP-2  
**Priority**: High  
**Business Value**: Foundation for secure, multi-user financial management with proper access control

**Description**: Implement secure user authentication and role-based access control for couples to manage their financial data independently and collaboratively. This epic establishes the user identity system, account security, and base currency preferences that underpin all financial tracking features.

**Key Features**:

- User registration with email validation and verification
- Secure password management with strong requirements
- JWT-based authentication system
- Base currency selection for multi-currency support
- Profile management and preferences
- Session management and security
- Partner account linking (Post-MVP)
- Password reset and account recovery (Post-MVP)
- Role-based permissions system (Post-MVP)
- Two-factor authentication (Post-MVP)

**MVP Scope**:

For the initial MVP (due October 15th), this epic focuses on:

- ✅ US1.1: Account Registration (essential for user onboarding)
- ✅ US1.3: Base Currency Selection (required for multi-currency support)
- ❌ US1.2: Partner Account Linking (deferred - users can have separate accounts)
- ❌ US1.4: Secure Password Reset (deferred - manual recovery process acceptable)
- ❌ US1.5: Role-Based Permissions (deferred - basic permissions sufficient)

**Definition of Done**

- All MVP user stories (US1.1, US1.3) implemented and tested
- Users can register with email and password
- Email verification system working
- Strong password requirements enforced
- Base currency selection during registration/profile setup
- JWT authentication working for API access
- All tests passing locally and in CI
- API documentation complete for auth endpoints
- Security best practices implemented (password hashing, secure tokens)
- Frontend forms accessible and responsive
- Clear error messaging for validation failures
- Performance acceptable (< 500ms for auth operations)

---

## User Stories

### US1.1: Account Registration (MVP)

**As a** Sarah (Budget-Conscious Partner),  
**I want** to create a secure account with my email and password,  
**So that** I can start tracking my finances privately and securely.

**Acceptance Criteria:**

- Email validation with proper format checking
- Password requirements: minimum 8 characters, 1 uppercase, 1 number, 1 special character
- Email verification sent upon registration
- Clear error messages for validation failures
- Success confirmation and redirect to login
- Duplicate email prevention

---

### US1.2: Partner Account Linking (Post-MVP)

**As a** Sarah (Budget-Conscious Partner),  
**I want** to link my account with my partner's account,  
**So that** we can share certain financial data while maintaining individual privacy.

**Acceptance Criteria:**

- Partner invitation via email with secure token
- Ability to accept/reject partner invitations
- Clear indication of linked partner status
- Option to unlink partner account with confirmation
- Shared data permissions clearly displayed
- Both partners must confirm the link

**MVP Note**: Deferred to post-MVP. Users will create separate accounts without linking functionality.

---

### US1.3: Base Currency Selection (MVP)

**As a** Maria (International Couple),  
**I want** to set my preferred base currency during profile setup,  
**So that** all my financial data is displayed in my familiar currency.

**Acceptance Criteria:**

- Currency dropdown with major currencies (EUR, USD, GBP, BRL, etc.)
- Currency symbol preview
- Ability to change base currency with recalculation warning
- Default to user's locale currency if detected
- Save preference to user profile
- Apply immediately to all displays

---

### US1.4: Secure Password Reset (Post-MVP)

**As a** David (Financial Planner),  
**I want** to reset my password securely if I forget it,  
**So that** I can regain access to my financial data without compromising security.

**Acceptance Criteria:**

- Password reset link sent to registered email only
- Reset token expires after 1 hour
- Old password invalidated after successful reset
- Email notification sent after password change
- Cannot reuse last 5 passwords
- Account locked after 5 failed attempts

**MVP Note**: Deferred to post-MVP. Manual password recovery through support acceptable for MVP timeline.

---

### US1.5: Role-Based Permissions (Post-MVP)

**As a** Alex (Tech-Savvy Partner),  
**I want** to configure detailed permissions for data sharing with my partner,  
**So that** I maintain control over which financial information is private or shared.

**Acceptance Criteria:**

- Granular permissions: view-only, edit, delete per resource type
- Default permissions set to most restrictive
- Permission changes require confirmation
- Audit log of all permission modifications
- Visual indicators for shared vs. private data
- Batch permission updates available

**MVP Note**: Deferred to post-MVP. Basic user-level permissions (all data owned by user) sufficient for initial release.

---

## Technical Architecture Notes

### Authentication Flow

- JWT tokens with access/refresh token pattern
- Access tokens expire in 15 minutes
- Refresh tokens expire in 7 days
- Secure httpOnly cookies for token storage

### Security Considerations

- Passwords hashed with bcrypt (cost factor 12)
- Email verification tokens expire in 24 hours
- Rate limiting on auth endpoints
- CSRF protection for state-changing operations
- SQL injection prevention via ORM

### Database Schema

- `users` table: id, email, password_hash, is_verified, is_active, base_currency, created_at, updated_at
- `email_verification_tokens` table: id, user_id, token, expires_at, created_at, used_at
- `refresh_tokens` table (Post-MVP): id, user_id, token, expires_at, created_at, revoked_at

### Dependencies

- FastAPI for backend API
- SQLAlchemy for ORM
- Alembic for migrations
- Pydantic for validation
- React Hook Form for frontend forms
- React Query for API state management

---

## Implementation Timeline (MVP)

**Week 1 - Account Registration (US1.1)**

- Days 1-2: Database schema and backend services
- Days 2-3: API endpoints and validation
- Days 3-4: Frontend registration form
- Day 5: Email verification and integration testing

**Week 1 - Base Currency Selection (US1.3)**

- Days 4-5: Currency model and user profile integration
- Can be developed in parallel with registration completion

**Estimated Effort**: 5 days with 1 developer, assuming 8-hour days
