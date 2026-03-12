/**
 * インフラ構築専用システム API
 */
import apiClient from './client';

export interface BuildProject {
  id: string;
  name: string;
  description: string;
  target_provider: string;
  blueprint: Record<string, unknown>;
  status: string;
  current_stage: string;
  created_at: string;
  updated_at: string;
  created_by: string;
}

export interface Blueprint {
  id: string;
  name: string;
  provider: string;
  content: string;
  variables: Record<string, unknown>;
  description: string;
  created_at: string;
  created_by: string;
}

export interface PipelineRun {
  id: string;
  project_id: string;
  stages: string[];
  status: string;
  current_stage: string | null;
  started_at: string;
  completed_at: string | null;
  logs: string[];
}

export interface InfraBuilderDashboard {
  total_projects: number;
  in_progress: number;
  completed: number;
  draft: number;
  total_blueprints: number;
  total_pipeline_runs: number;
  providers: string[];
}

export const infraBuilderApi = {
  async getDashboard(): Promise<InfraBuilderDashboard> {
    const response = await apiClient.get<InfraBuilderDashboard>('/api/v1/infra-builder/dashboard');
    return response.data;
  },

  async getProjects(status?: string, provider?: string): Promise<BuildProject[]> {
    const params = new URLSearchParams();
    if (status) params.append('status_filter', status);
    if (provider) params.append('provider', provider);
    const query = params.toString() ? `?${params.toString()}` : '';
    const response = await apiClient.get<BuildProject[]>(`/api/v1/infra-builder/projects${query}`);
    return response.data;
  },

  async getProject(projectId: string): Promise<BuildProject> {
    const response = await apiClient.get<BuildProject>(`/api/v1/infra-builder/projects/${projectId}`);
    return response.data;
  },

  async createProject(data: {
    name: string;
    description?: string;
    target_provider?: string;
    blueprint?: Record<string, unknown>;
  }): Promise<BuildProject> {
    const response = await apiClient.post<BuildProject>('/api/v1/infra-builder/projects', data);
    return response.data;
  },

  async getBlueprints(provider?: string): Promise<Blueprint[]> {
    const params = provider ? `?provider=${encodeURIComponent(provider)}` : '';
    const response = await apiClient.get<Blueprint[]>(`/api/v1/infra-builder/blueprints${params}`);
    return response.data;
  },

  async createBlueprint(data: {
    name: string;
    provider: string;
    content: string;
    variables?: Record<string, unknown>;
    description?: string;
  }): Promise<Blueprint> {
    const response = await apiClient.post<Blueprint>('/api/v1/infra-builder/blueprints', data);
    return response.data;
  },

  async getPipelines(projectId?: string, status?: string): Promise<PipelineRun[]> {
    const params = new URLSearchParams();
    if (projectId) params.append('project_id', projectId);
    if (status) params.append('status_filter', status);
    const query = params.toString() ? `?${params.toString()}` : '';
    const response = await apiClient.get<PipelineRun[]>(`/api/v1/infra-builder/pipelines${query}`);
    return response.data;
  },

  async runPipeline(projectId: string, stages?: string[]): Promise<PipelineRun> {
    const response = await apiClient.post<PipelineRun>('/api/v1/infra-builder/pipelines/run', {
      project_id: projectId,
      stages: stages || ['design', 'build', 'deploy', 'verify'],
    });
    return response.data;
  },
};
