# Users API Documentation

This document describes the Users API endpoints available in the Studio Caju backend.

## Base URL

```
/users
```

## Authorization

All endpoints require authentication via Bearer token and a tenant domain header:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Get Current User

Retrieves the authenticated user's account details.

**URL:** `GET /users/me`

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

### Change Password

Changes the authenticated user's password.

**URL:** `PATCH /users/me/change-password`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| password | string | Yes | New password |
| password_confirmation | string | Yes | Confirmation of the new password (must match password) |

**Example Request:**

```json
{
  "password": "newSecurePassword123",
  "password_confirmation": "newSecurePassword123"
}
```

**Response:**
- Status: 200 OK

```json
{
  "message": "Password has been changed!"
}
```

**Error Responses:**

- 400 Bad Request - If passwords don't match
```json
{
  "detail": "Passwords dont match."
}
```

### Delete Account

Deactivates the authenticated user's account (soft delete).

**URL:** `DELETE /users/me`

**Response:**
- Status: 200 OK

```json
{
  "message": "User deleted."
}
``` 