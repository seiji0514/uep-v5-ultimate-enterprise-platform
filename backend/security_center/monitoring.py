"""
セキュリティ監視モジュール
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ThreatLevel(str, Enum):
    """脅威レベル"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SecurityEvent(BaseModel):
    """セキュリティイベント"""

    id: str
    event_type: str  # intrusion, malware, data_breach, etc.
    threat_level: ThreatLevel
    source: str
    target: str
    description: str
    timestamp: datetime
    status: str = "open"  # open, investigating, resolved
    metadata: Optional[Dict[str, Any]] = None


class SecurityMonitor:
    """セキュリティ監視クラス"""

    def __init__(self):
        """セキュリティ監視器を初期化"""
        self._events: Dict[str, SecurityEvent] = {}
        self._alerts: List[Dict[str, Any]] = []

    def log_event(
        self,
        event_type: str,
        threat_level: ThreatLevel,
        source: str,
        target: str,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SecurityEvent:
        """セキュリティイベントを記録"""
        event_id = str(uuid.uuid4())

        event = SecurityEvent(
            id=event_id,
            event_type=event_type,
            threat_level=threat_level,
            source=source,
            target=target,
            description=description,
            timestamp=datetime.utcnow(),
            metadata=metadata,
        )

        self._events[event_id] = event

        # 高レベルの脅威の場合はアラートを生成
        if threat_level in [ThreatLevel.HIGH, ThreatLevel.CRITICAL]:
            self._create_alert(event)

        return event

    def _create_alert(self, event: SecurityEvent):
        """アラートを作成"""
        alert = {
            "id": str(uuid.uuid4()),
            "event_id": event.id,
            "threat_level": event.threat_level.value,
            "message": f"Security alert: {event.description}",
            "timestamp": event.timestamp.isoformat(),
            "acknowledged": False,
        }
        self._alerts.append(alert)

    def get_events(
        self,
        event_type: Optional[str] = None,
        threat_level: Optional[ThreatLevel] = None,
        status: Optional[str] = None,
    ) -> List[SecurityEvent]:
        """イベント一覧を取得"""
        events = list(self._events.values())

        if event_type:
            events = [e for e in events if e.event_type == event_type]

        if threat_level:
            events = [e for e in events if e.threat_level == threat_level]

        if status:
            events = [e for e in events if e.status == status]

        return sorted(events, key=lambda e: e.timestamp, reverse=True)

    def get_alerts(self, acknowledged: Optional[bool] = None) -> List[Dict[str, Any]]:
        """アラート一覧を取得"""
        alerts = self._alerts.copy()

        if acknowledged is not None:
            alerts = [a for a in alerts if a["acknowledged"] == acknowledged]

        return sorted(alerts, key=lambda a: a["timestamp"], reverse=True)

    def acknowledge_alert(self, alert_id: str) -> bool:
        """アラートを確認済みにする"""
        for alert in self._alerts:
            if alert["id"] == alert_id:
                alert["acknowledged"] = True
                return True
        return False


# グローバルインスタンス
security_monitor = SecurityMonitor()
