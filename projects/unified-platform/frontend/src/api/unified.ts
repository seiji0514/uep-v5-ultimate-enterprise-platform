import { api } from './client';

export interface ERPSummary {
  platform: string;
  version: string;
  modules: {
    販売管理: { order_count: number; total_sales: number };
    購買管理: { order_count: number; total_purchases: number };
    データ連携: { rules_count: number; last_sync_count: number; systems: string[] };
  };
}

export const authApi = {
  changePassword: (currentPassword: string, newPassword: string) =>
    api.post('/api/v1/auth/change-password', { current_password: currentPassword, new_password: newPassword }),
};

export const unifiedApi = {
  medical: {
    getPatients: (params?: { limit?: number; offset?: number }) => api.get<{ items: any[]; total: number }>('/api/v1/medical/patients', { params }),
    importPatientsCsv: (file: File) => {
      const fd = new FormData();
      fd.append('file', file);
      return api.post<{ imported: number }>('/api/v1/medical/patients/import', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
    },
    getAIDiagnosis: () => api.get<{ items: any[]; total: number }>('/api/v1/medical/ai-diagnosis'),
    getVitalSigns: () => api.get<{ items: any[]; total: number }>('/api/v1/medical/vital-signs'),
    getStats: () => api.get('/api/v1/medical/stats'),
  },
  aviation: {
    getFlights: (params?: { limit?: number; offset?: number }) => api.get<{ items: any[]; total: number }>('/api/v1/aviation/flights', { params }),
    importFlightsCsv: (file: File) => {
      const fd = new FormData();
      fd.append('file', file);
      return api.post<{ imported: number }>('/api/v1/aviation/flights/import', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
    },
    getAirports: () => api.get<{ items: any[]; total: number }>('/api/v1/aviation/airports'),
    getDelays: () => api.get('/api/v1/aviation/delays'),
    getDelayPrediction: () => api.get('/api/v1/aviation/delay-prediction'),
    getStats: () => api.get('/api/v1/aviation/stats'),
  },
  space: {
    getSatellites: () => api.get<{ items: any[]; total: number }>('/api/v1/space/satellites'),
    getLaunches: () => api.get<{ items: any[]; total: number }>('/api/v1/space/launches'),
    getApod: () => api.get('/api/v1/space/apod'),
    getStats: () => api.get('/api/v1/space/stats'),
  },
  unified: {
    getStats: () => api.get('/api/v1/unified/stats'),
  },
  erp: {
    getSummary: () => api.get<ERPSummary>('/api/v1/erp/summary'),
    getSalesOrders: (status?: string) => api.get('/api/v1/erp/sales/orders', { params: status ? { status } : {} }),
    getPurchasingOrders: (status?: string) => api.get('/api/v1/erp/purchasing/orders', { params: status ? { status } : {} }),
    getSalesOrder: (id: string) => api.get(`/api/v1/erp/sales/orders/${id}`),
    getPurchasingOrder: (id: string) => api.get(`/api/v1/erp/purchasing/orders/${id}`),
    updateSalesOrder: (id: string, data: { status?: string; invoice_no?: string; shipped_at?: string }) =>
      api.patch(`/api/v1/erp/sales/orders/${id}`, data),
    updatePurchasingOrder: (id: string, data: { status?: string; received_at?: string; invoice_no?: string }) =>
      api.patch(`/api/v1/erp/purchasing/orders/${id}`, data),
    getDataIntegrationRules: () => api.get('/api/v1/erp/data-integration/rules'),
    createSalesOrder: (data: { customer_id: string; customer_name: string; items: any[]; total_amount: number; notes?: string }) =>
      api.post('/api/v1/erp/sales/orders', data),
    createPurchasingOrder: (data: { supplier_id: string; supplier_name: string; items: any[]; total_amount: number; notes?: string }) =>
      api.post('/api/v1/erp/purchasing/orders', data),
  },
  legacyMigration: {
    getSummary: () => api.get('/api/v1/legacy-migration/summary'),
    getJobs: (limit?: number) => api.get('/api/v1/legacy-migration/jobs', { params: limit ? { limit } : {} }),
    getJob: (id: string) => api.get(`/api/v1/legacy-migration/jobs/${id}`),
    getLogs: (limit?: number) => api.get('/api/v1/legacy-migration/logs', { params: limit ? { limit } : {} }),
    createJob: (data: { name?: string; source_type: string; source_config?: Record<string, any>; target_system: string; mapping?: Record<string, string> }) =>
      api.post('/api/v1/legacy-migration/jobs', data),
    runJob: (jobId: string) => api.post(`/api/v1/legacy-migration/jobs/${jobId}/run`),
    validate: (data: { job_id: string }) => api.post('/api/v1/legacy-migration/validate', data),
  },
  dataIntegration: {
    getSummary: () => api.get('/api/v1/data-integration/summary'),
    getRules: () => api.get('/api/v1/data-integration/rules'),
    getLogs: (limit?: number) => api.get('/api/v1/data-integration/logs', { params: limit ? { limit } : {} }),
    createRule: (data: { source_system: string; target_system: string; sync_type?: string; schedule?: string }) =>
      api.post('/api/v1/data-integration/rules', data),
    executeSync: (ruleId: string) => api.post(`/api/v1/data-integration/sync/${ruleId}`),
  },
  dx: {
    getSummary: () => api.get('/api/v1/dx/summary'),
    getDocuments: (limit?: number) => api.get('/api/v1/dx/documents', { params: limit ? { limit } : {} }),
    createDocument: (data: { title: string; content?: string; category?: string }) =>
      api.post('/api/v1/dx/documents', data),
    getDocument: (id: string) => api.get(`/api/v1/dx/documents/${id}`),
    updateDocument: (id: string, data: { title?: string; content?: string; category?: string }) =>
      api.put(`/api/v1/dx/documents/${id}`, data),
    deleteDocument: (id: string) => api.delete(`/api/v1/dx/documents/${id}`),
    getWorkflows: (limit?: number) => api.get('/api/v1/dx/workflows', { params: limit ? { limit } : {} }),
    createWorkflow: (data: { name: string; description?: string; status?: string; steps?: any[] }) =>
      api.post('/api/v1/dx/workflows', data),
    getWorkflow: (id: string) => api.get(`/api/v1/dx/workflows/${id}`),
    updateWorkflow: (id: string, data: { name?: string; description?: string; status?: string; steps?: any[] }) =>
      api.put(`/api/v1/dx/workflows/${id}`, data),
    deleteWorkflow: (id: string) => api.delete(`/api/v1/dx/workflows/${id}`),
  },
  notifications: {
    list: () => api.get<{ items: any[]; total: number }>('/api/v1/notifications'),
    markRead: (id: number) => api.post(`/api/v1/notifications/${id}/read`),
  },
  search: (q: string, limit?: number) =>
    api.get<{ items: any[]; total: number }>('/api/v1/search', { params: { q, limit } }),
  widgets: {
    weather: () => api.get('/api/v1/widgets/weather'),
    calendar: () => api.get('/api/v1/widgets/calendar'),
  },
  health: {
    detail: () => api.get<{ health: any; ready: any; timestamp: string }>('/api/v1/health/detail'),
  },
  logs: {
    list: (limit?: number) => api.get<{ items: { ts: string; level: string; msg: string }[]; total: number }>('/api/v1/logs', { params: { limit } }),
  },
};
