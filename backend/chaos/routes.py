"""
Chaos Engineering API
障害シミュレーション（遅延、エラー注入）によるレジリエンス検証
※本番環境では無効化すること
"""
import asyncio
import random
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/api/v1/chaos", tags=["Chaos Engineering"])


class ChaosDelayRequest(BaseModel):
    """遅延注入リクエスト"""
    delay_ms: int = 100
    jitter_ms: Optional[int] = 0  # ランダム揺らぎ（0=なし）


class ChaosErrorRequest(BaseModel):
    """エラー注入リクエスト"""
    error_rate: float = 1.0  # 0.0～1.0（1.0=100%エラー）
    status_code: int = 500


@router.get("/status")
async def chaos_status():
    """Chaos Engineering 機能の状態確認"""
    return {
        "enabled": True,
        "endpoints": {
            "delay": "/api/v1/chaos/delay",
            "error": "/api/v1/chaos/error",
            "mixed": "/api/v1/chaos/mixed",
        },
        "description": "障害シミュレーション用エンドポイント（開発・検証環境向け）",
    }


@router.get("/delay")
async def chaos_delay(
    delay_ms: int = Query(100, ge=0, le=30000, description="遅延時間（ミリ秒）"),
    jitter_ms: int = Query(0, ge=0, le=5000, description="ランダム揺らぎ（ミリ秒）"),
):
    """
    遅延注入
    指定時間だけレスポンスを遅延させる（レイテンシ検証用）
    """
    actual_delay_ms = delay_ms
    if jitter_ms > 0:
        actual_delay_ms += random.randint(-jitter_ms, jitter_ms)
        actual_delay_ms = max(0, actual_delay_ms)

    await asyncio.sleep(actual_delay_ms / 1000.0)

    return {
        "status": "ok",
        "message": "Delay injection completed",
        "requested_delay_ms": delay_ms,
        "actual_delay_ms": actual_delay_ms,
    }


@router.post("/delay")
async def chaos_delay_post(request: ChaosDelayRequest):
    """遅延注入（POST）"""
    actual_delay_ms = request.delay_ms
    if request.jitter_ms and request.jitter_ms > 0:
        actual_delay_ms += random.randint(-request.jitter_ms, request.jitter_ms)
        actual_delay_ms = max(0, min(actual_delay_ms, 30000))

    await asyncio.sleep(actual_delay_ms / 1000.0)

    return {
        "status": "ok",
        "message": "Delay injection completed",
        "requested_delay_ms": request.delay_ms,
        "actual_delay_ms": actual_delay_ms,
    }


@router.get("/error")
async def chaos_error(
    error_rate: float = Query(1.0, ge=0.0, le=1.0, description="エラー発生率（0.0～1.0）"),
    status_code: int = Query(500, ge=400, le=599, description="返すHTTPステータスコード"),
):
    """
    エラー注入
    指定確率でHTTPエラーを返す（エラーハンドリング検証用）
    """
    if random.random() < error_rate:
        raise HTTPException(
            status_code=status_code,
            detail=f"Chaos engineering: Injected error (status={status_code})",
        )

    return {
        "status": "ok",
        "message": "No error injected (lucky request)",
    }


@router.post("/error")
async def chaos_error_post(request: ChaosErrorRequest):
    """エラー注入（POST）"""
    if random.random() < request.error_rate:
        raise HTTPException(
            status_code=request.status_code,
            detail=f"Chaos engineering: Injected error (status={request.status_code})",
        )

    return {
        "status": "ok",
        "message": "No error injected (lucky request)",
    }


@router.get("/mixed")
async def chaos_mixed(
    delay_ms: int = Query(50, ge=0, le=5000),
    error_rate: float = Query(0.5, ge=0.0, le=1.0),
):
    """
    混合シナリオ
    遅延＋エラー注入を組み合わせた検証
    """
    await asyncio.sleep(delay_ms / 1000.0)

    if random.random() < error_rate:
        raise HTTPException(
            status_code=503,
            detail="Chaos engineering: Service unavailable (mixed scenario)",
        )

    return {
        "status": "ok",
        "message": "Mixed chaos scenario completed successfully",
        "delay_ms": delay_ms,
        "error_rate": error_rate,
    }
