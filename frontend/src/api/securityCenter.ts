/**
 * セキュリティコマンドセンター API
 */
import apiClient from './client';

export interface SecurityEvent {
  id: string;
  event_type: string;
  threat_level: string;
  source: string;
  target: string;
  description: string;
  status: string;
  created_at: string;
}

export interface Incident {
  id: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  created_at: string;
  updated_at?: string;
}

export interface Risk {
  id: string;
  title: string;
  description: string;
  level: string;
  created_at: string;
}

export const securityCenterApi = {
  async getEvents(): Promise<SecurityEvent[]> {
    const response = await apiClient.get<SecurityEvent[]>('/api/v1/security-center/events');
    return response.data;
  },

  async getIncidents(): Promise<Incident[]> {
    const response = await apiClient.get<Incident[]>('/api/v1/security-center/incidents');
    return response.data;
  },

  async getRisks(): Promise<Risk[]> {
    const response = await apiClient.get<Risk[]>('/api/v1/security-center/risks');
    return response.data;
  },
};
