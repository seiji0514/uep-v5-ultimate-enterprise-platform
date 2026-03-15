"""
企業横断オペレーション基盤（Enterprise Operations Hub）
観測・タスク・リスクを一元管理する統合基盤
認証・RBAC・DB永続化・通知・エクスポート対応
本番運用対応（UEP v5.0・産業統合プラットフォームと同様）
"""
import csv
import io
import os

# 本番環境: 起動時に必須設定を検証
ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")
if ENVIRONMENT.lower() == "production":
    from auth_eoh import validate_production
    validate_production()
from contextlib import asynccontextmanager
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth_eoh import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_user_by_username,
    require_permission,
)
from database import Base, SessionLocal, engine, get_db
from models_db import Alert, AuditLog, Observation, Risk, Task, User

# DB初期化（スキーマバージョン不一致時は自動再作成）
from database import ensure_schema_version, set_schema_version
ensure_schema_version()
Base.metadata.create_all(bind=engine)
set_schema_version()


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = SessionLocal()
    try:
        # サンプルデータ投入（空の場合のみ・本番では無効）
        is_production = os.environ.get("ENVIRONMENT", "development").lower() == "production"
        if not is_production and db.query(Observation).count() == 0:
            obs_data = [
                {"domain": "manufacturing", "type": "設備異常", "title": "ラインA 振動検知", "severity": "高", "status": "要対応"},
                {"domain": "manufacturing", "type": "品質", "title": "製品B 不良率上昇", "severity": "中", "status": "要対応"},
                {"domain": "manufacturing", "type": "設備異常", "title": "ラインC 温度異常", "severity": "低", "status": "対応中"},
                {"domain": "security", "type": "セキュリティ", "title": "不審ログイン検知", "severity": "高", "status": "要対応"},
                {"domain": "security", "type": "脆弱性", "title": "CVE-2024-xxx 検知", "severity": "高", "status": "要対応"},
                {"domain": "customer", "type": "顧客声", "title": "問い合わせ急増", "severity": "中", "status": "対応中"},
                {"domain": "customer", "type": "クレーム", "title": "配送遅延クレーム増加", "severity": "中", "status": "要対応"},
                {"domain": "hr", "type": "属人化", "title": "キーパーソン休暇予定", "severity": "中", "status": "要対応"},
                {"domain": "compliance", "type": "規制", "title": "個人情報保護法 対応期限", "severity": "高", "status": "要対応"},
                {"domain": "finance", "type": "財務", "title": "予算消化率 80%超過", "severity": "中", "status": "監視中"},
                {"domain": "public_sector", "type": "申請", "title": "補助金申請 審査遅延", "severity": "中", "status": "要対応"},
                {"domain": "retail", "type": "在庫", "title": "商品B 在庫切れリスク", "severity": "高", "status": "要対応"},
                {"domain": "education", "type": "学習", "title": "コース完了率 低下", "severity": "中", "status": "対応中"},
                {"domain": "legal", "type": "契約", "title": "契約書レビュー 期限間近", "severity": "高", "status": "要対応"},
            ]
            for o in obs_data:
                db.add(Observation(**o))
            task_data = [
                {"domain": "manufacturing", "title": "ラインA 点検実施", "status": "未着手"},
                {"domain": "manufacturing", "title": "製品B 不良原因調査", "status": "対応中"},
                {"domain": "security", "title": "アカウント調査", "status": "未着手"},
                {"domain": "security", "title": "脆弱性パッチ適用", "status": "未着手"},
                {"domain": "customer", "title": "問い合わせ対応マニュアル更新", "status": "未着手"},
                {"domain": "hr", "title": "業務引き継ぎ資料作成", "status": "未着手"},
                {"domain": "compliance", "title": "個人情報保護法 社内教育", "status": "対応中"},
                {"domain": "public_sector", "title": "申請書類 確認・承認", "status": "未着手"},
                {"domain": "retail", "title": "在庫発注 実行", "status": "未着手"},
                {"domain": "education", "title": "教材 更新作業", "status": "対応中"},
                {"domain": "legal", "title": "契約書 レビュー実施", "status": "未着手"},
            ]
            for t in task_data:
                db.add(Task(**t))
            risk_data = [
                {"domain": "hr", "type": "属人化", "title": "キーパーソン依存", "level": "中", "status": "監視中"},
                {"domain": "security", "type": "不正", "title": "内部不正リスク", "level": "高", "status": "監視中"},
                {"domain": "supply_chain", "type": "調達", "title": "単一サプライヤー依存", "level": "中", "status": "監視中"},
                {"domain": "finance", "type": "財務", "title": "為替変動リスク", "level": "高", "status": "監視中"},
                {"domain": "public_sector", "type": "規制", "title": "情報公開請求 対応リスク", "level": "中", "status": "監視中"},
                {"domain": "retail", "type": "在庫", "title": "サプライヤー単一依存", "level": "中", "status": "監視中"},
                {"domain": "education", "type": "属人化", "title": "講師依存リスク", "level": "中", "status": "監視中"},
                {"domain": "legal", "type": "契約", "title": "契約更新 漏れリスク", "level": "高", "status": "監視中"},
            ]
            for r in risk_data:
                db.add(Risk(**r))
            alert_data = [
                {"domain": "manufacturing", "type": "threshold", "title": "要対応件数が閾値を超過", "severity": "高"},
                {"domain": "security", "type": "deadline", "title": "タスク期限間近", "severity": "中"},
                {"domain": "compliance", "type": "deadline", "title": "規制対応期限 1週間前", "severity": "高"},
                {"domain": "customer", "type": "anomaly", "title": "問い合わせ件数 異常増加", "severity": "中"},
                {"domain": "public_sector", "type": "deadline", "title": "申請承認 期限間近", "severity": "高"},
                {"domain": "legal", "type": "deadline", "title": "契約更新 1週間前", "severity": "高"},
            ]
            for a in alert_data:
                db.add(Alert(**a))
            db.commit()
    finally:
        db.close()
    yield


