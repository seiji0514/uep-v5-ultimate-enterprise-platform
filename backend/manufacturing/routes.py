"""
製造・IoT APIエンドポイント
予知保全API、センサーデータ取得、異常検知
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/manufacturing", tags=["製造・IoT"])


# デモ用サンプルデータ
def _predictive_maintenance_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "pm-001",
            "equipment": "CNC設備A",
            "predicted_failure": "2026-03-15",
            "confidence": 0.52,
            "status": "要メンテナンス",
            "line": "ライン1",
        },
        {
            "id": "pm-002",
            "equipment": "溶接ロボットB",
            "predicted_failure": "2026-04-02",
            "confidence": 0.78,
            "status": "監視中",
            "line": "ライン1",
        },
        {
            "id": "pm-003",
            "equipment": "プレス機C",
            "predicted_failure": "2026-05-10",
            "confidence": 0.65,
            "status": "正常",
            "line": "ライン2",
        },
        {
            "id": "pm-004",
            "equipment": "搬送ロボットD",
            "predicted_failure": "2026-03-28",
            "confidence": 0.88,
            "status": "要メンテナンス",
            "line": "ライン2",
        },
        {
            "id": "pm-005",
            "equipment": "組立ロボットE",
            "predicted_failure": "2026-06-01",
            "confidence": 0.72,
            "status": "監視中",
            "line": "ライン3",
        },
        {
            "id": "pm-006",
            "equipment": "検査装置F",
            "predicted_failure": "2026-04-15",
            "confidence": 0.67,
            "status": "監視中",
            "line": "ライン3",
        },
    ]


def _sensor_data_list() -> List[Dict[str, Any]]:
    return [
        {
            "sensor_id": "temp-001",
            "value": 72.5,
            "unit": "°C",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
            "equipment": "CNC設備A",
        },
        {
            "sensor_id": "vibration-002",
            "value": 0.12,
            "unit": "mm/s",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=2)).isoformat(),
            "equipment": "溶接ロボットB",
        },
        {
            "sensor_id": "pressure-003",
            "value": 5.2,
            "unit": "MPa",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
            "equipment": "プレス機C",
        },
        {
            "sensor_id": "temp-004",
            "value": 68.2,
            "unit": "°C",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=3)).isoformat(),
            "equipment": "搬送ロボットD",
        },
        {
            "sensor_id": "current-005",
            "value": 12.8,
            "unit": "A",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
            "equipment": "組立ロボットE",
        },
        {
            "sensor_id": "humidity-006",
            "value": 45.0,
            "unit": "%",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
            "equipment": "検査装置F",
        },
    ]


def _anomaly_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ano-001",
            "type": "振動異常",
            "equipment": "CNC設備A",
            "severity": "高",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        },
        {
            "id": "ano-002",
            "type": "温度上昇",
            "equipment": "溶接ロボットB",
            "severity": "中",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
        },
        {
            "id": "ano-003",
            "type": "圧力変動",
            "equipment": "プレス機C",
            "severity": "低",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=8)).isoformat(),
        },
        {
            "id": "ano-004",
            "type": "搬送異常",
            "equipment": "搬送ロボットD",
            "severity": "中",
            "detected_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        },
        {
            "id": "ano-005",
            "type": "電流異常",
            "equipment": "組立ロボットE",
            "severity": "高",
            "detected_at": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
        },
    ]


@router.get("/predictive-maintenance")
async def get_predictive_maintenance(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """予知保全一覧を取得"""
    return {
        "items": _predictive_maintenance_list(),
        "total": len(_predictive_maintenance_list()),
    }


@router.get("/sensor-data")
async def get_sensor_data(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """センサーデータを取得"""
    return {"items": _sensor_data_list(), "total": len(_sensor_data_list())}


@router.get("/opcua/read/{node_id:path}")
async def opcua_read_node(
    node_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """OPC-UA ノード読み取り"""
    from manufacturing.opcua_client import opcua_client

    result = opcua_client.read_node(node_id)
    return result or {"error": "Node not found"}


@router.get("/opcua/browse")
async def opcua_browse(
    node_id: str = "i=84",
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """OPC-UA ノードブラウズ"""
    from manufacturing.opcua_client import opcua_client

    return {"items": opcua_client.browse_nodes(node_id)}


@router.get("/anomalies")
async def get_anomalies(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """異常検知一覧を取得"""
    return {"items": _anomaly_list(), "total": len(_anomaly_list())}
