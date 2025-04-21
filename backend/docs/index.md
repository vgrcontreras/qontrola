# Studio Caju API Documentation

Welcome to the Studio Caju API documentation. This documentation provides details on how to use the Studio Caju backend API.

## Overview

Studio Caju is a comprehensive project management system designed for creative studios and agencies. The API provides endpoints for managing users, clients, projects, tasks, and more.

## Getting Started

To get started with the API, please refer to the following sections:

- [API Overview](api_index.md): General information about the API
- [Authentication](api_login.md): How to authenticate with the API
- [Users](api_users.md): User management endpoints
- [Clients](api_clients.md): Client management endpoints
- [Projects](api_projects.md): Project management endpoints
- [Tasks](api_tasks.md): Task management endpoints

## API Base URL

The base URL for all API endpoints is:

```
http://localhost:8000/api/v1
```

For production environments, use the appropriate domain.

## Authentication

Most endpoints require authentication. See the [Authentication](api_login.md) section for details on how to obtain and use authentication tokens.

## Response Format

All API responses are returned in JSON format.

## Error Handling

Error responses will include an error message and appropriate HTTP status code.

Example error response:

```json
{
  "detail": "Not found"
}
```

## Need Help?

If you need assistance with the API, please contact the development team or file an issue on the [GitHub repository](https://github.com/contreras3991/studio-caju). 