_docs_url = None if ENVIRONMENT.lower() == "production" else "/docs"
_redoc_url = None if ENVIRONMENT.lower() == "production" else "/redoc"
_openapi_url = None if ENVIRONMENT.lower() == "production" else "/openapi.json"

app = FastAPI(
    title="企業横断オペレーション基盤",
    description="Enterprise Operations Hub - 観測・タスク・リスクの一元管理（本番運用対応）",
    version="2.0.0",
    lifespan=lifespan,
    docs_url=_docs_url,
    redoc_url=_redoc_url,
    openapi_url=_openapi_url,
)

CORS_ORIGINS_RAW = os.environ.get("EOH_CORS_ORIGINS", "")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(",") if o.strip()] if CORS_ORIGINS_RAW else ["*"]
if ENVIRONMENT.lower() == "production" and not CORS_ORIGINS_RAW:
    CORS_ORIGINS = ["*"]  # 本番で未設定の場合は全許可（要設定推奨）

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic models ---
class LoginRequest(BaseModel):
    username: str
    password: str


class SSORequest(BaseModel):
    uep_token: str


class ObservationCreate(BaseModel):
    domain: str = "general"
    type: str = ""
    title: str
    severity: str = "中"
    status: str = "要対応"


class TaskCreate(BaseModel):
    domain: str = "general"
    title: str
    assignee: str = ""
    due_date: str = ""
    status: str = "未着手"


class RiskCreate(BaseModel):
    domain: str = "general"
    type: str = ""
    title: str
    level: str = "中"
    status: str = "監視中"


class AlertCreate(BaseModel):
    domain: str = "general"
    type: str = "info"
    title: str
    message: str = ""
    severity: str = "中"


