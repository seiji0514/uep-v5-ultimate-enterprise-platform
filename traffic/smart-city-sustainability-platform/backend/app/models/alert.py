"""
アラートモデル
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class Alert(Base):
    """アラートテーブル"""
    __tablename__ = "alerts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sensor_id = Column(UUID(as_uuid=True), ForeignKey("iot_sensors.id"))
    alert_type = Column(String(50), nullable=False)  # threshold_exceeded, anomaly_detected, system_error
    severity = Column(String(50), nullable=False)  # low, medium, high, critical
    message = Column(Text, nullable=False)
    status = Column(String(50), default="open")  # open, acknowledged, resolved
    acknowledged_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    acknowledged_at = Column(DateTime)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

