/**
 * 認証API（製造・IoTプラットフォーム用）
 */
import axios from 'axios';

const BASE = process.env.REACT_APP_MANUFACTURING_PLATFORM_URL || 'http://localhost:9002';

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
  user?: {
    username: string;
    email: string;
    full_name: string;
    department: string;
    roles: string[];
    is_active: boolean;
  };
}

export const authApi = {
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', credentials);
    return response.data;
  },
};
