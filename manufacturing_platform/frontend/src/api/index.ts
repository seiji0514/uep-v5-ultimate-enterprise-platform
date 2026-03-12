/**
 * 製造・IoTプラットフォーム API
 * スタンドアロン起動時: http://localhost:9002
 */
import axios from 'axios';

const BASE = process.env.REACT_APP_MANUFACTURING_PLATFORM_URL || 'http://localhost:9002';
const apiClient = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
});
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

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

const API = '/api/v1/manufacturing';

export const manufacturingApi = {
  async getPredictiveMaintenance() {
    const response = await apiClient.get<{ items: PredictiveMaintenance[]; total: number }>(
      `${API}/predictive-maintenance`
    );
    return response.data;
  },
  async getSensorData() {
    const response = await apiClient.get<{ items: SensorData[]; total: number }>(
      `${API}/sensor-data`
    );
    return response.data;
  },
  async getAnomalies() {
    const response = await apiClient.get<{ items: Anomaly[]; total: number }>(
      `${API}/anomalies`
    );
    return response.data;
  },
};
