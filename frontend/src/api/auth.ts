/**
 * 認証API
 */
import apiClient from './client';

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
  user: {
    username: string;
    email: string;
    full_name: string;
    department: string;
    roles: string[];
    is_active: boolean;
  };
}

export interface UserResponse {
  username: string;
  email: string;
  full_name: string;
  department: string;
  roles: string[];
  is_active: boolean;
}

export const authApi = {
  /**
   * ログイン
   */
  async login(credentials: LoginRequest): Promise<TokenResponse> {
    const response = await apiClient.post<TokenResponse>('/api/v1/auth/login', credentials);
    return response.data;
  },

  /**
   * 現在のユーザー情報を取得
   */
  async getCurrentUser(): Promise<UserResponse> {
    const response = await apiClient.get<UserResponse>('/api/v1/auth/me');
    return response.data;
  },

  /**
   * パスワード変更
   */
  async changePassword(currentPassword: string, newPassword: string): Promise<void> {
    await apiClient.post('/api/v1/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  /**
   * ログアウト（ローカルストレージからトークンを削除）
   */
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
  },
};
