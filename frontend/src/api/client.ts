/**
 * APIクライアント
 * バックエンドAPIとの通信を管理（本番対応: リフレッシュトークン自動延長）
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';
import { authApi } from './auth';

export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8080';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.request.use(
      (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (!error.response) {
          console.error('Network Error:', error.message);
          if (error.code === 'ECONNREFUSED') {
            console.error('Backend server is not running or not accessible at:', API_BASE_URL);
          }
          return Promise.reject(error);
        }

        if (error.response?.status === 401) {
          const originalRequest = error.config;
          if (!originalRequest._retry && localStorage.getItem('refresh_token')) {
            originalRequest._retry = true;
            try {
              const tokenData = await authApi.refreshToken();
              if (tokenData) {
                localStorage.setItem('access_token', tokenData.access_token);
                localStorage.setItem('user', JSON.stringify(tokenData.user));
                originalRequest.headers.Authorization = `Bearer ${tokenData.access_token}`;
                return this.client(originalRequest);
              }
            } catch {
              // リフレッシュ失敗時はログアウト
            }
          }
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user');
          window.dispatchEvent(new CustomEvent('auth:unauthorized'));
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.get<T>(url, config);
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.post<T>(url, data, config);
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.put<T>(url, data, config);
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.delete<T>(url, config);
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.client.patch<T>(url, data, config);
  }
}

export const apiClient = new ApiClient();
export default apiClient;
