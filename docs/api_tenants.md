# Tenants API Documentation

This document describes the Tenants API endpoints available in the Studio Caju backend.

## Base URL

```
/tenants
```

## Authorization

Some endpoints in this section are public, while others require authentication. The endpoints for managing a tenant require both a valid token and superuser privileges.

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Register Tenant

Registers a new tenant and creates the first admin user. This endpoint is public and does not require authentication.

**URL:** `POST /tenants/register`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Name of the tenant |
| domain | string | Yes | Domain identifier for the tenant |
| admin_user | object | Yes | Information about the initial admin user |
| admin_user.email | string | Yes | Email address of the admin user |
| admin_user.password | string | Yes | Password for the admin user |

**Example Request:**

```json
{
  "name": "ACME Corporation",
  "domain": "acme",
  "admin_user": {
    "email": "admin@acme.com",
    "password": "securepassword123"
  }
}
```

**Response:**
- Status: 201 Created

```json
{
  "id": "789e0123-a456-426614174000",
  "name": "ACME Corporation",
  "domain": "acme",
  "is_active": true,
  "created_at": "2024-04-20T14:30:45.123456"
}
```

**Error Responses:**

- 400 Bad Request - If the domain is already in use
```json
{
  "detail": "Domain already in use"
}
```

### Update Tenant

Updates information for the current tenant. Only accessible by tenant administrators (superusers).

**URL:** `PUT /tenants/current`

**Request Headers:**

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token with superuser privileges |
| X-Tenant-Domain | Yes | Domain of the tenant to update |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | New name for the tenant |
| domain | string | No | New domain identifier for the tenant |
| is_active | boolean | No | Status of the tenant |

**Example Request:**

```json
{
  "name": "ACME Corporation Updated",
  "domain": "acme-corp"
}
```

**Response:**
- Status: 200 OK

```json
{
  "id": "789e0123-a456-426614174000",
  "name": "ACME Corporation Updated",
  "domain": "acme-corp",
  "is_active": true,
  "created_at": "2024-04-20T14:30:45.123456"
}
```

**Error Responses:**

- 400 Bad Request - If the new domain is already in use
```json
{
  "detail": "Domain acme-corp is already in use"
}
```

- 401 Unauthorized - If the user is not authenticated
```json
{
  "detail": "Not authenticated"
}
```

- 403 Forbidden - If the user is not a superuser
```json
{
  "detail": "The user doesn't have enough privileges"
}
``` 