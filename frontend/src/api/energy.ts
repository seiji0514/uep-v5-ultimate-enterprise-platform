/**
 * エネルギー API
 * 需給予測API、スマートグリッド制御、メトリクス
 */
import apiClient from './client';

export interface DemandForecast {
  hour: string;
  predicted_kwh: number;
  actual_kwh: number | null;
  accuracy: number | null;
}

export interface SmartGridControl {
  zone: string;
  status: string;
  load_percent: number;
  renewable_percent: number;
}

export interface EnergyMetrics {
  total_generation_kwh: number;
  total_consumption_kwh: number;
  renewable_ratio: number;
  grid_stability: number;
  last_updated: string;
}

export const energyApi = {
  async getDemandForecast(): Promise<DemandForecast[]> {
    const response = await apiClient.get<{ items: DemandForecast[]; total: number }>(
      '/api/v1/energy/demand-forecast'
    );
    return response.data.items;
  },

  async getSmartGridControl(): Promise<SmartGridControl[]> {
    const response = await apiClient.get<{ items: SmartGridControl[]; total: number }>(
      '/api/v1/energy/smart-grid'
    );
    return response.data.items;
  },

  async getMetrics(): Promise<EnergyMetrics> {
    const response = await apiClient.get<EnergyMetrics>('/api/v1/energy/metrics');
    return response.data;
  },
};
