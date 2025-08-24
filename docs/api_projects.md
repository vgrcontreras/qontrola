# Projects API Documentation

This document describes the Projects API endpoints available in the Studio Caju backend.

## Base URL

```
/projects
```

## Authorization

All endpoints require authentication via Bearer token and a tenant domain header:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Create Project

Creates a new project within the current tenant.

**URL:** `POST /projects`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Project name |
| status_state | string | No | Project status state |
| project_value | float | No | Project monetary value |
| target_date | date | No | Project target completion date (YYYY-MM-DD) |

**Example Request:**

```json
{
  "name": "Customer Portal",
  "status_state": "active",
  "project_value": 50000.00,
  "target_date": "2023-12-31"
}
```

**Response:**
- Status: 201 Created

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Customer Portal",
  "status_state": "active",
  "project_value": 50000.00,
  "target_date": "2023-12-31",
  "created_at": "2023-07-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

**Error Responses:**

- 400 Bad Request - If the project already exists
```json
{
  "detail": "Project already exists"
}
```

### Get Project by ID

Retrieves a specific project by its ID.

**URL:** `GET /projects/{project_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_id | UUID | Yes | ID of the project to retrieve |

**Response:**
- Status: 200 OK

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Customer Portal",
  "status_state": "active",
  "project_value": 50000.00,
  "target_date": "2023-12-31",
  "created_at": "2023-07-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": null,
  "updated_by": null
}
```

**Error Responses:**

- 404 Not Found - If the project doesn't exist
```json
{
  "detail": "Project doesn't exist"
}
```

### List Projects

Retrieves all projects for the current tenant.

**URL:** `GET /projects`

**Response:**
- Status: 200 OK

```json
{
  "projects": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "Customer Portal",
      "status_state": "active",
      "project_value": 50000.00,
      "target_date": "2023-12-31",
      "created_at": "2023-07-20T14:30:45.123456",
      "created_by": "456e7890-12d3-a456-426614174000",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true,
      "updated_at": null,
      "updated_by": null
    }
  ]
}
```

### Update Project

Updates an existing project.

**URL:** `PATCH /projects/{project_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_id | UUID | Yes | ID of the project to update |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | New project name |
| status_state | string | No | New project status state |
| project_value | float | No | New project monetary value |
| target_date | date | No | New project target completion date (YYYY-MM-DD) |

**Example Request:**

```json
{
  "status_state": "completed",
  "project_value": 55000.00
}
```

**Response:**
- Status: 200 OK

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Customer Portal",
  "status_state": "completed",
  "project_value": 55000.00,
  "target_date": "2023-12-31",
  "created_at": "2023-07-20T14:30:45.123456",
  "created_by": "456e7890-12d3-a456-426614174000",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true,
  "updated_at": "2023-07-25T15:45:30.123456",
  "updated_by": "456e7890-12d3-a456-426614174000"
}
```

**Error Responses:**

- 404 Not Found - If the project doesn't exist
```json
{
  "detail": "Project doesn't exist"
}
```

- 409 Conflict - If updating the name and the new name already exists
```json
{
  "detail": "Project already exists"
}
```

### Delete Project

Deactivates a project (soft delete). Requires superuser privileges.

**URL:** `DELETE /projects/{project_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| project_id | UUID | Yes | ID of the project to delete |

**Response:**
- Status: 200 OK

```json
{
  "message": "Project deleted"
}
```

**Error Responses:**

- 404 Not Found - If the project doesn't exist
```json
{
  "detail": "Project doesn't exist"
}
``` 