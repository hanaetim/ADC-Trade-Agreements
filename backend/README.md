# International Agreements & Origin Application - Backend

FastAPI backend for the International Agreements & Origin Application, providing case registration, routing, trace visibility, and audit capabilities.

## Architecture

- **Framework**: FastAPI 0.115+
- **Database**: SQLite (local), PostgreSQL (deployed)
- **ORM**: SQLAlchemy 2.0 (synchronous)
- **Migrations**: Alembic
- **Authentication**: JWT with bcrypt password hashing
- **Testing**: pytest with httpx TestClient

## Prerequisites

- Python 3.11 or higher
- pip

## Setup

### Install Dependencies

```bash
pip install .
```

For PostgreSQL support:
```bash
pip install ".[postgres]"
```

For development tools (pytest, ruff, mypy):
```bash
pip install --dev
```

### Environment Configuration

Copy `dev.env` to `.env` or set environment variables:

```bash
cp dev.env .env
```

Configuration variables:
- `DATABASE_URL` - Database connection string (default: `sqlite:///./app.db`)
- `JWT_SECRET_KEY` - Secret key for JWT token signing (change in production!)
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_EXPIRY_MINUTES` - JWT token expiry time (default: 1440 = 24 hours)
- `CORS_ORIGINS` - Comma-separated list of allowed origins (default: `http://localhost:5173,http://localhost:3000`)
- `RATE_LIMIT_ENABLED` - Enable rate limiting (default: true)
- `DEBUG` - Debug mode (default: false)

### Database Setup

Run migrations:
```bash
python -m alembic upgrade head
```

Seed default users:
```bash
python -m app.seed
```

## Running the Application

Start the development server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at:
- Application: http://localhost:8000
- API Documentation: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc
- Health Check: http://localhost:8000/api/v1/health

## Default Users

The seed script creates one user per role:

| Email | Password | Role |
|-------|----------|------|
| applicant@example.com | Applicant123! | external_applicant |
| intake@example.com | Intake123! | intake_exception_handler |
| specialist@example.com | Specialist123! | specialist_reviewer |
| head@example.com | Head123! | section_head |
| policy@example.com | Policy123! | policy_legal_approver |
| committee@example.com | Committee123! | technical_committee |
| auditor@example.com | Auditor123! | auditor |

## Testing

Run all tests:
```bash
python -m pytest
```

Run with coverage:
```bash
python -m pytest --cov=app --cov-report=html
```

Run specific test file:
```bash
python -m pytest tests/test_smoke.py -v
```

## Code Quality

Run linting:
```bash
python -m ruff check app/
```

Run type checking:
```bash
python -m mypy app/
```

## Database Schema

The application uses the following core tables:

- **cases** - Canonical formal case records (FR-001, FR-002, FR-004)
- **case_attachments** - Submission evidence metadata (FR-001)
- **case_events** - Ordered step and trace event stream (FR-023, FR-024)
- **audit_logs** - Compliance and security audit log (FR-023, FR-024)
- **auth_sessions** - Revocable JWT session registry (NFR-015)
- **users** - User accounts with role-based access control

See `alembic/versions/001_initial_schema.py` for complete schema definition.

## Project Structure

```
backend/
├── alembic/                 # Database migrations
│   └── versions/
├── app/
│   ├── adapters/           # External system adapters (ICOS, etc.)
│   ├── core/               # Security utilities
│   ├── middleware/         # Custom middleware
│   ├── models/             # SQLAlchemy ORM models
│   ├── repositories/       # Data access layer
│   ├── routers/            # API route handlers
│   ├── schemas/            # Pydantic request/response models
│   ├── services/           # Business logic layer
│   ├── config.py           # Application configuration
│   ├── database.py         # Database engine and session
│   ├── main.py             # FastAPI application entry point
│   └── seed.py             # Seed data generation
├── tests/                  # Test suite
│   ├── conftest.py         # Shared test fixtures
│   └── test_smoke.py       # Smoke tests
├── .env                    # Environment variables (gitignored)
├── .env.example            # Example environment file
├── alembic.ini             # Alembic configuration
├── dev.env                 # Development environment (committed)
├── Dockerfile              # Container image definition
├── docker-entrypoint.sh    # Container entrypoint script
├── pyproject.toml          # Python project configuration
└── README.md               # This file
```

## Docker

Build the image:
```bash
docker build -t adc-trade-agreements-backend .
```

Run the container:
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=sqlite:////data/app.db \
  -v $(pwd)/data:/data \
  adc-trade-agreements-backend
```

## API Endpoints

### Health
- `GET /api/v1/health` - Health check with database connectivity status

### Authentication (to be implemented in later tasks)
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout

### Cases (to be implemented in later tasks)
- `POST /api/v1/cases` - Register a new case
- `GET /api/v1/cases` - List cases with filters
- `GET /api/v1/cases/{case_id}` - Get case details
- `GET /api/v1/cases/{case_id}/trace` - Get case trace timeline
- `POST /api/v1/cases/{case_id}/exception-actions` - Record intake exception action

## Security

- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens with expiration claims
- Session tokens stored as SHA-256 hashes
- CORS with explicit allowed origins
- Rate limiting on authentication endpoints
- Input validation via Pydantic schemas

## GDPR Compliance

- Personal data fields documented in schema comments
- Audit trail for all PII access/modification
- Soft-delete mechanism for user records
- Data retention policy metadata
- PII masking in logs

## Development

Create a new migration:
```bash
python -m alembic revision --autogenerate -m "description"
```

Rollback migration:
```bash
python -m alembic downgrade -1
```

## License

See LICENSE file in repository root.
