/**
 * 最適化API
 * 異常検知（閾値調整・アンサンブル）、ヘルスチェック
 */
import apiClient from './client';

export interface ThresholdConfig {
  metric: string;
  upper: number;
  lower: number;
  severity_high_ratio: number;
  severity_medium_ratio: number;
}

export interface AnomalyDetectResult {
  is_anomaly: boolean;
  severity?: string;
  value: number;
  metric: string;
  ensemble_votes?: number;
  ensemble_total?: number;
  detectors?: string[];
  detected_at?: string;
}

export const optimizationApi = {
  async getThresholds() {
    const response = await apiClient.get<{ thresholds: Record<string, ThresholdConfig> }>(
      '/api/v1/optimization/anomaly-detection/thresholds'
    );
    return response.data;
  },

  async updateThreshold(
    metric: string,
    params: { upper?: number; lower?: number; severity_high_ratio?: number; severity_medium_ratio?: number }
  ) {
    const q: Record<string, string> = {};
    if (params.upper != null) q.upper = String(params.upper);
    if (params.lower != null) q.lower = String(params.lower);
    if (params.severity_high_ratio != null) q.severity_high_ratio = String(params.severity_high_ratio);
    if (params.severity_medium_ratio != null) q.severity_medium_ratio = String(params.severity_medium_ratio);
    const response = await apiClient.put(
      `/api/v1/optimization/anomaly-detection/thresholds/${metric}`,
      undefined,
      { params: q }
    );
    return response.data;
  },

  async detectAnomaly(metric: string, value: number, history?: number[]) {
    const response = await apiClient.post<AnomalyDetectResult>(
      '/api/v1/optimization/anomaly-detection/detect',
      { metric, value, history }
    );
    return response.data;
  },

  async batchAnomalyDetection(domain: string, items: Array<Record<string, unknown>>) {
    const response = await apiClient.post<{ items: unknown[]; total: number }>(
      '/api/v1/optimization/anomaly-detection/batch',
      { domain, items }
    );
    return response.data;
  },
};
