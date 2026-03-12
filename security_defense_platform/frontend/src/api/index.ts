/**
 * 統合セキュリティ・防衛プラットフォーム API
 * スタンドアロン起動時: http://localhost:9001
 */
import axios from 'axios';

const SDP_BASE = process.env.REACT_APP_SECURITY_DEFENSE_PLATFORM_URL || 'http://localhost:9001';
const apiClient = axios.create({
  baseURL: SDP_BASE,
  headers: { 'Content-Type': 'application/json' },
});
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

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

export interface SuricataAlert {
  id: string;
  timestamp: string;
  src_ip: string;
  dest_ip: string;
  rule_id?: string;
  rule_msg: string;
  severity: string;
  source: string;
}

export interface WazuhAlert {
  id: string;
  timestamp: string;
  agent_id?: string;
  agent_name?: string;
  rule_id: string;
  rule_description: string;
  rule_level: number;
  source: string;
}

export interface ThreatIntelResult {
  ioc_type: string;
  ioc_value: string;
  is_malicious: boolean;
  confidence: number;
  sources: string[];
  details?: Record<string, unknown>;
}

export interface ComplianceReport {
  generated_at: string;
  period_start: string;
  period_end: string;
  summary: Record<string, number>;
  access_log_summary: Record<string, number>;
  incident_summary: Record<string, number>;
  security_events_summary: Record<string, number>;
  recommendations: string[];
}

const BASE = '/api/v1/security-defense-platform';

export const securityCenterApi = {
  async getEvents(params?: { event_type?: string; threat_level?: string; status?: string }): Promise<SecurityEvent[]> {
    const response = await apiClient.get<SecurityEvent[]>(`${BASE}/events`, { params });
    return (response as any).data;
  },
  async getIncidents(params?: { severity?: string; status?: string }): Promise<Incident[]> {
    const response = await apiClient.get<Incident[]>(`${BASE}/incidents`, { params });
    return (response as any).data;
  },
  async getRisks(params?: { category?: string; risk_level?: string }): Promise<Risk[]> {
    const response = await apiClient.get<Risk[]>(`${BASE}/risks`, { params });
    return (response as any).data;
  },
  async getAlerts(params?: { acknowledged?: boolean }) {
    const response = await apiClient.get<{ alerts: any[]; count: number }>(`${BASE}/alerts`, { params });
    return (response as any).data;
  },
  async getSecurityPosture() {
    const response = await apiClient.get(`${BASE}/security-posture`);
    return (response as any).data;
  },
};

export const cyberDefenseApi = {
  async getOverview() {
    const response = await apiClient.get(`${BASE}/cyber/overview`);
    return (response as any).data;
  },
  async getSuricataAlerts(limit = 50) {
    const response = await apiClient.get<SuricataAlert[]>(`${BASE}/cyber/suricata/alerts`, { params: { limit } });
    return (response as any).data;
  },
  async getWazuhAlerts(limit = 50) {
    const response = await apiClient.get<WazuhAlert[]>(`${BASE}/cyber/wazuh/alerts`, { params: { limit } });
    return (response as any).data;
  },
  async checkThreatIntel(iocType: string, iocValue: string) {
    const response = await apiClient.post<ThreatIntelResult>(`${BASE}/cyber/threat-intel/check`, {
      ioc_type: iocType,
      ioc_value: iocValue,
    });
    return (response as any).data;
  },
  async siemSearch(query?: string, source?: string, limit = 50) {
    const response = await apiClient.get(`${BASE}/cyber/siem/search`, { params: { query, source, limit } });
    return (response as any).data;
  },
  async getComplianceReport(periodDays = 30) {
    const response = await apiClient.get<ComplianceReport>(`${BASE}/cyber/compliance/report`, {
      params: { period_days: periodDays },
    });
    return (response as any).data;
  },
};
