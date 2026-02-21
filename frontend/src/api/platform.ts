/**
 * Level 2 プラットフォーム API
 */
import apiClient from './client';

export interface Tenant {
  id: string;
  name: string;
  organization: string;
  plan_id: string;
  status: string;
  contact_email: string;
  created_at: string;
  resource_limits?: { api_calls?: number; storage_gb?: number };
}

export interface SubscriptionPlan {
  id: string;
  name: string;
  price_monthly: number;
  features: string[];
  api_calls_limit: number;
  storage_gb: number;
}

export interface ApiListing {
  id: string;
  name: string;
  description: string;
  endpoint: string;
  provider_tenant_id: string;
  price_per_call: number;
  category: string;
  created_at: string;
  call_count: number;
}

export interface Level2Overview {
  level: number;
  name: string;
  features: {
    multi_tenant: { tenants_count: number; isolation_mode: string };
    saas: { plans_count: number; self_service: boolean };
    api_marketplace: { listings_count: number };
  };
}

export const platformApi = {
  async getOverview(): Promise<Level2Overview> {
    const response = await apiClient.get<Level2Overview>('/api/v1/platform/overview');
    return response.data;
  },

  async getTenants(): Promise<Tenant[]> {
    const response = await apiClient.get<Tenant[]>('/api/v1/platform/tenants');
    return response.data;
  },

  async getPlans(): Promise<SubscriptionPlan[]> {
    const response = await apiClient.get<SubscriptionPlan[]>('/api/v1/platform/plans');
    return response.data;
  },

  async getApiMarketplace(category?: string): Promise<ApiListing[]> {
    const params = category ? { category } : {};
    const response = await apiClient.get<ApiListing[]>('/api/v1/platform/api-marketplace', { params });
    return response.data;
  },

  async getSelfServiceConfig() {
    const response = await apiClient.get('/api/v1/platform/self-service-config');
    return response.data;
  },

  async getMultiTenantConfig() {
    const response = await apiClient.get('/api/v1/platform/multi-tenant-config');
    return response.data;
  },
};
