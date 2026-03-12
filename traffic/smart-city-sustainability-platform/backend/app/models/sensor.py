"""
IoTセンサーモデル
"""

from sqlalchemy import Column, String, Float, JSON, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class IoTSensor(Base):
    """IoTセンサーテーブル"""
    __tablename__ = "iot_sensors"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(String(255), unique=True, nullable=False, index=True)
    sensor_type = Column(String(50), nullable=False, index=True)  # environment, traffic, energy, security, infrastructure
    location_name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    status = Column(String(50), default="active", index=True)  # active, inactive, maintenance
    metadata = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

