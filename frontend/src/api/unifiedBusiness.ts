/**
 * 統合ビジネスプラットフォーム API
 * 業務効率化・DX / 人材・組織 / 顧客対応・CX
 */
import apiClient from './client';

export interface PlatformSummary {
  platform: string;
  version: string;
  modules: {
    '業務効率化・DX': {
      workflows: number;
      approval_requests: number;
      rpa_jobs: number;
    };
    '人材・組織': {
      disability_supports: number;
      onboarding_tasks: number;
    };
    '顧客対応・CX': {
      tickets: number;
    };
  };
}

export const unifiedBusinessApi = {
  async getSummary(): Promise<PlatformSummary> {
    const response = await apiClient.get<PlatformSummary>('/api/v1/unified-business/summary');
    return response.data;
  },

  async getWorkflows() {
    const response = await apiClient.get('/api/v1/unified-business/workflows');
    return response.data;
  },

  async getApprovalRequests() {
    const response = await apiClient.get('/api/v1/unified-business/approval-requests');
    return response.data;
  },

  async getRpaJobs() {
    const response = await apiClient.get('/api/v1/unified-business/rpa/jobs');
    return response.data;
  },

  async getDisabilitySupports() {
    const response = await apiClient.get('/api/v1/unified-business/hr/disability-supports');
    return response.data;
  },

  async getAccommodationChecklist() {
    const response = await apiClient.get('/api/v1/unified-business/hr/disability-supports/checklist');
    return response.data;
  },

  async getOnboardingTasks(employeeId?: string) {
    const params = employeeId ? { employee_id: employeeId } : {};
    const response = await apiClient.get('/api/v1/unified-business/hr/onboarding/tasks', { params });
    return response.data;
  },

  async getTickets(status?: string, customerId?: string) {
    const params: Record<string, string> = {};
    if (status) params.status = status;
    if (customerId) params.customer_id = customerId;
    const response = await apiClient.get('/api/v1/unified-business/customer/tickets', { params });
    return response.data;
  },
};
