"""
個人用 PC 容量確保 API
- Docker クリーンアップ
- Cドライブ容量確保

バックエンド起動: uvicorn main:app --reload --port 5002
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# cleanup モジュールの関数をインポート（親ディレクトリの cleanup.py）
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from cleanup import (
    C_DRIVE,
    format_size_mb,
    docker_available,
    docker_df,
    docker_prune,
    scan_c_drive,
    scan_temp_dirs,
    delete_path,
)

app = FastAPI(title="個人用 PC 容量確保 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/disk-info")
async def get_disk_info():
    """Cドライブの空き容量"""
    try:
        total, used, free = shutil.disk_usage(C_DRIVE)
        return {
            "drive": "C:",
            "total_mb": total / (1024 * 1024),
            "used_mb": used / (1024 * 1024),
            "free_mb": free / (1024 * 1024),
            "total": format_size_mb(total / (1024 * 1024)),
            "free": format_size_mb(free / (1024 * 1024)),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/docker")
async def get_docker_status():
    """Docker の状態と使用量"""
    available = docker_available()
    df_out = docker_df() if available else None
    return {
        "available": available,
        "df": df_out,
        "message": "Docker が利用可能です" if available else "Docker が起動していません",
    }


@app.post("/api/docker-prune")
async def run_docker_prune():
    """Docker クリーンアップ実行"""
    if not docker_available():
        raise HTTPException(status_code=400, detail="Docker が起動していません")
    ok, msg = docker_prune(dry_run=False)
    if not ok:
        raise HTTPException(status_code=500, detail=msg)
    return {"success": True, "message": msg}


@app.get("/api/scan")
async def scan_cleanup_targets(c_drive: bool = True, temp: bool = True):
    """削除候補をスキャン（safe=削除可, caution=注意）"""
    found = []
    if temp:
        found.extend(scan_temp_dirs())
    if c_drive:
        found.extend(scan_c_drive())
    total_mb = sum(f[1] for f in found)
    return {
        "items": [
            {"path": p, "size_mb": s, "desc": d, "safe": safe == "safe"}
            for p, s, d, safe in found
        ],
        "total_mb": total_mb,
        "total": format_size_mb(total_mb),
        "count": len(found),
    }


class CleanRequest(BaseModel):
    paths: list[str]


@app.post("/api/clean")
async def run_clean(request: CleanRequest):
    """指定パスを削除"""
    if not request.paths:
        raise HTTPException(status_code=400, detail="paths が空です")
    results = []
    freed = 0
    for path in request.paths:
        ok, msg = delete_path(path)
        size = 0
        if ok:
            # 削除成功時は元のサイズを取得できないため、スキャン結果から推測
            pass
        results.append({"path": path, "success": ok, "message": msg})
    return {
        "results": results,
        "message": "削除処理が完了しました",
    }


@app.get("/")
async def root():
    return {"message": "個人用 PC 容量確保 API", "docs": "/docs"}
