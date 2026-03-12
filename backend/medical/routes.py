"""
医療 APIエンドポイント
AI診断、音声応答、異常検知、医療プラットフォーム
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/medical", tags=["医療"])


def _ai_diagnosis_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "diag-001",
            "patient_id": "P001",
            "finding": "胸部X線異常所見",
            "confidence": 0.94,
            "status": "要確認",
            "modality": "X線",
        },
        {
            "id": "diag-002",
            "patient_id": "P002",
            "finding": "正常範囲",
            "confidence": 0.99,
            "status": "完了",
            "modality": "CT",
        },
        {
            "id": "diag-003",
            "patient_id": "P003",
            "finding": "眼底画像異常疑い",
            "confidence": 0.87,
            "status": "要精査",
            "modality": "眼底",
        },
        {
            "id": "diag-004",
            "patient_id": "P004",
            "finding": "MRI脳血管異常なし",
            "confidence": 0.96,
            "status": "完了",
            "modality": "MRI",
        },
        {
            "id": "diag-005",
            "patient_id": "P005",
            "finding": "皮膚病変要確認",
            "confidence": 0.82,
            "status": "要確認",
            "modality": "皮膚",
        },
        {
            "id": "diag-006",
            "patient_id": "P006",
            "finding": "心電図異常所見",
            "confidence": 0.91,
            "status": "要精査",
            "modality": "心電図",
        },
    ]


def _voice_response_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "vr-001",
            "type": "問診音声",
            "duration_sec": 45,
            "transcription": "頭痛が3日続いています",
            "status": "処理完了",
        },
        {
            "id": "vr-002",
            "type": "ナースコール",
            "duration_sec": 12,
            "transcription": "トイレに付き添いをお願いします",
            "status": "対応済み",
        },
        {
            "id": "vr-003",
            "type": "医師指示",
            "duration_sec": 90,
            "transcription": "投薬変更の指示を記録",
            "status": "処理中",
        },
        {
            "id": "vr-004",
            "type": "問診音声",
            "duration_sec": 60,
            "transcription": "めまいと吐き気があります",
            "status": "処理完了",
        },
        {
            "id": "vr-005",
            "type": "ナースコール",
            "duration_sec": 8,
            "transcription": "点滴の交換をお願いします",
            "status": "対応済み",
        },
        {
            "id": "vr-006",
            "type": "医師指示",
            "duration_sec": 120,
            "transcription": "検査オーダー登録",
            "status": "処理完了",
        },
    ]


def _anomaly_detection_list() -> List[Dict[str, Any]]:
    return [
        {
            "id": "ma-001",
            "type": "バイタル異常",
            "patient_id": "P001",
            "metric": "心拍数",
            "value": 125,
            "threshold": 100,
            "severity": "高",
        },
        {
            "id": "ma-002",
            "type": "検査値異常",
            "patient_id": "P002",
            "metric": "血糖値",
            "value": 280,
            "threshold": 200,
            "severity": "中",
        },
        {
            "id": "ma-003",
            "type": "バイタル異常",
            "patient_id": "P003",
            "metric": "血圧",
            "value": 185,
            "threshold": 140,
            "severity": "高",
        },
        {
            "id": "ma-004",
            "type": "検査値異常",
            "patient_id": "P004",
            "metric": "CRP",
            "value": 12.5,
            "threshold": 1.0,
            "severity": "中",
        },
        {
            "id": "ma-005",
            "type": "バイタル異常",
            "patient_id": "P005",
            "metric": "SpO2",
            "value": 88,
            "threshold": 92,
            "severity": "高",
        },
        {
            "id": "ma-006",
            "type": "検査値異常",
            "patient_id": "P006",
            "metric": "肝機能",
            "value": 180,
            "threshold": 40,
            "severity": "中",
        },
    ]


def _platform_stats() -> Dict[str, Any]:
    return {
        "active_patients": 156,
        "ai_diagnosis_today": 42,
        "voice_processed_today": 89,
        "anomalies_detected_today": 5,
        "last_updated": datetime.utcnow().isoformat(),
    }


@router.get("/ai-diagnosis")
async def get_ai_diagnosis(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """AI診断一覧を取得"""
    return {"items": _ai_diagnosis_list(), "total": len(_ai_diagnosis_list())}


@router.get("/voice-response")
async def get_voice_response(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """音声応答一覧を取得"""
    return {"items": _voice_response_list(), "total": len(_voice_response_list())}


@router.get("/anomaly-detection")
async def get_anomaly_detection(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """医療異常検知一覧を取得"""
    return {"items": _anomaly_detection_list(), "total": len(_anomaly_detection_list())}


@router.get("/fhir/patient/{patient_id}")
async def get_fhir_patient(
    patient_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """FHIR 患者リソース取得"""
    from medical.fhir_client import fhir_client

    result = fhir_client.get_patient(patient_id)
    return result or {"error": "Patient not found"}


@router.get("/fhir/observations/{patient_id}")
async def get_fhir_observations(
    patient_id: str,
    code: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """FHIR Observation 検索"""
    from medical.fhir_client import fhir_client

    return {"items": fhir_client.search_observations(patient_id, code)}


@router.get("/platform-stats")
async def get_platform_stats(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """医療プラットフォーム統計を取得"""
    return _platform_stats()
