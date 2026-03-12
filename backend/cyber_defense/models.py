"""
サイバー対策 データモデル
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class AlertSource(str, Enum):
    """アラートソース"""
    SURICATA = "suricata"
    WAZUH = "wazuh"
    INTERNAL = "internal"
    MISP = "misp"


class SuricataAlertCreate(BaseModel):
    """Suricata アラート取り込み"""
    timestamp: str
    src_ip: str
    dest_ip: str
    src_port: Optional[int] = None
    dest_port: Optional[int] = None
    proto: Optional[str] = None
    rule_id: str
    rule_msg: str
    severity: str = "medium"  # low, medium, high, critical
    metadata: Optional[Dict[str, Any]] = None


class WazuhAlertCreate(BaseModel):
    """Wazuh アラート取り込み"""
    timestamp: str
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    rule_id: str
    rule_level: int = 5
    rule_description: str
    full_log: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class ThreatIntelCheck(BaseModel):
    """脅威インテリジェンス照合リクエスト"""
    ioc_type: str  # ip, domain, hash
    ioc_value: str


class ThreatIntelResult(BaseModel):
    """脅威インテリジェンス照合結果"""
    ioc_type: str
    ioc_value: str
    is_malicious: bool
    confidence: float
    sources: List[str] = []
    details: Optional[Dict[str, Any]] = None


class SOARExecuteRequest(BaseModel):
    """SOAR プレイブック実行リクエスト"""
    alert_id: str
    actions: List[str] = []


class ComplianceReport(BaseModel):
    """コンプライアンスレポート"""
    generated_at: datetime
    period_start: str
    period_end: str
    summary: Dict[str, Any]
    access_log_summary: Dict[str, Any]
    incident_summary: Dict[str, Any]
    security_events_summary: Dict[str, Any]
    recommendations: List[str] = []
