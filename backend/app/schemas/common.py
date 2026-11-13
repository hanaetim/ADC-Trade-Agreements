"""Common schemas for API responses."""
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T")


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    detail: str
    status_code: int

    model_config = ConfigDict(json_schema_extra={"example": {"detail": "Resource not found", "status_code": 404}})


class PaginatedResponse(Generic[T], BaseModel):
    """Paginated collection wrapper."""

    items: list[T]
    total: int
    page: int
    page_size: int

    model_config = ConfigDict(from_attributes=True)
