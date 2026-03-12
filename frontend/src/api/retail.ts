/**
 * 小売・EC API
 */
import apiClient from './client';

export interface PosTransaction {
  id: string;
  store: string;
  amount: number;
  items: number;
  timestamp: string;
  payment: string;
}

export interface EcOrder {
  id: string;
  customer_id: string;
  amount: number;
  status: string;
  ordered_at: string;
}

export interface InventoryItem {
  sku: string;
  name: string;
  qty: number;
  reorder_level: number;
  status: string;
  store: string;
}

export const retailApi = {
  async getPosTransactions(): Promise<PosTransaction[]> {
    const res = await apiClient.get<{ items: PosTransaction[] }>('/api/v1/retail/pos-transactions');
    return res.data.items;
  },
  async getEcOrders(): Promise<EcOrder[]> {
    const res = await apiClient.get<{ items: EcOrder[] }>('/api/v1/retail/ec-orders');
    return res.data.items;
  },
  async getInventory(): Promise<InventoryItem[]> {
    const res = await apiClient.get<{ items: InventoryItem[] }>('/api/v1/retail/inventory');
    return res.data.items;
  },
  async getDashboard(): Promise<Record<string, number>> {
    const res = await apiClient.get('/api/v1/retail/dashboard');
    return res.data;
  },
};
