# Studio Caju API Documentation

This document provides an overview of all API endpoints available in the Studio Caju backend.

## API Groups

The API is organized into the following groups:

- [Tasks](api_tasks.md) - Manage tasks within projects
- [Projects](api_projects.md) - Manage projects within the tenant
- [Clients](api_clients.md) - Manage client organizations
- [Login](api_login.md) - Authentication endpoints
- [Users](api_users.md) - User self-management endpoints
- [Superuser](api_superuser.md) - User management endpoints (admin-only)
- [Tenants](api_tenants.md) - Tenant registration and management

## Common Headers

### Authentication

Most endpoints require authentication via Bearer token:

```
Authorization: Bearer <access_token>
```

### Tenant Context

Most endpoints also require specifying the tenant context:

```
X-Tenant-Domain: <tenant_domain>
```

## Error Formats

All error responses follow a standard format:

```json
{
  "detail": "Error message or error details object"
}
```

For validation errors, the detail will be an array:

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "error message",
      "type": "error_type"
    }
  ]
}
```

## Status Codes

The API uses conventional HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource successfully created
- `400 Bad Request` - Invalid input or validation error
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists or conflict
- `500 Internal Server Error` - Server error

## Getting Started

To use the API:

1. Register a tenant using `POST /tenants/register`
2. Obtain an access token using `POST /login`
3. Use the token in subsequent requests

## API Versioning

The current version of the API is v1 (implicit in the path). Future versions will be explicitly versioned in the URL path. 