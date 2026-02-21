/**
 * クラウドインフラ API
 */
import apiClient from './client';

export interface InfrastructureResource {
  id: string;
  name: string;
  resource_type: string;
  provider: string;
  region: string;
  status: string;
  created_at: string;
}

export interface IaCTemplate {
  id: string;
  name: string;
  provider: string;
  created_at: string;
  created_by: string;
}

export interface Deployment {
  id: string;
  name: string;
  platform: string;
  status: string;
  replicas: number;
  created_at: string;
}

export const cloudInfraApi = {
  async getResources(): Promise<InfrastructureResource[]> {
    const response = await apiClient.get<InfrastructureResource[]>('/api/v1/cloud-infra/resources');
    return response.data;
  },

  async getTemplates(): Promise<IaCTemplate[]> {
    const response = await apiClient.get<IaCTemplate[]>('/api/v1/cloud-infra/iac/templates');
    return response.data;
  },

  async getDeployments(): Promise<Deployment[]> {
    const response = await apiClient.get<Deployment[]>('/api/v1/cloud-infra/deployments');
    return response.data;
  },
};
