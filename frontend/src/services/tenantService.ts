import axios from 'axios';

// Define types based on backend schemas
export interface AdminUser {
  email: string;
  password: string;
}

export interface TenantRegistration {
  name: string;
  domain: string;
  admin_user: AdminUser;
}

export interface TenantResponse {
  id: string;
  name: string;
  domain: string;
  is_active: boolean;
}

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
});

/**
 * Register a new tenant
 */
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

export default {
  registerTenant,
}; 