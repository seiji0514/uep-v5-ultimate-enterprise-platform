"""
医療・ヘルスケアプラットフォーム - 個別起動用
UEP v5.0・統合基盤とは別に単独で起動する
"""
import sys
import os
from pathlib import Path

# プロジェクトルート・backend を path に追加
_project_root = os.path.dirname(os.path.abspath(__file__))
_uep_root = os.path.dirname(_project_root)
_backend = os.path.join(_uep_root, "backend")
for p in [_uep_root, _backend]:
    if p not in sys.path:
        sys.path.insert(0, p)

# backend を cwd に（.env, venv 等のため）
os.chdir(_backend)

# .env 読み込み
if Path(".env").exists():
    from dotenv import load_dotenv
    load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from core.database import init_db
from auth.routes import router as auth_router
from medical.routes import router as medical_router


@asynccontextmanager
async def lifespan(app):
    init_db()
    yield


app = FastAPI(
    title="医療・ヘルスケアプラットフォーム",
    description="UEP v5.0・統合基盤に属さない個別システム",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(medical_router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "medical-platform"}


def _find_available_port(start: int = 9003, end: int = 9010) -> int:
    """9003-9010の範囲で使用可能なポートを探す"""
    import socket
    for port in range(start, end + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            continue
    return start  # フォールバック


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("MEDICAL_PORT", "0"))
    if port == 0:
        port = _find_available_port()
        if port != 9003:
            print(f"*** ポート9003が使用中のため、ポート{port}で起動します ***")
            print(f"*** フロント .env に REACT_APP_MEDICAL_PLATFORM_URL=http://localhost:{port} を設定 ***\n")
    uvicorn.run(app, host="127.0.0.1", port=port)
