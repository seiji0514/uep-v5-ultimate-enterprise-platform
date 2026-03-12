/**
 * 医療 API
 * AI診断、音声応答、異常検知、医療プラットフォーム
 */
import apiClient from './client';

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

export const medicalApi = {
  async getAIDiagnosis(): Promise<AIDiagnosis[]> {
    const response = await apiClient.get<{ items: AIDiagnosis[]; total: number }>(
      '/api/v1/medical/ai-diagnosis'
    );
    return response.data.items;
  },

  async getVoiceResponse(): Promise<VoiceResponse[]> {
    const response = await apiClient.get<{ items: VoiceResponse[]; total: number }>(
      '/api/v1/medical/voice-response'
    );
    return response.data.items;
  },

  async getAnomalyDetection(): Promise<MedicalAnomaly[]> {
    const response = await apiClient.get<{ items: MedicalAnomaly[]; total: number }>(
      '/api/v1/medical/anomaly-detection'
    );
    return response.data.items;
  },

  async getPlatformStats(): Promise<PlatformStats> {
    const response = await apiClient.get<PlatformStats>('/api/v1/medical/platform-stats');
    return response.data;
  },
};
