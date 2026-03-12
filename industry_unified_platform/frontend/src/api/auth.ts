/**
 * 認証API（産業統合プラットフォーム用）
 */
import axios from 'axios';

const BASE = process.env.REACT_APP_INDUSTRY_UNIFIED_URL || 'http://localhost:9010';

const apiClient = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
});

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user?: Record<string, unknown>;
}

export const authApi = {
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', credentials);
    return response.data;
  },
};
