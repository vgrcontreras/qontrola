# Clients API Documentation

This document describes the Clients API endpoints available in the Studio Caju backend.

## Base URL

```
/clients
```

## Authorization

All endpoints require authentication via Bearer token and a tenant domain header:

```
Authorization: Bearer <access_token>
X-Tenant-Domain: <tenant_domain>
```

## Brazilian Identifier Validation

The API implements validation for Brazilian identification numbers:

- **CPF (Cadastro de Pessoas Físicas)**: For individuals, must be exactly 11 digits
- **CNPJ (Cadastro Nacional da Pessoa Jurídica)**: For businesses, must be exactly 14 digits

## Endpoints

### Create Client

Creates a new client within the current tenant.

**URL:** `POST /clients`

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Client name |
| client_type | string | Yes | Type of client |
| type_identifier | enum | Yes | Type of identification document (`cpf` or `cnpj`) |
| identifier | string | Yes | Identification number (11 digits for CPF, 14 digits for CNPJ) |

**Example Request (Individual):**

```json
{
  "name": "John Doe",
  "client_type": "individual",
  "type_identifier": "cpf",
  "identifier": "12345678901"
}
```

**Example Request (Business):**

```json
{
  "name": "ACME Corporation",
  "client_type": "business",
  "type_identifier": "cnpj",
  "identifier": "12345678901234"
}
```

**Response:**
- Status: 201 Created

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "ACME Corporation",
  "client_type": "business",
  "type_identifier": "cnpj",
  "identifier": "12345678901234",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

**Error Responses:**

- 400 Bad Request - If the client already exists
```json
{
  "detail": "Client already exists"
}
```

- 422 Unprocessable Entity - If the identifier length is invalid
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "identifier"],
      "msg": "CPF must have exactly 11 digits",
      "input": "1234567890"
    }
  ]
}
```

### Get Client by ID

Retrieves a specific client by its ID.

**URL:** `GET /clients/{client_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| client_id | UUID | Yes | ID of the client to retrieve |

**Response:**
- Status: 200 OK

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "ACME Corporation",
  "client_type": "business",
  "type_identifier": "cnpj",
  "identifier": "12345678901234",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

**Error Responses:**

- 404 Not Found - If the client doesn't exist
```json
{
  "detail": "Client not found"
}
```

### List Clients

Retrieves all clients for the current tenant.

**URL:** `GET /clients`

**Response:**
- Status: 200 OK

```json
{
  "clients": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "name": "ACME Corporation",
      "client_type": "business",
      "type_identifier": "cnpj",
      "identifier": "12345678901234",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true
    },
    {
      "id": "234f5678-e90c-23e4-b567-526614274001",
      "name": "John Doe",
      "client_type": "individual",
      "type_identifier": "cpf",
      "identifier": "12345678901",
      "tenant_id": "789e0123-a456-426614174000",
      "is_active": true
    }
  ]
}
```

### Update Client

Updates an existing client.

**URL:** `PATCH /clients/{client_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| client_id | UUID | Yes | ID of the client to update |

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | No | New client name |
| client_type | string | No | New client type |
| type_identifier | enum | No | New type of identification (`cpf` or `cnpj`) |
| identifier | string | No | New identification number (must match type_identifier requirements) |

**Example Request:**

```json
{
  "name": "Updated Corporation Name"
}
```

**Response:**
- Status: 200 OK

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Updated Corporation Name",
  "client_type": "business",
  "type_identifier": "cnpj",
  "identifier": "12345678901234",
  "tenant_id": "789e0123-a456-426614174000",
  "is_active": true
}
```

**Error Responses:**

- 404 Not Found - If the client doesn't exist
```json
{
  "detail": "Client not found"
}
```

- 409 Conflict - If updating the identifier and the new identifier already exists
```json
{
  "detail": "Client already exists"
}
```

- 422 Unprocessable Entity - If the identifier length is invalid
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "identifier"],
      "msg": "CNPJ must have exactly 14 digits",
      "input": "1234567890123"
    }
  ]
}
```

### Delete Client

Deactivates a client (soft delete). Requires superuser privileges.

**URL:** `DELETE /clients/{client_id}`

**Path Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| client_id | UUID | Yes | ID of the client to delete |

**Response:**
- Status: 200 OK

```json
{
  "message": "Client deleted"
}
```

**Error Responses:**

- 404 Not Found - If the client doesn't exist
```json
{
  "detail": "Client doesn't exist"
}
``` 