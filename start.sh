#!/bin/bash
# start.sh — Start the full-stack Abu Dhabi Customs International Agreements & Origin application
set -e
trap 'echo "Shutting down..."; [ -f .pids ] && while IFS= read -r pid; do kill "$pid" 2>/dev/null || true; done < .pids; rm -f .pids; exit 0' SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"
cd "$PROJECT_ROOT"

# Helper for native Windows path conversion under Git Bash
native_path() { 
    if command -v cygpath >/dev/null 2>&1; then 
        cygpath -m "$1"
    else 
        printf '%s' "$1"
    fi
}

# Port detection (works with or without lsof)
port_in_use() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1
    else
        netstat -an 2>/dev/null | grep -Eq "[:.]$1[[:space:]].*LISTEN"
    fi
}

find_available_port() {
    local port=$1
    while port_in_use "$port"; do
        echo "Port $port in use, trying $((port+1))..." >&2
        port=$((port+1))
    done
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Python 3.11+ (probe by running it - python3 may be Windows Store stub under Git Bash)
    PYTHON=""
    for c in python3 python; do
        if "$c" -c 'import sys' >/dev/null 2>&1; then
            PYTHON=$c
            break
        fi
    done

    if [ -n "$PYTHON" ]; then
        PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
            echo "❌ Python 3.11+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    # Node.js 20.19+/22.12+ (check engines from frontend/package.json: ^20.19.0 || >=22.12.0)
    if command -v node &>/dev/null; then
        NODE_VERSION=$(node --version | sed 's/v//')
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
        NODE_MINOR=$(echo $NODE_VERSION | cut -d. -f2)
        
        # Accept Node 20.19+ or Node 22.12+
        if [ "$NODE_MAJOR" -eq 20 ] && [ "$NODE_MINOR" -ge 19 ]; then
            echo "✓ Node.js $NODE_VERSION"
        elif [ "$NODE_MAJOR" -ge 22 ]; then
            # Node 22+ accepted, but verify minor for 22.x
            if [ "$NODE_MAJOR" -eq 22 ] && [ "$NODE_MINOR" -lt 12 ]; then
                echo "❌ Node.js 20.19+ or 22.12+ required (found $NODE_VERSION)"
                errors=$((errors+1))
            else
                echo "✓ Node.js $NODE_VERSION"
            fi
        else
            echo "❌ Node.js 20.19+ or 22.12+ required (found $NODE_VERSION)"
            errors=$((errors+1))
        fi
    else
        echo "❌ Node.js not found. Install from https://nodejs.org"
        errors=$((errors+1))
    fi

    # npm
    if ! command -v npm &>/dev/null; then
        echo "❌ npm not found"
        errors=$((errors+1))
    else
        echo "✓ npm $(npm --version)"
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# Stop any existing services from a previous run
echo "=== Cleaning up previous run ==="
if [ -f .pids ]; then
    while IFS= read -r pid; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "  Stopping PID $pid from previous run..."
            kill "$pid" 2>/dev/null || true
        fi
    done < .pids
    rm -f .pids
fi

# === Backend setup ===
BACKEND_DIR="$PROJECT_ROOT/backend"
echo "=== Setting up backend ==="
cd "$BACKEND_DIR"

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "  Creating virtual environment..."
    "$PYTHON" -m venv .venv
fi

# Activate venv (Git Bash on Windows uses Scripts/, macOS/Linux uses bin/)
if [ -f .venv/Scripts/activate ]; then 
    source .venv/Scripts/activate
else 
    source .venv/bin/activate
fi

# Install dependencies
echo "  Installing backend dependencies..."
pip install . -q

# Copy dev.env to .env if .env does not exist
if [ ! -f .env ]; then
    echo "  Creating .env from dev.env..."
    cp dev.env .env
fi

# Database migrations
echo "  Running database migrations..."
python -m alembic upgrade head

# Run seed data (idempotent)
echo "  Seeding database..."
python -m app.seed

# Pick free backend port starting from 9000
BACKEND_PORT=$(find_available_port 9000)

# === Frontend setup ===
FRONTEND_DIR="$PROJECT_ROOT/frontend"
echo ""
echo "=== Setting up frontend ==="
cd "$FRONTEND_DIR"

echo "  Installing frontend dependencies..."
npm install -q

# Pick free frontend port starting from 5173
FRONTEND_PORT=$(find_available_port 5173)

# Update CORS_ORIGINS in backend/.env to include frontend URL
echo "  Configuring CORS for frontend at http://localhost:$FRONTEND_PORT..."
cd "$BACKEND_DIR"
if grep -q "^CORS_ORIGINS=" .env; then
    # Use Python for reliable JSON array manipulation
    python -c "
import os
import json
cors = os.environ.get('CORS_ORIGINS', 'http://localhost:5173')
try:
    origins = json.loads(cors) if cors.startswith('[') else [cors]
except:
    origins = [cors]
frontend_origin = 'http://localhost:$FRONTEND_PORT'
if frontend_origin not in origins:
    origins.append(frontend_origin)
# Write back as JSON array
with open('.env', 'r') as f:
    lines = f.readlines()
with open('.env', 'w') as f:
    for line in lines:
        if line.startswith('CORS_ORIGINS='):
            f.write(f'CORS_ORIGINS={json.dumps(origins)}\n')
        else:
            f.write(line)
" || echo "CORS_ORIGINS=[\"http://localhost:$FRONTEND_PORT\"]" >> .env
else
    echo "CORS_ORIGINS=[\"http://localhost:$FRONTEND_PORT\"]" >> .env
fi

# === Start services ===
echo ""
echo "=== Starting services ==="

# Start backend
cd "$BACKEND_DIR"
echo "  Starting backend on http://localhost:$BACKEND_PORT..."
python -m uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT &
BACKEND_PID=$!
echo "$BACKEND_PID" > "$PROJECT_ROOT/.pids"

# Start frontend (BACKEND_PORT env var is read by vite.config.ts proxy)
cd "$FRONTEND_DIR"
echo "  Starting frontend on http://localhost:$FRONTEND_PORT..."
BACKEND_PORT="$BACKEND_PORT" npm run dev -- --port "$FRONTEND_PORT" &
FRONTEND_PID=$!
echo "$FRONTEND_PID" >> "$PROJECT_ROOT/.pids"

cd "$PROJECT_ROOT"

echo ""
echo "=========================================="
echo "=== Services running ==="
echo "  Backend:  http://localhost:$BACKEND_PORT"
echo "  Frontend: http://localhost:$FRONTEND_PORT"
echo "  API Docs: http://localhost:$BACKEND_PORT/docs"
echo ""
echo "=== Default Seed Credentials ==="
echo "  External Applicant:"
echo "    Email:    external@example.com"
echo "    Password: External-pass-1"
echo ""
echo "  Intake Exception Handler:"
echo "    Email:    intake@example.com"
echo "    Password: Intake-pass-1"
echo ""
echo "  Specialist Reviewer:"
echo "    Email:    specialist@example.com"
echo "    Password: Specialist-pass-1"
echo ""
echo "  Section Head:"
echo "    Email:    sectionhead@example.com"
echo "    Password: Section-pass-1"
echo ""
echo "  Policy & Legal Approver:"
echo "    Email:    policy@example.com"
echo "    Password: Policy-pass-1"
echo ""
echo "  Technical Committee:"
echo "    Email:    technical@example.com"
echo "    Password: Technical-pass-1"
echo ""
echo "  Auditor:"
echo "    Email:    auditor@example.com"
echo "    Password: Auditor-pass-1"
echo ""
echo "=========================================="
echo ""
echo "Press Ctrl+C to stop all services"
wait
