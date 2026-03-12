/**
 * サイバー対策 API
 * レベル4: IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス
 */
import apiClient from './client';

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

export const cyberDefenseApi = {
  async getOverview() {
    const response = await apiClient.get('/api/v1/security-defense-platform/cyber/overview');
    return response.data;
  },

  async getSuricataAlerts(limit = 50) {
    const response = await apiClient.get<SuricataAlert[]>('/api/v1/security-defense-platform/cyber/suricata/alerts', {
      params: { limit },
    });
    return response.data;
  },

  async getWazuhAlerts(limit = 50) {
    const response = await apiClient.get<WazuhAlert[]>('/api/v1/security-defense-platform/cyber/wazuh/alerts', {
      params: { limit },
    });
    return response.data;
  },

  async checkThreatIntel(iocType: string, iocValue: string) {
    const response = await apiClient.post<ThreatIntelResult>('/api/v1/security-defense-platform/cyber/threat-intel/check', {
      ioc_type: iocType,
      ioc_value: iocValue,
    });
    return response.data;
  },

  async siemSearch(query?: string, source?: string, limit = 50) {
    const response = await apiClient.get('/api/v1/security-defense-platform/cyber/siem/search', {
      params: { query, source, limit },
    });
    return response.data;
  },

  async getComplianceReport(periodDays = 30) {
    const response = await apiClient.get<ComplianceReport>('/api/v1/security-defense-platform/cyber/compliance/report', {
      params: { period_days: periodDays },
    });
    return response.data;
  },
};
