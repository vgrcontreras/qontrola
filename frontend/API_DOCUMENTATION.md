# Studio Caju Frontend API Integration

This document provides detailed information about how the Studio Caju frontend application interacts with backend APIs.

## API Client Configuration

The application uses Axios for API requests. A base API client is configured in each service file with default settings:

```typescript
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});
```

## Services

### Tenant Service

**File:** `src/services/tenantService.ts`

This service handles tenant-related API operations.

#### Data Models

```typescript
// Admin user data structure
export interface AdminUser {
  email: string;
  password: string;
}

// Tenant registration request data structure
export interface TenantRegistration {
  name: string;
  domain: string;
  admin_user: AdminUser;
}

// Tenant response data structure
export interface TenantResponse {
  id: string;
  name: string;
  domain: string;
  is_active: boolean;
}
```

#### API Methods

##### Register Tenant

Registers a new tenant with admin user information.

**Endpoint:** `POST /api/tenants/register`

**Function:**
```typescript
export const registerTenant = async (tenantData: TenantRegistration): Promise<TenantResponse> => {
  try {
    const response = await apiClient.post('/tenants/register', tenantData);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      // Get the error details from the response if available
      const errorMessage = error.response.data?.detail || 'Failed to create account';
      throw new Error(errorMessage);
    }
    throw error;
  }
};
```

**Input Parameters:**
- `tenantData`: Object containing tenant name, domain, and admin user credentials

**Returns:**
- Promise that resolves to a TenantResponse object

**Error Handling:**
- Catches Axios errors and extracts detailed error messages from the API response
- Rethrows errors with descriptive messages for UI error handling

## Error Handling Strategy

The service layer implements a consistent error handling strategy:

1. Each API call is wrapped in a try/catch block
2. Axios errors are checked using `axios.isAxiosError()`
3. Error details are extracted from the API response when available
4. Errors are thrown with descriptive messages for UI components to handle

Example error handling in components:

```typescript
const handleSubmit = async (data: FormData) => {
  try {
    setLoading(true);
    const result = await tenantService.registerTenant(data);
    // Handle success
  } catch (error) {
    setError(error instanceof Error ? error.message : 'An unexpected error occurred');
  } finally {
    setLoading(false);
  }
};
```

## API Request/Response Flow

1. **Component Layer**: UI components call service functions with required data
2. **Service Layer**: Services format requests, call APIs, and handle errors
3. **API Response**: Responses are returned to components for state updates

## Future API Enhancements

Planned improvements for the API integration layer:

1. **Authentication Integration**:
   - Token-based authentication
   - Refresh token mechanism
   - Auth headers for protected routes

2. **Request Interceptors**:
   - Add authentication headers to requests
   - Handle expired tokens

3. **Response Interceptors**:
   - Global error handling
   - Response data transformation

4. **API Caching**:
   - Implement request caching for frequently used data
   - Cache invalidation strategies

5. **Additional Services**:
   - User service for authentication and user management
   - Configuration service for tenant settings
   - Dashboard data service for analytics 