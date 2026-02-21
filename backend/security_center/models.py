"""
統合セキュリティコマンドセンター関連のデータモデル
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class SecurityEventCreate(BaseModel):
    """セキュリティイベント作成モデル"""

    event_type: str
    threat_level: str
    source: str
    target: str
    description: str
    metadata: Optional[Dict[str, Any]] = None


class IncidentCreate(BaseModel):
    """インシデント作成モデル"""

    title: str
    description: str
    severity: str
    affected_systems: Optional[List[str]] = None
    incident_type: Optional[str] = None


class IncidentUpdate(BaseModel):
    """インシデント更新モデル"""

    status: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None


class RiskCreate(BaseModel):
    """リスク作成モデル"""

    name: str
    description: str
    category: str
    likelihood: float
    impact: float
    mitigation: Optional[str] = None
