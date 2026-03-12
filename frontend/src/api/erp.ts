/**
 * ERP（統合基幹業務システム）API
 * 販売管理・購買管理・データ連携基盤
 */
import apiClient from './client';

export interface ERPSummary {
  platform: string;
  version: string;
  modules: {
    販売管理: { order_count: number; total_sales: number };
    購買管理: { order_count: number; total_purchases: number };
    データ連携: { rules_count: number; last_sync_count: number; systems: string[] };
  };
}

export const erpApi = {
  getSummary: () => apiClient.get<ERPSummary>('/api/v1/erp/summary'),
  getSalesOrders: (status?: string) =>
    apiClient.get('/api/v1/erp/sales/orders', { params: status ? { status } : {} }),
  getPurchasingOrders: (status?: string) =>
    apiClient.get('/api/v1/erp/purchasing/orders', { params: status ? { status } : {} }),
  getDataIntegrationRules: () => apiClient.get('/api/v1/erp/data-integration/rules'),
  getDataIntegrationLogs: (limit?: number) =>
    apiClient.get('/api/v1/erp/data-integration/logs', { params: limit ? { limit } : {} }),
};
