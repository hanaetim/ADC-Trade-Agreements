"""Authentication request/response schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class LoginRequest(BaseModel):
    """Login request body."""

    email: EmailStr
    password: str


class AuthUser(BaseModel):
    """Authenticated user information."""

    user_id: uuid.UUID
    email: str
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    """Token response with access token and user info."""

    access_token: str
    token_type: str
    user: AuthUser
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)
