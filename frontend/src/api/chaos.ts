/**
 * Chaos Engineering API
 * 障害シミュレーション（遅延・エラー注入）のフロントエンドAPI
 */
import apiClient from './client';

export interface ChaosStatus {
  enabled: boolean;
  endpoints: {
    delay: string;
    error: string;
    mixed: string;
  };
  description: string;
}

export interface ChaosDelayResponse {
  status: string;
  message: string;
  requested_delay_ms: number;
  actual_delay_ms: number;
}

export interface ChaosErrorResponse {
  status: string;
  message: string;
}

export interface ChaosMixedResponse {
  status: string;
  message: string;
  delay_ms: number;
  error_rate: number;
}

export const chaosApi = {
  getStatus: () => apiClient.get<ChaosStatus>('/api/v1/chaos/status'),
  delay: (delayMs: number, jitterMs = 0) =>
    apiClient.get<ChaosDelayResponse>(`/api/v1/chaos/delay?delay_ms=${delayMs}&jitter_ms=${jitterMs}`),
  delayPost: (delayMs: number, jitterMs = 0) =>
    apiClient.post<ChaosDelayResponse>('/api/v1/chaos/delay', { delay_ms: delayMs, jitter_ms: jitterMs }),
  error: (errorRate: number, statusCode = 500) =>
    apiClient.get<ChaosErrorResponse>(`/api/v1/chaos/error?error_rate=${errorRate}&status_code=${statusCode}`),
  errorPost: (errorRate: number, statusCode = 500) =>
    apiClient.post<ChaosErrorResponse>('/api/v1/chaos/error', { error_rate: errorRate, status_code: statusCode }),
  mixed: (delayMs: number, errorRate: number) =>
    apiClient.get<ChaosMixedResponse>(`/api/v1/chaos/mixed?delay_ms=${delayMs}&error_rate=${errorRate}`),
};
