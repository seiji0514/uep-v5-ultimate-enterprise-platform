"""
IoTセンサースキーマ
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class SensorBase(BaseModel):
    """センサーベーススキーマ"""
    sensor_id: str = Field(..., description="センサーID")
    sensor_type: str = Field(..., description="センサータイプ（environment, traffic, energy, security, infrastructure）")
    location_name: Optional[str] = Field(None, description="場所名")
    latitude: Optional[float] = Field(None, description="緯度")
    longitude: Optional[float] = Field(None, description="経度")
    status: str = Field("active", description="ステータス（active, inactive, maintenance）")
    metadata: Optional[Dict[str, Any]] = Field(None, description="メタデータ")


class SensorCreate(SensorBase):
    """センサー作成スキーマ"""
    pass


class SensorResponse(SensorBase):
    """センサー応答スキーマ"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

