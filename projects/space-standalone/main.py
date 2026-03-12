#!/usr/bin/env python3
"""
宇宙系スタンドアロンシステム（UEP v5.0 から独立）
衛星データ可視化、軌道情報、NASA API連携
"""
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="宇宙系スタンドアロンシステム", version="1.0.0")

# サンプルデータ（公開データ・ダミー）
SATELLITES = [
    {"id": "ISS", "name": "国際宇宙ステーション", "orbit_km": 408, "inclination": 51.6, "period_min": 92.9, "status": "運用中"},
    {"id": "HUBBLE", "name": "ハッブル宇宙望遠鏡", "orbit_km": 547, "inclination": 28.5, "period_min": 96.0, "status": "運用中"},
    {"id": "STARLINK-001", "name": "Starlink", "orbit_km": 550, "inclination": 53.0, "period_min": 96.5, "status": "運用中"},
]

LAUNCHES = [
    {"id": "L001", "mission": "ISS補給", "date": "2026-03-15", "vehicle": "Falcon 9", "status": "予定"},
    {"id": "L002", "mission": "衛星打ち上げ", "date": "2026-03-20", "vehicle": "H-IIA", "status": "予定"},
]


@app.get("/")
async def root():
    return {"service": "宇宙系スタンドアロンシステム", "status": "ok", "version": "1.0.0"}


@app.get("/api/v1/satellites")
async def get_satellites() -> Dict[str, Any]:
    """衛星一覧（サンプル）"""
    return {"items": SATELLITES, "total": len(SATELLITES)}


@app.get("/api/v1/satellites/{satellite_id}")
async def get_satellite(satellite_id: str) -> Dict[str, Any]:
    """衛星詳細"""
    for s in SATELLITES:
        if s["id"] == satellite_id:
            return s
    return {"error": "Not found"}


@app.get("/api/v1/launches")
async def get_launches() -> Dict[str, Any]:
    """打ち上げ予定（サンプル）"""
    return {"items": LAUNCHES, "total": len(LAUNCHES)}


@app.get("/api/v1/apod")
async def get_apod() -> Dict[str, Any]:
    """NASA APOD風（サンプル・実際のAPI連携は要APIキー）"""
    return {
        "title": "Earth from ISS",
        "explanation": "サンプルデータ。実際のNASA APOD API連携にはAPIキーが必要です。",
        "url": "https://api.nasa.gov/planetary/apod",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
    }


@app.get("/api/v1/stats")
async def get_stats() -> Dict[str, Any]:
    """宇宙ミッション統計"""
    return {
        "tracked_satellites": len(SATELLITES),
        "upcoming_launches": len(LAUNCHES),
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """ダッシュボードHTML"""
    html = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>宇宙系スタンドアロン</title>
<style>body{font-family:sans-serif;margin:2rem;background:#0d1117;color:#c9d1d9;}
.card{background:#161b22;padding:1rem;border-radius:8px;margin:1rem 0;border:1px solid #30363d;}
h1{color:#58a6ff;} a{color:#58a6ff;} .status{color:#7ee787;}</style></head>
<body>
<h1>宇宙系スタンドアロンシステム</h1>
<p class="status">UEP v5.0 から独立した個人プロジェクト</p>
<div class="card"><h3>API</h3>
<ul><li><a href="/api/v1/satellites">/api/v1/satellites</a> 衛星一覧</li>
<li><a href="/api/v1/launches">/api/v1/launches</a> 打ち上げ予定</li>
<li><a href="/api/v1/apod">/api/v1/apod</a> NASA APOD風</li>
<li><a href="/api/v1/stats">/api/v1/stats</a> 統計</li></ul></div>
<div class="card"><p>※サンプルデータ。衛星データ可視化・分析用途。NASA API連携は要APIキー。</p></div>
</body></html>
"""
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
