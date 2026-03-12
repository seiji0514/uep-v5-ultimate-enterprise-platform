/**
 * 金融・FinTech API
 * 決済API、リスクスコア、取引監視
 */
import apiClient from './client';

export interface Payment {
  id: string;
  amount: number;
  currency: string;
  status: string;
  created_at: string;
}

export interface RiskScore {
  transaction_id: string;
  risk_score: number;
  level: string;
  factors: string[];
}

export interface TransactionMonitoring {
  id: string;
  type: string;
  amount: number;
  status: string;
  alert: string | null;
}

export const fintechApi = {
  async getPayments(): Promise<Payment[]> {
    const response = await apiClient.get<{ items: Payment[]; total: number }>(
      '/api/v1/fintech/payments'
    );
    return response.data.items;
  },

  async getRiskScores(): Promise<RiskScore[]> {
    const response = await apiClient.get<{ items: RiskScore[]; total: number }>(
      '/api/v1/fintech/risk-scores'
    );
    return response.data.items;
  },

  async getTransactionMonitoring(): Promise<TransactionMonitoring[]> {
    const response = await apiClient.get<{ items: TransactionMonitoring[]; total: number }>(
      '/api/v1/fintech/transaction-monitoring'
    );
    return response.data.items;
  },
};
