"""
統合セキュリティダッシュボードモジュール
"""
from typing import Dict, Any
from datetime import datetime, timedelta
from security_center.monitoring import security_monitor
from security_center.incident_response import incident_response
from security_center.risk_analysis import risk_analyzer


class SecurityDashboard:
    """統合セキュリティダッシュボードクラス"""

    def get_dashboard_data(self) -> Dict[str, Any]:
        """セキュリティダッシュボードデータを取得"""
        # 最近24時間のイベント
        events = security_monitor.get_events()
        recent_events = [e for e in events if len(events) <= 10]

        # アクティブなインシデント
        active_incidents = incident_response.list_incidents(status="open")

        # リスク分析
        risk_posture = risk_analyzer.analyze_security_posture()

        # アラート
        alerts = security_monitor.get_alerts(acknowledged=False)

        return {
            "security_posture": risk_posture,
            "active_incidents": len(active_incidents),
            "unacknowledged_alerts": len(alerts),
            "recent_events": [
                {
                    "id": e.id,
                    "type": e.event_type,
                    "threat_level": e.threat_level.value,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in recent_events
            ],
            "top_risks": [
                {
                    "name": r.name,
                    "level": r.risk_level.value,
                    "score": r.likelihood * r.impact
                }
                for r in risk_analyzer.list_risks()[:5]
            ],
            "incident_summary": {
                "open": len([i for i in active_incidents if i.status.value == "open"]),
                "investigating": len([i for i in active_incidents if i.status.value == "investigating"]),
                "resolved_today": 0
            }
        }


# グローバルインスタンス
security_dashboard = SecurityDashboard()
