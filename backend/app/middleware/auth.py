"""Authentication middleware and dependencies."""
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.auth import AuthUser
from app.services.auth_service import AuthService


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> AuthUser:
    """
    FastAPI dependency to extract and validate current user from Authorization header.

    Args:
        request: FastAPI request object
        db: Database session

    Returns:
        AuthUser with validated user info

    Raises:
        HTTPException 401: If token is missing or invalid
    """
    # Extract token from Authorization: Bearer {token} header
    authorization = request.headers.get("Authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )

    parts = authorization.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = parts[1]

    # Validate token via AuthService
    auth_service = AuthService(db)

    try:
        user = auth_service.validate_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def require_role(*allowed_roles: str):
    """
    FastAPI dependency factory for RBAC enforcement.

    Args:
        allowed_roles: Roles permitted to access the endpoint

    Returns:
        Dependency function that raises 403 if user role not in allowed_roles
    """

    def role_checker(current_user: Annotated[AuthUser, Depends(get_current_user)]) -> AuthUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}",
            )
        return current_user

    return role_checker
