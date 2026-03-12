#!/usr/bin/env python3
"""
医療系スタンドアロンシステム（UEP v5.0 から独立）
FHIR風API、AI診断サンプル、医療ダッシュボード
"""
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI(title="医療系スタンドアロンシステム", version="1.0.0")

# サンプルデータ（実患者データは使用しない）
AI_DIAGNOSIS = [
    {"id": "diag-001", "patient_id": "P001", "finding": "胸部X線異常所見", "confidence": 0.94, "status": "要確認"},
    {"id": "diag-002", "patient_id": "P002", "finding": "正常範囲", "confidence": 0.99, "status": "完了"},
    {"id": "diag-003", "patient_id": "P003", "finding": "眼底画像異常疑い", "confidence": 0.87, "status": "要精査"},
]

VITAL_SIGNS = [
    {"patient_id": "P001", "heart_rate": 72, "blood_pressure": "120/80", "spo2": 98, "timestamp": datetime.utcnow().isoformat()},
    {"patient_id": "P002", "heart_rate": 68, "blood_pressure": "118/76", "spo2": 99, "timestamp": datetime.utcnow().isoformat()},
]


@app.get("/")
async def root():
    return {"service": "医療系スタンドアロンシステム", "status": "ok", "version": "1.0.0"}


@app.get("/api/v1/ai-diagnosis")
async def get_ai_diagnosis() -> Dict[str, Any]:
    """AI診断一覧（サンプルデータ）"""
    return {"items": AI_DIAGNOSIS, "total": len(AI_DIAGNOSIS)}


@app.get("/api/v1/vital-signs")
async def get_vital_signs() -> Dict[str, Any]:
    """バイタルサイン一覧（サンプルデータ）"""
    return {"items": VITAL_SIGNS, "total": len(VITAL_SIGNS)}


@app.get("/api/v1/fhir/patient/{patient_id}")
async def get_fhir_patient(patient_id: str) -> Dict[str, Any]:
    """FHIR風 患者リソース（サンプル）"""
    return {
        "resourceType": "Patient",
        "id": patient_id,
        "identifier": [{"system": "urn:oid:1.2.392.200119.6.102.100", "value": patient_id}],
        "name": [{"family": "サンプル", "given": ["患者"]}],
        "gender": "unknown",
        "birthDate": "1980-01-01",
        "_note": "サンプルデータ（実患者データは使用していません）",
    }


@app.get("/api/v1/stats")
async def get_stats() -> Dict[str, Any]:
    """医療プラットフォーム統計"""
    return {
        "active_patients": 156,
        "ai_diagnosis_today": 42,
        "anomalies_detected_today": 5,
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """ダッシュボードHTML"""
    html = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>医療系スタンドアロン</title>
<style>body{font-family:sans-serif;margin:2rem;background:#f5f5f5;}
.card{background:#fff;padding:1rem;border-radius:8px;margin:1rem 0;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
h1{color:#1976d2;} .status{color:#4caf50;}</style></head>
<body>
<h1>医療系スタンドアロンシステム</h1>
<p class="status">UEP v5.0 から独立した個人プロジェクト</p>
<div class="card"><h3>API</h3>
<ul><li><a href="/api/v1/ai-diagnosis">/api/v1/ai-diagnosis</a></li>
<li><a href="/api/v1/vital-signs">/api/v1/vital-signs</a></li>
<li><a href="/api/v1/stats">/api/v1/stats</a></li></ul></div>
<div class="card"><p>※サンプルデータのみ使用。実患者データは使用していません。</p></div>
</body></html>
"""
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
