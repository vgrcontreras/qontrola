from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectRequestCreate(BaseModel):
    name: str
    status_state: str | None = None
    project_value: float | None = None
    target_date: date | None = None
    category_name: str | None = None


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    status_state: str | None
    project_value: float | None
    target_date: date | None
    created_at: datetime
    created_by: UUID
    is_active: bool
    category_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class ProjectRequestGet(ProjectResponse):
    updated_at: datetime | None
    updated_by: UUID | None

    model_config = ConfigDict(from_attributes=True)


class ProjectRequestGetList(BaseModel):
    projects: list[ProjectRequestGet]


class ProjectResquestUpdate(BaseModel):
    name: str | None = None
    status_state: str | None = None
    project_value: float | None = None
    target_date: date | None = None
    category_name: str | None = None
