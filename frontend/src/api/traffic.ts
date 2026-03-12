/**
 * 交通 API
 * 交通管理、航空管制、スマートシティ持続可能性プラットフォーム
 */
import apiClient from './client';

export interface TrafficManagement {
  id: string;
  zone: string;
  congestion_level: number;
  status: string;
  signal_adjustment: string;
}

export interface AirTrafficControl {
  id: string;
  flight: string;
  altitude_ft: number;
  status: string;
  eta_minutes: number;
}

export interface SmartCitySustainability {
  co2_reduction_today_kg: number;
  ev_charging_sessions: number;
  public_transit_ridership: number;
  traffic_flow_optimization: number;
  last_updated: string;
}

export const trafficApi = {
  async getTrafficManagement(): Promise<TrafficManagement[]> {
    const response = await apiClient.get<{ items: TrafficManagement[]; total: number }>(
      '/api/v1/traffic/traffic-management'
    );
    return response.data.items;
  },

  async getAirTrafficControl(): Promise<AirTrafficControl[]> {
    const response = await apiClient.get<{ items: AirTrafficControl[]; total: number }>(
      '/api/v1/traffic/air-traffic-control'
    );
    return response.data.items;
  },

  async getSmartCitySustainability(): Promise<SmartCitySustainability> {
    const response = await apiClient.get<SmartCitySustainability>(
      '/api/v1/traffic/smart-city-sustainability'
    );
    return response.data;
  },
};
