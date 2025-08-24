# Login API Documentation

This document describes the Login API endpoints available in the Studio Caju backend.

## Base URL

```
/login
```

## Authentication Header

For the refresh token endpoint, authentication is required:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Endpoints

### Login

Authenticates a user and returns an access token.

**URL:** `POST /login`

**Request Headers:**

| Header | Required | Description |
|--------|----------|-------------|
| X-Tenant-Domain | Yes | Domain of the tenant to authenticate against |

**Request Body (Form Data):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| username | string | Yes | User's email address |
| password | string | Yes | User's password |

**Response:**
- Status: 200 OK

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- 400 Bad Request - If tenant header is missing
```json
{
  "detail": "X-Tenant-Domain header is required"
}
```

- 404 Not Found - If tenant doesn't exist
```json
{
  "detail": "Tenant not found or inactive"
}
```

- 400 Bad Request - If credentials are incorrect
```json
{
  "detail": "Incorrect email or password"
}
```

### Refresh Token

Refreshes an existing access token.

**URL:** `POST /login/refresh_token`

**Request Headers:**

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token from previous login |
| X-Tenant-Domain | Yes | Domain of the tenant |

**Response:**
- Status: 200 OK

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**

- 401 Unauthorized - If the token is invalid or expired
```json
{
  "detail": "Could not validate credentials"
}
``` 