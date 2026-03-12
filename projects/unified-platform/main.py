#!/usr/bin/env python3
"""
Unified Platform: Medical + Aviation + Space
Phase 1-5: DB, Docker, Redis, Auth, Audit, K8s, CI/CD, Tracing, Compliance
"""
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Depends, Request, Form, Body, UploadFile, File, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

from config import get_config
from database import get_db, init_db, check_db_health
from models import User, Patient, AIDiagnosis, VitalSign, Flight, Airport, Satellite, Launch, AuditLog, Notification
from services.auth import get_current_user, require_auth, create_access_token, verify_password, hash_password
from services.audit import write_audit
from services.redis_client import cache_get, cache_set, login_attempt_incr, login_attempt_reset, is_login_locked, notification_mark_read, notification_read_ids

# Phase 5: Prometheus metrics (status_code for alerting)
REQUEST_COUNT = Counter("unified_http_requests_total", "Total requests", ["method", "status_code"])
REQUEST_LATENCY = Histogram("unified_http_request_duration_seconds", "Request latency")

# WebSocket: 接続管理・リアルタイム配信
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, data: dict):
        import json
        msg = json.dumps(data)
        for conn in list(self.active_connections):
            try:
                await conn.send_text(msg)
            except Exception:
                self.disconnect(conn)

ws_manager = ConnectionManager()


def setup_tracing():
    """Phase 5: OpenTelemetry"""
    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
        cfg = get_config()
        if cfg.get("otlp_endpoint"):
            provider = TracerProvider()
            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=cfg["otlp_endpoint"])))
            trace.set_tracer_provider(provider)
            FastAPIInstrumentor.instrument_app(app)
    except Exception:
        pass


def _run_seed():
    from seed_data import seed
    seed(force=False)
    # ERP・DXサンプルデータ
    try:
        _erp_seed_sample_data()
    except Exception:
        pass
    try:
        _dx_seed_sample_data()
    except Exception:
        pass
    try:
        _legacy_seed_sample_jobs()
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    import logging
    _setup_logging()
    await init_db()
    try:
        await asyncio.to_thread(_run_seed)
        logging.getLogger("uvicorn").info("Seed completed")
    except Exception as e:
        logging.getLogger("uvicorn").error(f"Seed failed: {e}")
    # WebSocket ブロードキャストループ開始
    _ws_task = asyncio.create_task(_ws_broadcast_loop())
    yield
    _ws_task.cancel()
    try:
        await _ws_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="統合基盤プラットフォーム",
    version="5.0.0",
    lifespan=lifespan,
)

# CORS: Vite dev (5173-5175) や 8000/8001/8080、WSL IP (172.x) からのアクセスを許可
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://127.0.0.1:5173",
        "http://localhost:5174", "http://127.0.0.1:5174",
        "http://localhost:5175", "http://127.0.0.1:5175",
        "http://localhost:8000", "http://127.0.0.1:8000",
        "http://localhost:8001", "http://127.0.0.1:8001",
        "http://localhost:8080", "http://127.0.0.1:8080",
        "http://localhost:50000", "http://127.0.0.1:50000",
        "http://172.19.0.1:8000", "http://172.19.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# React frontend (if built)
_frontend_dist = os.path.join(os.path.dirname(__file__), "frontend_dist")
if os.path.isdir(_frontend_dist):
    _assets = os.path.join(_frontend_dist, "assets")
    if os.path.isdir(_assets):
        app.mount("/assets", StaticFiles(directory=_assets), name="assets")


import logging
import json
import uuid
from collections import deque

_logger = logging.getLogger(__name__)

# ログビューア用: 直近500行をメモリに保持
_LOG_BUFFER: deque = deque(maxlen=500)


class BufferHandler(logging.Handler):
    def emit(self, record):
        try:
            _LOG_BUFFER.append({
                "ts": datetime.utcnow().strftime("%H:%M:%S"),
                "level": record.levelname,
                "msg": record.getMessage(),
            })
        except Exception:
            pass


def _setup_logging():
    """ログレベル設定（LOG_LEVEL 環境変数）"""
    cfg = get_config()
    level = getattr(logging, cfg.get("log_level", "INFO"), logging.INFO)
    logging.basicConfig(level=level)
    buf = BufferHandler()
    logging.getLogger().addHandler(buf)
    for name in ["uvicorn", "uvicorn.error"]:
        logging.getLogger(name).setLevel(level)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]
    with REQUEST_LATENCY.time():
        response = await call_next(request)
    REQUEST_COUNT.labels(method=request.method, status_code=str(response.status_code)).inc()
    # 構造化ログ（JSON形式、request_id付与）
    log_obj = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": response.status_code,
    }
    _logger.info(json.dumps(log_obj, ensure_ascii=False))
    return response


# Phase 3: セキュリティヘッダー
@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response


