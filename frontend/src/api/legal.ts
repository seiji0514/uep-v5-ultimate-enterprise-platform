/**
 * 法務 API
 */
import apiClient from './client';

export interface ContractReview {
  id: string;
  title: string;
  status: string;
  risk_level: string;
  submitted_at: string;
}

export interface RegulatoryItem {
  id: string;
  name: string;
  deadline: string;
  status: string;
}

export interface IpPortfolio {
  id: string;
  type: string;
  title: string;
  status: string;
  filing_date: string;
}

export const legalApi = {
  async getContractReviews(): Promise<ContractReview[]> {
    const res = await apiClient.get<{ items: ContractReview[] }>('/api/v1/legal/contract-reviews');
    return res.data.items;
  },
  async getRegulatory(): Promise<RegulatoryItem[]> {
    const res = await apiClient.get<{ items: RegulatoryItem[] }>('/api/v1/legal/regulatory');
    return res.data.items;
  },
  async getIpPortfolio(): Promise<IpPortfolio[]> {
    const res = await apiClient.get<{ items: IpPortfolio[] }>('/api/v1/legal/ip-portfolio');
    return res.data.items;
  },
  async getDashboard(): Promise<Record<string, number>> {
    const res = await apiClient.get('/api/v1/legal/dashboard');
    return res.data;
  },
};
