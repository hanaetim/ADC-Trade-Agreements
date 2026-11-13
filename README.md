# Abu Dhabi Customs - International Agreements & Origin Application

A full-stack web application enabling Abu Dhabi Customs to execute international agreements and origin management workflows with consistency, traceability, and controllable automation while preserving human authority at defined decision gates.

## Project Purpose

The International Agreements & Origin application provides:
- **Automated intake and routing** with deterministic policy enforcement via AGN1 (Intake & Routing Agent)
- **Case management** for origin rulings, agreement updates, inquiries, studies, certificate sampling, and disputes
- **Full audit trail** with immutable event and audit logs for every case transition
- **Role-based access control** supporting seven distinct user roles from external applicants to technical committee members
- **Visibility policy enforcement** ensuring appropriate information disclosure based on role
- **Traceable decision-making** with recorded rationale for all agent-assisted and deterministic rule outcomes

## Directory Structure

```
adc-trade-agreements/
├── backend/                 # FastAPI backend (Python 3.11+)
│   ├── app/
│   │   ├── main.py         # Application entrypoint, router registration
│   │   ├── config.py       # Environment-driven settings
│   │   ├── database.py     # SQLAlchemy engine, session, Base
│   │   ├── models/         # ORM models (cases, users, events, audit)
│   │   ├── schemas/        # Pydantic request/response DTOs
│   │   ├── repositories/   # Data access layer
│   │   ├── services/       # Business logic (agents, rules, routing)
│   │   ├── routers/        # API endpoints (/api/v1/*)
│   │   ├── middleware/     # Auth, CORS, error handling, correlation
│   │   └── adapters/       # External system integrations (ICOS)
│   ├── alembic/            # Database migrations
│   ├── tests/              # Unit, integration, acceptance tests
│   ├── dev.env             # Local development configuration (committed)
│   ├── pyproject.toml      # Dependencies and build config
│   ├── Dockerfile          # Backend container image
│   └── docker-entrypoint.sh # Migration runner for containers
│
├── frontend/                # React + TypeScript + Vite frontend
│   ├── src/
│   │   ├── App.tsx         # Route configuration
│   │   ├── main.tsx        # Application entrypoint
│   │   ├── lib/            # API client, auth context
│   │   ├── pages/          # Page components (Queue, Submission, Detail, Trace)
│   │   ├── components/     # Reusable UI components
│   │   └── types/          # TypeScript interfaces (mirrors backend schemas)
│   ├── e2e/                # Playwright end-to-end tests
│   ├── package.json        # Dependencies and scripts
│   ├── vite.config.ts      # Dev server with /api proxy
│   ├── Dockerfile          # Frontend container image (nginx)
│   └── default.conf.template # Nginx configuration for API proxy
│
├── start.sh                # Cross-platform startup script (macOS, Linux, Windows/Git Bash)
├── stop.sh                 # Service shutdown script
├── docker-compose.yml      # SQLite-based container deployment
├── docker-compose.postgres.yml # PostgreSQL override for production
├── .github/workflows/ci.yml # CI pipeline (lint, type-check, test, build)
└── README.md               # This file
```

## Prerequisites

### For Local Development (No Docker Required)

