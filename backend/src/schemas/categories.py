"""Category schemas for the API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CategoryCreate(BaseModel):
    """Schema for creating a new category."""

    name: str


class CategoryResponse(BaseModel):
    """Schema for category response."""

    id: UUID
    name: str
    tenant_id: UUID
    created_at: datetime
    updated_at: datetime | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class CategoryList(BaseModel):
    """Schema for list of categories."""

    categories: list[CategoryResponse]
