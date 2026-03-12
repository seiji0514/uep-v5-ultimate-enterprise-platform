"""
サイバー対策 サービス層
Suricata, Wazuh, MISP 連携（外部サービス未起動時はメモリ内で動作）
"""
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from security_center.monitoring import SecurityEvent, ThreatLevel, security_monitor

# メモリ内ストア（外部サービス未連携時のフォールバック）
_suricata_alerts: Dict[str, Dict[str, Any]] = {}
_wazuh_alerts: Dict[str, Dict[str, Any]] = {}
_audit_logs: List[Dict[str, Any]] = []


# デモ用初期データ
def _init_demo_data():
    """デモ用サンプルデータ"""
    global _suricata_alerts, _wazuh_alerts
    if _suricata_alerts:
        return
    # Suricata デモアラート
    for i, (rid, msg, sev) in enumerate(
        [
            ("2000001", "ET SCAN Potential SSH Scan", "high"),
            ("2000002", "ET MALWARE Possible C&C Beacon", "critical"),
            ("2000003", "ET SCAN Nmap Scan Detection", "medium"),
        ]
    ):
        aid = str(uuid.uuid4())
        _suricata_alerts[aid] = {
            "id": aid,
            "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
            "src_ip": "192.168.1.100",
            "dest_ip": "10.0.0.1",
            "rule_id": rid,
            "rule_msg": msg,
            "severity": sev,
            "source": "suricata",
        }
    # Wazuh デモアラート
    for i, (rid, desc, lvl) in enumerate(
        [
            ("100002", "File integrity monitoring: File changed", 7),
            ("100003", "Rootcheck: Rootkit detected", 12),
            ("100004", "Authentication failure", 5),
        ]
    ):
        aid = str(uuid.uuid4())
        _wazuh_alerts[aid] = {
            "id": aid,
            "timestamp": (datetime.utcnow() - timedelta(hours=i)).isoformat(),
            "agent_id": "001",
            "rule_id": rid,
            "rule_description": desc,
            "rule_level": lvl,
            "source": "wazuh",
        }


def ingest_suricata_alert(data: Dict[str, Any]) -> Dict[str, Any]:
    """Suricata アラートを取り込み、Security Center に連携"""
    _init_demo_data()
    alert_id = str(uuid.uuid4())
    sev_map = {
        "low": ThreatLevel.LOW,
        "medium": ThreatLevel.MEDIUM,
        "high": ThreatLevel.HIGH,
        "critical": ThreatLevel.CRITICAL,
    }
    threat = sev_map.get(data.get("severity", "medium").lower(), ThreatLevel.MEDIUM)
    # Security Center にイベント登録
    security_monitor.log_event(
        event_type="ids_alert",
        threat_level=threat,
        source=data.get("src_ip", "unknown"),
        target=data.get("dest_ip", "unknown"),
        description=data.get("rule_msg", "Suricata alert"),
        metadata={"rule_id": data.get("rule_id"), "source": "suricata"},
    )
    alert = {
        "id": alert_id,
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
        "src_ip": data.get("src_ip", ""),
        "dest_ip": data.get("dest_ip", ""),
        "rule_id": data.get("rule_id", ""),
        "rule_msg": data.get("rule_msg", ""),
        "severity": data.get("severity", "medium"),
        "source": "suricata",
    }
    _suricata_alerts[alert_id] = alert
    return alert


def ingest_wazuh_alert(data: Dict[str, Any]) -> Dict[str, Any]:
    """Wazuh アラートを取り込み、Security Center に連携"""
    _init_demo_data()
    alert_id = str(uuid.uuid4())
    lvl = data.get("rule_level", 5)
    threat = (
        ThreatLevel.CRITICAL
        if lvl >= 12
        else (ThreatLevel.HIGH if lvl >= 8 else ThreatLevel.MEDIUM)
    )
    security_monitor.log_event(
        event_type="edr_alert",
        threat_level=threat,
        source=data.get("agent_name", data.get("agent_id", "unknown")),
        target="endpoint",
        description=data.get("rule_description", "Wazuh alert"),
        metadata={"rule_id": data.get("rule_id"), "source": "wazuh"},
    )
    alert = {
        "id": alert_id,
        "timestamp": data.get("timestamp", datetime.utcnow().isoformat()),
        "agent_id": data.get("agent_id"),
        "agent_name": data.get("agent_name"),
        "rule_id": data.get("rule_id", ""),
        "rule_description": data.get("rule_description", ""),
        "rule_level": lvl,
        "source": "wazuh",
    }
    _wazuh_alerts[alert_id] = alert
    return alert


