/**
 * Level 5 グローバルエンタープライズ API
 */
import apiClient from './client';

export interface Level5Overview {
  level: number;
  name: string;
  scope: string;
  features: {
    multi_region: { regions_count: number };
    high_availability: { target_sla: string };
    zero_downtime_deploy: { strategies: number };
    disaster_recovery: { rpo_seconds: number };
    compliance: { frameworks: string[] };
  };
}

export interface Region {
  id: string;
  name: string;
  provider: string;
  status: string;
  endpoints: Record<string, string>;
  data_residency: string;
}

export interface MultiRegionConfig {
  regions: Region[];
  routing: string;
}

export interface HAComponent {
  name: string;
  replicas: number;
  strategy: string;
  health_check_interval_sec?: number;
  auto_failover?: boolean;
}

export interface ComplianceItem {
  id: string;
  item: string;
  status: string;
}

export const globalEnterpriseApi = {
  async getOverview(): Promise<Level5Overview> {
    const response = await apiClient.get<Level5Overview>('/api/v1/global-enterprise/overview');
    return response.data;
  },

  async getMultiRegionConfig(): Promise<MultiRegionConfig> {
    const response = await apiClient.get<MultiRegionConfig>('/api/v1/global-enterprise/multi-region');
    return response.data;
  },

  async getHighAvailabilityConfig(): Promise<{ target_sla: string; components: HAComponent[] }> {
    const response = await apiClient.get('/api/v1/global-enterprise/high-availability');
    return response.data;
  },

  async getZeroDowntimeDeployConfig(): Promise<{ strategies: Array<{ name: string; description: string; enabled: boolean }> }> {
    const response = await apiClient.get('/api/v1/global-enterprise/zero-downtime-deploy');
    return response.data;
  },

  async getDisasterRecoveryConfig(): Promise<{ rpo_seconds: number; rto_seconds: number; backup: object; failover: object }> {
    const response = await apiClient.get('/api/v1/global-enterprise/disaster-recovery');
    return response.data;
  },

  async getComplianceChecklist(): Promise<Record<string, ComplianceItem[]>> {
    const response = await apiClient.get<Record<string, ComplianceItem[]>>('/api/v1/global-enterprise/compliance');
    return response.data;
  },
};
