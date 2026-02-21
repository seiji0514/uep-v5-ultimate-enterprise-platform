"""
インシデント対応モジュール
"""
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class IncidentSeverity(str, Enum):
    """インシデント重大度"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, Enum):
    """インシデントステータス"""

    OPEN = "open"
    INVESTIGATING = "investigating"
    CONTAINED = "contained"
    RESOLVED = "resolved"
    CLOSED = "closed"


class Incident(BaseModel):
    """インシデント"""

    id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN
    affected_systems: List[str] = []
    assigned_to: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class IncidentResponse:
    """インシデント対応クラス"""

    def __init__(self):
        """インシデント対応を初期化"""
        self._incidents: Dict[str, Incident] = {}
        self._response_playbooks: Dict[str, Dict[str, Any]] = {}
        self._initialize_playbooks()

    def _initialize_playbooks(self):
        """レスポンスプレイブックを初期化"""
        self._response_playbooks = {
            "data_breach": {
                "steps": [
                    "1. 影響範囲の特定",
                    "2. データ漏洩の停止",
                    "3. 影響を受けたシステムの隔離",
                    "4. 関係者への通知",
                    "5. フォレンジック調査の実施",
                ]
            },
            "malware": {
                "steps": [
                    "1. 感染システムの特定",
                    "2. ネットワークからの隔離",
                    "3. マルウェアの除去",
                    "4. システムの復旧",
                    "5. 再発防止策の実施",
                ]
            },
            "intrusion": {
                "steps": [
                    "1. 侵入経路の特定",
                    "2. アクセスの遮断",
                    "3. 影響範囲の評価",
                    "4. システムのセキュア化",
                    "5. 監視の強化",
                ]
            },
        }

    def create_incident(
        self,
        title: str,
        description: str,
        severity: IncidentSeverity,
        affected_systems: Optional[List[str]] = None,
        incident_type: Optional[str] = None,
    ) -> Incident:
        """インシデントを作成"""
        incident_id = str(uuid.uuid4())

        incident = Incident(
            id=incident_id,
            title=title,
            description=description,
            severity=severity,
            affected_systems=affected_systems or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            metadata={"type": incident_type} if incident_type else None,
        )

        self._incidents[incident_id] = incident

        # 自動対応を実行（簡易実装）
        if incident_type and incident_type in self._response_playbooks:
            self._execute_automated_response(incident, incident_type)

        return incident

    def _execute_automated_response(self, incident: Incident, incident_type: str):
        """自動対応を実行"""
        playbook = self._response_playbooks.get(incident_type)
        if playbook:
            # 自動対応のロジック（簡易実装）
            incident.metadata = incident.metadata or {}
            incident.metadata["automated_response"] = {
                "playbook": incident_type,
                "steps": playbook["steps"],
                "executed_at": datetime.utcnow().isoformat(),
            }

    def update_incident(
        self,
        incident_id: str,
        status: Optional[IncidentStatus] = None,
        assigned_to: Optional[str] = None,
        resolution: Optional[str] = None,
    ) -> Optional[Incident]:
        """インシデントを更新"""
        incident = self._incidents.get(incident_id)
        if not incident:
            return None

        if status:
            incident.status = status
            if status == IncidentStatus.RESOLVED:
                incident.resolved_at = datetime.utcnow()

        if assigned_to:
            incident.assigned_to = assigned_to

        if resolution:
            incident.resolution = resolution

        incident.updated_at = datetime.utcnow()
        return incident

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        """インシデントを取得"""
        return self._incidents.get(incident_id)

    def list_incidents(
        self,
        severity: Optional[IncidentSeverity] = None,
        status: Optional[IncidentStatus] = None,
    ) -> List[Incident]:
        """インシデント一覧を取得"""
        incidents = list(self._incidents.values())

        if severity:
            incidents = [i for i in incidents if i.severity == severity]

        if status:
            incidents = [i for i in incidents if i.status == status]

        return sorted(incidents, key=lambda i: i.created_at, reverse=True)

    def get_response_playbook(self, incident_type: str) -> Optional[Dict[str, Any]]:
        """レスポンスプレイブックを取得"""
        return self._response_playbooks.get(incident_type)


# グローバルインスタンス
incident_response = IncidentResponse()
