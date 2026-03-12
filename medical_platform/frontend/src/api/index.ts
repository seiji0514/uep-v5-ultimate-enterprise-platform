/**
 * 医療・ヘルスケアプラットフォーム API
 * スタンドアロン起動時: http://localhost:9003
 */
import axios from 'axios';

const BASE = process.env.REACT_APP_MEDICAL_PLATFORM_URL || 'http://localhost:9003';
const apiClient = axios.create({
  baseURL: BASE,
  headers: { 'Content-Type': 'application/json' },
});
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export interface AIDiagnosis {
  id: string;
  patient_id: string;
  finding: string;
  confidence: number;
  status: string;
}

export interface VoiceResponse {
  id: string;
  type: string;
  duration_sec: number;
  transcription: string;
  status: string;
}

export interface MedicalAnomaly {
  id: string;
  type: string;
  patient_id: string;
  metric: string;
  value: number;
  threshold: number;
  severity: string;
}

export interface PlatformStats {
  active_patients: number;
  ai_diagnosis_today: number;
  voice_processed_today: number;
  anomalies_detected_today: number;
  last_updated: string;
}

const API = '/api/v1/medical';

export const medicalApi = {
  async getAIDiagnosis() {
    const response = await apiClient.get<{ items: AIDiagnosis[]; total: number }>(
      `${API}/ai-diagnosis`
    );
    return response.data;
  },
  async getVoiceResponse() {
    const response = await apiClient.get<{ items: VoiceResponse[]; total: number }>(
      `${API}/voice-response`
    );
    return response.data;
  },
  async getAnomalyDetection() {
    const response = await apiClient.get<{ items: MedicalAnomaly[]; total: number }>(
      `${API}/anomaly-detection`
    );
    return response.data;
  },
  async getPlatformStats() {
    const response = await apiClient.get<PlatformStats>(`${API}/platform-stats`);
    return response.data;
  },
};
