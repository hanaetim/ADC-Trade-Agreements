"""Correlation ID middleware for request tracing (FR-023, FR-024)."""
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    """Middleware to generate and propagate correlation IDs for request tracing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:  # type: ignore[override]
        """Generate or extract correlation ID and propagate through request context."""
        # Check if client provided correlation ID
        correlation_id = request.headers.get("X-Correlation-ID")

        # Generate new ID if not provided
        if not correlation_id:
            correlation_id = str(uuid.uuid4())

        # Store in request state for access by route handlers
        request.state.correlation_id = correlation_id

        # Process request
        response: Response = await call_next(request)  # type: ignore[assignment]

        # Add correlation ID to response headers
        response.headers["X-Correlation-ID"] = correlation_id

        return response
