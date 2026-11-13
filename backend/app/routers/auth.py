"""Authentication endpoints."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth import get_current_user
from app.middleware.rate_limit import login_rate_limiter
from app.schemas.auth import AuthUser, LoginRequest, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT token.

    Request body:
        - email: User email address
        - password: User password

    Returns:
        - access_token: JWT token for authentication
        - token_type: Always "bearer"
        - user: User profile with id, email, role, is_active
        - expires_at: Token expiration timestamp

    Raises:
        401: Invalid credentials or inactive account
        429: Too many login attempts (rate limited)
        500: Internal server error

    Rate limiting:
        - Maximum 5 attempts per 5-minute window (per IP address)
        - In-process fixed-window counter for single-instance MVP
        - NOTE: Move to shared store (Redis) for horizontal scaling
    """
    # Check rate limit by IP address
    client_ip = request.client.host if request.client else "unknown"
    if login_rate_limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later.",
        )

    auth_service = AuthService(db)

    try:
        token_response = auth_service.login(
            email=credentials.email,
            password=credentials.password,
        )
        return token_response
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post("/logout")
def logout(
    request: Request,
    current_user: Annotated[AuthUser, Depends(get_current_user)],
    db: Session = Depends(get_db),
):
    """
    Revoke current session by setting revoked_at timestamp.

    Requires authentication via Authorization: Bearer {token} header.

    Returns:
        - message: Success confirmation

    Raises:
        401: Missing or invalid token
        500: Internal server error
    """
    # Extract token from Authorization header
    authorization = request.headers.get("Authorization", "")
    parts = authorization.split()

    if len(parts) != 2:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header",
        )

    token = parts[1]

    # Revoke session
    auth_service = AuthService(db)
    revoked = auth_service.logout(token)

    if not revoked:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session not found or already revoked",
        )

    return {"message": "Logged out successfully"}
