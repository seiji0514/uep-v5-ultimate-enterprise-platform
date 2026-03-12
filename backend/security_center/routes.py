"""
統合セキュリティ・防衛プラットフォーム API
セキュリティコマンドセンター + サイバー対策（IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス）
補強スキル: eBPF（Falco Webhook連携）
"""
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Request, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .incident_response import (
    Incident,
    IncidentSeverity,
    IncidentStatus,
    incident_response,
)
from .models import IncidentCreate, IncidentUpdate, RiskCreate, SecurityEventCreate
from .monitoring import SecurityEvent, ThreatLevel, security_monitor
from .risk_analysis import Risk, RiskLevel, risk_analyzer

router = APIRouter(prefix="/api/v1/security-defense-platform", tags=["統合セキュリティ・防衛プラットフォーム"])

# サイバー対策（IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス）を統合
from cyber_defense.routes import router as cyber_defense_router

router.include_router(cyber_defense_router, prefix="/cyber")


@router.get("/events", response_model=List[SecurityEvent])
@require_permission("read")
async def list_security_events(
    event_type: Optional[str] = None,
    threat_level: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """セキュリティイベント一覧を取得"""
    threat_level_enum = ThreatLevel(threat_level) if threat_level else None
    events = security_monitor.get_events(
        event_type=event_type, threat_level=threat_level_enum, status=status
    )
    return events


@router.post(
    "/events", response_model=SecurityEvent, status_code=status.HTTP_201_CREATED
)
@require_permission("read")
async def create_security_event(
    event_data: SecurityEventCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """セキュリティイベントを作成"""
    threat_level = ThreatLevel(event_data.threat_level)
    event = security_monitor.log_event(
        event_type=event_data.event_type,
        threat_level=threat_level,
        source=event_data.source,
        target=event_data.target,
        description=event_data.description,
        metadata=event_data.metadata,
    )
    return event


@router.get("/alerts")
@require_permission("read")
async def list_alerts(
    acknowledged: Optional[bool] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """アラート一覧を取得"""
    alerts = security_monitor.get_alerts(acknowledged=acknowledged)
    return {"alerts": alerts, "count": len(alerts)}


@router.post("/alerts/{alert_id}/acknowledge")
@require_permission("read")
async def acknowledge_alert(
    alert_id: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """アラートを確認済みにする"""
    success = security_monitor.acknowledge_alert(alert_id)
    if success:
        return {"message": "Alert acknowledged"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found"
        )


@router.get("/incidents", response_model=List[Incident])
@require_permission("read")
async def list_incidents(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """インシデント一覧を取得"""
    severity_enum = IncidentSeverity(severity) if severity else None
    status_enum = IncidentStatus(status) if status else None
    incidents = incident_response.list_incidents(
        severity=severity_enum, status=status_enum
    )
    return incidents


@router.post("/incidents", response_model=Incident, status_code=status.HTTP_201_CREATED)
@require_permission("read")
async def create_incident(
    incident_data: IncidentCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """インシデントを作成"""
    severity = IncidentSeverity(incident_data.severity)
    incident = incident_response.create_incident(
        title=incident_data.title,
        description=incident_data.description,
        severity=severity,
        affected_systems=incident_data.affected_systems,
        incident_type=incident_data.incident_type,
    )
    return incident


@router.put("/incidents/{incident_id}", response_model=Incident)
@require_permission("read")
async def update_incident(
    incident_id: str,
    incident_data: IncidentUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """インシデントを更新"""
    status_enum = IncidentStatus(incident_data.status) if incident_data.status else None
    incident = incident_response.update_incident(
        incident_id=incident_id,
        status=status_enum,
        assigned_to=incident_data.assigned_to,
        resolution=incident_data.resolution,
    )

    if not incident:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found"
        )

    return incident


@router.get("/risks", response_model=List[Risk])
@require_permission("read")
async def list_risks(
    category: Optional[str] = None,
    risk_level: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """リスク一覧を取得"""
    risk_level_enum = RiskLevel(risk_level) if risk_level else None
    risks = risk_analyzer.list_risks(category=category, risk_level=risk_level_enum)
    return risks


@router.post("/risks", response_model=Risk, status_code=status.HTTP_201_CREATED)
@require_permission("read")
async def register_risk(
    risk_data: RiskCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """リスクを登録"""
    risk = risk_analyzer.register_risk(
        name=risk_data.name,
        description=risk_data.description,
        category=risk_data.category,
        likelihood=risk_data.likelihood,
        impact=risk_data.impact,
        mitigation=risk_data.mitigation,
    )
    return risk


@router.get("/security-posture")
@require_permission("read")
async def get_security_posture(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """セキュリティ態勢を取得"""
    posture = risk_analyzer.analyze_security_posture()
    return posture


# Falco Webhook（認証不要・内部ネットワーク用）
@router.post("/falco/alerts", status_code=status.HTTP_202_ACCEPTED)
async def falco_webhook(
    request: Request,
    x_falco_signature: Optional[str] = Header(None),
):
    """Falco eBPF アラート受信（Webhook連携）"""
    body = await request.json()
    # Falco 出力形式: { "output": "...", "priority": "...", "rule": "...", ... }
    output = body.get("output", "")
    priority = body.get("priority", "WARNING")
    rule = body.get("rule", "unknown")
    # セキュリティモニターに登録
    threat_map = {"Critical": "critical", "Error": "high", "Warning": "medium"}
    threat_level = threat_map.get(priority, "medium")
    security_monitor.log_event(
        event_type=f"falco:{rule}",
        threat_level=ThreatLevel(threat_level),
        source="falco",
        target="uep-runtime",
        description=output,
        metadata={"raw": body},
    )
    return {"received": True, "rule": rule}