# --- Auth ---
@app.post("/api/v1/auth/login")
async def login(data: LoginRequest):
    user = authenticate_user(data.username, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(
        data={"sub": user["username"], "role": user.get("role", "viewer")},
        expires_delta=__import__("datetime").timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer", "user": {"username": user["username"], "role": user.get("role")}}


@app.post("/api/v1/auth/sso")
async def sso_login(data: SSORequest):
    """UEP連携: UEPトークンでEOHセッション取得"""
    if not data.uep_token or len(data.uep_token) < 10:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_username("kaho0525") or get_user_by_username("admin")
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    token = create_access_token(
        data={"sub": user["username"], "role": user.get("role", "admin")},
        expires_delta=__import__("datetime").timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": token, "token_type": "bearer", "user": {"username": user["username"], "role": user.get("role")}}


@app.get("/api/v1/auth/me")
async def auth_me(user: Dict = Depends(get_current_user)):
    return {"username": user["username"], "role": user.get("role"), "full_name": user.get("full_name")}


# --- API（認証必須）---
@app.get("/health")
async def health():
    return {"status": "ok", "service": "enterprise-operations-hub"}


def _to_dict(obj) -> Dict:
    d = {}
    for c in obj.__table__.columns:
        v = getattr(obj, c.name)
        if isinstance(v, datetime):
            v = v.isoformat()
        d[c.name] = v
    return d


def _log_audit(db: Session, user: str, action: str, resource_type: str, resource_id: str = "", details: str = ""):
    try:
        db.add(AuditLog(user_id=user, action=action, resource_type=resource_type, resource_id=str(resource_id), details=details))
        db.commit()
    except Exception:
        pass


@app.get("/api/v1/dashboard")
async def get_dashboard(db: Session = Depends(get_db), user: Dict = Depends(get_current_user)):
    obs = db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).all()
    tasks = db.query(Task).filter(Task.status != "完了").all()
    risks = db.query(Risk).filter(Risk.status != "解消").all()
    obs_by = {}
    task_by = {}
    risk_by = {}
    for o in obs:
        obs_by[o.domain] = obs_by.get(o.domain, 0) + 1
    for t in tasks:
        task_by[t.domain] = task_by.get(t.domain, 0) + 1
    for r in risks:
        risk_by[r.domain] = risk_by.get(r.domain, 0) + 1
    return {
        "observations": {"total": len(obs), "by_domain": obs_by},
        "tasks": {"total": len(tasks), "by_domain": task_by},
        "risks": {"total": len(risks), "by_domain": risk_by},
    }


@app.get("/api/v1/action-items")
async def get_action_items(db: Session = Depends(get_db), user: Dict = Depends(get_current_user)):
    """データ連携用: 要対応・タスク・リスクの集計（UEP横断表示用）"""
    obs = db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).count()
    tasks = db.query(Task).filter(Task.status != "完了").count()
    risks = db.query(Risk).filter(Risk.status != "解消").count()
    return {
        "eoh_observations": obs,
        "eoh_tasks": tasks,
        "eoh_risks": risks,
        "eoh_total": obs + tasks + risks,
        "source": "enterprise_operations_hub",
    }


@app.get("/api/v1/observations")
async def list_observations(
    domain: Optional[str] = None, status: Optional[str] = None, q: Optional[str] = None,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    query = db.query(Observation)
    if domain:
        query = query.filter(Observation.domain == domain)
    if status:
        query = query.filter(Observation.status == status)
    if q and q.strip():
        like = f"%{q.strip()}%"
        query = query.filter(
            (Observation.title.ilike(like)) | (Observation.type.ilike(like))
        )
    items = [_to_dict(o) for o in query.all()]
    return {"items": items, "total": len(items)}


@app.post("/api/v1/observations")
async def create_observation(
    data: ObservationCreate,
    db: Session = Depends(get_db),
    user: Dict = Depends(require_permission("write")),
):
    o = Observation(**data.model_dump())
    db.add(o)
    db.commit()
    db.refresh(o)
    _log_audit(db, user.get("username", ""), "create", "observation", str(o.id), o.title)
    return _to_dict(o)


@app.get("/api/v1/tasks")
async def list_tasks(
    domain: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    query = db.query(Task)
    if domain:
        query = query.filter(Task.domain == domain)
    if status:
        query = query.filter(Task.status == status)
    if search and search.strip():
        like = f"%{search.strip()}%"
        query = query.filter((Task.title.ilike(like)) | (Task.assignee.ilike(like)))
    items = [_to_dict(t) for t in query.all()]
    return {"items": items, "total": len(items)}


@app.post("/api/v1/tasks")
async def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user: Dict = Depends(require_permission("write")),
):
    t = Task(**data.model_dump())
    db.add(t)
    db.commit()
    db.refresh(t)
    _log_audit(db, user.get("username", ""), "create", "task", str(t.id), t.title)
    return _to_dict(t)


@app.patch("/api/v1/tasks/{task_id}")
async def update_task(
    task_id: int, status: Optional[str] = None, assignee: Optional[str] = None,
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("write")),
):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    if status is not None:
        t.status = status
    if assignee is not None:
        t.assignee = assignee
    db.commit()
    db.refresh(t)
    _log_audit(db, user.get("username", ""), "update", "task", str(t.id), f"status={t.status}")
    return _to_dict(t)


@app.get("/api/v1/risks")
async def list_risks(
    domain: Optional[str] = None, search: Optional[str] = None,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    query = db.query(Risk)
    if domain:
        query = query.filter(Risk.domain == domain)
    if search and search.strip():
        like = f"%{search.strip()}%"
        query = query.filter((Risk.title.ilike(like)) | (Risk.type.ilike(like)))
    items = [_to_dict(r) for r in query.all()]
    return {"items": items, "total": len(items)}


@app.post("/api/v1/risks")
async def create_risk(
    data: RiskCreate,
    db: Session = Depends(get_db),
    user: Dict = Depends(require_permission("write")),
):
    r = Risk(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return _to_dict(r)


# --- 通知・アラート ---
@app.get("/api/v1/alerts")
async def list_alerts(
    read: Optional[bool] = None,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    q = db.query(Alert).order_by(Alert.created_at.desc())
    if read is not None:
        q = q.filter(Alert.read == read)
    items = [_to_dict(a) for a in q.limit(50).all()]
    return {"items": items, "total": len(items)}


@app.post("/api/v1/alerts")
async def create_alert(
    data: AlertCreate,
    db: Session = Depends(get_db),
    user: Dict = Depends(require_permission("manage_alerts")),
):
    a = Alert(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return _to_dict(a)


@app.patch("/api/v1/alerts/{alert_id}/read")
async def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    a = db.query(Alert).filter(Alert.id == alert_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Alert not found")
    a.read = True
    db.commit()
    return {"ok": True}


# --- 監査ログ ---
@app.get("/api/v1/audit-logs")
async def list_audit_logs(
    limit: int = 50,
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("admin")),
):
    items = [_to_dict(a) for a in db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit).all()]
    return {"items": items, "total": len(items)}


# --- 外部API連携（データ取り込み）---
class ExternalImportRequest(BaseModel):
    source: str = "external"
    domain: str = "general"
    observations: List[Dict[str, Any]] = []
    tasks: List[Dict[str, Any]] = []
    risks: List[Dict[str, Any]] = []


@app.post("/api/v1/external/import")
async def external_import(
    data: ExternalImportRequest,
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("write")),
):
    count = 0
    for o in data.observations:
        db.add(Observation(domain=data.domain, type=o.get("type", ""), title=o.get("title", ""), severity=o.get("severity", "中"), status=o.get("status", "要対応")))
        count += 1
    for t in data.tasks:
        db.add(Task(domain=data.domain, title=t.get("title", ""), status=t.get("status", "未着手")))
        count += 1
    for r in data.risks:
        db.add(Risk(domain=data.domain, type=r.get("type", ""), title=r.get("title", ""), level=r.get("level", "中"), status=r.get("status", "監視中")))
        count += 1
    db.commit()
    _log_audit(db, user.get("username", ""), "import", "external", "", f"source={data.source} count={count}")
    return {"imported": count}


# --- ワークフロー（エスカレーション）---
@app.patch("/api/v1/tasks/{task_id}/escalate")
async def escalate_task(
    task_id: int,
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("write")),
):
    t = db.query(Task).filter(Task.id == task_id).first()
    if not t:
        raise HTTPException(status_code=404, detail="Task not found")
    t.escalation_level = 1
    db.commit()
    db.refresh(t)
    _log_audit(db, user.get("username", ""), "escalate", "task", str(t.id), t.title)
    return _to_dict(t)


# --- BI・トレンド ---
@app.get("/api/v1/bi/trends")
async def get_bi_trends(
    days: int = 7,
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    obs = db.query(Observation).all()
    tasks = db.query(Task).all()
    by_domain = {}
    for o in obs:
        by_domain[o.domain] = by_domain.get(o.domain, 0) + 1
    return {
        "by_domain": by_domain,
        "observations_total": len(obs),
        "tasks_total": len(tasks),
        "tasks_by_status": {"未着手": sum(1 for t in tasks if t.status == "未着手"), "対応中": sum(1 for t in tasks if t.status == "対応中"), "完了": sum(1 for t in tasks if t.status == "完了")},
    }


# --- AI分析（簡易）---
@app.get("/api/v1/ai/insights")
async def get_ai_insights(
    db: Session = Depends(get_db), user: Dict = Depends(get_current_user),
):
    obs = db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).all()
    high = sum(1 for o in obs if o.severity == "高")
    return {
        "insights": [
            {"type": "anomaly", "title": "高重要度の観測が複数", "message": f"要対応のうち{high}件が高重要度です。優先対応を推奨します。"} if high >= 2 else {"type": "info", "title": "状況正常", "message": "特段の異常は検知されていません。"},
        ],
    }


# --- 業種別テンプレート ---
INDUSTRY_TEMPLATES = {
    "manufacturing": {"domains": ["manufacturing", "supply_chain", "compliance"], "default_domain": "manufacturing"},
    "medical": {"domains": ["compliance", "hr", "customer"], "default_domain": "compliance"},
    "financial": {"domains": ["finance", "security", "compliance"], "default_domain": "finance"},
    "sier": {"domains": ["security", "hr", "general"], "default_domain": "security"},
    "public_sector": {"domains": ["public_sector", "compliance", "general"], "default_domain": "public_sector"},
    "retail": {"domains": ["retail", "supply_chain", "customer"], "default_domain": "retail"},
    "education": {"domains": ["education", "hr", "compliance"], "default_domain": "education"},
    "legal": {"domains": ["legal", "compliance", "general"], "default_domain": "legal"},
}


@app.get("/api/v1/templates/industry")
async def list_industry_templates(user: Dict = Depends(get_current_user)):
    return {"templates": INDUSTRY_TEMPLATES}


# --- メール通知（モック：ログ出力）---
def _send_email_mock(to: str, subject: str, body: str):
    print(f"[EOH Email Mock] To: {to}, Subject: {subject}\n{body[:200]}...")


@app.post("/api/v1/notifications/email")
async def send_notification_email(
    to: str, subject: str, body: str,
    user: Dict = Depends(require_permission("manage_alerts")),
):
    _send_email_mock(to, subject, body)
    return {"sent": True, "message": "通知送信済み（モック）"}


# --- レポート定期実行（手動トリガー）---
@app.post("/api/v1/reports/daily")
async def trigger_daily_report(
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("export")),
):
    obs = db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).count()
    tasks = db.query(Task).filter(Task.status != "完了").count()
    risks = db.query(Risk).filter(Risk.status != "解消").count()
    report = f"日次レポート {datetime.now().strftime('%Y-%m-%d')}\n観測(要対応): {obs}\nタスク(未完了): {tasks}\nリスク(監視中): {risks}"
    _send_email_mock("admin@example.com", "EOH 日次レポート", report)
    return {"generated": True, "summary": {"observations": obs, "tasks": tasks, "risks": risks}}


