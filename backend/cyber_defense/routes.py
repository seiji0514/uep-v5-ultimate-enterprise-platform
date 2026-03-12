"""
サイバー対策 API エンドポイント
レベル4: IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .models import (
    SOARExecuteRequest,
    SuricataAlertCreate,
    ThreatIntelCheck,
    ThreatIntelResult,
    WazuhAlertCreate,
)
from .services import (
    check_threat_intel,
    generate_compliance_report,
    get_cyber_defense_overview,
    get_suricata_alerts,
    get_wazuh_alerts,
    ingest_suricata_alert,
    ingest_wazuh_alert,
)

router = APIRouter(tags=["サイバー対策"])
# prefix なし: security_center で prefix="/cyber" として include → /api/v1/security-center/cyber/*


@router.get("/overview")
@require_permission("read")
async def cyber_defense_overview(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """サイバー対策ダッシュボード概要"""
    return get_cyber_defense_overview()


# --- Suricata (IDS/IPS) ---
@router.get("/suricata/alerts", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_suricata_alerts(
    limit: int = Query(50, ge=1, le=200),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """Suricata アラート一覧"""
    return get_suricata_alerts(limit=limit)


@router.post("/suricata/alerts")
@require_permission("read")
async def create_suricata_alert(
    data: SuricataAlertCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """Suricata アラート取り込み（Webhook/Filebeat 等から）"""
    return ingest_suricata_alert(data.model_dump())


# --- Wazuh (EDR) ---
@router.get("/wazuh/alerts", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_wazuh_alerts(
    limit: int = Query(50, ge=1, le=200),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """Wazuh アラート一覧"""
    return get_wazuh_alerts(limit=limit)


@router.post("/wazuh/alerts")
@require_permission("read")
async def create_wazuh_alert(
    data: WazuhAlertCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """Wazuh アラート取り込み（Webhook 等から）"""
    return ingest_wazuh_alert(data.model_dump())


# --- 脅威インテリジェンス (MISP) ---
@router.post("/threat-intel/check", response_model=ThreatIntelResult)
@require_permission("read")
async def threat_intel_check(
    data: ThreatIntelCheck,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """IOC 照合（IP/ドメイン/ハッシュ）"""
    return check_threat_intel(data.ioc_type, data.ioc_value)


# --- SIEM 検索（簡易） ---
@router.get("/siem/search")
@require_permission("read")
async def siem_search(
    query: Optional[str] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ログ検索（OpenSearch 未連携時は内部イベントから検索）"""
    from security_center.monitoring import security_monitor

    events = security_monitor.get_events()
    results = [
        {
            "id": e.id,
            "event_type": e.event_type,
            "threat_level": e.threat_level.value,
            "source": e.source,
            "target": e.target,
            "description": e.description,
            "timestamp": e.timestamp.isoformat(),
        }
        for e in events
    ]
    if query:
        q = query.lower()
        results = [
            r
            for r in results
            if q in r.get("description", "").lower() or q in r.get("source", "").lower()
        ]
    if source:
        results = [r for r in results if r.get("source") == source]
    return {"results": results[:limit], "total": len(results)}


# --- SOAR 連携 ---
@router.get("/soar/playbooks")
@require_permission("read")
async def list_soar_playbooks(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """SOAR プレイブック一覧"""
    from cyber_defense.soar_integration import get_available_playbooks

    return {"playbooks": get_available_playbooks()}


@router.post("/soar/execute")
@require_permission("read")
async def execute_soar_playbook(
    data: SOARExecuteRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """SOAR プレイブック実行"""
    from cyber_defense.soar_integration import PlaybookAction, execute_playbook

    action_enums = [
        PlaybookAction(a)
        for a in data.actions
        if a in [e.value for e in PlaybookAction]
    ]
    return execute_playbook(data.alert_id, action_enums)


# --- コンプライアンスレポート ---
@router.get("/compliance/report", response_model=Dict[str, Any])
@require_permission("read")
async def compliance_report(
    period_days: int = Query(30, ge=1, le=365),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コンプライアンスレポート"""
    return generate_compliance_report(period_days=period_days)
