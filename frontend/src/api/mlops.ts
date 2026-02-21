/**
 * MLOps API
 */
import apiClient from './client';

export interface MLPipeline {
  id: string;
  name: string;
  description?: string;
  stages: string[];
  status: string;
  created_at: string;
  created_by: string;
  updated_at?: string;
}

export interface MLModel {
  id: string;
  name: string;
  version: string;
  status: string;
  framework: string;
  accuracy?: number;
  created_at: string;
  created_by: string;
}

export interface Experiment {
  id: string;
  name: string;
  description?: string;
  status: string;
  metrics?: Record<string, number>;
  created_at: string;
  created_by: string;
}

export const mlopsApi = {
  async getPipelines(): Promise<MLPipeline[]> {
    const response = await apiClient.get<MLPipeline[]>('/api/v1/mlops/pipelines');
    return response.data;
  },

  async getModels(): Promise<MLModel[]> {
    const response = await apiClient.get<MLModel[]>('/api/v1/mlops/models');
    return response.data;
  },

  async getExperiments(): Promise<Experiment[]> {
    const response = await apiClient.get<Experiment[]>('/api/v1/mlops/experiments');
    return response.data;
  },
};