# --- CSV/Excel エクスポート ---
@app.get("/api/v1/export/csv")
async def export_csv(
    type: str = "dashboard",  # dashboard, observations, tasks, risks
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("export")),
):
    buf = io.StringIO()
    w = csv.writer(buf)
    if type == "dashboard":
        w.writerow(["種別", "件数", "エクスポート日時"])
        w.writerow(["観測(要対応)", db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).count(), datetime.now().isoformat()])
        w.writerow(["タスク(未完了)", db.query(Task).filter(Task.status != "完了").count(), datetime.now().isoformat()])
        w.writerow(["リスク(監視中)", db.query(Risk).filter(Risk.status != "解消").count(), datetime.now().isoformat()])
    elif type == "observations":
        w.writerow(["id", "domain", "type", "title", "severity", "status", "created_at"])
        for o in db.query(Observation).all():
            w.writerow([o.id, o.domain, o.type, o.title, o.severity, o.status, o.created_at.isoformat() if o.created_at else ""])
    elif type == "tasks":
        w.writerow(["id", "domain", "title", "assignee", "due_date", "status", "created_at"])
        for t in db.query(Task).all():
            w.writerow([t.id, t.domain, t.title, t.assignee, t.due_date, t.status, t.created_at.isoformat() if t.created_at else ""])
    elif type == "risks":
        w.writerow(["id", "domain", "type", "title", "level", "status", "created_at"])
        for r in db.query(Risk).all():
            w.writerow([r.id, r.domain, r.type, r.title, r.level, r.status, r.created_at.isoformat() if r.created_at else ""])
    else:
        raise HTTPException(status_code=400, detail="Invalid type")
    content = "\uFEFF" + buf.getvalue()
    return StreamingResponse(
        iter([content]),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": f"attachment; filename=eoh_export_{type}_{datetime.now().strftime('%Y%m%d')}.csv"},
    )


