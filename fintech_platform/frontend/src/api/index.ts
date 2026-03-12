/**
 * 金融・FinTechプラットフォーム API
 * スタンドアロン起動時: http://localhost:9004
 */
import axios from 'axios';

const BASE = process.env.REACT_APP_FINTECH_PLATFORM_URL || 'http://localhost:9004';
const apiClient = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
});
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

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

const API = '/api/v1/fintech';

export const fintechApi = {
  async getPayments() {
    const response = await apiClient.get<{ items: Payment[]; total: number }>(`${API}/payments`);
    return response.data;
  },
  async getRiskScores() {
    const response = await apiClient.get<{ items: RiskScore[]; total: number }>(`${API}/risk-scores`);
    return response.data;
  },
  async getTransactionMonitoring() {
    const response = await apiClient.get<{ items: TransactionMonitoring[]; total: number }>(
      `${API}/transaction-monitoring`
    );
    return response.data;
  },
  async runStressTest(portfolioValue = 1000000) {
    const response = await apiClient.get(`${API}/stress-test`, {
      params: { portfolio_value: portfolioValue },
    });
    return response.data;
  },
};
