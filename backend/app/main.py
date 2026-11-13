"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.middleware.correlation import CorrelationIdMiddleware
from app.middleware.error_handlers import register_error_handlers
from app.routers import auth, cases, health, trace
from app.seed import run_seed


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan for startup and shutdown events."""
    # Run seed data on startup (skip during tests)
    import os
    if not os.environ.get("TESTING"):
        run_seed()
    yield
    # Cleanup on shutdown (if needed)


app = FastAPI(
    title="International Agreements & Origin Application",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Register global error handlers
register_error_handlers(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID middleware
app.add_middleware(CorrelationIdMiddleware)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(cases.router, prefix="/api", tags=["cases"])
app.include_router(trace.router, prefix="/api/v1/cases", tags=["trace"])


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "International Agreements & Origin Application API"}