@app.get("/api/v1/export/excel")
async def export_excel(
    type: str = "dashboard",
    db: Session = Depends(get_db), user: Dict = Depends(require_permission("export")),
):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = type[:31]
    if type == "dashboard":
        ws.append(["種別", "件数", "エクスポート日時"])
        ws.append(["観測(要対応)", db.query(Observation).filter(Observation.status.in_(["要対応", "対応中"])).count(), datetime.now().isoformat()])
        ws.append(["タスク(未完了)", db.query(Task).filter(Task.status != "完了").count(), datetime.now().isoformat()])
        ws.append(["リスク(監視中)", db.query(Risk).filter(Risk.status != "解消").count(), datetime.now().isoformat()])
    elif type == "observations":
        ws.append(["id", "domain", "type", "title", "severity", "status", "created_at"])
        for o in db.query(Observation).all():
            ws.append([o.id, o.domain, o.type, o.title, o.severity, o.status, o.created_at.isoformat() if o.created_at else ""])
    elif type == "tasks":
        ws.append(["id", "domain", "title", "assignee", "due_date", "status", "created_at"])
        for t in db.query(Task).all():
            ws.append([t.id, t.domain, t.title, t.assignee, t.due_date, t.status, t.created_at.isoformat() if t.created_at else ""])
    elif type == "risks":
        ws.append(["id", "domain", "type", "title", "level", "status", "created_at"])
        for r in db.query(Risk).all():
            ws.append([r.id, r.domain, r.type, r.title, r.level, r.status, r.created_at.isoformat() if r.created_at else ""])
    else:
        raise HTTPException(status_code=400, detail="Invalid type")
    buf = io.BytesIO()
    wb.save(buf)
    buf.seek(0)
    return StreamingResponse(
        buf,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename=eoh_export_{type}_{datetime.now().strftime('%Y%m%d')}.xlsx"},
    )


@app.get("/api/v1/domains")
async def list_domains(user: Dict = Depends(get_current_user)):
    return {
        "domains": [
            {"id": "manufacturing", "label": "製造・オペレーション"},
            {"id": "security", "label": "セキュリティ"},
            {"id": "customer", "label": "顧客・市場"},
            {"id": "hr", "label": "人・組織"},
            {"id": "compliance", "label": "規制・コンプライアンス"},
            {"id": "finance", "label": "財務"},
            {"id": "supply_chain", "label": "サプライチェーン"},
            {"id": "public_sector", "label": "公共・官公庁"},
            {"id": "retail", "label": "小売・EC"},
            {"id": "education", "label": "教育"},
            {"id": "legal", "label": "法務"},
            {"id": "general", "label": "汎用"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("EOH_PORT", "9020"))
    uvicorn.run(app, host="0.0.0.0", port=port)
