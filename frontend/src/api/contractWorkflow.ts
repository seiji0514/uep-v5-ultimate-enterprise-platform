/**
 * 契約ワークフロー API
 * 見積・契約・納品・請求の一気通貫
 */
import apiClient from './client';

export const contractWorkflowApi = {
  getEstimates: () => apiClient.get<{ items: any[] }>('/api/v1/contract-workflow/estimates'),
  getContracts: () => apiClient.get<{ items: any[] }>('/api/v1/contract-workflow/contracts'),
  getDeliveries: () => apiClient.get<{ items: any[] }>('/api/v1/contract-workflow/deliveries'),
  getInvoices: () => apiClient.get<{ items: any[] }>('/api/v1/contract-workflow/invoices'),
  exportPdf: async (type: string, id: string): Promise<Blob> => {
    const res = await apiClient.get(`/api/v1/contract-workflow/export/${type}/${id}`, {
      responseType: 'blob',
    });
    return res.data;
  },
};
