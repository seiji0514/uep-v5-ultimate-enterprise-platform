/**
 * IDOP API
 */
import apiClient from './client';

export interface CICDPipeline {
  id: string;
  name: string;
  description?: string;
  stages: string[];
  status: string;
  created_at: string;
  created_by: string;
}

export interface Application {
  id: string;
  name: string;
  description?: string;
  environment: string;
  status: string;
  created_at: string;
}

export const idopApi = {
  async getPipelines(): Promise<CICDPipeline[]> {
    const response = await apiClient.get<CICDPipeline[]>('/api/v1/idop/pipelines');
    return response.data;
  },

  async getApplications(): Promise<Application[]> {
    const response = await apiClient.get<Application[]>('/api/v1/idop/applications');
    return response.data;
  },
};
