"""
ダッシュボードサービス
"""

from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import pandas as pd
from app.core.influxdb_client import query_time_series_data
from app.services.environment_service import EnvironmentService
from app.services.traffic_service import TrafficService
from app.services.energy_service import EnergyService
from loguru import logger


class DashboardService:
    """ダッシュボードサービス"""
    
    def __init__(self, db: Session):
        self.db = db
        self.env_service = EnvironmentService(db)
        self.traffic_service = TrafficService(db)
        self.energy_service = EnergyService(db)
    
    async def get_dashboard_overview(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """ダッシュボード概要の取得"""
        try:
            if not start_time:
                start_time = datetime.now() - pd.Timedelta(days=1)
            if not end_time:
                end_time = datetime.now()
            
            # 環境データの概要
            env_data = await self.env_service.get_environment_data(
                start_time=start_time,
                end_time=end_time,
                limit=1000
            )
            
            # 交通データの概要
            traffic_data = await self.traffic_service.get_traffic_data(
                start_time=start_time,
                end_time=end_time,
                limit=1000
            )
            
            # エネルギーデータの概要
            energy_data = await self.energy_service.get_energy_data(
                start_time=start_time,
                end_time=end_time,
                limit=1000
            )
            
            return {
                "period": {
                    "start": start_time.isoformat(),
                    "end": end_time.isoformat()
                },
                "environment": {
                    "data_points": len(env_data),
                    "sensors": len(set(d.get("sensor_id") for d in env_data if "sensor_id" in d))
                },
                "traffic": {
                    "data_points": len(traffic_data),
                    "sensors": len(set(d.get("sensor_id") for d in traffic_data if "sensor_id" in d))
                },
                "energy": {
                    "data_points": len(energy_data),
                    "sensors": len(set(d.get("sensor_id") for d in energy_data if "sensor_id" in d))
                }
            }
            
        except Exception as e:
            logger.error(f"ダッシュボード概要取得エラー: {e}")
            raise
    
    def get_dashboard_kpi(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """統合KPIの取得"""
        try:
            if not start_time:
                start_time = datetime.now() - pd.Timedelta(days=1)
            if not end_time:
                end_time = datetime.now()
            
            # エネルギーバランス
            energy_balance = self.energy_service.get_energy_balance(
                start_time=start_time,
                end_time=end_time
            )
            
            # 渋滞データ
            congestion = self.traffic_service.get_congestion_data(
                start_time=start_time,
                end_time=end_time
            )
            
            return {
                "energy": {
                    "total_consumption": energy_balance.get("total_consumption", 0),
                    "total_generation": energy_balance.get("total_generation", 0),
                    "self_sufficiency_rate": energy_balance.get("self_sufficiency_rate", 0)
                },
                "traffic": {
                    "congestion_rate": congestion.get("congestion_rate", 0),
                    "congestion_count": congestion.get("congestion_count", 0)
                }
            }
            
        except Exception as e:
            logger.error(f"統合KPI取得エラー: {e}")
            raise
    
    def get_alerts_summary(
        self,
        severity: Optional[str] = None,
        status: Optional[str] = None
    ) -> dict:
        """アラートサマリーの取得"""
        try:
            from app.services.alert_service import AlertService
            alert_service = AlertService(self.db)
            
            alerts = alert_service.get_alerts(
                severity=severity,
                status=status,
                limit=1000
            )
            
            severity_count = {}
            status_count = {}
            
            for alert in alerts:
                sev = alert.get("severity", "unknown")
                stat = alert.get("status", "unknown")
                
                severity_count[sev] = severity_count.get(sev, 0) + 1
                status_count[stat] = status_count.get(stat, 0) + 1
            
            return {
                "total": len(alerts),
                "by_severity": severity_count,
                "by_status": status_count
            }
            
        except Exception as e:
            logger.error(f"アラートサマリー取得エラー: {e}")
            raise

