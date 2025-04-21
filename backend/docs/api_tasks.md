# Tasks API Documentation

This document describes the Tasks API endpoints available in the Studio Caju backend.

## Base URL

```
/tasks
```

## Authorization

All endpoints require authentication via Bearer token and a tenant domain header:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Create Task

Creates a new task within a project.

**URL:** `POST /tasks`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Task title |
| description | string | No | Task description |
| status | string | No | Task status (default: "to_do") |
| priority | string | No | Task priority (default: "medium") |
| due_date | date | No | Task due date (format: YYYY-MM-DD) |
| project_id | UUID | Yes | ID of the project to which the task belongs |

**Example Request:**

```json
{
  "title": "Implement user authentication",
  "description": "Add login, registration, and password reset functionality",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-30",
  "project_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

**Response:**
- Status: 201 Created

```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement user authentication",
  "description": "Add login, registration, and password reset functionality",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-30",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

**Error Responses:**

- 404 Not Found - If the project doesn't exist
```json
{
  "detail": "Project doesn't exist"
}
```

- 400 Bad Request - If required fields are missing
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Get Task by ID

Retrieves a specific task by its ID.

**URL:** `GET /tasks/{task_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | ID of the task to retrieve |

**Response:**
- Status: 200 OK

```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement user authentication",
  "description": "Add login, registration, and password reset functionality",
  "status": "to_do",
  "priority": "high",
  "due_date": "2024-05-30",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": null,
  "updated_by": null
}
```

**Error Responses:**

- 404 Not Found - If the task doesn't exist
```json
{
  "detail": "Task doesn't exist"
}
```

### List Tasks

Retrieves all tasks for the current tenant, with optional filtering by project.

**URL:** `GET /tasks`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_id | UUID | No | Filter tasks by project ID |

**Response:**
- Status: 200 OK

```json
{
  "tasks": [
    {
      "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
      "title": "Implement user authentication",
      "description": "Add login, registration, and password reset functionality",
      "status": "to_do",
      "priority": "high",
      "due_date": "2024-05-30",
      "project_id": "123e4567-e89b-12d3-a456-426614174000",
      "created_at": "2024-04-20T14:30:45.123456",
      "created_by": "456e7890-12d3-a456-426614174000",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true,
      "updated_at": null,
      "updated_by": null
    }
  ]
}
```

### Update Task

Updates an existing task.

**URL:** `PATCH /tasks/{task_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | ID of the task to update |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | No | New task title |
| description | string | No | New task description |
| status | string | No | New task status |
| priority | string | No | New task priority |
| due_date | date | No | New task due date (format: YYYY-MM-DD) |
| project_id | UUID | No | New project ID |

**Example Request:**

```json
{
  "status": "in_progress",
  "description": "Updated description with additional details"
}
```

**Response:**
- Status: 200 OK

```json
{
  "id": "098f6bcd-4621-3373-8ade-4e832627b4f6",
  "title": "Implement user authentication",
  "description": "Updated description with additional details",
  "status": "in_progress",
  "priority": "high",
  "due_date": "2024-05-30",
  "project_id": "123e4567-e89b-12d3-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": "2024-04-20T15:45:30.123456",
  "updated_by": "456e7890-12d3-a456-426614174000"
}
```

**Error Responses:**

- 404 Not Found - If the task doesn't exist
```json
{
  "detail": "Task doesn't exist"
}
```

- 404 Not Found - If updating the project_id and the new project doesn't exist
```json
{
  "detail": "Project doesn't exist"
}
```

### Delete Task

Deactivates a task (soft delete).

**URL:** `DELETE /tasks/{task_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| task_id | UUID | Yes | ID of the task to delete |

**Response:**
- Status: 200 OK

```json
{
  "message": "Task deleted"
}
```

**Error Responses:**

- 404 Not Found - If the task doesn't exist
```json
{
  "detail": "Task doesn't exist"
}
```

## Common Status and Priority Values

While the API accepts any string values for status and priority, the following values are recommended for consistency:

### Status Values
- `to_do` - Task has not been started
- `in_progress` - Task is currently being worked on
- `review` - Task is completed and awaiting review
- `done` - Task is completed and approved

### Priority Values
- `low` - Low priority task
- `medium` - Medium priority task
- `high` - High priority task
- `critical` - Critical priority task 