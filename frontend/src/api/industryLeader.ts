/**
 * Level 4 インダストリーリーダー API
 */
import apiClient from './client';

export interface Level4Overview {
  level: number;
  name: string;
  scope: string;
  features: {
    global_scale: { cdn: boolean; multilingual: number };
    cutting_edge_ai: { technologies_count: number };
    industry_standard: { specs_count: number };
    business_domains?: { domains_count: number };
  };
}

export const industryLeaderApi = {
  async getOverview(): Promise<Level4Overview> {
    const response = await apiClient.get<Level4Overview>('/api/v1/industry-leader/overview');
    return response.data;
  },

  async getGlobalCdnConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/global-cdn');
    return response.data;
  },

  async getMultilingualConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/multilingual');
    return response.data;
  },

  async getCuttingEdgeAiConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/cutting-edge-ai');
    return response.data;
  },

  async getIndustryStandard() {
    const response = await apiClient.get('/api/v1/industry-leader/industry-standard');
    return response.data;
  },

  async getReasoningAiConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/reasoning-ai');
    return response.data;
  },

  async getMcpA2aConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/mcp-a2a');
    return response.data;
  },

  async getGovernanceWorkflowConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/governance-workflow');
    return response.data;
  },

  async getOnDeviceAiConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/on-device-ai');
    return response.data;
  },

  async getBusinessDomainConfig() {
    const response = await apiClient.get('/api/v1/industry-leader/business-domain');
    return response.data;
  },
};
