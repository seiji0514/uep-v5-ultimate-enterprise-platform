"""
エネルギーデータサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
import pandas as pd
from app.core.influxdb_client import write_time_series_data, query_time_series_data
from loguru import logger


class EnergyService:
    """エネルギーデータサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def get_energy_data(
        self,
        sensor_id: Optional[str] = None,
        energy_type: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """エネルギーデータの取得"""
        try:
            if not start_time:
                start_time = datetime.now() - pd.Timedelta(days=1)
            if not end_time:
                end_time = datetime.now()
            
            filters = {}
            if sensor_id:
                filters["sensor_id"] = sensor_id
            if energy_type:
                filters["energy_type"] = energy_type
            
            data = await query_time_series_data(
                measurement="energy_data",
                start=start_time.isoformat(),
                stop=end_time.isoformat(),
                filters=filters
            )
            
            return data[skip:skip+limit]
            
        except Exception as e:
            logger.error(f"エネルギーデータ取得エラー: {e}")
            return []
    
    async def create_energy_data(
        self,
        sensor_id: str,
        energy_type: str,
        consumption: float,
        generation: Optional[float] = None
    ) -> dict:
        """エネルギーデータの作成"""
        try:
            fields = {"consumption": consumption}
            if generation:
                fields["generation"] = generation
            
            await write_time_series_data(
                measurement="energy_data",
                tags={
                    "sensor_id": sensor_id,
                    "energy_type": energy_type
                },
                fields=fields
            )
            
            logger.info(f"エネルギーデータ作成成功: sensor_id={sensor_id}, energy_type={energy_type}")
            return {"message": "エネルギーデータを作成しました", "sensor_id": sensor_id}
            
        except Exception as e:
            logger.error(f"エネルギーデータ作成エラー: {e}")
            raise
    
    def get_energy_balance(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """エネルギーバランスの取得"""
        try:
            data = self.get_energy_data(
                start_time=start_time,
                end_time=end_time,
                limit=10000
            )
            
            total_consumption = sum(d.get("consumption", 0) for d in data if "consumption" in d)
            total_generation = sum(d.get("generation", 0) for d in data if "generation" in d)
            
            return {
                "total_consumption": total_consumption,
                "total_generation": total_generation,
                "balance": total_generation - total_consumption,
                "self_sufficiency_rate": (total_generation / total_consumption * 100) if total_consumption > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"エネルギーバランス取得エラー: {e}")
            raise

