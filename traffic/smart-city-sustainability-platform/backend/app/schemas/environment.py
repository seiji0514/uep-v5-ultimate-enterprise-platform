"""
環境データスキーマ
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class EnvironmentDataBase(BaseModel):
    """環境データベーススキーマ"""
    sensor_id: str = Field(..., description="センサーID")
    data_type: str = Field(..., description="データタイプ（air_quality, water_quality, soil_quality, biodiversity）")
    value: float = Field(..., description="値")
    unit: str = Field(..., description="単位")


class EnvironmentDataCreate(EnvironmentDataBase):
    """環境データ作成スキーマ"""
    pass


class EnvironmentDataResponse(EnvironmentDataBase):
    """環境データ応答スキーマ"""
    id: UUID
    timestamp: datetime
    
    class Config:
        from_attributes = True

