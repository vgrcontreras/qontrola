from datetime import date, datetime

from pydantic import BaseModel


class ProjectRequestCreate(BaseModel):
    name: str
    status_state: str | None = None
    project_value: float | None = None
    target_date: date | None = None


class ProjectResponse(BaseModel):
    id: int
    name: str
    status_state: str
    project_value: float
    target_date: date
    created_at: datetime
    created_by: int
    is_active: bool


class ProjectRequestGet(ProjectResponse):
    updated_at: datetime | None
    updated_by: int | None


class ProjectRequestGetList(BaseModel):
    projects: list[ProjectRequestGet]


class ProjectResquestUpdate(BaseModel):
    name: str | None = None
    status_state: str | None = None
    project_value: float | None = None
    target_date: date | None = None
