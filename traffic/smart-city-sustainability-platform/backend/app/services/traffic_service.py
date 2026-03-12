"""
交通データサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import pandas as pd
from app.core.influxdb_client import write_time_series_data, query_time_series_data
from loguru import logger


class TrafficService:
    """交通データサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_traffic_data(
        self,
        sensor_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """交通データの取得"""
        try:
            if not start_time:
                start_time = datetime.now() - pd.Timedelta(days=1)
            if not end_time:
                end_time = datetime.now()
            
            filters = {}
            if sensor_id:
                filters["sensor_id"] = sensor_id
            
            data = await query_time_series_data(
                measurement="traffic_data",
                start=start_time.isoformat(),
                stop=end_time.isoformat(),
                filters=filters
            )
            
            return data[skip:skip+limit]
            
        except Exception as e:
            logger.error(f"交通データ取得エラー: {e}")
            return []
    
    async def create_traffic_data(
        self,
        sensor_id: str,
        vehicle_count: int,
        average_speed: float,
        occupancy: float
    ) -> dict:
        """交通データの作成"""
        try:
            await write_time_series_data(
                measurement="traffic_data",
                tags={"sensor_id": sensor_id},
                fields={
                    "vehicle_count": vehicle_count,
                    "average_speed": average_speed,
                    "occupancy": occupancy
                }
            )
            
            logger.info(f"交通データ作成成功: sensor_id={sensor_id}")
            return {"message": "交通データを作成しました", "sensor_id": sensor_id}
            
        except Exception as e:
            logger.error(f"交通データ作成エラー: {e}")
            raise
    
    def get_congestion_data(
        self,
        location: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """渋滞データの取得"""
        try:
            data = self.get_traffic_data(
                start_time=start_time,
                end_time=end_time,
                limit=10000
            )
            
            # 渋滞判定（平均速度が30km/h以下、または占有率が80%以上）
            congestion_count = 0
            for d in data:
                if "average_speed" in d and d["average_speed"] < 30:
                    congestion_count += 1
                elif "occupancy" in d and d["occupancy"] > 80:
                    congestion_count += 1
            
            return {
                "total_data_points": len(data),
                "congestion_count": congestion_count,
                "congestion_rate": congestion_count / len(data) * 100 if len(data) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"渋滞データ取得エラー: {e}")
            raise

