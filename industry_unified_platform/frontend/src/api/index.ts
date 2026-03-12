/**
 * 産業統合プラットフォーム API
 * 製造・医療・金融・統合セキュリティ・防衛を1つのバックエンド（9010）で提供
 */
import axios from 'axios';

const DEFAULT_BASE = process.env.REACT_APP_INDUSTRY_API_URL || process.env.REACT_APP_INDUSTRY_UNIFIED_URL || 'http://localhost:9010';

export function getApiBaseUrl(): string {
  try {
    const override = localStorage.getItem('industry_api_base_url');
    if (override && override.trim()) return override.trim();
  } catch { /* ignore */ }
  return DEFAULT_BASE;
}

const apiClient = axios.create({
  baseURL: DEFAULT_BASE,
  headers: { 'Content-Type': 'application/json' },
});
apiClient.interceptors.request.use((config) => {
  const base = getApiBaseUrl();
  if (base) config.baseURL = base;
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// 製造
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

// 医療
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

// 金融
export interface Payment {
  id: string;
  amount: number;
  currency: string;
  status: string;
  created_at: string;
}
export interface RiskScore {
  transaction_id: string;
  risk_score: number;
  level: string;
  factors: string[];
}
export interface TransactionMonitoring {
  id: string;
  type: string;
  amount: number;
  status: string;
  alert: string | null;
}

// 統合セキュリティ・防衛
export interface SecurityEvent {
  id: string;
  event_type: string;
  threat_level: string;
  source: string;
  target: string;
  description: string;
  status: string;
  created_at?: string;
  timestamp?: string;
}
export interface SecurityIncident {
  id: string;
  title: string;
  description: string;
  severity: string;
  status: string;
  created_at: string;
  updated_at?: string;
}
export interface SecurityRisk {
  id: string;
  title?: string;
  name?: string;
  description: string;
  level?: string;
  risk_level?: string;
  created_at: string;
}

const SEC_BASE = '/api/v1/security-defense-platform';

export const securityCenterApi = {
  async getEvents(params?: { event_type?: string; threat_level?: string; status?: string }) {
    const r = await apiClient.get<SecurityEvent[]>(`${SEC_BASE}/events`, { params });
    return r.data;
  },
  async getIncidents(params?: { severity?: string; status?: string }) {
    const r = await apiClient.get<SecurityIncident[]>(`${SEC_BASE}/incidents`, { params });
    return r.data;
  },
  async getRisks(params?: { category?: string; risk_level?: string }) {
    const r = await apiClient.get<SecurityRisk[]>(`${SEC_BASE}/risks`, { params });
    return r.data;
  },
  async getOverview() {
    const r = await apiClient.get(`${SEC_BASE}/cyber/overview`);
    return r.data;
  },
};

export const manufacturingApi = {
  async getPredictiveMaintenance() {
    const r = await apiClient.get<{ items: PredictiveMaintenance[]; total: number }>('/api/v1/manufacturing/predictive-maintenance');
    return r.data;
  },
  async getSensorData() {
    const r = await apiClient.get<{ items: SensorData[]; total: number }>('/api/v1/manufacturing/sensor-data');
    return r.data;
  },
  async getAnomalies() {
    const r = await apiClient.get<{ items: Anomaly[]; total: number }>('/api/v1/manufacturing/anomalies');
    return r.data;
  },
};

export const medicalApi = {
  async getAIDiagnosis() {
    const r = await apiClient.get<{ items: AIDiagnosis[]; total: number }>('/api/v1/medical/ai-diagnosis');
    return r.data;
  },
  async getVoiceResponse() {
    const r = await apiClient.get<{ items: VoiceResponse[]; total: number }>('/api/v1/medical/voice-response');
    return r.data;
  },
  async getAnomalyDetection() {
    const r = await apiClient.get<{ items: MedicalAnomaly[]; total: number }>('/api/v1/medical/anomaly-detection');
    return r.data;
  },
  async getPlatformStats() {
    const r = await apiClient.get<PlatformStats>('/api/v1/medical/platform-stats');
    return r.data;
  },
};

export const fintechApi = {
  async getPayments() {
    const r = await apiClient.get<{ items: Payment[]; total: number }>('/api/v1/fintech/payments');
    return r.data;
  },
  async getRiskScores() {
    const r = await apiClient.get<{ items: RiskScore[]; total: number }>('/api/v1/fintech/risk-scores');
    return r.data;
  },
  async getTransactionMonitoring() {
    const r = await apiClient.get<{ items: TransactionMonitoring[]; total: number }>('/api/v1/fintech/transaction-monitoring');
    return r.data;
  },
  async runStressTest(portfolioValue = 1000000) {
    const r = await apiClient.get('/api/v1/fintech/stress-test', { params: { portfolio_value: portfolioValue } });
    return r.data;
  },
};

// インフラ・運用系（SIer・クラウドベンダー）
export interface IacProject {
  id: string;
  name: string;
  provider: string;
  status: string;
  last_deploy: string;
}
export interface OrchestrationDeployment {
  id: string;
  app: string;
  env: string;
  status: string;
  replicas: number;
  updated: string;
}
export interface MonitoringAlert {
  id: string;
  service: string;
  metric: string;
  value: number;
  threshold: number;
  severity: string;
  status: string;
}
export interface OptimizationRecommendation {
  id: string;
  type: string;
  resource: string;
  saving_estimate: number;
  action: string;
}
export const infraOpsApi = {
  async getIacProjects() {
    const r = await apiClient.get<{ items: IacProject[]; total: number }>('/api/v1/infra-ops/iac-projects');
    return r.data;
  },
  async getOrchestrationDeployments() {
    const r = await apiClient.get<{ items: OrchestrationDeployment[]; total: number }>('/api/v1/infra-ops/orchestration-deployments');
    return r.data;
  },
  async getMonitoringAlerts() {
    const r = await apiClient.get<{ items: MonitoringAlert[]; total: number }>('/api/v1/infra-ops/monitoring-alerts');
    return r.data;
  },
  async getOptimizationRecommendations() {
    const r = await apiClient.get<{ items: OptimizationRecommendation[]; total: number }>('/api/v1/infra-ops/optimization-recommendations');
    return r.data;
  },
  async getDashboard() {
    const r = await apiClient.get<{ iac_projects: number; deployments: number; alerts_open: number; optimization_savings: number }>('/api/v1/infra-ops/dashboard');
    return r.data;
  },
};

// DX・データ系
export interface DataLakeCatalog {
  id: string;
  name: string;
  size_gb: number;
  records: number;
  last_ingest: string;
}
export interface MlModel {
  id: string;
  name: string;
  accuracy: number;
  status: string;
  inference_count_today: number;
}
export interface GenerativeAiUsage {
  id: string;
  operation: string;
  model: string;
  tokens_today: number;
  status: string;
}
export interface DataPipeline {
  id: string;
  name: string;
  schedule: string;
  status: string;
  last_run: string;
}
export const dxDataApi = {
  async getDataLakeCatalogs() {
    const r = await apiClient.get<{ items: DataLakeCatalog[]; total: number }>('/api/v1/dx-data/data-lake-catalogs');
    return r.data;
  },
  async getMlModels() {
    const r = await apiClient.get<{ items: MlModel[]; total: number }>('/api/v1/dx-data/ml-models');
    return r.data;
  },
  async getGenerativeAiUsage() {
    const r = await apiClient.get<{ items: GenerativeAiUsage[]; total: number }>('/api/v1/dx-data/generative-ai-usage');
    return r.data;
  },
  async getDataPipelines() {
    const r = await apiClient.get<{ items: DataPipeline[]; total: number }>('/api/v1/dx-data/data-pipelines');
    return r.data;
  },
  async getDashboard() {
    const r = await apiClient.get<{ data_lake_total_gb: number; ml_models_count: number; genai_tokens_today: number; pipelines_running: number }>('/api/v1/dx-data/dashboard');
    return r.data;
  },
};

// コンプライアンス・ガバナンス系
export interface RegulatoryItem {
  id: string;
  regulation: string;
  status: string;
  last_audit: string;
  compliance_score: number;
}
export interface AuditLog {
  id: string;
  action: string;
  user: string;
  resource: string;
  result: string;
  timestamp: string;
}
export interface GovernancePolicy {
  id: string;
  name: string;
  version: string;
  status: string;
  updated: string;
}
export interface AuditFinding {
  id: string;
  severity: string;
  description: string;
  status: string;
  due_date: string;
}
export const complianceGovernanceApi = {
  async getRegulatoryItems() {
    const r = await apiClient.get<{ items: RegulatoryItem[]; total: number }>('/api/v1/compliance-governance/regulatory-items');
    return r.data;
  },
  async getAuditLogs() {
    const r = await apiClient.get<{ items: AuditLog[]; total: number }>('/api/v1/compliance-governance/audit-logs');
    return r.data;
  },
  async getGovernancePolicies() {
    const r = await apiClient.get<{ items: GovernancePolicy[]; total: number }>('/api/v1/compliance-governance/governance-policies');
    return r.data;
  },
  async getAuditFindings() {
    const r = await apiClient.get<{ items: AuditFinding[]; total: number }>('/api/v1/compliance-governance/audit-findings');
    return r.data;
  },
  async getDashboard() {
    const r = await apiClient.get<{ regulatory_compliance_avg: number; audit_findings_open: number; policies_count: number; audit_logs_today: number }>('/api/v1/compliance-governance/dashboard');
    return r.data;
  },
};

// サプライチェーン系
export interface LogisticsShipment {
  id: string;
  origin: string;
  destination: string;
  status: string;
  eta: string;
}
export interface InventoryItem {
  id: string;
  sku: string;
  name: string;
  qty: number;
  reorder_level: number;
  status: string;
}
export interface ProcurementOrder {
  id: string;
  supplier: string;
  amount: number;
  status: string;
  delivery_date: string;
}
export interface DemandForecast {
  sku: string;
  period: string;
  forecast: number;
  actual_last: number;
  accuracy: number;
}
export const supplyChainApi = {
  async getLogisticsShipments() {
    const r = await apiClient.get<{ items: LogisticsShipment[]; total: number }>('/api/v1/supply-chain/logistics-shipments');
    return r.data;
  },
  async getInventoryItems() {
    const r = await apiClient.get<{ items: InventoryItem[]; total: number }>('/api/v1/supply-chain/inventory-items');
    return r.data;
  },
  async getProcurementOrders() {
    const r = await apiClient.get<{ items: ProcurementOrder[]; total: number }>('/api/v1/supply-chain/procurement-orders');
    return r.data;
  },
  async getDemandForecast() {
    const r = await apiClient.get<{ items: DemandForecast[]; total: number }>('/api/v1/supply-chain/demand-forecast');
    return r.data;
  },
  async getDashboard() {
    const r = await apiClient.get<{ shipments_in_transit: number; inventory_reorder_count: number; procurement_total: number; inventory_total_units: number }>('/api/v1/supply-chain/dashboard');
    return r.data;
  },
};

// Phase 2: 実データ連携
export const dataIntegrationApi = {
  async importCsv(rows: string[][], domain: string = 'general') {
    const r = await apiClient.post<{ saved: number; domain: string }>('/api/v1/data-integration/csv', { rows, domain });
    return r.data;
  },
  async getStoredCsv(domain?: string) {
    const r = await apiClient.get<{ items: any[]; total: number }>('/api/v1/data-integration/csv', { params: domain ? { domain } : {} });
    return r.data;
  },
};
