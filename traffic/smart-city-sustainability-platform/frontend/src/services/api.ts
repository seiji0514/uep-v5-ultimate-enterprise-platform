import axios from 'axios';

// Docker環境では backend:8000、開発環境では localhost:8000
const API_BASE_URL = process.env.REACT_APP_API_URL || 
  (import.meta.env.DEV ? 'http://localhost:8000' : 'http://backend:8000');

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// IoTセンサーAPI
export const sensorService = {
  getSensors: (params?: any) => apiClient.get('/api/v1/sensors/', { params }),
  getSensor: (sensorId: string) => apiClient.get(`/api/v1/sensors/${sensorId}`),
  createSensor: (data: any) => apiClient.post('/api/v1/sensors/', data),
  updateSensor: (sensorId: string, data: any) => apiClient.put(`/api/v1/sensors/${sensorId}`, data),
  deleteSensor: (sensorId: string) => apiClient.delete(`/api/v1/sensors/${sensorId}`),
};

// 環境データAPI
export const environmentService = {
  getData: (params?: any) => apiClient.get('/api/v1/environment/data', { params }),
  createData: (data: any) => apiClient.post('/api/v1/environment/data', data),
  analyze: (params?: any) => apiClient.get('/api/v1/environment/analysis', { params }),
  predict: (params?: any) => apiClient.get('/api/v1/environment/predictions', { params }),
};

// 交通データAPI
export const trafficService = {
  getData: (params?: any) => apiClient.get('/api/v1/traffic/data', { params }),
  createData: (data: any) => apiClient.post('/api/v1/traffic/data', data),
  getCongestion: (params?: any) => apiClient.get('/api/v1/traffic/congestion', { params }),
};

// エネルギーデータAPI
export const energyService = {
  getData: (params?: any) => apiClient.get('/api/v1/energy/data', { params }),
  createData: (data: any) => apiClient.post('/api/v1/energy/data', data),
  getBalance: (params?: any) => apiClient.get('/api/v1/energy/balance', { params }),
};

// ESGレポートAPI
export const esgService = {
  getReports: (params?: any) => apiClient.get('/api/v1/esg/reports', { params }),
  generateReport: (data: any) => apiClient.post('/api/v1/esg/reports/generate', data),
  getCarbonFootprint: (params?: any) => apiClient.get('/api/v1/esg/carbon-footprint', { params }),
  createCarbonFootprint: (data: any) => apiClient.post('/api/v1/esg/carbon-footprint', data),
};

// ダッシュボードAPI
export const dashboardService = {
  getOverview: (params?: any) => apiClient.get('/api/v1/dashboard/overview', { params }),
  getKPI: (params?: any) => apiClient.get('/api/v1/dashboard/kpi', { params }),
  getAlertsSummary: (params?: any) => apiClient.get('/api/v1/dashboard/alerts-summary', { params }),
};

// アラートAPI
export const alertService = {
  getAlerts: (params?: any) => apiClient.get('/api/v1/alerts/', { params }),
  acknowledgeAlert: (alertId: string, userId: string) =>
    apiClient.post(`/api/v1/alerts/${alertId}/acknowledge`, { user_id: userId }),
  resolveAlert: (alertId: string) => apiClient.post(`/api/v1/alerts/${alertId}/resolve`),
};

// 判断支援API
export const decisionSupportService = {
  performScenarioAnalysis: (data: any) => apiClient.post('/api/v1/decision-support/scenario-analysis', data),
  performRiskAssessment: (data: any) => apiClient.post('/api/v1/decision-support/risk-assessment', data),
  generateRunbook: (data: any) => apiClient.post('/api/v1/decision-support/generate-runbook', data),
  getLogs: (params?: any) => apiClient.get('/api/v1/decision-support/logs', { params }),
};

export default apiClient;

