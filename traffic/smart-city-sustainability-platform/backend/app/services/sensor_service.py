"""
IoTセンサーサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.sensor import IoTSensor
from app.schemas.sensor import SensorCreate, SensorResponse
from loguru import logger


class SensorService:
    """IoTセンサーサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_sensors(
        self,
        sensor_type: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[SensorResponse]:
        """センサー一覧の取得"""
        query = self.db.query(IoTSensor)
        
        if sensor_type:
            query = query.filter(IoTSensor.sensor_type == sensor_type)
        
        if status:
            query = query.filter(IoTSensor.status == status)
        
        sensors = query.offset(skip).limit(limit).all()
        return [SensorResponse.model_validate(sensor) for sensor in sensors]
    
    def get_sensor(self, sensor_id: str) -> Optional[SensorResponse]:
        """センサー詳細の取得"""
        sensor = self.db.query(IoTSensor).filter(IoTSensor.sensor_id == sensor_id).first()
        if sensor:
            return SensorResponse.model_validate(sensor)
        return None
    
    def create_sensor(self, sensor: SensorCreate) -> SensorResponse:
        """センサーの作成"""
        db_sensor = IoTSensor(**sensor.model_dump())
        self.db.add(db_sensor)
        self.db.commit()
        self.db.refresh(db_sensor)
        logger.info(f"センサー作成成功: {sensor.sensor_id}")
        return SensorResponse.model_validate(db_sensor)
    
    def update_sensor(self, sensor_id: str, sensor: SensorCreate) -> Optional[SensorResponse]:
        """センサーの更新"""
        db_sensor = self.db.query(IoTSensor).filter(IoTSensor.sensor_id == sensor_id).first()
        if not db_sensor:
            return None
        
        for key, value in sensor.model_dump().items():
            setattr(db_sensor, key, value)
        
        self.db.commit()
        self.db.refresh(db_sensor)
        logger.info(f"センサー更新成功: {sensor_id}")
        return SensorResponse.model_validate(db_sensor)
    
    def delete_sensor(self, sensor_id: str) -> bool:
        """センサーの削除"""
        db_sensor = self.db.query(IoTSensor).filter(IoTSensor.sensor_id == sensor_id).first()
        if not db_sensor:
            return False
        
        self.db.delete(db_sensor)
        self.db.commit()
        logger.info(f"センサー削除成功: {sensor_id}")
        return True

