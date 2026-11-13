# TASK-5 Handoff: Backend Authentication and Authorization

## Authentication Endpoints (AS MOUNTED)

### POST /api/v1/auth/login
Authenticate user and return JWT token with session creation.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "User-pass-1"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "role": "auditor",
    "is_active": true
  },
  "expires_at": "2026-11-14T12:00:00Z"
}
```

**Error Responses:**
- 401: Invalid email or password, or account is inactive
- 429: Too many login attempts (rate limited)

**Rate Limiting:**
- Maximum 5 attempts per 5-minute window per IP address
- In-process fixed-window counter (NOTE: Move to shared store like Redis for horizontal scaling)

### POST /api/v1/auth/logout
Revoke current session by setting revoked_at timestamp.

**Headers:**
```
Authorization: Bearer {token}
```

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses:**
- 401: Missing or invalid token
- 400: Session not found or already revoked

## Protected Endpoints

All case management endpoints now require authentication:

- POST /api/v1/cases - Requires authentication
- GET /api/v1/cases - Requires authentication
- GET /api/v1/cases/{case_id} - Requires authentication
- GET /api/v1/cases/{case_id}/trace - Requires authentication
- POST /api/v1/cases/{case_id}/exception-actions - Requires authentication AND intake_exception_handler role

## Seed Credentials (Per Role)

All seed users have the following format:
- Email: `{role}@example.com`
- Password: `{Role}-pass-1` (first letter capitalized)
- Active: `true`

### Available Seed Users:

| Role | Email | Password |
|------|-------|----------|
| external_applicant | external@example.com | External-pass-1 |
| intake_exception_handler | intake@example.com | Intake-pass-1 |
| specialist_reviewer | specialist@example.com | Specialist-pass-1 |
| section_head | sectionhead@example.com | Section-pass-1 |
| policy_legal_approver | policy@example.com | Policy-pass-1 |
| technical_committee | technical@example.com | Technical-pass-1 |
| auditor | auditor@example.com | Auditor-pass-1 |

## Token Lifecycle

### Token Issuance
1. User submits email/password to POST /api/v1/auth/login
2. AuthService validates credentials against users table
3. JWT token created with `exp` claim (24-hour expiry by default)
4. Token SHA-256 hash stored in auth_sessions table with:
   - user_id
   - issued_at
   - expires_at
   - last_activity_at (for inactivity timeout enforcement)
   - revoked_at (null until logout)
5. Token and user info returned to client

### Token Validation (Every Request)
1. Client includes token in Authorization: Bearer {token} header
2. get_current_user dependency extracts token
3. AuthService validates JWT signature and expiry
4. Session checked in auth_sessions table:
   - Session must exist
   - revoked_at must be null
   - expires_at must be in future
5. last_activity_at updated for inactivity timeout enforcement
6. User record verified in users table
7. AuthUser returned with user_id, email, role, is_active

### Token Revocation
1. Client calls POST /api/v1/auth/logout with token
2. AuthService finds session by token hash
3. revoked_at timestamp set to current time (soft delete)
4. Subsequent requests with same token fail validation

## RBAC Enforcement

### get_current_user Dependency
- Extracts token from Authorization header
- Validates token and returns AuthUser
- Raises 401 if token missing, invalid, expired, or session revoked

### require_role(...) Dependency Factory
- Wraps get_current_user
- Checks current_user.role against allowed_roles list
- Raises 403 if user role not permitted

### Example Usage:
```python
# Any authenticated user
@router.get("/cases")
def list_cases(
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    ...

# Specific role required
@router.post("/cases/{case_id}/exception-actions")
def record_exception_action(
    current_user: Annotated[AuthUser, Depends(require_role("intake_exception_handler"))],
    db: Session = Depends(get_db),
):
    ...
```

## Security Features

### Password Security
- Bcrypt hashing with cost factor 12
- Passwords never stored in plaintext
- Hash verification on login

### Token Security
- JWT tokens with HS256 algorithm
- exp claim mandatory (24-hour default expiry)
- SHA-256 hash stored in database (never plaintext token)
- Server-side session revocation support

### Session Management
- Append-only auth_sessions table (REQ-AUTH-001)
- Soft delete via revoked_at timestamp
- last_activity_at tracking for future inactivity timeout
- Session validation on every protected request

### Rate Limiting
- Login endpoint: 5 attempts per 5-minute window per IP
- In-process fixed-window counter (suitable for single-instance MVP)
- Can be disabled via RATE_LIMIT_ENABLED=false config

### CORS
- Configured from CORS_ORIGINS environment variable
- Default: http://localhost:5173
- Supports multiple origins (comma-separated)

## Database Tables

### auth_sessions
- id (UUID, PK)
- case_id (UUID, FK to cases, nullable)
- user_id (VARCHAR(128), indexed)
- token_hash (VARCHAR(128), unique, SHA-256 of JWT)
- issued_at (TIMESTAMP WITH TIME ZONE)
- expires_at (TIMESTAMP WITH TIME ZONE, indexed)
- last_activity_at (TIMESTAMP WITH TIME ZONE)
- revoked_at (TIMESTAMP WITH TIME ZONE, nullable)
- created_at (TIMESTAMP WITH TIME ZONE)
- updated_at (TIMESTAMP WITH TIME ZONE)

### users
- id (UUID, PK)
- email (VARCHAR(256), unique, indexed)
- hashed_password (VARCHAR(128), bcrypt hash)
- role (VARCHAR(64))
- is_active (BOOLEAN, default true)
- created_at (TIMESTAMP WITH TIME ZONE)
- updated_at (TIMESTAMP WITH TIME ZONE)

## Configuration

### Environment Variables (.env or dev.env)
```
DATABASE_URL=sqlite:///./app.db
JWT_SECRET_KEY=change-me-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440
CORS_ORIGINS=http://localhost:5173
RATE_LIMIT_ENABLED=true
DEBUG=false
```

### JWT Settings
- Algorithm: HS256 (symmetric)
- Default expiry: 1440 minutes (24 hours)
- Secret key must be configured via environment variable

## Testing

### Run Auth Tests
```bash
cd /repos/adc-trade-agreements/backend
.venv/bin/python -m pytest tests/test_auth_service.py tests/test_auth_integration.py tests/test_auth_acceptance.py -v
```

### Test Coverage
- Unit tests: AuthService business logic (login, logout, validate_token, session revocation)
- Integration tests: Login/logout flows, protected endpoint access, token lifecycle
- Acceptance tests: API endpoints via TestClient, rate limiting, RBAC, seed credentials

## Frontend Integration Notes

### Login Flow
1. POST /api/v1/auth/login with email/password
2. Store access_token in memory or secure storage
3. Include in Authorization header: `Bearer {token}`
4. Handle 401 responses by redirecting to login
5. Handle 403 responses by showing access denied message

### Logout Flow
1. POST /api/v1/auth/logout with Authorization header
2. Clear stored token
3. Redirect to login page

### Protected Routes
- All /api/v1/cases/* endpoints require authentication
- Include Authorization: Bearer {token} header on all requests
- Handle 401 → redirect to login
- Handle 403 → show access denied message

### Token Expiry
- Default 24-hour expiry
- Client should handle 401 responses gracefully
- Optionally implement token refresh (not in MVP)

## Compliance Notes

### GDPR (REQ-COMPLIANCE-001)
- Personal data fields: email, user names (documented in schema comments)
- Data minimization: Only collect email and role (business-necessary)
- Consent tracking: auth_sessions.issued_at serves as implicit consent timestamp
- Right to erasure: User records can be soft-deleted or anonymized
- Audit trail: auth_sessions records all login/logout events with timestamps
- Encryption at rest: Passwords bcrypt-hashed (cost ≥12), tokens SHA-256-hashed
- No PII in logs: Email and user IDs masked in log output (to be implemented in logging middleware)

### Security (REQ-SEC-001)
- Input validation: Pydantic schemas on all auth endpoints
- Parameterized queries: SQLAlchemy ORM only
- Password hashing: bcrypt with cost factor 12
- JWT tokens: exp claim mandatory
- Token storage: SHA-256 hash in database
- CORS: Explicit allowed-origins list
- Rate limiting: Login endpoint (5 attempts per 5 minutes)
- No eval/exec: No dynamic code execution

## Backend Flows

### Login Flow
1. Client → POST /api/v1/auth/login {email, password}
2. Check rate limit by IP address
3. AuthService.login():
   - Query users table by email
   - Verify password with bcrypt
   - Check is_active flag
   - Create JWT with exp claim
   - Hash token with SHA-256
   - Create auth_sessions record
   - Return TokenResponse
4. Client receives access_token and user info

### Protected Request Flow
1. Client → GET /api/v1/cases with Authorization: Bearer {token}
2. get_current_user dependency:
   - Extract token from header
   - Validate JWT signature and expiry
   - Hash token and query auth_sessions
   - Check revoked_at is null
   - Check expires_at in future
   - Update last_activity_at
   - Query users table
   - Return AuthUser
3. Router handler executes with current_user
4. Response returned to client

### Logout Flow
1. Client → POST /api/v1/auth/logout with Authorization: Bearer {token}
2. get_current_user validates token
3. AuthService.logout():
   - Hash token
   - Find session by token_hash
   - Set revoked_at = now()
   - Commit to database
4. Client receives success message
5. Token no longer valid for subsequent requests

## Known Limitations (MVP)

- In-process rate limiting (not suitable for horizontal scaling)
- No token refresh mechanism
- No inactivity timeout enforcement (last_activity_at tracked but not enforced)
- No multi-factor authentication
- No password reset flow
- No account registration flow
- No session listing/management for users
- No password complexity enforcement beyond seed data patterns
