from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskRequestCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = 'to_do'
    priority: str = 'medium'
    due_date: date | None = None
    project_id: UUID
    category_name: str | None = None


class TaskResponse(BaseModel):
    id: UUID
    title: str
    description: str | None
    status: str
    priority: str
    due_date: date | None
    project_id: UUID
    created_at: datetime
    created_by: UUID
    is_active: bool
    category_id: UUID | None = None

    model_config = ConfigDict(from_attributes=True)


class TaskRequestGet(TaskResponse):
    updated_at: datetime | None
    updated_by: UUID | None

    model_config = ConfigDict(from_attributes=True)


class TaskRequestGetList(BaseModel):
    tasks: list[TaskRequestGet]


class TaskRequestUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None
    due_date: date | None = None
    project_id: UUID | None = None
    category_name: str | None = None