# --- Auth ---
@app.post("/api/v1/auth/login")
async def login(username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    """DB 認証。DEMO_LOGIN_ENABLED=true 時のみデモ認証（kaho0525/0525, admin/admin）を許可"""
    cfg = get_config()
    demo_ok = cfg.get("demo_login_enabled", False)
    # 1) DB 認証を試行
    r = await db.execute(select(User).where(User.username == username, User.is_active == True))
    u = r.scalars().first()
    if u and verify_password(password, u.password_hash):
        return {"access_token": create_access_token(username), "token_type": "bearer"}
    # 2) デモ有効時のみハードコード認証を許可
    if demo_ok and ((username == "kaho0525" and password == "0525") or (username == "admin" and password == "admin")):
        return {"access_token": create_access_token(username), "token_type": "bearer"}
    return JSONResponse({"detail": "Invalid credentials"}, status_code=401)


@app.post("/api/v1/auth/change-password")
async def change_password(
    request: Request,
    body: dict = Body(...),
    db: AsyncSession = Depends(get_db),
    user: str = Depends(require_auth),
):
    """ログイン中のユーザーがパスワードを変更"""
    if user == "api-key-user":
        return JSONResponse({"detail": "API key users cannot change password."}, status_code=400)
    current_password = body.get("current_password") or ""
    new_password = body.get("new_password") or ""
    r = await db.execute(select(User).where(User.username == user, User.is_active == True))
    u = r.scalars().first()
    if not u or not verify_password(current_password, u.password_hash):
        return JSONResponse({"detail": "Current password is incorrect."}, status_code=400)
    if len(new_password) < 8:
        return JSONResponse({"detail": "New password must be at least 8 characters."}, status_code=400)
    if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        return JSONResponse({"detail": "New password must contain both letters and numbers."}, status_code=400)
    u.password_hash = hash_password(new_password)
    await db.commit()
    await write_audit(db, "password_changed", "auth", user_id=user, ip_address=request.client.host if request.client else None)
    return {"message": "Password updated successfully."}


# --- Medical ---
def _summarize_finding(finding: str | None) -> str:
    """AI所見の自然言語要約（ルールベース）"""
    if not finding:
        return ""
    s = finding.lower()
    if "normal" in s and "finding" in s:
        return "異常なし"
    if "abnormality" in s or "abnormal" in s:
        return "要フォロー"
    if "irregularity" in s or "irregular" in s:
        return "不整検出"
    if "opacity" in s:
        return "陰影あり"
    if "follow-up" in s or "recommended" in s:
        return "経過観察推奨"
    if len(finding) > 40:
        return finding[:40] + "…"
    return finding


@app.get("/api/v1/medical/patients")
async def get_patients(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    cnt = await db.execute(select(func.count(Patient.id)))
    total = cnt.scalar() or 0
    r = await db.execute(select(Patient).limit(limit).offset(offset))
    items = [{"id": x.id, "identifier": x.identifier, "family_name": x.family_name, "given_name": x.given_name, "gender": x.gender, "birth_date": x.birth_date} for x in r.scalars().all()]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@app.get("/api/v1/medical/ai-diagnosis")
async def get_ai_diagnosis(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(AIDiagnosis))
    items = [{"id": f"diag-{x.id}", "patient_id": x.patient_id, "finding": x.finding, "confidence": x.confidence, "status": x.status, "created_at": x.created_at.isoformat() if x.created_at else None, "summary": _summarize_finding(x.finding)} for x in r.scalars().all()]
    return {"items": items, "total": len(items)}


@app.get("/api/v1/medical/vital-signs")
async def get_vital_signs(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(VitalSign))
    items = [{"patient_id": x.patient_id, "heart_rate": x.heart_rate, "blood_pressure": x.blood_pressure, "spo2": x.spo2, "timestamp": x.recorded_at.isoformat()} for x in r.scalars().all()]
    return {"items": items, "total": len(items)}


@app.get("/api/v1/medical/fhir/patient/{patient_id}")
async def get_fhir_patient(patient_id: str, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(Patient).where(Patient.id == patient_id))
    p = r.scalar_one_or_none()
    if not p:
        return {"error": "Not found"}
    return {
        "resourceType": "Patient",
        "id": p.id,
        "identifier": [{"system": "urn:oid:1.2.392.200119.6.102.100", "value": p.identifier}],
        "name": [{"family": p.family_name, "given": [p.given_name]}],
        "gender": p.gender,
        "birthDate": p.birth_date,
    }


@app.get("/api/v1/medical/stats")
async def get_medical_stats(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(func.count(Patient.id)))
    cnt = r.scalar() or 0
    return {"active_patients": cnt, "ai_diagnosis_today": 42, "anomalies_detected_today": 5, "last_updated": datetime.utcnow().isoformat()}


# --- CSV インポート ---
@app.post("/api/v1/medical/patients/import")
async def import_patients_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    """CSV: id,identifier,family_name,given_name,gender,birth_date"""
    import csv
    import io
    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except Exception:
        text = content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    added = 0
    for row in reader:
        pid = (row.get("id") or row.get("identifier") or "").strip()
        if not pid:
            continue
        p = Patient(
            id=pid[:32],
            identifier=row.get("identifier", pid)[:64],
            family_name=(row.get("family_name") or "")[:128],
            given_name=(row.get("given_name") or "")[:128],
            gender=(row.get("gender") or "")[:16],
            birth_date=(row.get("birth_date") or "")[:16],
        )
        db.merge(p)
        added += 1
    await db.commit()
    return {"imported": added}


@app.post("/api/v1/aviation/flights/import")
async def import_flights_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    """CSV: flight_id,route,departure,arrival,status,aircraft"""
    import csv
    import io
    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except Exception:
        text = content.decode("utf-8", errors="replace")
    reader = csv.DictReader(io.StringIO(text))
    added = 0
    for row in reader:
        fid = (row.get("flight_id") or "").strip()
        if not fid:
            continue
        f = Flight(flight_id=fid[:32], route=(row.get("route") or "")[:32], departure=(row.get("departure") or "")[:16],
                   arrival=(row.get("arrival") or "")[:16], status=(row.get("status") or "OnTime")[:64], aircraft=(row.get("aircraft") or "")[:32])
        db.merge(f)
        added += 1
    await db.commit()
    return {"imported": added}


# --- Aviation ---
@app.get("/api/v1/aviation/flights")
async def get_flights(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    cnt = await db.execute(select(func.count(Flight.id)))
    total = cnt.scalar() or 0
    r = await db.execute(select(Flight).limit(limit).offset(offset))
    items = [{"flight_id": x.flight_id, "route": x.route, "departure": x.departure, "arrival": x.arrival, "status": x.status, "aircraft": x.aircraft} for x in r.scalars().all()]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@app.get("/api/v1/aviation/airports")
async def get_airports(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(Airport))
    items = [{"airport": x.code, "departures_today": x.departures_today, "arrivals_today": x.arrivals_today, "congestion": x.congestion, "weather": x.weather} for x in r.scalars().all()]
    return {"items": items, "total": len(items)}


@app.get("/api/v1/aviation/delays")
async def get_delays(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(Flight))
    flights = r.scalars().all()
    delayed = sum(1 for f in flights if f.status == "Delayed")
    on_time = sum(1 for f in flights if f.status == "OnTime")
    total = len(flights) or 1
    return {
        "on_time_rate": round(on_time / total, 2) if total else 0.92,
        "avg_delay_minutes": 8,
        "delayed_flights_today": delayed,
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/aviation/delay-prediction")
async def get_delay_prediction(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    """遅延予測: Open-Meteo天候 + 空港混雑の簡易モデル"""
    import httpx
    r = await db.execute(select(Airport))
    airports = r.scalars().all()
    r2 = await db.execute(select(Flight))
    flights = r2.scalars().all()
    delayed = sum(1 for f in flights if f.status == "Delayed")
    total = len(flights) or 1
    delay_ratio = delayed / total if total else 0.1

    # 東京（NRT/HND）の天候を Open-Meteo で取得（APIキー不要）
    weather_risk = 0
    weather_desc = "Unknown"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(
                "https://api.open-meteo.com/v1/forecast",
                params={"latitude": 35.77, "longitude": 140.39, "current": "weather_code,precipitation"},
            )
            if resp.status_code == 200:
                j = resp.json()
                wc = j.get("current", {}).get("weather_code", 0)
                # WMO codes: 0=clear, 1-3=clouds, 61-67=rain, 80-82=showers, 95-99=thunderstorm
                if wc >= 95:
                    weather_risk, weather_desc = 35, "Thunderstorm"
                elif wc >= 80 or 61 <= wc <= 67:
                    weather_risk, weather_desc = 25, "Rain"
                elif 51 <= wc <= 57:
                    weather_risk, weather_desc = 15, "Drizzle"
                elif 1 <= wc <= 3:
                    weather_risk, weather_desc = 5, "Cloudy"
                else:
                    weather_desc = "Clear"
    except Exception:
        weather_desc = "N/A"

    congestion_risk = 0
    for a in airports:
        if a.congestion == "High":
            congestion_risk += 20
        elif a.congestion == "Medium":
            congestion_risk += 8

    delay_ratio_risk = 15 if delay_ratio > 0.2 else (8 if delay_ratio > 0.1 else 0)
    risk_score = min(100, int(weather_risk + congestion_risk + delay_ratio_risk))
    level = "high" if risk_score >= 50 else ("medium" if risk_score >= 25 else "low")

    return {
        "risk_score": risk_score,
        "level": level,
        "weather": weather_desc,
        "weather_risk": weather_risk,
        "congestion_risk": congestion_risk,
        "delay_ratio_risk": delay_ratio_risk,
        "last_updated": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/aviation/stats")
async def get_aviation_stats(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(func.count(Flight.id)))
    cnt = r.scalar() or 0
    return {"total_flights_today": 568, "on_time_rate": 0.92, "active_airports": 4, "last_updated": datetime.utcnow().isoformat()}


# --- Space ---
@app.get("/api/v1/space/satellites")
async def get_satellites(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    cnt = await db.execute(select(func.count(Satellite.id)))
    total = cnt.scalar() or 0
    r = await db.execute(select(Satellite).limit(limit).offset(offset))
    items = [{"id": x.satellite_id, "name": x.name, "orbit_km": x.orbit_km, "inclination": x.inclination, "period_min": x.period_min, "status": x.status} for x in r.scalars().all()]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@app.get("/api/v1/space/satellites/{satellite_id}")
async def get_satellite(satellite_id: str, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(Satellite).where(Satellite.satellite_id == satellite_id))
    x = r.scalar_one_or_none()
    if not x:
        return {"error": "Not found"}
    return {"id": x.satellite_id, "name": x.name, "orbit_km": x.orbit_km, "inclination": x.inclination, "period_min": x.period_min, "status": x.status}


@app.get("/api/v1/space/launches")
async def get_launches(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(Launch))
    items = [{"id": x.launch_id, "mission": x.mission, "date": x.launch_date, "vehicle": x.vehicle, "status": x.status} for x in r.scalars().all()]
    return {"items": items, "total": len(items)}


@app.get("/api/v1/space/apod")
async def get_apod(_user: str = Depends(require_auth)):
    """NASA APOD - APIキーが NASA_API_KEY に設定されていれば実データ取得"""
    import httpx
    api_key = os.environ.get("NASA_API_KEY", "").strip()
    if api_key:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(
                    "https://api.nasa.gov/planetary/apod",
                    params={"api_key": api_key},
                )
                if resp.status_code == 200:
                    j = resp.json()
                    return {
                        "title": j.get("title", ""),
                        "explanation": j.get("explanation", ""),
                        "url": j.get("url", ""),
                        "date": j.get("date", datetime.utcnow().strftime("%Y-%m-%d")),
                        "media_type": j.get("media_type", "image"),
                    }
        except Exception:
            pass
    return {
        "title": "Earth from ISS",
        "explanation": "Sample. Set NASA_API_KEY in env for real APOD. Get key at https://api.nasa.gov",
        "url": "",
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "media_type": "image",
    }


@app.get("/api/v1/space/stats")
async def get_space_stats(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(func.count(Satellite.id)))
    cnt = r.scalar() or 0
    return {"tracked_satellites": cnt, "upcoming_launches": 2, "last_updated": datetime.utcnow().isoformat()}


# --- ERP（統合基幹業務システム）---
import uuid as _uuid
_erp_sales_orders: Dict[str, Dict[str, Any]] = {}
_erp_purchase_orders: Dict[str, Dict[str, Any]] = {}
_erp_sync_rules: Dict[str, Dict[str, Any]] = {}
_erp_sync_logs: List[Dict[str, Any]] = []

def _erp_seed_sample_data():
    """サンプルデータ投入（初回のみ）"""
    if _erp_sales_orders:
        return
    now = datetime.utcnow().isoformat()
    # 受注（明細付き・ステータス多様）
    samples_sales = [
        {"cid": "C001", "cname": "株式会社サンプルA", "amt": 150000, "st": "confirmed", "items": [{"product_id": "P001", "product_name": "商品A", "quantity": 10, "unit_price": 15000}]},
        {"cid": "C002", "cname": "有限会社テストB", "amt": 280000, "st": "shipped", "items": [{"product_id": "P002", "product_name": "商品B", "quantity": 5, "unit_price": 56000}], "invoice_no": "INV-2024-001", "shipped_at": "2024-03-08T10:00:00"},
        {"cid": "C003", "cname": "合同会社デモC", "amt": 95000, "st": "draft", "items": [{"product_id": "P003", "product_name": "商品C", "quantity": 19, "unit_price": 5000}]},
        {"cid": "C004", "cname": "株式会社グローバルD", "amt": 420000, "st": "invoiced", "items": [{"product_id": "P001", "product_name": "商品A", "quantity": 20, "unit_price": 21000}]},
        {"cid": "C005", "cname": "有限会社ローカルE", "amt": 78000, "st": "paid", "items": [{"product_id": "P005", "product_name": "商品E", "quantity": 13, "unit_price": 6000}], "invoice_no": "INV-2024-002", "shipped_at": "2024-03-05T14:30:00"},
    ]
    for i, r in enumerate(samples_sales, 1):
        items = r.get("items", [])
        amt = sum(it.get("quantity", 0) * it.get("unit_price", 0) for it in items) or r["amt"]
        oid = f"SO-{datetime.utcnow().strftime('%Y%m%d')}-{str(i).zfill(4)}"
        _erp_sales_orders[oid] = {"id": oid, "customer_id": r["cid"], "customer_name": r["cname"], "total_amount": amt, "status": r["st"], "items": items, "invoice_no": r.get("invoice_no"), "shipped_at": r.get("shipped_at"), "notes": "サンプル受注", "created_at": now, "updated_at": now}
    # 発注（明細付き）
    samples_purchase = [
        {"sid": "S001", "sname": "仕入先株式会社X", "amt": 120000, "st": "ordered", "items": [{"product_id": "M001", "product_name": "原材料A", "quantity": 100, "unit_price": 1200}]},
        {"sid": "S002", "sname": "供給元有限会社Y", "amt": 350000, "st": "received", "items": [{"product_id": "M002", "product_name": "部品B", "quantity": 50, "unit_price": 7000}], "received_at": "2024-03-07T09:00:00"},
        {"sid": "S003", "sname": "調達先合同会社Z", "amt": 78000, "st": "draft", "items": [{"product_id": "M003", "product_name": "資材C", "quantity": 26, "unit_price": 3000}]},
        {"sid": "S004", "sname": "株式会社調達プロ", "amt": 195000, "st": "paid", "items": [{"product_id": "M001", "product_name": "原材料A", "quantity": 65, "unit_price": 3000}], "received_at": "2024-03-01T11:00:00"},
    ]
    for i, r in enumerate(samples_purchase, 1):
        items = r.get("items", [])
        amt = sum(it.get("quantity", 0) * it.get("unit_price", 0) for it in items) or r["amt"]
        oid = f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{str(i).zfill(4)}"
        _erp_purchase_orders[oid] = {"id": oid, "supplier_id": r["sid"], "supplier_name": r["sname"], "total_amount": amt, "status": r["st"], "items": items, "received_at": r.get("received_at"), "notes": "サンプル発注", "created_at": now, "updated_at": now}
    # データ連携ルール（スケジュール・マッピング付き）
    _erp_sync_rules["sync-erp_sales-accounting"] = {"id": "sync-erp_sales-accounting", "source_system": "erp_sales", "target_system": "accounting", "sync_type": "batch", "schedule": "0 2 * * *", "mapping": {"total_amount": "debit_amount", "customer_id": "partner_code"}, "enabled": True, "created_at": now}
    _erp_sync_rules["sync-erp_purchasing-accounting"] = {"id": "sync-erp_purchasing-accounting", "source_system": "erp_purchasing", "target_system": "accounting", "sync_type": "batch", "schedule": "0 3 * * *", "mapping": {"total_amount": "credit_amount", "supplier_id": "vendor_code"}, "enabled": True, "created_at": now}
    _erp_sync_rules["sync-accounting-hr"] = {"id": "sync-accounting-hr", "source_system": "accounting", "target_system": "hr", "sync_type": "realtime", "schedule": None, "mapping": {}, "enabled": True, "created_at": now}
    # サンプル同期ログ
    _erp_sync_logs.extend([
        {"rule_id": "sync-erp_sales-accounting", "source_system": "erp_sales", "target_system": "accounting", "executed_at": now, "status": "success", "records_synced": 45},
        {"rule_id": "sync-erp_purchasing-accounting", "source_system": "erp_purchasing", "target_system": "accounting", "executed_at": now, "status": "success", "records_synced": 28},
    ])

def _erp_sales_summary():
    total = sum(o["total_amount"] for o in _erp_sales_orders.values() if o.get("status") != "cancelled")
    return {"order_count": len([o for o in _erp_sales_orders.values() if o.get("status") != "cancelled"]), "total_sales": total}

def _erp_purchasing_summary():
    total = sum(o["total_amount"] for o in _erp_purchase_orders.values() if o.get("status") != "cancelled")
    return {"order_count": len([o for o in _erp_purchase_orders.values() if o.get("status") != "cancelled"]), "total_purchases": total}

def _erp_integration_summary():
    return {"rules_count": len(_erp_sync_rules), "last_sync_count": len(_erp_sync_logs), "systems": ["erp_sales", "erp_purchasing", "accounting", "hr"]}

@app.get("/api/v1/erp/summary")
async def get_erp_summary(_user: str = Depends(require_auth)):
    """ERP統合サマリー"""
    return {
        "platform": "ERP（統合基幹業務システム）",
        "version": "1.0.0",
        "modules": {
            "販売管理": _erp_sales_summary(),
            "購買管理": _erp_purchasing_summary(),
            "データ連携": _erp_integration_summary(),
        },
    }

@app.get("/api/v1/erp/sales/orders")
async def list_erp_sales_orders(status: Optional[str] = None, limit: int = 100, _user: str = Depends(require_auth)):
    """受注一覧"""
    orders = list(_erp_sales_orders.values())
    if status:
        orders = [o for o in orders if o.get("status") == status]
    return sorted(orders, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

@app.get("/api/v1/erp/purchasing/orders")
async def list_erp_purchasing_orders(status: Optional[str] = None, limit: int = 100, _user: str = Depends(require_auth)):
    """発注一覧"""
    orders = list(_erp_purchase_orders.values())
    if status:
        orders = [o for o in orders if o.get("status") == status]
    return sorted(orders, key=lambda x: x.get("created_at", ""), reverse=True)[:limit]

@app.get("/api/v1/erp/data-integration/rules")
async def list_erp_sync_rules(_user: str = Depends(require_auth)):
    """データ連携ルール一覧"""
    return list(_erp_sync_rules.values())


@app.post("/api/v1/erp/sales/orders")
async def create_erp_sales_order(body: dict = Body(...), _user: str = Depends(require_auth)):
    """受注作成"""
    oid = f"SO-{datetime.utcnow().strftime('%Y%m%d')}-{_uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow().isoformat()
    order = {
        "id": oid,
        "customer_id": body.get("customer_id", ""),
        "customer_name": body.get("customer_name", ""),
        "items": body.get("items", []),
        "total_amount": float(body.get("total_amount", 0)),
        "status": "draft",
        "notes": body.get("notes"),
        "created_at": now,
        "updated_at": now,
    }
    _erp_sales_orders[oid] = order
    return order


@app.post("/api/v1/erp/purchasing/orders")
async def create_erp_purchasing_order(body: dict = Body(...), _user: str = Depends(require_auth)):
    """発注作成"""
    oid = f"PO-{datetime.utcnow().strftime('%Y%m%d')}-{_uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow().isoformat()
    order = {
        "id": oid,
        "supplier_id": body.get("supplier_id", ""),
        "supplier_name": body.get("supplier_name", ""),
        "items": body.get("items", []),
        "total_amount": float(body.get("total_amount", 0)),
        "status": "draft",
        "notes": body.get("notes"),
        "created_at": now,
        "updated_at": now,
    }
    _erp_purchase_orders[oid] = order
    return order

@app.get("/api/v1/erp/sales/orders/{order_id}")
async def get_erp_sales_order(order_id: str, _user: str = Depends(require_auth)):
    """受注詳細"""
    o = _erp_sales_orders.get(order_id)
    if not o:
        return JSONResponse({"detail": "Order not found"}, status_code=404)
    return o

@app.get("/api/v1/erp/purchasing/orders/{order_id}")
async def get_erp_purchasing_order(order_id: str, _user: str = Depends(require_auth)):
    """発注詳細"""
    o = _erp_purchase_orders.get(order_id)
    if not o:
        return JSONResponse({"detail": "Order not found"}, status_code=404)
    return o

@app.patch("/api/v1/erp/sales/orders/{order_id}")
async def update_erp_sales_order(order_id: str, body: dict = Body(...), _user: str = Depends(require_auth)):
    """受注更新（ステータス・請求番号・出荷日）"""
    o = _erp_sales_orders.get(order_id)
    if not o:
        return JSONResponse({"detail": "Order not found"}, status_code=404)
    if "status" in body:
        o["status"] = body["status"]
    if "invoice_no" in body:
        o["invoice_no"] = body["invoice_no"]
    if "shipped_at" in body:
        o["shipped_at"] = body["shipped_at"]
    o["updated_at"] = datetime.utcnow().isoformat()
    return o

@app.patch("/api/v1/erp/purchasing/orders/{order_id}")
async def update_erp_purchasing_order(order_id: str, body: dict = Body(...), _user: str = Depends(require_auth)):
    """発注更新（ステータス・入荷日・請求番号）"""
    o = _erp_purchase_orders.get(order_id)
    if not o:
        return JSONResponse({"detail": "Order not found"}, status_code=404)
    if "status" in body:
        o["status"] = body["status"]
    if "received_at" in body:
        o["received_at"] = body["received_at"]
    if "invoice_no" in body:
        o["invoice_no"] = body["invoice_no"]
    o["updated_at"] = datetime.utcnow().isoformat()
    return o


# --- レガシー刷新 ---
_legacy_migration_jobs: Dict[str, Dict[str, Any]] = {}
_legacy_migration_logs: List[Dict[str, Any]] = []

@app.get("/api/v1/legacy-migration/summary")
async def get_legacy_migration_summary(_user: str = Depends(require_auth)):
    """レガシー移行ツールサマリー"""
    jobs = list(_legacy_migration_jobs.values())
    completed = len([j for j in jobs if j.get("status") == "completed"])
    return {
        "platform": "レガシー刷新・クラウド移行",
        "jobs": len(jobs),
        "completed": completed,
        "pending": len(jobs) - completed,
        "tools": ["データ移行ツール", "レガシーAPIアダプター", "移行検証ダッシュボード"],
        "last_updated": datetime.utcnow().isoformat(),
    }

@app.get("/api/v1/legacy-migration/jobs")
async def list_legacy_migration_jobs(limit: int = 50, _user: str = Depends(require_auth)):
    """移行ジョブ一覧"""
    jobs = sorted(_legacy_migration_jobs.values(), key=lambda x: x.get("created_at", ""), reverse=True)
    return jobs[:limit]

@app.post("/api/v1/legacy-migration/jobs")
async def create_legacy_migration_job(body: dict = Body(...), _user: str = Depends(require_auth)):
    """移行ジョブ作成"""
    jid = f"job-{_uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    src_cfg = body.get("source_config", {})
    if body.get("source_type") == "csv" and not src_cfg:
        src_cfg = {"file_path": "/data/legacy/export.csv", "encoding": "utf-8", "delimiter": ","}
    elif body.get("source_type") == "db" and not src_cfg:
        src_cfg = {"host": "legacy-db.internal", "port": 5432, "database": "legacy"}
    job = {
        "id": jid,
        "name": body.get("name", f"移行ジョブ {jid[:8]}"),
        "source_type": body.get("source_type", "csv"),
        "source_config": src_cfg,
        "target_system": body.get("target_system", "erp_sales"),
        "mapping": body.get("mapping", {"id": "external_id", "amount": "total_amount"}),
        "status": "pending",
        "created_at": now,
        "updated_at": now,
    }
    _legacy_migration_jobs[jid] = job
    return job

@app.get("/api/v1/legacy-migration/jobs/{job_id}")
async def get_legacy_migration_job(job_id: str, _user: str = Depends(require_auth)):
    """移行ジョブ詳細"""
    job = _legacy_migration_jobs.get(job_id)
    if not job:
        return JSONResponse({"detail": "Job not found"}, status_code=404)
    return job

@app.post("/api/v1/legacy-migration/jobs/{job_id}/run")
async def run_legacy_migration_job(job_id: str, _user: str = Depends(require_auth)):
    """移行ジョブ実行"""
    job = _legacy_migration_jobs.get(job_id)
    if not job:
        return JSONResponse({"detail": "Job not found"}, status_code=404)
    job["status"] = "running"
    job["updated_at"] = datetime.utcnow().isoformat()
    # シミュレーション: 即完了（レコード数はランダム）
    import random
    recs = random.randint(10, 500)
    job["status"] = "completed"
    job["completed_at"] = datetime.utcnow().isoformat()
    job["records_migrated"] = recs
    job["errors"] = []
    log = {"job_id": job_id, "executed_at": job["completed_at"], "records_migrated": recs, "status": "success"}
    _legacy_migration_logs.insert(0, log)
    if len(_legacy_migration_logs) > 50:
        _legacy_migration_logs.pop()
    return job

@app.get("/api/v1/legacy-migration/logs")
async def list_legacy_migration_logs(limit: int = 20, _user: str = Depends(require_auth)):
    """移行実行ログ"""
    return {"items": _legacy_migration_logs[:limit], "total": len(_legacy_migration_logs)}

@app.post("/api/v1/legacy-migration/validate")
async def validate_legacy_migration(body: dict = Body(...), _user: str = Depends(require_auth)):
    """移行前検証（シミュレーション）"""
    job_id = body.get("job_id", "")
    return {"valid": True, "warnings": [], "source_record_count": 100, "mapping_errors": 0}


def _legacy_seed_sample_jobs():
    """レガシー移行サンプルジョブ（初回のみ）"""
    if _legacy_migration_jobs:
        return
    now = datetime.utcnow().isoformat()
    for j in [
        {"name": "旧販売DB→ERP移行", "source_type": "db", "target_system": "erp_sales", "status": "completed", "records_migrated": 1250},
        {"name": "CSV一括取込 購買", "source_type": "csv", "target_system": "erp_purchasing", "status": "pending"},
    ]:
        jid = f"job-{_uuid.uuid4().hex[:12]}"
        _legacy_migration_jobs[jid] = {
            "id": jid, "name": j["name"], "source_type": j["source_type"],
            "source_config": {"file_path": "/data/import.csv"} if j["source_type"] == "csv" else {"host": "legacy-db", "database": "sales_legacy"},
            "target_system": j["target_system"], "mapping": {}, "status": j["status"],
            "created_at": now, "updated_at": now,
            **({"completed_at": now, "records_migrated": j["records_migrated"]} if j.get("records_migrated") else {}),
        }


# --- データ連携基盤 ---
def _data_integration_last_sync():
    return _erp_sync_logs[0]["executed_at"] if _erp_sync_logs else datetime.utcnow().isoformat()

@app.get("/api/v1/data-integration/summary")
async def get_data_integration_summary(_user: str = Depends(require_auth)):
    """データ連携基盤サマリー"""
    return {
        "platform": "データ連携基盤",
        "rules_count": len(_erp_sync_rules),
        "pipelines": len(_erp_sync_logs),
        "systems": ["erp_sales", "erp_purchasing", "accounting", "hr", "unified_business"],
        "last_sync": _data_integration_last_sync(),
    }

@app.get("/api/v1/data-integration/rules")
async def list_data_integration_rules(_user: str = Depends(require_auth)):
    """データ連携ルール一覧"""
    return list(_erp_sync_rules.values())

@app.post("/api/v1/data-integration/rules")
async def create_data_integration_rule(body: dict = Body(...), _user: str = Depends(require_auth)):
    """データ連携ルール作成"""
    rid = f"sync-{body.get('source_system', 'src')}-{body.get('target_system', 'tgt')}"
    if rid in _erp_sync_rules:
        rid = f"{rid}-{_uuid.uuid4().hex[:6]}"
    rule = {
        "id": rid,
        "source_system": body.get("source_system", ""),
        "target_system": body.get("target_system", ""),
        "sync_type": body.get("sync_type", "batch"),
        "schedule": body.get("schedule"),
        "enabled": True,
        "created_at": datetime.utcnow().isoformat(),
    }
    _erp_sync_rules[rid] = rule
    return rule

@app.post("/api/v1/data-integration/sync/{rule_id}")
async def execute_data_integration_sync(rule_id: str, _user: str = Depends(require_auth)):
    """データ連携同期実行"""
    rule = _erp_sync_rules.get(rule_id)
    if not rule:
        return JSONResponse({"detail": "Rule not found"}, status_code=404)
    import random
    recs = random.randint(5, 200)
    log = {
        "rule_id": rule_id,
        "source_system": rule.get("source_system"),
        "target_system": rule.get("target_system"),
        "executed_at": datetime.utcnow().isoformat(),
        "status": "success",
        "records_synced": recs,
    }
    _erp_sync_logs.insert(0, log)
    if len(_erp_sync_logs) > 100:
        _erp_sync_logs.pop()
    return {"success": True, "log": log}

@app.get("/api/v1/data-integration/logs")
async def list_data_integration_logs(limit: int = 20, _user: str = Depends(require_auth)):
    """データ連携実行ログ"""
    return {"items": _erp_sync_logs[:limit], "total": len(_erp_sync_logs)}

@app.patch("/api/v1/data-integration/rules/{rule_id}")
async def update_data_integration_rule(rule_id: str, body: dict = Body(...), _user: str = Depends(require_auth)):
    """連携ルール更新（有効/無効・スケジュール）"""
    rule = _erp_sync_rules.get(rule_id)
    if not rule:
        return JSONResponse({"detail": "Rule not found"}, status_code=404)
    if "enabled" in body:
        rule["enabled"] = bool(body["enabled"])
    if "schedule" in body:
        rule["schedule"] = body["schedule"]
    if "mapping" in body:
        rule["mapping"] = body["mapping"]
    return rule


# --- DX推進基盤 ---
_dx_documents: Dict[str, Dict[str, Any]] = {}
_dx_workflows: Dict[str, Dict[str, Any]] = {}

def _dx_seed_sample_data():
    """DXサンプルデータ（初回のみ）"""
    if _dx_documents:
        return
    now = datetime.utcnow().isoformat()
    for d in [
        {"title": "業務マニュアル 販売編", "content": "受注から出荷までの標準プロセス...", "category": "manual"},
        {"title": "契約書テンプレート 基本型", "content": "甲乙の契約に関する条項...", "category": "contract"},
        {"title": "月次レポート 2024年2月", "content": "売上・利益・在庫のサマリ...", "category": "report"},
        {"title": "セキュリティポリシー", "content": "情報セキュリティ管理規定...", "category": "policy"},
    ]:
        did = f"doc-{_uuid.uuid4().hex[:12]}"
        _dx_documents[did] = {"id": did, "title": d["title"], "content": d["content"], "category": d["category"], "version": 1, "created_at": now, "updated_at": now}
    for w in [
        {"name": "稟議承認フロー", "description": "10万円以上の経費申請", "status": "active", "steps": [{"name": "申請", "role": "applicant"}, {"name": "課長承認", "role": "manager"}, {"name": "部長承認", "role": "director"}]},
        {"name": "休暇申請", "description": "有給・代休の申請", "status": "active", "steps": [{"name": "申請", "role": "applicant"}, {"name": "上長承認", "role": "supervisor"}]},
        {"name": "契約締結フロー", "description": "新規取引先との契約", "status": "draft", "steps": [{"name": "起案", "role": "sales"}, {"name": "法務確認", "role": "legal"}, {"name": "決裁", "role": "executive"}]},
    ]:
        wid = f"wf-{_uuid.uuid4().hex[:12]}"
        _dx_workflows[wid] = {"id": wid, "name": w["name"], "description": w["description"], "status": w["status"], "steps": w["steps"], "created_at": now, "updated_at": now}

@app.get("/api/v1/dx/summary")
async def get_dx_summary(_user: str = Depends(require_auth)):
    """DX推進基盤サマリー"""
    return {
        "platform": "DX推進基盤",
        "documents": len(_dx_documents),
        "workflows": len(_dx_workflows),
        "features": ["ドキュメント管理", "電子承認フロー", "データ可視化・BI"],
        "last_updated": datetime.utcnow().isoformat(),
    }

# ドキュメント CRUD
@app.get("/api/v1/dx/documents")
async def list_dx_documents(limit: int = 50, _user: str = Depends(require_auth)):
    docs = sorted(_dx_documents.values(), key=lambda x: x.get("updated_at", ""), reverse=True)[:limit]
    return {"items": docs, "total": len(_dx_documents)}

@app.post("/api/v1/dx/documents")
async def create_dx_document(body: dict = Body(...), _user: str = Depends(require_auth)):
    did = f"doc-{_uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    doc = {
        "id": did,
        "title": body.get("title", ""),
        "content": body.get("content", ""),
        "category": body.get("category", "general"),
        "version": 1,
        "created_at": now,
        "updated_at": now,
    }
    _dx_documents[did] = doc
    return doc

@app.get("/api/v1/dx/documents/{doc_id}")
async def get_dx_document(doc_id: str, _user: str = Depends(require_auth)):
    doc = _dx_documents.get(doc_id)
    if not doc:
        return JSONResponse({"detail": "Document not found"}, status_code=404)
    return doc

@app.put("/api/v1/dx/documents/{doc_id}")
async def update_dx_document(doc_id: str, body: dict = Body(...), _user: str = Depends(require_auth)):
    doc = _dx_documents.get(doc_id)
    if not doc:
        return JSONResponse({"detail": "Document not found"}, status_code=404)
    doc["title"] = body.get("title", doc["title"])
    doc["content"] = body.get("content", doc["content"])
    doc["category"] = body.get("category", doc["category"])
    doc["version"] = doc.get("version", 1) + 1
    doc["updated_at"] = datetime.utcnow().isoformat()
    return doc

@app.delete("/api/v1/dx/documents/{doc_id}")
async def delete_dx_document(doc_id: str, _user: str = Depends(require_auth)):
    if doc_id not in _dx_documents:
        return JSONResponse({"detail": "Document not found"}, status_code=404)
    del _dx_documents[doc_id]
    return {"ok": True}

# ワークフロー CRUD
@app.get("/api/v1/dx/workflows")
async def list_dx_workflows(limit: int = 50, _user: str = Depends(require_auth)):
    wfs = sorted(_dx_workflows.values(), key=lambda x: x.get("updated_at", ""), reverse=True)[:limit]
    return {"items": wfs, "total": len(_dx_workflows)}

@app.post("/api/v1/dx/workflows")
async def create_dx_workflow(body: dict = Body(...), _user: str = Depends(require_auth)):
    wid = f"wf-{_uuid.uuid4().hex[:12]}"
    now = datetime.utcnow().isoformat()
    wf = {
        "id": wid,
        "name": body.get("name", ""),
        "description": body.get("description", ""),
        "status": body.get("status", "draft"),
        "steps": body.get("steps", []),
        "created_at": now,
        "updated_at": now,
    }
    _dx_workflows[wid] = wf
    return wf

@app.get("/api/v1/dx/workflows/{wf_id}")
async def get_dx_workflow(wf_id: str, _user: str = Depends(require_auth)):
    wf = _dx_workflows.get(wf_id)
    if not wf:
        return JSONResponse({"detail": "Workflow not found"}, status_code=404)
    return wf

@app.put("/api/v1/dx/workflows/{wf_id}")
async def update_dx_workflow(wf_id: str, body: dict = Body(...), _user: str = Depends(require_auth)):
    wf = _dx_workflows.get(wf_id)
    if not wf:
        return JSONResponse({"detail": "Workflow not found"}, status_code=404)
    wf["name"] = body.get("name", wf["name"])
    wf["description"] = body.get("description", wf["description"])
    wf["status"] = body.get("status", wf["status"])
    wf["steps"] = body.get("steps", wf["steps"])
    wf["updated_at"] = datetime.utcnow().isoformat()
    return wf

@app.delete("/api/v1/dx/workflows/{wf_id}")
async def delete_dx_workflow(wf_id: str, _user: str = Depends(require_auth)):
    if wf_id not in _dx_workflows:
        return JSONResponse({"detail": "Workflow not found"}, status_code=404)
    del _dx_workflows[wf_id]
    return {"ok": True}


# --- Unified ---
@app.get("/api/v1/unified/stats")
async def get_unified_stats(db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    r = await db.execute(select(func.count(Patient.id)))
    p = r.scalar() or 0
    r = await db.execute(select(func.count(Flight.id)))
    f = r.scalar() or 0
    r = await db.execute(select(func.count(Satellite.id)))
    s = r.scalar() or 0
    return {"medical_patients": p, "aviation_flights": f, "space_satellites": s, "last_updated": datetime.utcnow().isoformat()}


# --- 通知センター ---
@app.get("/api/v1/notifications")
async def get_notifications(db: AsyncSession = Depends(get_db), user: str = Depends(require_auth)):
    """通知一覧（既読状態付き）"""
    r = await db.execute(select(Notification).order_by(Notification.created_at.desc()).limit(50))
    items = [
        {"id": x.id, "title": x.title, "body": x.body, "severity": x.severity, "domain": x.domain, "created_at": x.created_at.isoformat() if x.created_at else None}
        for x in r.scalars().all()
    ]
    read_ids = await notification_read_ids(user or "") if user else set()
    for it in items:
        it["read"] = it["id"] in read_ids
    return {"items": items, "total": len(items)}


@app.post("/api/v1/notifications/{notif_id:int}/read")
async def mark_notification_read(notif_id: int, user: str = Depends(require_auth)):
    """通知を既読にする"""
    await notification_mark_read(user, notif_id)
    return {"ok": True}


# --- 全ドメイン横断検索 ---
@app.get("/api/v1/search")
async def search(q: str = "", limit: int = 20, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    """患者・フライト・衛星を横断検索"""
    q = (q or "").strip()[:100]
    results = []
    if len(q) < 1:
        return {"items": results, "total": 0}
    q_like = f"%{q}%"
    # Patients
    r = await db.execute(select(Patient).where(
        (Patient.identifier.ilike(q_like)) | (Patient.family_name.ilike(q_like)) | (Patient.given_name.ilike(q_like))
    ).limit(limit))
    for x in r.scalars().all():
        results.append({"domain": "medical", "type": "patient", "id": x.id, "label": f"{x.family_name or ''} {x.given_name or ''}".strip() or x.identifier, "detail": x.identifier})
    # Flights
    r = await db.execute(select(Flight).where(
        (Flight.flight_id.ilike(q_like)) | (Flight.route.ilike(q_like))
    ).limit(limit))
    for x in r.scalars().all():
        results.append({"domain": "aviation", "type": "flight", "id": x.flight_id, "label": f"{x.flight_id} {x.route}", "detail": x.route})
    # Satellites
    r = await db.execute(select(Satellite).where(
        (Satellite.satellite_id.ilike(q_like)) | (Satellite.name.ilike(q_like))
    ).limit(limit))
    for x in r.scalars().all():
        results.append({"domain": "space", "type": "satellite", "id": x.satellite_id, "label": x.name or x.satellite_id, "detail": x.satellite_id})
    return {"items": results[:limit], "total": len(results)}


# --- 天気・カレンダー・TODO（ウィジェット用） ---
@app.get("/api/v1/widgets/weather")
async def get_weather(_user: str = Depends(require_auth)):
    """天気ウィジェット（サンプル。OPENWEATHER_API_KEY で実データ）"""
    api_key = os.environ.get("OPENWEATHER_API_KEY", "").strip()
    if api_key:
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                r = await client.get("https://api.openweathermap.org/data/2.5/weather", params={"q": "Tokyo", "appid": api_key, "units": "metric"})
                if r.status_code == 200:
                    j = r.json()
                    return {"city": j.get("name", "Tokyo"), "temp": j.get("main", {}).get("temp"), "desc": j.get("weather", [{}])[0].get("description", ""), "icon": j.get("weather", [{}])[0].get("icon", "")}
        except Exception:
            pass
    return {"city": "Tokyo", "temp": 22, "desc": "晴れ（サンプル）", "icon": "01d"}


@app.get("/api/v1/widgets/calendar")
async def get_calendar(_user: str = Depends(require_auth)):
    """カレンダーウィジェット（今日・今週）"""
    from datetime import date, timedelta
    today = date.today()
    week = [today + timedelta(days=i) for i in range(7)]
    return {"today": today.isoformat(), "week": [d.isoformat() for d in week], "weekday": today.strftime("%A")}


# --- Phase 3: 監査ログ API ---
@app.get("/api/v1/admin/audit-logs")
async def get_audit_logs(limit: int = 100, offset: int = 0, db: AsyncSession = Depends(get_db), _user: str = Depends(require_auth)):
    """監査ログ取得（管理者用）"""
    r = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).offset(offset))
    items = [
        {
            "id": x.id,
            "timestamp": x.timestamp.isoformat(),
            "user_id": x.user_id,
            "action": x.action,
            "resource": x.resource,
            "resource_id": x.resource_id,
            "details": x.details,
            "ip_address": x.ip_address,
        }
        for x in r.scalars().all()
    ]
    cnt = await db.execute(select(func.count(AuditLog.id)))
    total = cnt.scalar() or 0
    return {"items": items, "total": total}


# --- アラート通知（Slack Webhook） ---
@app.post("/api/v1/admin/alert")
async def send_admin_alert(title: str = "", message: str = "", _user: str = Depends(require_auth)):
    """管理者用: Slack にアラート送信（SLACK_WEBHOOK_URL 設定時）"""
    from services.alert import send_alert
    ok = await send_alert(title or "UEP Alert", message or "No message", "info")
    return {"sent": ok}


# --- Seed (手動実行用) ---
@app.api_route("/api/v1/seed", methods=["GET", "POST"])
async def run_seed(force: bool = False):
    """DB が空の場合にシードを手動実行。force=1 で既存データを消して再投入。GET/POST 両方可"""
    import asyncio
    from seed_data import seed
    try:
        await asyncio.to_thread(seed, force)
        return {"status": "ok", "message": "Seed completed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# --- WebSocket: リアルタイム更新 ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """クライアント接続。30秒ごとに refresh をブロードキャスト"""
    import asyncio
    import json
    await ws_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                if payload.get("type") == "ping":
                    await websocket.send_text(json.dumps({"type": "pong", "ts": datetime.utcnow().isoformat()}))
            except json.JSONDecodeError:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


async def _ws_broadcast_loop():
    """30秒ごとに refresh をブロードキャスト（接続中クライアント向け）"""
    import asyncio
    import json
    while True:
        await asyncio.sleep(30)
        if ws_manager.active_connections:
            await ws_manager.broadcast({"type": "refresh", "ts": datetime.utcnow().isoformat()})


# --- Health (Phase 3: K8s probes) ---
@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    db_ok = await check_db_health()
    return {"status": "ready" if db_ok else "degraded", "database": db_ok}


@app.get("/api/v1/health/detail")
async def health_detail(_user: str = Depends(require_auth)):
    """ヘルスダッシュボード用: health, ready, 簡易メトリクス"""
    db_ok = await check_db_health()
    return {
        "health": {"status": "ok"},
        "ready": {"status": "ready" if db_ok else "degraded", "database": db_ok},
        "timestamp": datetime.utcnow().isoformat(),
    }


@app.get("/api/v1/logs")
async def get_logs(limit: int = 100, _user: str = Depends(require_auth)):
    """ログビューア用: 直近のログを取得"""
    n = min(500, max(1, limit))
    return {"items": list(_LOG_BUFFER)[-n:], "total": len(_LOG_BUFFER)}


# --- Phase 3: Prometheus metrics ---
@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


# --- 起動モード情報（ダッシュボード用） ---
DEPLOY_COMMANDS = {
    "default": [
        ("通常起動", "./start.sh"),
        ("監視付き", "./start.sh monitoring"),
        ("冗長構成", "./start.sh redundant"),
        ("冗長+監視", "./start.sh redundant monitoring"),
    ],
    "monitoring": [
        ("通常起動", "./start.sh"),
        ("監視付き", "./start.sh monitoring"),
        ("冗長構成", "./start.sh redundant"),
        ("冗長+監視", "./start.sh redundant monitoring"),
    ],
    "redundant": [
        ("通常起動", "./start.sh"),
        ("監視付き", "./start.sh monitoring"),
        ("冗長構成", "./start.sh redundant"),
        ("冗長+監視", "./start.sh redundant monitoring"),
    ],
    "redundant+monitoring": [
        ("通常起動", "./start.sh"),
        ("監視付き", "./start.sh monitoring"),
        ("冗長構成", "./start.sh redundant"),
        ("冗長+監視", "./start.sh redundant monitoring"),
    ],
}


@app.get("/api/v1/deploy-info")
async def deploy_info(_user: str = Depends(require_auth)):
    """現在の起動モードと切り替えコマンド"""
    mode = os.environ.get("DEPLOY_MODE", "default")
    mode_label = {"default": "通常", "monitoring": "監視付き", "redundant": "冗長", "redundant+monitoring": "冗長+監視"}.get(mode, mode)
    commands = DEPLOY_COMMANDS.get(mode, DEPLOY_COMMANDS["default"])
    return {"mode": mode, "mode_label": mode_label, "commands": [{"label": l, "cmd": c} for l, c in commands]}


# --- Root ---
@app.get("/")
async def root():
    if os.path.isdir(_frontend_dist):
        return FileResponse(os.path.join(_frontend_dist, "index.html"))
    return {"service": "統合基盤プラットフォーム", "status": "ok", "version": "5.0.0"}


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    mode = os.environ.get("DEPLOY_MODE", "default")
    mode_label = {"default": "通常", "monitoring": "監視付き", "redundant": "冗長", "redundant+monitoring": "冗長+監視"}.get(mode, mode)
    commands = DEPLOY_COMMANDS.get(mode, DEPLOY_COMMANDS["default"])
    cmd_rows = "".join(f'<tr><td>{l}</td><td><code>{c}</code></td></tr>' for l, c in commands)
    html = f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>統合基盤プラットフォーム</title>
<style>
*{{box-sizing:border-box;}}body{{font-family:system-ui,sans-serif;margin:0;background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);color:#e2e8f0;min-height:100vh;}}
.container{{max-width:1200px;margin:0 auto;padding:2rem;}}
h1{{color:#38bdf8;font-size:2rem;}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:1.5rem;}}
.card{{background:rgba(30,41,59,0.8);border:1px solid #334155;border-radius:12px;padding:1.5rem;transition:transform .2s;}}
.card:hover{{transform:translateY(-2px);border-color:#38bdf8;}}
.card h3{{color:#38bdf8;margin-top:0;}}
a{{color:#7dd3fc;text-decoration:none;}}
a:hover{{text-decoration:underline;}}
.badge{{display:inline-block;padding:.2em .6em;border-radius:6px;font-size:.75rem;margin:.2em;}}
.m{{background:#22c55e33;color:#4ade80;}}
.a{{background:#3b82f633;color:#60a5fa;}}
.s{{background:#8b5cf633;color:#a78bfa;}}
.deploy{{background:#64748b33;color:#94a3b8;}}
.deploy code{{background:#1e293b;padding:.2em .4em;border-radius:4px;font-size:.9em;}}
.deploy table{{width:100%;border-collapse:collapse;}}
.deploy td{{padding:.4em 0;border-bottom:1px solid #334155;}}
</style></head>
<body>
<div class="container">
<h1>統合基盤プラットフォーム</h1>
<p>Unified Platform | Medical | Aviation | Space</p>
<div class="card deploy"><h3>起動モード</h3>
<p><strong>現在のモード:</strong> <span class="badge">{mode_label}</span> <a href="/deploy">詳細</a></p>
<p><strong>切り替え・起動コマンド</strong>（WSL 内で <code>cd projects/unified-platform</code> の後）:</p>
<table>{cmd_rows}</table>
</div>
<div class="grid">
<div class="card"><h3><span class="badge m">Medical</span></h3>
<ul><li><a href="/api/v1/medical/ai-diagnosis">/api/v1/medical/ai-diagnosis</a></li>
<li><a href="/api/v1/medical/vital-signs">/api/v1/medical/vital-signs</a></li>
<li><a href="/api/v1/medical/fhir/patient/P001">Patient</a></li>
<li><a href="/api/v1/medical/stats">/stats</a></li></ul></div>
<div class="card"><h3><span class="badge a">Aviation</span></h3>
<ul><li><a href="/api/v1/aviation/flights">/api/v1/aviation/flights</a></li>
<li><a href="/api/v1/aviation/airports">/api/v1/aviation/airports</a></li>
<li><a href="/api/v1/aviation/delays">/delays</a></li>
<li><a href="/api/v1/aviation/stats">/stats</a></li></ul></div>
<div class="card"><h3><span class="badge s">Space</span></h3>
<ul><li><a href="/api/v1/space/satellites">/api/v1/space/satellites</a></li>
<li><a href="/api/v1/space/launches">/api/v1/space/launches</a></li>
<li><a href="/api/v1/space/apod">/apod</a></li>
<li><a href="/api/v1/space/stats">/stats</a></li></ul></div>
</div>
<div class="card"><h3>Unified</h3>
<ul><li><a href="/api/v1/unified/stats">/api/v1/unified/stats</a></li>
<li><a href="/health">/health</a></li>
<li><a href="/ready">/ready</a></li>
<li><a href="/metrics">/metrics</a> (Prometheus)</li></ul></div>
<div class="card"><p>Auth: POST /api/v1/auth/login (admin/admin) or X-API-Key: unified-demo-key</p></div>
</div>
</body></html>
"""
    return html


@app.get("/deploy", response_class=HTMLResponse)
async def deploy_page():
    """起動モード・切り替えコマンド専用ページ"""
    mode = os.environ.get("DEPLOY_MODE", "default")
    mode_label = {"default": "通常", "monitoring": "監視付き", "redundant": "冗長", "redundant+monitoring": "冗長+監視"}.get(mode, mode)
    commands = DEPLOY_COMMANDS.get(mode, DEPLOY_COMMANDS["default"])
    cmd_rows = "".join(f'<tr><td>{l}</td><td><code>{c}</code></td></tr>' for l, c in commands)
    return f"""
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>起動モード - 統合基盤</title>
<style>
*{{box-sizing:border-box;}}body{{font-family:system-ui,sans-serif;margin:0;background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);color:#e2e8f0;min-height:100vh;padding:2rem;}}
.container{{max-width:700px;margin:0 auto;}}
h1{{color:#38bdf8;}}
.card{{background:rgba(30,41,59,0.9);border:1px solid #334155;border-radius:12px;padding:1.5rem;margin:1rem 0;}}
.card h2{{color:#38bdf8;margin-top:0;}}
.badge{{display:inline-block;padding:.3em .6em;border-radius:6px;background:#38bdf833;color:#7dd3fc;}}
code{{background:#1e293b;padding:.2em .5em;border-radius:4px;font-size:.95em;}}
pre{{background:#1e293b;padding:1rem;border-radius:8px;overflow-x:auto;}}
pre code{{padding:0;}}
h3{{color:#94a3b8;font-size:1rem;margin:1rem 0 .5rem;}}
table{{width:100%;border-collapse:collapse;margin-top:.5rem;}}
td{{padding:.5em 0;border-bottom:1px solid #334155;}}
td:first-child{{width:140px;color:#94a3b8;}}
a{{color:#7dd3fc;}}
</style></head>
<body>
<div class="container">
<h1>起動モード</h1>
<p><a href="/dashboard">← ダッシュボードへ</a></p>
<div class="card">
<h2>現在のモード</h2>
<p><span class="badge">{mode_label}</span></p>
</div>
<div class="card">
<h2>切り替え・起動コマンド</h2>
<p>WSL 内で実行:</p>
<pre><code>cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform</code></pre>
<table>{cmd_rows}</table>
</div>
<div class="card">
<h2>起動方法</h2>
<h3>1. 反映手順（Docker）</h3>
<p>WSL 内で実行:</p>
<pre><code>cd /mnt/c/uep-v5-ultimate-enterprise-platform/projects/unified-platform
docker compose down
docker compose up -d --build</code></pre>
<p>※ <code>--build</code> でコード変更を反映</p>
<h3>2. 統合起動スクリプト（推奨・通常はこちら）</h3>
<pre><code>cd projects/unified-platform
chmod +x start.sh   # 初回のみ
./start.sh</code></pre>
<p>オプション: <code>./start.sh monitoring</code> / <code>redundant</code> / <code>redundant monitoring</code></p>
<h3>3. 個別コマンド</h3>
<table>
<tr><td>通常</td><td><code>docker compose up -d</code></td></tr>
<tr><td>監視付き</td><td><code>docker compose --profile monitoring up -d</code></td></tr>
<tr><td>冗長</td><td><code>docker compose -f docker-compose.yml -f docker-compose.redundant.yml --profile redundant up -d</code></td></tr>
</table>
<h3>4. 停止</h3>
<pre><code>docker compose down</code></pre>
</div>
</div>
</body></html>
"""


# SPA: /medical, /aviation, /space, /settings, /login 等は React に委譲（リロード時も index.html を返す）
# registerSW.js, manifest.webmanifest 等のルートファイルは実ファイルを返す（404だと白画面の原因）
@app.get("/{path:path}")
async def spa_catchall(path: str):
    if os.path.isdir(_frontend_dist):
        full_path = os.path.join(_frontend_dist, path)
        if os.path.isfile(full_path):
            return FileResponse(full_path)
        return FileResponse(os.path.join(_frontend_dist, "index.html"))
    return {"detail": "Not Found"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
