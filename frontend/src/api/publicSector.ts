/**
 * 公共・官公庁 API
 */
import apiClient from './client';

export interface Application {
  id: string;
  type: string;
  applicant: string;
  status: string;
  submitted_at: string;
  office: string;
}

export interface ApprovalWorkflow {
  id: string;
  title: string;
  current_step: string;
  status: string;
  deadline: string;
}

export const publicSectorApi = {
  async getApplications(): Promise<Application[]> {
    const res = await apiClient.get<{ items: Application[] }>('/api/v1/public-sector/applications');
    return res.data.items;
  },
  async getApprovalWorkflow(): Promise<ApprovalWorkflow[]> {
    const res = await apiClient.get<{ items: ApprovalWorkflow[] }>('/api/v1/public-sector/approval-workflow');
    return res.data.items;
  },
  async getDashboard(): Promise<Record<string, number>> {
    const res = await apiClient.get('/api/v1/public-sector/dashboard');
    return res.data;
  },
};
