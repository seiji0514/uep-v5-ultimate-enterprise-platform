#!/usr/bin/env python3
"""
航空系スタンドアロンシステム（UEP v5.0 から独立）
フライトデータ分析、運航スケジュール可視化、空港混雑予測
"""
from datetime import datetime
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="航空系スタンドアロンシステム", version="1.0.0")

# サンプルデータ（公開データ・ダミーデータ）
FLIGHTS = [
    {"flight_id": "JL001", "route": "NRT-LAX", "departure": "09:00", "arrival": "04:00", "status": "定刻", "aircraft": "B777"},
    {"flight_id": "NH002", "route": "HND-SFO", "departure": "10:30", "arrival": "05:30", "status": "定刻", "aircraft": "B787"},
    {"flight_id": "JL003", "route": "NRT-SIN", "departure": "14:00", "arrival": "20:00", "status": "15分遅延", "aircraft": "B737"},
]

AIRPORT_STATS = [
    {"airport": "NRT", "departures_today": 156, "arrivals_today": 148, "congestion": "中", "weather": "晴れ"},
    {"airport": "HND", "departures_today": 412, "arrivals_today": 398, "congestion": "高", "weather": "晴れ"},
]


@app.get("/")
async def root():
    return {"service": "航空系スタンドアロンシステム", "status": "ok", "version": "1.0.0"}


@app.get("/api/v1/flights")
async def get_flights() -> Dict[str, Any]:
    """フライト一覧（サンプル）"""
    return {"items": FLIGHTS, "total": len(FLIGHTS)}


@app.get("/api/v1/airports")
async def get_airports() -> Dict[str, Any]:
    """空港統計（サンプル）"""
    return {"items": AIRPORT_STATS, "total": len(AIRPORT_STATS)}


@app.get("/api/v1/delays")
async def get_delays() -> Dict[str, Any]:
    """遅延分析（サンプル）"""
    return {
        "on_time_rate": 0.92,
        "avg_delay_minutes": 8,
        "delayed_flights_today": 12,
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/stats")
async def get_stats() -> Dict[str, Any]:
    """運航統計"""
    return {
        "total_flights_today": 568,
        "on_time_rate": 0.92,
        "active_airports": 4,
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    """ダッシュボードHTML"""
    html = """
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>航空系スタンドアロン</title>
<style>body{font-family:sans-serif;margin:2rem;background:#e3f2fd;}
.card{background:#fff;padding:1rem;border-radius:8px;margin:1rem 0;box-shadow:0 2px 4px rgba(0,0,0,0.1);}
h1{color:#0d47a1;} .status{color:#1976d2;}</style></head>
<body>
<h1>航空系スタンドアロンシステム</h1>
<p class="status">UEP v5.0 から独立した個人プロジェクト</p>
<div class="card"><h3>API</h3>
<ul><li><a href="/api/v1/flights">/api/v1/flights</a> フライト一覧</li>
<li><a href="/api/v1/airports">/api/v1/airports</a> 空港統計</li>
<li><a href="/api/v1/delays">/api/v1/delays</a> 遅延分析</li>
<li><a href="/api/v1/stats">/api/v1/stats</a> 運航統計</li></ul></div>
<div class="card"><p>※サンプルデータ。地上系・データ分析・可視化用途。</p></div>
</body></html>
"""
    return html


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