- **Python 3.11+** — [Download](https://python.org/downloads)
- **Node.js 20.19+ or 22.12+** with npm — [Download](https://nodejs.org)
- **Git** — Required on Windows for `start.sh` execution via Git Bash

### For Docker Deployment

- **Docker** 24+ and **Docker Compose** 2.20+

## Quick Start (Local Development)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd adc-trade-agreements
   ```

2. **Start the application**

   ```bash
   ./start.sh
   ```

   On **Windows**, run `start.bat` (which launches `start.sh` via Git Bash), or run `start.sh` directly in Git Bash.

   The script will:
   - Check prerequisites (Python 3.11+, Node.js 20.19+/22.12+, npm)
   - Create Python virtual environment (`.venv/`) if missing
   - Install backend dependencies (`pip install .`)
   - Copy `backend/dev.env` to `backend/.env` if `.env` does not exist
   - Run database migrations (`alembic upgrade head`)
   - Seed the database with 7 users and 4 sample cases
   - Find available ports (backend from 9000, frontend from 5173)
   - Start backend server (uvicorn)
   - Start frontend dev server (Vite with `/api` proxy to backend)
   - Display URLs and seed credentials

3. **Access the application**

   - **Frontend**: http://localhost:5173 (or next available port)
   - **Backend API Docs**: http://localhost:9000/docs (or next available port)
   - **Backend Health**: http://localhost:9000/health

4. **Log in** with one of the seed credentials (see table below)

5. **Stop the application**

   Press `Ctrl+C` in the terminal running `start.sh`, or run:

   ```bash
   ./stop.sh
   ```

## Seed Credentials

Seven users are created automatically with different roles:

| Role | Email | Password | Capabilities |
|------|-------|----------|--------------|
| **External Applicant** | external@example.com | External-pass-1 | Submit cases, view own submissions |
| **Intake Exception Handler** | intake@example.com | Intake-pass-1 | Resolve intake exceptions, take manual actions on blocked cases |
| **Specialist Reviewer** | specialist@example.com | Specialist-pass-1 | Review and validate case details |
| **Section Head** | sectionhead@example.com | Section-pass-1 | Approve decisions at section level |
| **Policy & Legal Approver** | policy@example.com | Policy-pass-1 | Review policy/legal escalations |
| **Technical Committee** | technical@example.com | Technical-pass-1 | Handle technical disputes |
| **Auditor** | auditor@example.com | Auditor-pass-1 | View audit logs and case traces |

## API Documentation

When the backend is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:9000/docs
- **ReDoc**: http://localhost:9000/redoc

### Key Endpoints

All API endpoints are mounted under `/api/v1`:

- **POST /api/v1/auth/login** — Authenticate and receive JWT token
- **POST /api/v1/auth/logout** — Revoke current session
- **POST /api/v1/cases** — Register new case
- **GET /api/v1/cases** — List cases (with pagination and filters)
- **GET /api/v1/cases/{case_id}** — Get case details
- **GET /api/v1/cases/{case_id}/trace** — View complete case trace with events
- **POST /api/v1/cases/{case_id}/exception-actions** — Take manual action on blocked cases (requires `intake_exception_handler` role)
- **GET /api/v1/health** — Health check (unauthenticated)

## Testing

### Backend Tests

```bash
cd backend

# Activate virtual environment
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Run all tests
python -m pytest tests/ -v

# Run tests with coverage
python -m pytest tests/ --cov=app --cov-report=term-missing

# Run specific test categories
python -m pytest tests/test_agn1_orchestrator.py -v        # AGN1 agent tests
python -m pytest tests/test_auth_acceptance.py -v          # Auth API tests
python -m pytest tests/test_case_acceptance.py -v          # Case API tests
python -m pytest tests/test_trace_acceptance.py -v         # Trace API tests

# Lint and type-check
python -m ruff check app/
python -m mypy app/ --ignore-missing-imports
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm test

# Run unit tests in watch mode
npm run test -- --watch

# Lint and type-check
npm run lint
npm run type-check

# Build production bundle
npm run build
```

### End-to-End Tests

```bash
cd frontend

# Run Playwright E2E tests (requires both backend and frontend running)
npx playwright test

# Run specific test suite
npx playwright test e2e/wireframe_01_case_submission.spec.ts
npx playwright test e2e/journey_new_request_to_routing.spec.ts

# Show test report
npx playwright show-report
```

## Docker Deployment

### SQLite (Development/Single-Instance)

```bash
# Start services
docker compose up

# Start in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f frontend
```

Access the application at http://localhost

### PostgreSQL (Production)

```bash
# Start with PostgreSQL
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up

# Start in background
docker compose -f docker-compose.yml -f docker-compose.postgres.yml up -d

# Stop services
docker compose -f docker-compose.yml -f docker-compose.postgres.yml down

# Remove volumes (WARNING: deletes all data)
docker compose -f docker-compose.yml -f docker-compose.postgres.yml down -v
```

The PostgreSQL override:
- Runs `postgres:16-alpine` as the `database` service
- Updates backend `DATABASE_URL` to point at the database service
- Installs PostgreSQL driver via `pip install .[postgres]`
- Persists data in `postgres-data` volume

## Database Management

### Migrations

Migrations are managed with Alembic and run automatically by `start.sh` and the Docker entrypoint.

```bash
cd backend
source .venv/bin/activate

# Apply all pending migrations
alembic upgrade head

# Create new migration (after modifying models)
alembic revision --autogenerate -m "Description of change"

# Review the generated migration before committing
cat alembic/versions/<new_revision>.py

# Downgrade one revision
alembic downgrade -1

# Show current revision
alembic current

# Show migration history
alembic history
```

### Seed Data

The seed script is idempotent and safe to run multiple times:

```bash
cd backend
source .venv/bin/activate
python -m app.seed
```

Seeds:
- 7 users (one per role) with known passwords
- 4 sample cases in various states (routed, intake_blocked, queued_for_review)
- Case events showing ATS1→ATS2→ATS3 intake workflow execution
- Audit log entries for case registration

## Environment Configuration

### Backend (`backend/.env`)

The application reads configuration from `backend/.env`. On first run, `start.sh` copies `backend/dev.env` to `backend/.env`.

Key settings:

```bash
# Database (SQLite for local dev, PostgreSQL for production)
DATABASE_URL=sqlite:///./app.db

# JWT authentication
JWT_SECRET_KEY=dev-secret-key-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=1440

# CORS (automatically updated by start.sh with frontend port)
CORS_ORIGINS=["http://localhost:5173"]

# Rate limiting
RATE_LIMIT_ENABLED=true

# Debug mode (disable in production)
DEBUG=true
```

**Production checklist**:
- Set `DATABASE_URL` to PostgreSQL connection string
- Generate cryptographically secure `JWT_SECRET_KEY`
- Set `DEBUG=false`
- Configure `CORS_ORIGINS` with actual frontend domain(s)
- Review `JWT_EXPIRY_MINUTES` per security policy

### Frontend

The frontend uses `import.meta.env.VITE_API_URL ?? '/api'` as the API base URL. By default, all API calls are relative (`/api/...`) and proxied:

- **Local dev**: Vite dev server proxies `/api` to `http://localhost:<BACKEND_PORT>`
- **Docker**: nginx forwards `/api` to `backend:8000`
- **Production**: Set `VITE_API_URL` environment variable at build time only if the API is on a different origin

No frontend `.env` file is required for local development.

## CI/CD

The `.github/workflows/ci.yml` workflow runs on push and pull requests to `main`:

### Backend Job
1. Starts PostgreSQL service container
2. Installs Python 3.11 and dependencies
3. Runs `ruff check app/` (lint)
4. Runs `mypy app/` (type-check)
5. Runs `alembic upgrade head` (migrations against PostgreSQL)
6. Runs `pytest --cov=app` (tests with coverage)

### Frontend Job
1. Installs Node.js 22 and dependencies
2. Runs `npm run lint`
3. Runs `npm run type-check`
4. Runs `npm test` (Vitest unit tests)
5. Runs `npm run build` (production build)

Both jobs must pass for the build to succeed.

## Architecture

### Backend Stack
- **Framework**: FastAPI 0.115+
- **ORM**: SQLAlchemy 2.0+ (synchronous)
- **Migrations**: Alembic 1.14+
- **Validation**: Pydantic 2.10+
- **Auth**: PyJWT 2.10+ with bcrypt password hashing
- **Database**: SQLite (local), PostgreSQL 16+ (production)

### Frontend Stack
- **Framework**: React 18.3+
- **Language**: TypeScript 5.7+
- **Build Tool**: Vite 6.0+
- **Routing**: React Router 6.28+
- **Styling**: Tailwind CSS 3.4+
- **Testing**: Vitest 2.1+, Playwright 1.49+

### Key Features Implemented (MVP Scope)

- **FR-001**: Case registration with unique IAO-YYYY-NNNNNN reference, workflow classification, and reasoned rejection
- **FR-002**: Completeness and eligibility validation at intake via Deterministic Rule Engine
- **FR-004**: Workflow routing to correct atomic step and accountable role
- **FR-023**: Per-case step and trace view with agent outputs, routing decisions, and recorded rationale
- **FR-024**: Visibility of reasoning, routing, and approval chain with role-based evidence inspection

### Agent Orchestration

**AGN1 (Intake & Routing Agent)** executes the ATS1→ATS2→ATS3 workflow:

- **ATS1 (Completeness Validation)**: Deterministic Rule Engine checks required fields
- **ATS2 (Eligibility Validation)**: Deterministic Rule Engine validates workflow type eligibility
- **ATS3 (Routing Resolution)**: Agent classifies workflow type and resolves next step + accountable role

Outcome states:
- `routed` — Case successfully passed intake and routed to next workflow step
- `intake_blocked` — Case failed completeness/eligibility validation, routed to intake exception queue
- `queued_for_review` — Case passed intake but requires manual review before proceeding

**AGN2-AGN6 are registered but deferred** (not implemented in MVP):
- AGN2: Request Comprehension (deferred)
- AGN3: Origin Determination (deferred)
- AGN4: Decision Drafting (deferred)
- AGN5: Approval & Issuance (deferred)
- AGN6: Dispute Adjudication (deferred)

### Security Features

- **Password hashing**: bcrypt with cost factor 12
- **JWT tokens**: Mandatory `exp` claim, tokens stored as SHA-256 hashes in database
- **Session management**: Revocable sessions with inactivity timeout tracking
- **Rate limiting**: 5 login attempts per 5-minute window per IP (disabled for E2E tests via `RATE_LIMIT_ENABLED=false`)
- **RBAC**: Role-based endpoint protection via `require_role()` dependency
- **Audit trail**: Immutable audit_log and case_events tables recording all security-relevant actions
- **CORS**: Explicit origin allowlist, never wildcard with credentials
- **Input validation**: Pydantic schemas with field-level validators on all endpoints
- **SQL injection prevention**: Parameterized queries via SQLAlchemy ORM only

### Observability

- **Correlation IDs**: Generated per request via middleware, propagated through all service calls and audit logs
- **Audit logging**: Dedicated `AuditService` records security/compliance events with severity, actor, entity tracking
- **Structured events**: Immutable `case_events` table captures every case transition with decision source (deterministic vs agent)
- **Health endpoints**: `/health` for liveness, `/api/v1/health` for authenticated health check

## Production Deployment Notes

### Database
- **Use PostgreSQL 16+** in production (required for horizontal scaling, proven enterprise-grade reliability)
- Enable connection pooling (already configured in SQLAlchemy engine for PostgreSQL dialect)
- Set up automated backups and point-in-time recovery (PITR)
- Review retention policies for `audit_log` and `case_events` tables

### Security
- Generate cryptographically secure `JWT_SECRET_KEY` (minimum 32 bytes, base64-encoded random)
- Set `DEBUG=false`
- Configure `CORS_ORIGINS` with actual frontend domain(s), never `["*"]`
- Use HTTPS/TLS for all traffic
- Rotate JWT secret on a defined schedule
- Review rate limiting thresholds for production load
- Enable firewall rules to restrict database access

### Infrastructure
- **Horizontal scaling**: Backend is stateless and horizontally scalable (all session state in database)
- **Rate limiting**: Move from in-process counter to shared store (Redis) when running multiple backend instances
- **Session storage**: Consider Redis for session cache to reduce database load
- **CDN**: Serve frontend static assets via CDN
- **Load balancer**: Use health endpoint (`/health`) for liveness checks

### Monitoring
- Track request rate, latency, error rate
- Monitor database connection pool usage
- Alert on failed login attempts (potential brute-force)
- Track agent execution disposition (success/failure rates)
- Monitor audit log growth rate

### Compliance
- Audit logs retained per regulatory requirements (default: indefinite, review for GDPR/compliance)
- Session tokens revocable on logout (supports "right to be forgotten")
- Personal data documented in models (email, applicant_name)
- Data minimization: only collect required fields

## Troubleshooting

### Port Already in Use
If `start.sh` reports ports 9000 or 5173 in use, it automatically finds the next available port. Check the output for actual URLs.

### Python Version Issues
- **"Python 3.11+ required"**: Install Python 3.11 or later from python.org
- **Windows "python3 not found"**: Use `python` instead of `python3` after activating venv

### Node Version Issues
- **"Node.js 20.19+ or 22.12+ required"**: Install Node.js 22.x LTS from nodejs.org
- Check version: `node --version`

### Database Migration Errors
```bash
# Reset database (WARNING: deletes all data)
cd backend
rm app.db
source .venv/bin/activate
alembic upgrade head
python -m app.seed
```

### Frontend Build Errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Docker Issues
- **Port conflicts**: Stop services using port 80/8000, or modify `docker-compose.yml` ports
- **Build failures**: Run `docker compose build --no-cache`
- **Database connection errors**: Ensure PostgreSQL service is healthy: `docker compose logs database`

### Authentication Issues
- **401 Unauthorized**: Token may be expired (check JWT_EXPIRY_MINUTES) or invalid
- **403 Forbidden**: User lacks required role for endpoint
- **429 Too Many Requests**: Rate limit exceeded, wait 5 minutes or disable with `RATE_LIMIT_ENABLED=false`

## Development Workflow

### Adding a New Feature

1. **Update models** in `backend/app/models/`
2. **Create migration**: `cd backend && alembic revision --autogenerate -m "Add feature"`
3. **Review and edit** the generated migration file
4. **Add schemas** in `backend/app/schemas/`
5. **Add repository methods** in `backend/app/repositories/`
6. **Add service logic** in `backend/app/services/`
7. **Add router endpoints** in `backend/app/routers/`
8. **Add tests**: unit (`test_<feature>_service.py`), integration (`test_<feature>_integration.py`), acceptance (`test_<feature>_acceptance.py`)
9. **Add frontend types** in `frontend/src/types/`
10. **Add UI components** in `frontend/src/components/` and `frontend/src/pages/`
11. **Add frontend tests** in `frontend/src/__tests__/`
12. **Update API documentation** (auto-generated from FastAPI schemas)

### Code Quality

```bash
# Backend
cd backend
source .venv/bin/activate
ruff check app/           # Lint
mypy app/                 # Type-check
pytest --cov=app          # Test with coverage

# Frontend
cd frontend
npm run lint              # ESLint
npm run type-check        # TypeScript
npm test                  # Vitest
npm run build             # Production build verification
```

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions, please contact the Abu Dhabi Customs development team.
