/**
 * 製造・IoT API
 * 予知保全API、センサーデータ取得、異常検知
 */
import apiClient from './client';

export interface PredictiveMaintenance {
  id: string;
  equipment: string;
  predicted_failure: string;
  confidence: number;
  status: string;
}

export interface SensorData {
  sensor_id: string;
  value: number;
  unit: string;
  timestamp: string;
}

export interface Anomaly {
  id: string;
  type: string;
  equipment: string;
  severity: string;
  detected_at: string;
}

export const manufacturingApi = {
  async getPredictiveMaintenance(): Promise<PredictiveMaintenance[]> {
    const response = await apiClient.get<{ items: PredictiveMaintenance[]; total: number }>(
      '/api/v1/manufacturing/predictive-maintenance'
    );
    return response.data.items;
  },

  async getSensorData(): Promise<SensorData[]> {
    const response = await apiClient.get<{ items: SensorData[]; total: number }>(
      '/api/v1/manufacturing/sensor-data'
    );
    return response.data.items;
  },

  async getAnomalies(): Promise<Anomaly[]> {
    const response = await apiClient.get<{ items: Anomaly[]; total: number }>(
      '/api/v1/manufacturing/anomalies'
    );
    return response.data.items;
  },
};
