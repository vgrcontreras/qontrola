# Superuser API Documentation

This document describes the Superuser API endpoints available in the Studio Caju backend.

## Base URL

```
/superuser
```

## Authorization

All endpoints in this section require authentication via Bearer token, a tenant domain header, and superuser privileges:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Create User

Creates a new user within the current tenant.

**URL:** `POST /superuser`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | User's email address |
| password | string | Yes | User's password |
| is_active | boolean | No | Whether the user is active (default: true) |
| is_superuser | boolean | No | Whether the user has superuser privileges (default: false) |

**Example Request:**

```json
{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "is_superuser": false
}
```

**Response:**
- Status: 201 Created

```json
{
  "id": "456e7890-12d3-a456-426614174000",
  "email": "newuser@example.com",
  "is_active": true,
  "is_superuser": false,
  "tenant_id": "789e0123-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456"
}
```

**Error Responses:**

- 400 Bad Request - If the user already exists
```json
{
  "detail": "User already exists"
}
```

### List Users

Retrieves all users in the current tenant.

**URL:** `GET /superuser`

**Response:**
- Status: 200 OK

```json
{
  "users": [
    {
      "id": "456e7890-12d3-a456-426614174000",
      "email": "admin@example.com",
      "is_active": true,
      "is_superuser": true,
      "tenant_id": "789e0123-a456-426614174000",
      "created_at": "2024-04-20T14:30:45.123456"
    },
    {
      "id": "567f8901-23e4-5678-9012-34567890abcd",
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "tenant_id": "789e0123-a456-426614174000",
      "created_at": "2024-04-20T15:30:45.123456"
    }
  ]
}
```

### Get User by ID

Retrieves a specific user by ID.

**URL:** `GET /superuser/{user_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | UUID | Yes | ID of the user to retrieve |

**Response:**
- Status: 200 OK

```json
{
  "id": "456e7890-12d3-a456-426614174000",
  "email": "user@example.com",
  "is_active": true,
  "is_superuser": false,
  "tenant_id": "789e0123-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456"
}
```

**Error Responses:**

- 404 Not Found - If the user doesn't exist
```json
{
  "detail": "User Not Found"
}
```

### Update User

Updates an existing user's information.

**URL:** `PATCH /superuser/{user_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | UUID | Yes | ID of the user to update |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | No | New email address |
| password | string | No | New password |
| is_active | boolean | No | New active status |
| is_superuser | boolean | No | New superuser status |

**Example Request:**

```json
{
  "is_superuser": true,
  "email": "promoted_user@example.com",
  "is_active": true,
  "is_superuser": true
}
```

**Response:**
- Status: 200 OK

```json
{
  "id": "456e7890-12d3-a456-426614174000",
  "email": "promoted_user@example.com",
  "is_active": true,
  "is_superuser": true,
  "tenant_id": "789e0123-a456-426614174000",
  "created_at": "2024-04-20T14:30:45.123456"
}
```

**Error Responses:**

- 404 Not Found - If the user doesn't exist
```json
{
  "detail": "User Not Found"
}
```

- 409 Conflict - If the email is already in use
```json
{
  "detail": "User email already exists"
}
```

### Delete User

Deactivates a user (soft delete).

**URL:** `DELETE /superuser/{user_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_id | UUID | Yes | ID of the user to delete |

**Response:**
- Status: 200 OK

```json
{
  "message": "User deleted"
}
```

**Error Responses:**

- 404 Not Found - If the user doesn't exist
```json
{
  "detail": "User Not Found"
}
``` 