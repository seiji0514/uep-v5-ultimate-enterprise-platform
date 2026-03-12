/**
 * サプライチェーン API
 */
import apiClient from './client';

export interface LogisticsShipment {
  id: string;
  origin: string;
  destination: string;
  status: string;
  eta: string;
  carrier: string;
}

export interface InventoryItem {
  id: string;
  sku: string;
  name: string;
  qty: number;
  reorder_level: number;
  status: string;
  warehouse: string;
}

export interface ProcurementOrder {
  id: string;
  supplier: string;
  amount: number;
  status: string;
  delivery_date: string;
  items: number;
}

export const supplyChainApi = {
  async getLogistics(): Promise<LogisticsShipment[]> {
    const res = await apiClient.get<{ items: LogisticsShipment[] }>('/api/v1/supply-chain/logistics-shipments');
    return res.data.items;
  },
  async getInventory(): Promise<InventoryItem[]> {
    const res = await apiClient.get<{ items: InventoryItem[] }>('/api/v1/supply-chain/inventory-items');
    return res.data.items;
  },
  async getProcurement(): Promise<ProcurementOrder[]> {
    const res = await apiClient.get<{ items: ProcurementOrder[] }>('/api/v1/supply-chain/procurement-orders');
    return res.data.items;
  },
  async getDashboard(): Promise<Record<string, number>> {
    const res = await apiClient.get('/api/v1/supply-chain/dashboard');
    return res.data;
  },
};