def get_suricata_alerts(limit: int = 50) -> List[Dict[str, Any]]:
    """Suricata アラート一覧"""
    _init_demo_data()
    items = sorted(
        _suricata_alerts.values(), key=lambda x: x.get("timestamp", ""), reverse=True
    )
    return items[:limit]


def get_wazuh_alerts(limit: int = 50) -> List[Dict[str, Any]]:
    """Wazuh アラート一覧"""
    _init_demo_data()
    items = sorted(
        _wazuh_alerts.values(), key=lambda x: x.get("timestamp", ""), reverse=True
    )
    return items[:limit]


def check_threat_intel(ioc_type: str, ioc_value: str) -> Dict[str, Any]:
    """脅威インテリジェンス照合（MISP 未連携時はデモ用ルールベース）"""
    # デモ用: 既知の悪意IP/ドメインの簡易チェック
    malicious_ips = {"192.168.1.100", "10.0.0.99"}
    malicious_domains = {"malware.example.com", "c2.evil.org"}
    malicious_hashes = {
        "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    }
    if ioc_type == "ip":
        is_mal = ioc_value in malicious_ips
    elif ioc_type == "domain":
        is_mal = any(d in ioc_value.lower() for d in malicious_domains)
    elif ioc_type == "hash":
        is_mal = ioc_value.lower() in malicious_hashes
    else:
        is_mal = False
    return {
        "ioc_type": ioc_type,
        "ioc_value": ioc_value,
        "is_malicious": is_mal,
        "confidence": 0.85 if is_mal else 0.0,
        "sources": ["misp" if is_mal else "internal"],
        "details": {"source": "demo" if not is_mal else "threat_intel"},
    }


def generate_compliance_report(period_days: int = 30) -> Dict[str, Any]:
    """コンプライアンスレポート生成"""
    now = datetime.utcnow()
    start = now - timedelta(days=period_days)
    events = security_monitor.get_events()
    incidents = []  # incident_response から取得可能だが簡略化
    critical = sum(1 for e in events if e.threat_level == ThreatLevel.CRITICAL)
    high = sum(1 for e in events if e.threat_level == ThreatLevel.HIGH)
    return {
        "generated_at": now.isoformat(),
        "period_start": start.isoformat(),
        "period_end": now.isoformat(),
        "summary": {
            "total_events": len(events),
            "critical_count": critical,
            "high_count": high,
            "incidents_count": len(incidents),
        },
        "access_log_summary": {"total_requests": 0, "failed_auth": 0},
        "incident_summary": {"total": len(incidents), "resolved": 0},
        "security_events_summary": {
            "total": len(events),
            "critical": critical,
            "high": high,
        },
        "recommendations": [
            "定期的な脆弱性スキャン実施",
            "ログ保持期間の見直し",
            "インシデント対応手順の整備",
        ],
    }


def get_cyber_defense_overview() -> Dict[str, Any]:
    """サイバー対策ダッシュボード概要"""
    _init_demo_data()
    sur_alerts = get_suricata_alerts(limit=10)
    waz_alerts = get_wazuh_alerts(limit=10)
    events = security_monitor.get_events()
    critical = sum(1 for e in events if e.threat_level == ThreatLevel.CRITICAL)
    high = sum(1 for e in events if e.threat_level == ThreatLevel.HIGH)
    return {
        "suricata": {"alerts_count": len(_suricata_alerts), "recent": sur_alerts[:5]},
        "wazuh": {"alerts_count": len(_wazuh_alerts), "recent": waz_alerts[:5]},
        "security_events": {"total": len(events), "critical": critical, "high": high},
        "threat_intel": {"status": "available"},
        "compliance": {"status": "available"},
    }
