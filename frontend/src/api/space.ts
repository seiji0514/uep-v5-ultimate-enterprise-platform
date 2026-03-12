/**
 * 宇宙・航空 API
 * 衛星軌道追跡、航空宇宙システム、時空操作
 */
import apiClient from './client';

export interface SatelliteTracking {
  id: string;
  name: string;
  orbit: string;
  altitude_km: number;
  status: string;
  next_pass: string | null;
}

export interface AerospaceSystem {
  id: string;
  system: string;
  status: string;
  uptime_percent: number;
}

export interface SpacetimeOperation {
  id: string;
  operation: string;
  satellite: string;
  scheduled: string;
  status: string;
}

export const spaceApi = {
  async getSatelliteTracking(): Promise<SatelliteTracking[]> {
    const response = await apiClient.get<{ items: SatelliteTracking[]; total: number }>(
      '/api/v1/space/satellite-tracking'
    );
    return response.data.items;
  },

  async getAerospaceSystems(): Promise<AerospaceSystem[]> {
    const response = await apiClient.get<{ items: AerospaceSystem[]; total: number }>(
      '/api/v1/space/aerospace-systems'
    );
    return response.data.items;
  },

  async getSpacetimeOperations(): Promise<SpacetimeOperation[]> {
    const response = await apiClient.get<{ items: SpacetimeOperation[]; total: number }>(
      '/api/v1/space/spacetime-operations'
    );
    return response.data.items;
  },
};
