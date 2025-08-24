# Task Feature Implementation

**Date:** April 20, 2024  
**Feature:** Task Management  
**Author:** Studio Caju Team

## Overview

The Task feature extends the application with task management capabilities, allowing users to create, track, and manage tasks associated with projects. Each task belongs to a project and includes properties like title, description, status, priority, and due date.

## Implementation Details

### Database Schema

The Task model has been added to the application with the following properties:

| Field | Type | Description | Constraints |
|-------|------|-------------|------------|
| id | UUID | Primary key | Auto-generated |
| title | string | Task title | Required |
| description | string | Task description | Optional |
| status | string | Current status | Default: "to_do" |
| priority | string | Priority level | Default: "medium" |
| due_date | date | Deadline | Optional |
| project_id | UUID | Associated project | Required, Foreign key |
| tenant_id | UUID | Associated tenant | Required, Foreign key |
| created_by | UUID | User who created the task | Required |
| created_at | datetime | Creation timestamp | Auto-generated |
| updated_by | UUID | User who last updated the task | Optional |
| updated_at | datetime | Last update timestamp | Auto-updated |
| is_active | boolean | Whether the task is active | Default: true |

### Relationships

- Each task belongs to one project (`Project`)
- Each task belongs to one tenant (`Tenant`)
- Projects have a one-to-many relationship with tasks

### API Endpoints

The following REST API endpoints have been implemented:

#### Create a New Task

```
POST /tasks
```

Creates a new task within the specified project.

**Request Body:**
```json
{
  "title": "Implement login page",
  "description": "Create a responsive login page with email and password fields",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-15",
  "project_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response:** (201 Created)
```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement login page",
  "description": "Create a responsive login page with email and password fields",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-15",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

#### Get a Task by ID

```
GET /tasks/{task_id}
```

Retrieves a specific task by its ID.

**Response:** (200 OK)
```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement login page",
  "description": "Create a responsive login page with email and password fields",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-15",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": null,
  "updated_by": null
}
```

#### List All Tasks

```
GET /tasks
```

Retrieves all tasks for the current tenant.

**Optional Query Parameters:**
- `project_id`: Filter tasks by project ID

**Response:** (200 OK)
```json
{
  "tasks": [
    {
      "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
      "title": "Implement login page",
      "description": "Create a responsive login page with email and password fields",
      "status": "to_do",
      "priority": "high",
      "due_date": "2024-05-15",
      "project_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2024-04-20T14:30:45.123456",
      "created_by": "456e7890-12d3-a456-426614174000",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true,
      "updated_at": null,
      "updated_by": null
    },
    {
      "id": "098f6bcd-4621-3373-8ade-4e832627b4f7",
      "title": "Design database schema",
      "description": "Create ERD and SQL scripts for the new module",
      "status": "in_progress",
      "priority": "medium",
      "due_date": "2024-05-10",
      "project_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2024-04-19T10:15:30.123456",
      "created_by": "456e7890-12d3-a456-426614174000",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true,
      "updated_at": "2024-04-20T09:30:00.123456",
      "updated_by": "456e7890-12d3-a456-426614174000"
    }
  ]
}
```

#### Update a Task

```
PATCH /tasks/{task_id}
```

Updates an existing task.

**Request Body:**
```json
{
  "title": "Implement login page with OAuth",
  "status": "in_progress",
  "priority": "high"
}
```

**Response:** (200 OK)
```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement login page with OAuth",
  "description": "Create a responsive login page with email and password fields",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-05-15",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": "2024-04-20T15:45:30.123456",
  "updated_by": "456e7890-12d3-a456-426614174000"
}
```

#### Delete a Task

```
DELETE /tasks/{task_id}
```

Deactivates a task (soft delete).

**Response:** (200 OK)
```json
{
  "message": "Task deleted"
}
```

### Error Handling

The API returns appropriate error responses in the following cases:

- **404 Not Found**: When the task or project doesn't exist
- **400 Bad Request**: When required fields are missing
- **401 Unauthorized**: When the user is not authenticated
- **403 Forbidden**: When the user doesn't have permission to access the task

Example error response:

```json
{
  "detail": "Project doesn't exist"
}
```

## Data Models

### Task Model (SQLAlchemy)

```python
@table_registry.mapped_as_dataclass
class Task:
    __tablename__ = 'tasks'

    # Required fields without defaults
    title: Mapped[str] = mapped_column(nullable=False)
    # Foreign keys
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False
    )
    tenant_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey('tenants.id'), nullable=False
    )
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    
    # Fields with defaults or init=False
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), init=False, primary_key=True, default=uuid.uuid4
    )
    description: Mapped[str] = mapped_column(nullable=True, default=None)
    status: Mapped[str] = mapped_column(nullable=False, default='to_do')
    priority: Mapped[str] = mapped_column(nullable=False, default='medium')
    due_date: Mapped[date] = mapped_column(nullable=True, default=None)
    # Relationships
    project: Mapped['Project'] = relationship(
        back_populates='tasks', init=False
    )
    tenant: Mapped['Tenant'] = relationship(
        back_populates='tasks', init=False
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, onupdate=func.now(), nullable=True
    )
    updated_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=None, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(default=True)
```

### Schema Models (Pydantic)

```python
class TaskRequestCreate(BaseModel):
    title: str
    description: str | None = None
    status: str = 'to_do'
    priority: str = 'medium'
    due_date: date | None = None
    project_id: UUID


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
    tenant_id: UUID
    is_active: bool

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
```

## Usage Examples

### Creating a Task

```python
import requests
import uuid
from datetime import date

api_url = "http://localhost:8000"
headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Tenant-Domain": "example.com"
}

task_data = {
    "title": "Implement user registration",
    "description": "Create API endpoints and frontend for user registration",
    "status": "to_do",
    "priority": "high",
    "due_date": "2024-06-01",
    "project_id": str(project_id)  # UUID of an existing project
}

response = requests.post(f"{api_url}/tasks", json=task_data, headers=headers)
if response.status_code == 201:
    task = response.json()
    print(f"Task created with ID: {task['id']}")
else:
    print(f"Error: {response.json()}")
```

### Updating Task Status

```python
import requests

api_url = "http://localhost:8000"
headers = {
    "Authorization": f"Bearer {access_token}",
    "X-Tenant-Domain": "example.com"
}

update_data = {
    "status": "in_progress"
}

task_id = "098f6bcd-4621-3373-8ade-4e832627b4f6"  # ID of existing task
response = requests.patch(f"{api_url}/tasks/{task_id}", json=update_data, headers=headers)
if response.status_code == 200:
    task = response.json()
    print(f"Task updated: {task['title']} - Status: {task['status']}")
else:
    print(f"Error: {response.json()}")
```

## Testing

The implementation includes comprehensive tests for all endpoints, covering:

- Task creation
- Task retrieval (by ID and listing)
- Task updating
- Task deletion
- Error handling for various scenarios

## Migration Guide

To add the tasks table to your database, run the following command:

```bash
alembic revision --autogenerate -m "Add Task model"
alembic upgrade head
```

## Note on Status and Priority Values

While the current implementation accepts any string for status and priority, common values are:

**Status:**
- `to_do` - Not started
- `in_progress` - Currently being worked on
- `review` - Ready for review
- `done` - Completed

**Priority:**
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority
- `critical` - Critical priority 