"""
産業統合プラットフォーム - 個別起動用
製造・IoT + 医療・ヘルスケア + 金融・FinTech + 統合セキュリティ・防衛 を1つに統合
UEP v5.0・統合基盤とは別に単独で起動する
"""
import sys
import os
from pathlib import Path

_project_root = os.path.dirname(os.path.abspath(__file__))
_uep_root = os.path.dirname(_project_root)
_backend = os.path.join(_uep_root, "backend")
for p in [_uep_root, _backend]:
    if p not in sys.path:
        sys.path.insert(0, p)

os.chdir(_backend)

if Path(".env").exists():
    from dotenv import load_dotenv
    load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import init_db
from auth.routes import router as auth_router
from manufacturing.routes import router as manufacturing_router
from medical.routes import router as medical_router
from fintech.routes import router as fintech_router
from security_center.routes import router as security_center_router
from infra_ops.routes import router as infra_ops_router
from dx_data.routes import router as dx_data_router
from compliance_governance.routes import router as compliance_governance_router
from supply_chain.routes import router as supply_chain_router
from data_integration.routes import router as data_integration_router
from public_sector.routes import router as public_sector_router
from retail.routes import router as retail_router
from education.routes import router as education_router
from legal.routes import router as legal_router

# 本番モード判定
ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
CORS_ORIGINS_RAW = os.environ.get("CORS_ORIGINS", "")
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS_RAW.split(",") if o.strip()] if CORS_ORIGINS_RAW else ["*"]


@asynccontextmanager
async def lifespan(app):
    init_db()
    if ENVIRONMENT != "production" or DEBUG:
        try:
            from core.seed_demo import init_unified_demo_data
            init_unified_demo_data()
        except Exception as e:
            print(f"Warning: Demo seed failed: {e}")
    yield


app = FastAPI(
    title="産業統合プラットフォーム",
    description="製造・IoT + 医療・ヘルスケア + 金融・FinTech + 統合セキュリティ・防衛 を統合した個別システム",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if DEBUG else None,
    redoc_url="/redoc" if DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(manufacturing_router)
app.include_router(medical_router)
app.include_router(fintech_router)
app.include_router(security_center_router)
app.include_router(infra_ops_router)
app.include_router(dx_data_router)
app.include_router(compliance_governance_router)
app.include_router(supply_chain_router)
app.include_router(data_integration_router)
app.include_router(public_sector_router)
app.include_router(retail_router)
app.include_router(education_router)
app.include_router(legal_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "industry-unified-platform"}


def _find_available_port(start: int = 9010, end: int = 9015) -> int:
    import socket
    for port in range(start, end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    return start


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("INDUSTRY_UNIFIED_PORT", "0"))
    host = os.environ.get("INDUSTRY_UNIFIED_HOST", "0.0.0.0" if ENVIRONMENT == "production" else "127.0.0.1")
    if port == 0:
        port = _find_available_port()
        if port != 9010:
            print(f"*** ポート9010が使用中のため、ポート{port}で起動します ***")
            print(f"*** フロント .env に REACT_APP_INDUSTRY_API_URL=http://localhost:{port} を設定 ***\n")
    uvicorn.run(app, host=host, port=port)
